#!/usr/bin/env python3
"""Verify and optionally read one explicitly supplied, pinned Assay owner.

This is a file-integrity boundary, not discovery or a permission attestation.
It never downloads, installs, executes Assay code or searches for other roots.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys


BINDING = Path(__file__).resolve().parents[1] / "assets" / "assay-binding.json"


class BindingFailure(Exception):
    def __init__(self, reason: str, detail: str, code: int = 2):
        super().__init__(detail)
        self.reason, self.code = reason, code


def checked_bytes(root: Path, relative: str, expected: str) -> bytes:
    path = root / relative
    try:
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(root):
            raise BindingFailure("resource_outside_root", relative)
        if any(p.is_symlink() for p in [path, *path.parents] if p != root and p.is_relative_to(root)):
            raise BindingFailure("symlink_resource", relative)
        data = path.read_bytes()
    except PermissionError as exc:
        raise BindingFailure("permission_denied", relative) from exc
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError) as exc:
        raise BindingFailure("resource_unreadable", relative) from exc
    if hashlib.sha256(data).hexdigest() != expected:
        raise BindingFailure("resource_changed", relative, 1)
    return data


def resolve(root: Path, method: str, resource: str, provider_state: str, read: bool = False) -> dict:
    if provider_state != "enabled":
        raise BindingFailure("provider_disabled", "The selected source route is disabled.")
    try:
        binding = json.loads(BINDING.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise BindingFailure("binding_unreadable", str(exc)) from exc
    if method not in binding["owners"]:
        raise BindingFailure("missing_required_peer", method)
    component = PurePosixPath(resource)
    if component.is_absolute() or ".." in component.parts or "\\" in resource:
        raise BindingFailure("invalid_resource_path", resource)
    prefix = f"skills/{method}/"
    relative = prefix + component.as_posix()
    expected = binding["owners"][method]
    if relative not in expected:
        raise BindingFailure("unbound_resource", relative)
    try:
        root = root.expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise BindingFailure("root_unavailable", str(exc)) from exc
    if not root.is_dir():
        raise BindingFailure("root_unavailable", str(root))
    for path, digest in binding["identity_files"].items():
        checked_bytes(root, path, digest)
    owner_root = root / "skills" / method
    if not owner_root.is_dir():
        raise BindingFailure("missing_required_peer", method)
    # Untracked executable/resource additions could affect a verified owner's imports.
    actual = {
        p.relative_to(root).as_posix()
        for p in owner_root.rglob("*")
        if p.is_file()
        and "evals" not in p.relative_to(owner_root).parts
        and "__pycache__" not in p.relative_to(owner_root).parts
        and not p.name.endswith(".pyc")
    }
    extra = sorted(actual - set(expected))
    if extra:
        raise BindingFailure("unexpected_owner_resource", extra[0], 1)
    selected = b""
    for path, digest in expected.items():
        data = checked_bytes(root, path, digest)
        if path == relative:
            selected = data
    head = None
    if (root / ".git").exists():
        try:
            run = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                capture_output=True, text=True, timeout=10, check=False,
            )
            if run.returncode:
                raise BindingFailure("revision_unreadable", run.stderr.strip())
            head = run.stdout.strip()
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise BindingFailure("revision_unreadable", str(exc)) from exc
        if head != binding["assay"]["commit"]:
            raise BindingFailure("unsupported_revision", head, 1)
    result = {
        "status": "verified", "reason": "matched_owner_bytes", "route": "explicit-source",
        "provider_state": "caller-declared-enabled", "assay": binding["assay"],
        "git_head": head, "root": str(root), "method": method, "path": str(root / relative),
        "sha256": hashlib.sha256(selected).hexdigest(), "checked_files": len(expected) + len(binding["identity_files"]),
        "native_discovery": "not_observed", "permission_attestation": False,
    }
    if read:
        try:
            result["content"] = selected.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BindingFailure("resource_not_utf8", relative) from exc
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assay-root", required=True, type=Path)
    parser.add_argument("--provider-state", required=True, choices=["enabled", "disabled"])
    parser.add_argument("--method", required=True)
    parser.add_argument("--resource", default="SKILL.md")
    parser.add_argument("--read", action="store_true", help="Return the actual verified UTF-8 content.")
    args = parser.parse_args()
    try:
        result = resolve(args.assay_root, args.method, args.resource, args.provider_state, args.read)
    except BindingFailure as exc:
        print(json.dumps({"status": "incompatible" if exc.code == 1 else "unavailable", "reason": exc.reason, "detail": str(exc)}, ensure_ascii=False))
        return exc.code
    except OSError as exc:
        print(json.dumps({"status": "unavailable", "reason": "resource_unreadable", "detail": str(exc)}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
