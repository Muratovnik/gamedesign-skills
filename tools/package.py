#!/usr/bin/env python3
"""Build a deterministic archive from the explicitly public source tree."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]

# Only declared public source, maintainer and release files enter the package.
# Unlisted top-level paths and unapproved GitHub metadata stay out by default.
PUBLIC_ROOT_FILES = frozenset({
    "AGENTS.md",
    ".betterleaks.toml",
    ".gitattributes",
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "NOTICE.md",
    "README.md",
    "SECURITY.md",
    "VERSION",
    "catalog.json",
    "plugin.json",
    "requirements-dev.txt",
    "relkit.toml",
})
PUBLIC_ROOT_DIRECTORIES = frozenset({
    ".claude-plugin",
    ".github",
    "docs",
    "examples",
    "skills",
    "tests",
    "tools",
})
PUBLIC_NESTED_FILES = frozenset({".agents/plugins/marketplace.json"})
PUBLIC_GITHUB_FILES = frozenset({"relkit.pyz", "relkit.pyz.sha256"})
PUBLIC_GITHUB_DIRECTORIES = frozenset({"workflows"})

# These names denote local state or development/client material wherever they
# occur inside an approved public subtree. They are pruned before recursion.
EXCLUDED_DIRECTORIES = frozenset({
    ".agents", ".cache", ".claude", ".codex", ".git", ".godot",
    ".mypy_cache", ".private", ".pytest_cache", ".ruff_cache", ".state",
    ".tox", ".venv", "__pycache__", "client", "clients", "dist", "evals",
    "local", "node_modules", "scratch", "temp", "tmp", "venv",
})
EXCLUDED_FILES = frozenset({".ds_store", "thumbs.db"})


def _is_reparse_point(info: os.stat_result) -> bool:
    attributes = getattr(info, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & reparse_flag)


def _checked_root(root: Path) -> Path:
    """Reject linked roots and ancestors before resolving the source path."""
    absolute = Path(os.path.abspath(root))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            raise ValueError(f"Source root does not exist: {root}") from None
        if _is_reparse_point(info):
            raise ValueError(f"Archive refuses symlinks or reparse points: {current}")
    if not absolute.is_dir():
        raise ValueError(f"Source root is not a directory: {root}")
    return absolute


def _excluded_file(name: str) -> bool:
    lowered = name.casefold()
    return (
        lowered in EXCLUDED_FILES
        or lowered == ".env"
        or lowered.startswith(".env.")
        or lowered.endswith((".local", ".private", ".secret", ".state"))
        or ".local." in lowered
    )


def _walk_public_tree(root: Path, directory: Path, collected: list[Path]) -> None:
    try:
        entries = sorted(os.scandir(directory), key=lambda entry: entry.name.casefold())
    except OSError as exc:
        raise ValueError(f"Cannot inspect public source directory {directory}: {exc}") from exc

    for entry in entries:
        if entry.name.casefold() in EXCLUDED_DIRECTORIES or _excluded_file(entry.name):
            continue
        path = Path(entry.path)
        try:
            info = entry.stat(follow_symlinks=False)
        except OSError as exc:
            raise ValueError(f"Cannot inspect source path {path}: {exc}") from exc
        if _is_reparse_point(info):
            raise ValueError(f"Archive refuses symlinks or reparse points: {path.relative_to(root)}")
        if stat.S_ISDIR(info.st_mode):
            _walk_public_tree(root, path, collected)
        elif stat.S_ISREG(info.st_mode):
            if path.suffix.casefold() not in {".pyc", ".pyo"}:
                collected.append(path)
        else:
            raise ValueError(f"Archive refuses non-regular source files: {path.relative_to(root)}")


def _walk_public_github(root: Path, directory: Path, collected: list[Path]) -> None:
    """Include the release tool and workflows, leaving other GitHub state out."""
    try:
        entries = sorted(os.scandir(directory), key=lambda entry: entry.name.casefold())
    except OSError as exc:
        raise ValueError(f"Cannot inspect public GitHub directory {directory}: {exc}") from exc

    for entry in entries:
        name = entry.name
        if name.casefold() in EXCLUDED_DIRECTORIES or _excluded_file(name):
            continue
        path = Path(entry.path)
        info = entry.stat(follow_symlinks=False)
        if _is_reparse_point(info):
            raise ValueError(f"Archive refuses symlinks or reparse points: {path.relative_to(root)}")
        if name in PUBLIC_GITHUB_FILES:
            if not stat.S_ISREG(info.st_mode):
                raise ValueError(f"Expected a regular public GitHub file: {path.relative_to(root)}")
            collected.append(path)
        elif name in PUBLIC_GITHUB_DIRECTORIES:
            if not stat.S_ISDIR(info.st_mode):
                raise ValueError(f"Expected a public GitHub directory: {path.relative_to(root)}")
            _walk_public_tree(root, path, collected)


def members(root: Path) -> list[Path]:
    """Return the sorted files admitted by the public-source policy."""
    root = _checked_root(root)
    files: list[Path] = []

    for name in sorted(PUBLIC_ROOT_FILES | PUBLIC_NESTED_FILES):
        path = root
        parts = Path(name).parts
        for index, part in enumerate(parts):
            path = path / part
            try:
                info = path.lstat()
            except FileNotFoundError:
                break
            if _is_reparse_point(info):
                raise ValueError(f"Archive refuses symlinks or reparse points: {path.relative_to(root)}")
            if index < len(parts) - 1:
                if not stat.S_ISDIR(info.st_mode):
                    raise ValueError(f"Expected a public source directory: {path.relative_to(root)}")
            elif not stat.S_ISREG(info.st_mode):
                raise ValueError(f"Expected a regular public source file: {name}")
            elif not _excluded_file(part):
                files.append(path)

    for name in sorted(PUBLIC_ROOT_DIRECTORIES):
        path = root / name
        try:
            info = path.lstat()
        except FileNotFoundError:
            continue
        if _is_reparse_point(info):
            raise ValueError(f"Archive refuses symlinks or reparse points: {name}")
        if not stat.S_ISDIR(info.st_mode):
            raise ValueError(f"Expected a public source directory: {name}")
        if name == ".github":
            _walk_public_github(root, path, files)
        else:
            _walk_public_tree(root, path, files)

    if not files:
        raise ValueError("Archive would be empty")
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def _is_excluded_output(root: Path, destination: Path) -> bool:
    try:
        relative = destination.relative_to(root)
    except ValueError:
        return False
    if relative.as_posix() in PUBLIC_NESTED_FILES:
        return False
    return any(part.casefold() in EXCLUDED_DIRECTORIES for part in relative.parts[:-1])


def validate_destination(root: Path, destination: Path) -> Path:
    """Reject a destination that a later package build could include."""
    root = _checked_root(root)
    candidate = Path(os.path.abspath(destination))
    current = Path(candidate.anchor)
    for part in candidate.parts[1:]:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            break
        if _is_reparse_point(info):
            raise ValueError(f"Archive refuses symlinks or reparse points in output path: {current}")
    resolved = candidate.resolve(strict=False)
    if resolved.is_relative_to(root) and not _is_excluded_output(root, resolved):
        raise ValueError("Put archives and receipts outside public source roots or in excluded output storage")
    return candidate


def build(root: Path, output: Path) -> dict:
    root = _checked_root(root)
    output = validate_destination(root, output)
    if output.exists():
        raise FileExistsError(output)
    files = members(root)
    inventory = []
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(root).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo("game-design/" + relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            inventory.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return {
        "schema_version": 1,
        "version": (root / "VERSION").read_text(encoding="utf-8").strip(),
        "archive": output.name,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "files": inventory,
        "excluded": sorted(EXCLUDED_DIRECTORIES),
        "evaluation_included": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        output = validate_destination(ROOT, args.output)
        receipt = validate_destination(ROOT, args.receipt)
        if receipt.exists():
            parser.error("Receipt already exists; choose a new destination")
        if output.resolve() == receipt.resolve():
            parser.error("Archive and receipt must be distinct")
        result = build(ROOT, output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"archive": str(output), "sha256": result["sha256"], "file_count": len(result["files"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
