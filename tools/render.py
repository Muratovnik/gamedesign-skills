#!/usr/bin/env python3
"""Render the two client projections from the release inventory; never install."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def projections(root: Path = ROOT) -> dict[str, str]:
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    identity = {
        "name": catalog["name"], "version": version,
        "description": "Seven composable game design methods, original playable examples and explicit artifact adapters.",
        "license": "MIT",
    }
    portable = {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", **identity,
                "keywords": ["game-design", "gameplay", "narrative", "prototyping"]}
    # Both clients discover the conventional skills/ directory. Listing it again
    # in Claude's additive field would create an unnecessary second load path.
    return {
        "plugin.json": json.dumps(portable, indent=2) + "\n",
        ".claude-plugin/plugin.json": json.dumps(identity, indent=2) + "\n",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = []
    for relative, expected in projections().items():
        path = ROOT / relative
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            changed.append(relative)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8")
    print(json.dumps({"status": "stale" if args.check and changed else "current", "files": changed}))
    return int(args.check and bool(changed))


if __name__ == "__main__":
    raise SystemExit(main())
