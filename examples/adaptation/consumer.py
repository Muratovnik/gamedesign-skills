#!/usr/bin/env python3
"""Consume the two East Gate content versions through actual toy-game actions."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def require_object(value, label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def require_text(value, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")
    return value


def validate_content(artifact: dict, expected_revision: str) -> None:
    require_object(artifact, "Content artifact")
    if type(artifact.get("schema_version")) is not int or artifact["schema_version"] != 1:
        raise ValueError("Unsupported content schema version")
    require_text(artifact.get("revision"), "Content revision")
    if artifact.get("artifact_id") != "east-gate" or artifact.get("revision") != expected_revision:
        raise ValueError("Wrong artifact or stale revision")
    require_text(artifact.get("guide"), "Guide")
    require_text(artifact.get("locale"), "Locale")
    lines = artifact.get("lines", [])
    if not isinstance(lines, list) or not lines or not all(isinstance(line, str) and line.strip() for line in lines):
        raise ValueError("No usable verse lines")
    code = "".join(line.lstrip()[0].upper() for line in lines)
    directions = require_object(artifact.get("directions"), "Direction repertoire")
    if not directions:
        raise ValueError("No playable directions")
    for key, value in directions.items():
        require_text(key, "Direction ID")
        require_text(value, "Direction label")
    require_text(artifact.get("exit_id"), "Exit ID")
    inferred = [key for key, value in directions.items() if value == code]
    if inferred != [artifact.get("exit_id")]:
        raise ValueError("The authored clue does not resolve to the playable exit")
    sign = require_object(artifact.get("later_sign"), "Later sign")
    require_text(sign.get("text"), "Later sign text")
    if sign.get("direction_id") != artifact["exit_id"]:
        raise ValueError("The later sign breaks the transferred direction relation")
    if artifact.get("display") not in ("four-lines", "one-line-carousel"):
        raise ValueError("Unsupported presentation mode")
    if "aid" in artifact:
        require_text(artifact["aid"], "Aid mode")


def view(artifact: dict, expected_revision: str, line: int) -> dict:
    validate_content(artifact, expected_revision)
    lines = artifact["lines"]
    if type(line) is not int or not 1 <= line <= len(lines):
        raise ValueError("The requested display line is unavailable")
    carousel = artifact["display"] == "one-line-carousel"
    actions = ["next-line", "choose-direction"] if carousel else ["choose-direction"]
    if artifact.get("aid") == "line-pins":
        actions.insert(0, "pin-current-line" if carousel else "pin-line")
    return {"artifact_id": artifact["artifact_id"], "revision": artifact["revision"],
            "guide": artifact["guide"], "visible_lines": [lines[line - 1]] if carousel else lines,
            "current_line": line if carousel else None,
            "next_line": (line % len(lines)) + 1 if carousel else None,
            "permitted_actions": actions,
            "directions": artifact["directions"], "evidence_scope": "actual serialized text presentation, not a rendered device"}


def play(artifact: dict, expected_revision: str, pins: list[int], choice: str) -> dict:
    validate_content(artifact, expected_revision)
    lines, directions = artifact["lines"], artifact["directions"]
    require_text(choice, "Direction choice")
    if choice not in directions:
        raise ValueError("Action is not in the displayed direction repertoire")
    if not isinstance(pins, list) or any(type(index) is not int or index < 1 or index > len(lines) for index in pins):
        raise ValueError("Pin references a missing displayed line")
    if pins and artifact.get("aid") != "line-pins":
        raise ValueError("Pin action is unavailable in this version")
    notebook = [lines[index - 1] for index in dict.fromkeys(pins)]
    opened = choice == artifact["exit_id"]
    return {"artifact_id": artifact["artifact_id"], "revision": artifact["revision"],
            "display": artifact["display"], "actions": [{"pin_line": index} for index in pins] + [{"choose": choice}],
            "notebook": notebook, "gate": "open" if opened else "closed", "token": "ferryman" if opened else None,
            "next_scene": artifact["later_sign"]["text"] if opened else "Return to the verse and choose again.",
            "evidence_scope": "deterministic content and action semantics; no human or device observation"}


def enter_ferry(artifact: dict, expected_revision: str, state: dict) -> dict:
    validate_content(artifact, expected_revision)
    require_object(state, "Saved state")
    if state.get("artifact_id") != artifact["artifact_id"] or state.get("revision") != expected_revision:
        raise ValueError("The incoming game state belongs to another artifact or revision")
    if state.get("gate") != "open" or state.get("token") != "ferryman":
        raise ValueError("Entering the ferry requires an open gate and an unspent token")
    actions = state.get("actions")
    if not isinstance(actions, list) or not actions:
        raise ValueError("Saved actions must be a nonempty array")
    choices = []
    for action in actions:
        require_object(action, "Saved action")
        if set(action) == {"choose"}:
            choice = require_text(action["choose"], "Saved direction")
            if choice not in artifact["directions"]:
                raise ValueError("Saved direction is unavailable")
            choices.append(choice)
        elif set(action) == {"pin_line"}:
            index = action["pin_line"]
            if type(index) is not int or not 1 <= index <= len(artifact["lines"]) or artifact.get("aid") != "line-pins":
                raise ValueError("Saved pin does not name an available line action")
        else:
            raise ValueError("Unknown saved action record")
    if choices != [artifact["later_sign"]["direction_id"]]:
        raise ValueError("The saved direction does not reach this ferry")
    return {"artifact_id": artifact["artifact_id"], "revision": expected_revision,
            "gate": "open", "token": None, "voyage_started": True,
            "departed_from": choices[0], "displayed_sign": artifact["later_sign"]["text"],
            "history": ["east-gate-opened", "ferryman-token-spent"],
            "evidence_scope": "a second process consumed the saved direction and token; no human observation"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--expect-revision", required=True)
    parser.add_argument("--pin", type=int, action="append", default=[])
    parser.add_argument("--choose")
    parser.add_argument("--operation", choices=["view", "play", "enter-ferry"], default="play")
    parser.add_argument("--line", type=int, default=1)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        raw = args.artifact.read_bytes()
        artifact = json.loads(raw)
        if args.operation == "view":
            result = view(artifact, args.expect_revision, args.line)
        elif args.operation == "play":
            if args.choose is None:
                raise ValueError("Play requires a direction choice")
            result = play(artifact, args.expect_revision, args.pin, args.choose)
        else:
            if args.state is None:
                raise ValueError("The ferry consumer requires a saved state")
            state_raw = args.state.read_bytes()
            state = require_object(json.loads(state_raw), "Saved state")
            if state.get("input_sha256") != hashlib.sha256(raw).hexdigest():
                raise ValueError("The saved state was produced from different content bytes")
            result = enter_ferry(artifact, args.expect_revision, state)
            result["consumed_state_sha256"] = hashlib.sha256(state_raw).hexdigest()
        result["input_sha256"] = hashlib.sha256(raw).hexdigest()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "invalid", "reason": str(exc)}))
        return 2
    print(json.dumps({"status": "executed", "operation": args.operation, "gate": result.get("gate"), "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
