"""Import synthetic session and event CSVs into SQLite and query their declared meanings."""

import csv
from contextlib import closing
from pathlib import Path
import sqlite3

from state import SKILL
from validate_artifact import digest, read_json, validate


def csv_rows(path, fields):
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != fields:
            raise ValueError("Unexpected CSV columns in " + path.name)
        rows = list(reader)
    if not rows:
        raise ValueError("An input table is empty: " + path.name)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError("A CSV row has extra or missing columns.")
    return rows


def query(sessions_path, events_path, dictionary_path, build_id, cohort, database_path):
    dictionary = validate(read_json(dictionary_path), SKILL / "assets" / "telemetry-dictionary.schema.json")
    if build_id not in dictionary["builds"]:
        raise ValueError("No outcome definition exists for this build.")
    definition = dictionary["builds"][build_id]
    sessions = csv_rows(sessions_path, ["session_id", "actor_id", "game_id", "build_id", "cohort", "capture_complete", "expected_resolution_tick"])
    events = csv_rows(events_path, ["event_id", "session_id", "build_id", "sequence_no", "run_tick", "event_name"])
    with closing(sqlite3.connect(":memory:")) as database:
        database.row_factory = sqlite3.Row
        database.executescript("""
            PRAGMA foreign_keys = ON;
            CREATE TABLE sessions (
                session_id TEXT PRIMARY KEY, actor_id TEXT NOT NULL, game_id TEXT NOT NULL,
                build_id TEXT NOT NULL, cohort TEXT NOT NULL,
                capture_complete INTEGER NOT NULL CHECK (capture_complete IN (0, 1)),
                expected_resolution_tick INTEGER NOT NULL CHECK (expected_resolution_tick >= 0),
                UNIQUE (session_id, build_id));
            CREATE TABLE events (
                event_id TEXT PRIMARY KEY, session_id TEXT NOT NULL, build_id TEXT NOT NULL,
                sequence_no INTEGER NOT NULL CHECK (sequence_no > 0),
                run_tick INTEGER NOT NULL CHECK (run_tick >= 0), event_name TEXT NOT NULL,
                FOREIGN KEY (session_id, build_id) REFERENCES sessions (session_id, build_id),
                UNIQUE (session_id, sequence_no));
        """)
        for row in sessions:
            if not all(row.values()) or row["game_id"] != dictionary["game_id"] or row["build_id"] not in dictionary["builds"]:
                raise ValueError("Session identity or game/build meaning is missing.")
            database.execute("INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
                (row["session_id"], row["actor_id"], row["game_id"], row["build_id"], row["cohort"],
                 int(row["capture_complete"]), int(row["expected_resolution_tick"])))
        for row in events:
            if row["build_id"] not in dictionary["builds"] or row["event_name"] not in dictionary["builds"][row["build_id"]]["allowed_events"]:
                raise ValueError("Unknown event meaning for this build.")
            database.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)",
                (row["event_id"], row["session_id"], row["build_id"], int(row["sequence_no"]), int(row["run_tick"]), row["event_name"]))
        backwards = database.execute("""SELECT COUNT(*) FROM (
            SELECT run_tick, LAG(run_tick) OVER (PARTITION BY session_id ORDER BY sequence_no) AS previous_tick
            FROM events) WHERE run_tick < previous_tick""").fetchone()[0]
        if backwards:
            raise ValueError("The declared monotonic run clock moved backwards.")
        sql_path = Path(__file__).with_name("outcome-query.sql")
        rows = [dict(row) for row in database.execute(sql_path.read_text(),
            {"build_id": build_id, "cohort": cohort, "outcome_event": definition["outcome_event"],
             "before_resolution": int(definition["requires_before_resolution"])})]
        if not rows:
            raise ValueError("No sessions in the requested build and cohort.")
        if database_path.exists():
            raise ValueError("Refusing to replace an existing output database.")
        database.commit()
        with closing(sqlite3.connect(database_path)) as durable_database:
            database.backup(durable_database)
    with closing(sqlite3.connect(database_path)) as reopened:
        reopened_sessions = reopened.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        reopened_events = reopened.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    counts = {name: sum(row["outcome"] == name for row in rows) for name in ("success", "failure", "unknown", "not_attempted")}
    known = counts["success"] + counts["failure"]
    return {"status": "queried", "record_kind": "synthetic", "game_id": dictionary["game_id"],
            "build_id": build_id, "cohort": cohort, "outcome_definition": definition["meaning"],
            "clock": dictionary["clock"], "sessions": rows, "counts": counts, "selected_sessions": len(rows),
            "success_fraction_among_known_attempts": counts["success"] / known if known else None,
            "known_attempt_denominator": known, "reopened_database": {"sessions": reopened_sessions, "events": reopened_events},
            "input_sha256": {"sessions": digest(sessions_path), "events": digest(events_path),
                             "dictionary": digest(dictionary_path), "query": digest(sql_path)},
            "limits": ["Synthetic fixture counts are not observed audience frequencies.",
                       "Build-specific event definitions cannot be pooled into a causal change estimate.",
                       "Missing capture, event sequence gaps, or missing end events remain unknown outcomes."]}
