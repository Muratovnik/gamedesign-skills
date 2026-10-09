#!/usr/bin/env python3
"""Import bounded observation rows without turning missing or synthetic data into human evidence."""

import argparse
import csv
import json
from pathlib import Path
import sys

from validate_artifact import digest, read_json, validate
from jsonschema.exceptions import SchemaError, ValidationError

FIELDS = ("participant_id", "object_id", "build_id", "task_id", "attempted", "completed",
          "elapsed_s", "assistance", "report", "missing_reason", "recording_ref")


def import_observations(csv_path: Path, manifest_path: Path):
    manifest = validate(read_json(manifest_path), Path(__file__).resolve().parent.parent / "assets" / "observation.schema.json")
    with csv_path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(FIELDS):
            raise ValueError("Observation columns differ from the documented contract.")
        rows = list(reader)
    if not rows:
        raise ValueError("No observations were supplied.")
    seen = set()
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("A row has an extra or missing CSV field.")
        key = (row["participant_id"], row["object_id"], row["task_id"])
        if key in seen or not all(key):
            raise ValueError("Duplicate or empty observation identity.")
        seen.add(key)
        if row["build_id"] != manifest["build_id"]:
            raise ValueError("Observation and manifest builds differ.")
        if row["attempted"] not in {"yes", "no", "unknown"} or row["completed"] not in {"yes", "no", "unknown"}:
            raise ValueError("Attempt and outcome must be yes, no or unknown.")
        if row["assistance"] not in {"none", "facilitator", "persistent-aid", "unknown"}:
            raise ValueError("Unknown assistance category.")
        if row["completed"] == "yes" and row["attempted"] != "yes":
            raise ValueError("A completed action must have an observed attempt.")
        if row["completed"] == "unknown" and not row["missing_reason"]:
            raise ValueError("Unknown outcomes need a missingness reason.")
        if row["elapsed_s"]:
            elapsed = float(row["elapsed_s"])
            if not 0 <= elapsed < float("inf"):
                raise ValueError("Elapsed seconds must be finite and non-negative.")
        if manifest["record_kind"] != "synthetic" and not row["recording_ref"]:
            raise ValueError("Non-synthetic rows need an inspectable recording or material reference.")
    known = [row for row in rows if row["attempted"] == "yes" and row["completed"] != "unknown"]
    unaided = [row for row in known if row["assistance"] == "none"]
    status = "synthetic_format_demonstration" if manifest["record_kind"] == "synthetic" else "imported_source_requires_interpretation"
    return {"status": status, "source_id": manifest["source_id"], "record_kind": manifest["record_kind"],
            "question": manifest["question"], "game_id": manifest["game_id"], "build_id": manifest["build_id"],
            "conditions": manifest["conditions"], "collection_method": manifest["collection_method"],
            "units": manifest["units"],
            "source_sha256": {"csv": digest(csv_path), "manifest": digest(manifest_path)},
            "rows": rows, "counts": {"all": len(rows), "known_attempt_outcomes": len(known),
                "unknown_outcomes": sum(row["completed"] == "unknown" for row in rows),
                "unaided_known_attempts": len(unaided),
                "unaided_completed": sum(row["completed"] == "yes" for row in unaided)},
            "human_claim": "not_established", "relation_available_as_reported": manifest["relation_available"],
            "limits": manifest["limitations"] + ["Import validates format and preserves records. Authenticity, suitability, and causal interpretation require inspection of the cited material."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = import_observations(args.csv, args.manifest)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write("\n")
        print(json.dumps({"status": result["status"], "counts": result["counts"], "human_claim": result["human_claim"]}))
        return 0
    except (OSError, ValueError, SchemaError, ValidationError) as error:
        print(json.dumps({"status": "invalid_or_missing_evidence", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
