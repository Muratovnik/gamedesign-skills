#!/usr/bin/env python3
"""Build the two public source assets for a versioned release."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

import package

ROOT = package.ROOT
ARCHIVE_TEMPLATE = "gamedesign-skills-{version}-source.zip"
VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?\Z")


def expected_assets(version: str) -> tuple[str, str]:
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"Invalid release version: {version!r}")
    archive = ARCHIVE_TEMPLATE.format(version=version)
    return archive, "SHA256SUMS"


def build(output: Path, version: str, root: Path = ROOT) -> dict:
    """Write the archive and checksum list; the directory must be empty."""
    archive_name, sums_name = expected_assets(version)
    root = package._checked_root(root)
    output = Path(output).absolute()
    archive_path = package.validate_destination(root, output / archive_name)
    sums_path = package.validate_destination(root, output / sums_name)
    if output.exists():
        if not output.is_dir():
            raise ValueError(f"Output must be a directory: {output}")
        if any(output.iterdir()):
            raise FileExistsError(f"Output directory must be empty: {output}")
    actual_version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if actual_version != version:
        raise ValueError(f"Requested version {version} does not match VERSION ({actual_version})")

    output.mkdir(parents=True, exist_ok=True)
    manifest = package.build(root, archive_path)
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    sums_path.write_text(f"{digest}  {archive_name}\n", encoding="ascii", newline="\n")
    return {
        "version": version,
        "archive": archive_name,
        "sha256": digest,
        "file_count": len(manifest["files"]),
        "assets": [archive_name, sums_name],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build", help="build the versioned source assets")
    build_parser.add_argument("--output", type=Path, required=True, help="new or empty assets directory")
    build_parser.add_argument("--version", required=True)
    args = parser.parse_args()
    try:
        result = build(args.output, args.version)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
