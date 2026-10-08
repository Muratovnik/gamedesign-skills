#!/usr/bin/env python3
"""Project one permitted observer view, then choose content using only that view."""

import argparse
import json
from pathlib import Path
import sys

from content_rules import rejection_reasons, validate_content
from state import SKILL, observer_view
from validate_artifact import digest, read_json, validate
from jsonschema.exceptions import SchemaError, ValidationError


def select_content(view, content, stage):
    validate(view, SKILL / "assets" / "observer-view.schema.json")
    validate_content(content, view["game_id"])
    selected = []
    rejected = []
    for item in content["items"]:
        if item["stage"] != stage:
            continue
        reasons = rejection_reasons(view, item)
        if reasons:
            rejected.append({"id": item["id"], "reasons": reasons})
        else:
            selected.append({key: item[key] for key in ("id", "action", "text")})
    if not selected and not rejected:
        return {"status": "missing_evidence", "reason": "no_items_in_requested_stage", "selected": [], "rejected": []}
    return {"status": "supported" if selected else "refuted", "observer_id": view["observer_id"],
            "stage": stage, "selected": selected, "rejected": rejected,
            "selected_count": len(selected), "inspected_count": len(selected) + len(rejected),
            "decision": "operate-winch" if any(i["action"] == "operate-winch" for i in selected)
                else selected[0]["action"] if selected else None,
            "limits": "A deterministic policy consumed a supplied observer view; no human negotiation or LLM context isolation was tested."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    view = subs.add_parser("view")
    view.add_argument("--save", type=Path, required=True)
    view.add_argument("--actor", required=True)
    choice = subs.add_parser("choose")
    choice.add_argument("--view", type=Path, required=True)
    choice.add_argument("--content", type=Path, required=True)
    choice.add_argument("--stage", required=True)
    for sub in (view, choice):
        sub.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "view":
            result = observer_view(read_json(args.save), args.actor)
            code = 0
        else:
            result = select_content(read_json(args.view), read_json(args.content), args.stage)
            result["input_sha256"] = {"view": digest(args.view), "content": digest(args.content)}
            code = {"supported": 0, "refuted": 1, "missing_evidence": 2}[result["status"]]
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write("\n")
        print(json.dumps({"status": result.get("status", "observer_projected"), "output_sha256": digest(args.output),
                          "selected_count": result.get("selected_count")}))
        return code
    except (OSError, ValueError, KeyError, TypeError, SchemaError, ValidationError) as error:
        print(json.dumps({"status": "invalid_or_missing_evidence", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
