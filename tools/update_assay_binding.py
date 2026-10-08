#!/usr/bin/env python3
"""Update a release binding from an explicitly chosen clean Assay checkout."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tomllib


def build(root: Path, revision: str) -> dict:
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if head != revision:
        raise ValueError("Supplied revision differs from checkout HEAD")
    if subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True).strip():
        raise ValueError("Assay source is dirty; bind reviewed exact bytes only")
    catalog = tomllib.loads((root / "catalog.toml").read_text(encoding="utf-8"))
    tracked = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).decode().split("\0")
    owners = {}
    for entry in catalog["assets"]:
        if entry["kind"] != "skill":
            continue
        prefix = entry["path"] + "/"
        files = [p for p in tracked if p.startswith(prefix) and "evals" not in Path(p).parts]
        owners[Path(entry["path"]).name] = {
            p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sorted(files)
        }
    return {
        "schema_version": 1,
        "assay": {"repository": "https://github.com/Muratovnik/assay", "version": (root / "VERSION").read_text(encoding="utf-8").strip(), "commit": head},
        "scope": "Identity files and selected owner runtime resources, excluding evaluator inputs. No native discovery claim.",
        "identity_files": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in ["VERSION", "catalog.toml", "LICENSE"]},
        "owners": owners,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assay-root", required=True, type=Path)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    target = Path(__file__).resolve().parents[1] / "skills/game-design/assets/assay-binding.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(build(args.assay_root, args.revision), indent=2) + "\n", encoding="utf-8", newline="\n")
    print(target)
