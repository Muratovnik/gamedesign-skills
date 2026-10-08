#!/usr/bin/env python3
"""Validate a supplied JSON artifact with the installed JSON Schema library."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError, ValidationError
except ImportError as error:
    print(json.dumps({"status": "dependency_unavailable", "error": str(error),
                      "required": "Install scripts/requirements.txt into a disposable or project virtual environment."}), file=sys.stderr)
    raise SystemExit(2)


def read_json(path: Path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        # The stdlib parser accepts NaN/Infinity and overflowing exponents by default.
        json.dumps(value, allow_nan=False)
        return value
    except RecursionError as error:
        raise ValueError("JSON nesting exceeds the supported parser depth.") from error


def validate(instance, schema_path: Path):
    schema = read_json(schema_path)
    try:
        json.dumps(instance, allow_nan=False)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(instance)
    except RecursionError as error:
        raise ValueError("JSON nesting exceeds the supported validation depth.") from error
    return instance


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    try:
        value = validate(read_json(args.input), args.schema)
        print(json.dumps({"status": "valid_format", "input_sha256": digest(args.input),
                          "schema_sha256": digest(args.schema),
                          "inspected_documents": 1, "root_type": type(value).__name__,
                          "limit": "No consumer operation or game property was checked."}))
        return 0
    except (OSError, ValueError, SchemaError, ValidationError) as error:
        print(json.dumps({"status": "invalid_or_missing_evidence", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
