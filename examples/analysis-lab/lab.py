#!/usr/bin/env python3
"""Execute bounded Lantern Crew calculations, state operations and a telemetry query."""

import argparse
import json
from pathlib import Path
import sqlite3
import sys

from economy import resource_path, waiting_distribution
from state import DEFAULT_CONTENT, SKILL, migrate, recover, resumed_survey, validate_state
from telemetry import query
from validate_artifact import digest, read_json, validate
from jsonschema.exceptions import SchemaError, ValidationError


def write_new(path, data):
    encoded = json.dumps(data, indent=2, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8") as stream:
        stream.write(encoded)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for name in ("resources", "migrate", "recover", "survey"):
        sub = subs.add_parser(name)
        sub.add_argument("--input", type=Path, required=True)
        sub.add_argument("--output", type=Path, required=True)
        if name in ("recover", "survey"):
            sub.add_argument("--operation-id", required=True)
        if name == "recover":
            sub.add_argument("--content", type=Path, default=DEFAULT_CONTENT,
                             help="Recovery action repertoire (default: the adjacent fixtures/content.json)")
    wait = subs.add_parser("waiting")
    wait.add_argument("--p", type=float, required=True)
    wait.add_argument("--horizon", type=int, default=30)
    wait.add_argument("--guarantee-at", type=int, default=12)
    wait.add_argument("--output", type=Path, required=True)
    telemetry = subs.add_parser("telemetry")
    for name in ("sessions", "events", "dictionary", "database", "output"):
        telemetry.add_argument("--" + name, type=Path, required=True)
    telemetry.add_argument("--build", required=True)
    telemetry.add_argument("--cohort", required=True)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError("Refusing to replace an existing output file.")
        if args.command == "waiting":
            result = waiting_distribution(args.p, args.horizon, args.guarantee_at)
            code = 0
        elif args.command == "telemetry":
            result = query(args.sessions, args.events, args.dictionary, args.build, args.cohort, args.database)
            code = 0
        else:
            source = read_json(args.input)
            if args.command == "resources":
                validate(source, SKILL / "assets" / "resource-model.schema.json")
                result = resource_path(source)
                code = 0 if result["status"] == "supported" else 1
            elif args.command == "migrate":
                result = migrate(source)
                code = 0
            else:
                result, interpretation = (recover(source, args.operation_id, args.content)
                    if args.command == "recover" else resumed_survey(source, args.operation_id))
                if interpretation["status"] == "refuted":
                    print(json.dumps(interpretation))
                    return 1
                print(json.dumps(interpretation))
                code = 0
        write_new(args.output, result)
        reopened = read_json(args.output)
        if args.command in ("migrate", "recover", "survey"):
            validate_state(reopened)
        if reopened != result:
            raise ValueError("Reopened output differs from producer result.")
        print(json.dumps({"operation": args.command, "status": "consumer_reopened", "output_sha256": digest(args.output),
                          "input_sha256": digest(args.input) if hasattr(args, "input") else None}))
        return code
    except (OSError, ValueError, KeyError, TypeError, SchemaError, ValidationError, sqlite3.Error) as error:
        print(json.dumps({"status": "invalid_or_missing_evidence", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
