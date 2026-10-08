#!/usr/bin/env python3
"""Verify downloaded source assets and exercise the shipped East Gate consumer."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import zipfile

ARCHIVE_TEMPLATE = "gamedesign-skills-{version}-source.zip"
MAX_UNCOMPRESSED_BYTES = 1024 * 1024 * 1024
SHA256_LINE = re.compile(r"([0-9a-f]{64})  ([^\r\n]+)\n\Z")


def expected_assets(version: str) -> tuple[str, str]:
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?", version):
        raise ValueError(f"Invalid release version: {version!r}")
    return ARCHIVE_TEMPLATE.format(version=version), "SHA256SUMS"


def _is_reparse(info: os.stat_result) -> bool:
    attributes = getattr(info, "st_file_attributes", 0)
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & flag)


def _check_path_ancestors(path: Path) -> Path:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            break
        if _is_reparse(info):
            raise ValueError(f"Refusing symlinks or reparse points: {current}")
    return absolute


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_extract(archive_path: Path, destination: Path) -> list[str]:
    destination.mkdir(parents=True, exist_ok=False)
    files: list[tuple[zipfile.ZipInfo, PurePosixPath]] = []
    seen: set[str] = set()
    total_size = 0
    try:
        archive = zipfile.ZipFile(archive_path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise ValueError(f"Invalid source archive: {exc}") from exc
    with archive:
        for info in archive.infolist():
            raw_name = info.orig_filename
            if (
                not raw_name
                or "\x00" in raw_name
                or "\\" in raw_name
                or raw_name.startswith("/")
                or "//" in raw_name
            ):
                raise ValueError(f"Unsafe archive member name: {raw_name!r}")
            relative = PurePosixPath(raw_name)
            if (
                relative.is_absolute()
                or relative.as_posix() != raw_name
                or len(relative.parts) < 2
                or relative.parts[0] != "game-design"
                or any(part in {"", ".", ".."} for part in relative.parts)
            ):
                raise ValueError(f"Unsafe archive member path: {raw_name!r}")
            key = raw_name.casefold()
            if key in seen:
                raise ValueError(f"Duplicate archive member: {raw_name}")
            seen.add(key)
            if info.is_dir():
                raise ValueError(f"Unexpected directory entry: {raw_name}")
            mode = (info.external_attr >> 16) & 0xFFFF
            if stat.S_IFMT(mode) != stat.S_IFREG:
                raise ValueError(f"Archive member is not a regular file: {raw_name}")
            if info.flag_bits & 0x1:
                raise ValueError(f"Encrypted archive member is not supported: {raw_name}")
            if info.file_size < 0:
                raise ValueError(f"Invalid archive member size: {raw_name}")
            total_size += info.file_size
            if total_size > MAX_UNCOMPRESSED_BYTES:
                raise ValueError("Archive exceeds the 1 GiB extraction limit")
            files.append((info, relative))

        file_names = {path.as_posix() for _, path in files}
        for name in file_names:
            parts = PurePosixPath(name).parts
            for end in range(1, len(parts)):
                if PurePosixPath(*parts[:end]).as_posix() in file_names:
                    raise ValueError(f"Archive file blocks a directory path: {name}")

        extracted = []
        written_size = 0
        for info, relative in files:
            target = destination.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                with archive.open(info) as source, target.open("xb") as output:
                    while chunk := source.read(1024 * 1024):
                        written_size += len(chunk)
                        if written_size > MAX_UNCOMPRESSED_BYTES:
                            raise ValueError("Archive exceeds the 1 GiB extraction limit")
                        output.write(chunk)
            except (OSError, RuntimeError, zipfile.BadZipFile, EOFError) as exc:
                raise ValueError(f"Could not read archive member {info.filename}: {exc}") from exc
            extracted.append(relative.as_posix())
    return sorted(extracted)


def _run_consumer(script: Path, arguments: list[str], scratch: Path) -> dict:
    environment = {
        "PATH": os.environ.get("PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        "WINDIR": os.environ.get("WINDIR", ""),
        "TEMP": str(scratch),
        "TMP": str(scratch),
    }
    try:
        result = subprocess.run(
            [sys.executable, "-I", str(script), *arguments],
            cwd=scratch,
            env=environment,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"East Gate consumer could not run: {exc}") from exc
    if result.returncode != 0:
        raise ValueError(f"East Gate consumer failed ({result.returncode}): {result.stdout}{result.stderr}")
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("East Gate consumer did not return JSON") from exc
    if report.get("status") != "executed":
        raise ValueError(f"East Gate consumer returned an unexpected result: {report!r}")
    return report


def verify(assets: Path, version: str, temp: Path) -> dict:
    archive_name, sums_name = expected_assets(version)
    assets = _check_path_ancestors(assets)
    temp = _check_path_ancestors(temp)
    if not assets.is_dir():
        raise ValueError(f"Assets path is not a directory: {assets}")
    if temp.exists():
        raise FileExistsError(f"Smoke scratch must be a new path: {temp}")
    if temp == assets or assets.is_relative_to(temp) or temp.is_relative_to(assets):
        raise ValueError("Smoke scratch and downloaded assets must be separate paths")

    with os.scandir(assets) as entries:
        actual_names = set()
        for entry in entries:
            info = entry.stat(follow_symlinks=False)
            if _is_reparse(info) or not stat.S_ISREG(info.st_mode):
                raise ValueError(f"Downloaded asset is not a regular file: {entry.name}")
            actual_names.add(entry.name)
    expected_names = {archive_name, sums_name}
    if actual_names != expected_names:
        raise ValueError(f"Expected exactly {sorted(expected_names)}, found {sorted(actual_names)}")

    archive_path = assets / archive_name
    sums_text = (assets / sums_name).read_text(encoding="ascii")
    match = SHA256_LINE.fullmatch(sums_text)
    if not match or match.group(2) != archive_name:
        raise ValueError("SHA256SUMS must contain exactly the expected archive name and one digest")
    digest = _sha256_file(archive_path)
    if digest != match.group(1):
        raise ValueError("Downloaded source archive checksum does not match SHA256SUMS")

    temp.mkdir(parents=True, exist_ok=False)
    extracted_root = temp / "extracted"
    extracted = _safe_extract(archive_path, extracted_root)
    source_root = extracted_root / "game-design"
    source_version = (source_root / "VERSION").read_text(encoding="utf-8").strip()
    if source_version != version:
        raise ValueError(f"Archive VERSION is {source_version!r}, expected {version!r}")

    catalog = json.loads((source_root / "catalog.json").read_text(encoding="utf-8"))
    entries = catalog.get("skills") if isinstance(catalog, dict) else None
    if not isinstance(entries, list):
        raise ValueError("catalog.json must contain a skills array")
    names = [item.get("name") for item in entries if isinstance(item, dict)]
    if len(names) != len(entries) or len(names) != 7 or len(set(names)) != 7:
        raise ValueError("catalog.json must define exactly seven uniquely named skills")
    skills_dir = source_root / "skills"
    actual_skills = {path.name for path in skills_dir.iterdir() if path.is_dir()}
    if actual_skills != set(names):
        raise ValueError(f"Extracted skills differ from catalog: expected {sorted(names)}, found {sorted(actual_skills)}")
    missing_skill_docs = [name for name in names if not (skills_dir / name / "SKILL.md").is_file()]
    if missing_skill_docs:
        raise ValueError(f"Extracted skills are missing SKILL.md: {sorted(missing_skill_docs)}")

    adaptation = source_root / "examples" / "adaptation"
    consumer = adaptation / "consumer.py"
    artifact = adaptation / "fixtures" / "east-gate-en.json"
    run_dir = temp / "consumer-runs"
    run_dir.mkdir()
    play_output = run_dir / "play.json"
    play_report = _run_consumer(
        consumer,
        ["--artifact", str(artifact), "--expect-revision", "east-gate-en-1", "--choose", "east", "--output", str(play_output)],
        run_dir,
    )
    play_result = json.loads(play_output.read_text(encoding="utf-8"))
    if play_result.get("gate") != "open" or play_result.get("token") != "ferryman":
        raise ValueError("East Gate play did not open the gate and award the ferryman token")

    ferry_output = run_dir / "ferry.json"
    ferry_report = _run_consumer(
        consumer,
        ["--operation", "enter-ferry", "--artifact", str(artifact), "--expect-revision", "east-gate-en-1",
         "--state", str(play_output), "--output", str(ferry_output)],
        run_dir,
    )
    ferry_result = json.loads(ferry_output.read_text(encoding="utf-8"))
    if ferry_result.get("voyage_started") is not True or ferry_result.get("token") is not None:
        raise ValueError("East Gate ferry did not consume the saved token and start the voyage")

    return {
        "status": "pass",
        "version": version,
        "archive": archive_name,
        "sha256": digest,
        "archive_files": len(extracted),
        "skills": sorted(actual_skills),
        "east_gate": {"play": play_report, "ferry": ferry_report},
        "static_check": "not_run",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, required=True, help="directory containing the downloaded release assets")
    parser.add_argument("--version", required=True)
    parser.add_argument("--temp", type=Path, required=True, help="new project-owned scratch directory")
    args = parser.parse_args()
    try:
        result = verify(args.assets, args.version, args.temp)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
