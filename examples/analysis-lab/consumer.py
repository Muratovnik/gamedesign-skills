#!/usr/bin/env python3
"""Project one permitted observer view, then choose content using only that view."""

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

from state import SKILL, validate_state
from validate_artifact import digest, read_json, validate
from jsonschema.exceptions import SchemaError, ValidationError


def observer_view(state, actor_id):
    validate_state(state)
    if state["schema_version"] != 2:
        raise ValueError("The content consumer requires migrated schema 2.")
    matches = [a for a in state["actors"] if a["id"] == actor_id]
    if len(matches) != 1:
        raise ValueError("Observer identity is missing or ambiguous.")
    actor = matches[0]
    known = set(actor["known_fact_ids"]) | {f["id"] for f in state["facts"] if f["public"]}
    facts = {f["id"]: f["value"] for f in state["facts"] if f["id"] in known}
    right_kinds = []
    now = datetime.fromisoformat(state["clock_utc"])
    if actor["status"] == "active":
        for right in state["rights"]:
            delegated = any(d["right_id"] == right["id"] and d["from_id"] == right["owner_id"]
                            and d["to_id"] == actor_id and d["accepted"] for d in state["delegations"])
            if (right["owner_id"] == actor_id or delegated) and datetime.fromisoformat(right["expires_at"]) > now:
                right_kinds.append(right["kind"])
    return {"schema_version": 1, "game_id": state["game_id"], "build_id": state["build_id"],
            "observer_id": actor_id, "active": actor["status"] == "active", "clock_utc": state["clock_utc"],
            "facts": facts, "unlock_ids": actor["unlock_ids"], "right_kinds": sorted(set(right_kinds)),
            "can_spend_crew_scrap": actor["status"] == "active" and state["roles"]["treasurer_id"] == actor_id,
            "scrap": {a["owner_id"]: a["amount"] for a in state["accounts"] if a["owner_id"] in (actor_id, state["crew_id"])},
            "history_ids": [event["id"] for event in state["history"]], "generator_operational": state["world"]["generator"]}


def select_content(view, content, stage):
    validate(view, SKILL / "assets" / "observer-view.schema.json")
    validate(content, SKILL / "assets" / "content.schema.json")
    if view["game_id"] != content["game_id"]:
        raise ValueError("Content and observer belong to different games.")
    if len({item["id"] for item in content["items"]}) != len(content["items"]):
        raise ValueError("Content identities are duplicated.")
    selected = []
    rejected = []
    for item in content["items"]:
        if item["stage"] != stage:
            continue
        reasons = []
        if not view["active"]:
            reasons.append("observer_away")
        for key, available in (("required_facts", view["facts"]), ("required_unlocks", view["unlock_ids"]),
                               ("required_rights", view["right_kinds"])):
            if not set(item[key]) <= set(available):
                reasons.append(key)
        if set(item["forbidden_history"]) & set(view["history_ids"]):
            reasons.append("already_emitted_history")
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
