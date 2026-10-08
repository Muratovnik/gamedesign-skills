#!/usr/bin/env python3
"""Run this native episode in a disposable project and assess named properties."""

import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import uuid
from importlib.metadata import version

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / "skills" / "game-design"
sys.path.insert(0, str(SKILL / "scripts"))
from validate_artifact import digest, read_json, validate  # noqa: E402
from jsonschema.exceptions import SchemaError, ValidationError  # noqa: E402

SOURCES = ("project.godot", "episode.tscn", "episode.gd", "player.gd")
REPORT_SCHEMA = SKILL / "assets" / "episode-report.schema.json"
CLAIMS = ("escape", "recovery-blocked", "body-blocked", "camera-signals")


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def source_identity():
    return {name: digest(HERE / name) for name in SOURCES}


def run(godot: Path, fixture_path: Path, output: Path):
    fixture_path = fixture_path.resolve()
    validate(read_json(fixture_path), SKILL / "assets" / "episode.schema.json")
    godot = godot.resolve(strict=True)
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    project = output / "project"
    project.mkdir()
    before = source_identity()
    for name in SOURCES:
        shutil.copy2(HERE / name, project / name)
    shutil.copy2(fixture_path, output / "fixture.json")
    env = os.environ.copy()
    for key, directory in (("XDG_CONFIG_HOME", "config"), ("XDG_DATA_HOME", "data"), ("XDG_CACHE_HOME", "cache")):
        target = output / "host-state" / directory
        target.mkdir(parents=True)
        env[key] = str(target)
    env["GODOT_SILENCE_ROOT_WARNING"] = "1"
    run_id = str(uuid.uuid4())
    receipt = {"run_id": run_id, "status": "attempted", "host": platform.platform(),
               "python": sys.version, "binary_path": str(godot), "binary_sha256": digest(godot),
               "fixture_sha256": digest(fixture_path), "source_sha256": before, "commands": [],
               "qualification_source_sha256": digest(Path(__file__)),
               "schema_sha256": digest(SKILL / "assets" / "episode.schema.json"),
               "report_schema_sha256": digest(REPORT_SCHEMA),
               "jsonschema_version": version("jsonschema")}
    commands = [
        [str(godot), "--version"],
        [str(godot), "--headless", "--path", str(project), "--editor", "--import", "--quit"],
        [str(godot), "--headless", "--path", str(project), "--", "--fixture=" + str(output / "fixture.json"),
         "--output=" + str(output / "report.json"), "--run-id=" + run_id],
    ]
    for phase, command in zip(("version", "native-import", "native-execution"), commands):
        try:
            result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=30, check=False)
        except (OSError, subprocess.TimeoutExpired) as error:
            if isinstance(error, subprocess.TimeoutExpired):
                for channel in ("stdout", "stderr"):
                    partial = getattr(error, channel) or b""
                    if isinstance(partial, bytes):
                        partial = partial.decode("utf-8", errors="replace")
                    (output / (phase + "." + channel + ".log")).write_text(partial, encoding="utf-8")
            receipt["commands"].append({"phase": phase, "argv": command, "exit_code": None})
            receipt.update(status="unavailable", failed_phase=phase, error=str(error))
            write_json(output / "receipt.json", receipt)
            return 2
        (output / (phase + ".stdout.log")).write_text(result.stdout, encoding="utf-8")
        (output / (phase + ".stderr.log")).write_text(result.stderr, encoding="utf-8")
        receipt["commands"].append({"phase": phase, "argv": command, "exit_code": result.returncode})
        if phase == "version":
            receipt["engine_version"] = result.stdout.strip()
        if result.returncode != 0:
            receipt.update(status="unavailable", failed_phase=phase)
            write_json(output / "receipt.json", receipt)
            return 2
    if not (output / "report.json").is_file():
        receipt.update(status="unavailable", failed_phase="missing_consumer_report")
    else:
        try:
            report = validate(read_json(output / "report.json"), REPORT_SCHEMA)
            exact = (report["run_id"] == run_id and report["fixture_sha256"] == receipt["fixture_sha256"]
                     and report["source_sha256"] == before and source_identity() == before)
            receipt.update(status="consumer_executed" if exact else "invalid_evidence", identity_matches=exact,
                           report_sha256=digest(output / "report.json"))
        except (OSError, ValueError, TypeError, SchemaError, ValidationError) as error:
            receipt.update(status="invalid_evidence", failed_phase="report_validation", error=str(error))
    write_json(output / "receipt.json", receipt)
    return 0 if receipt["status"] == "consumer_executed" else 2


def assess(fixture_path: Path, report_path: Path, claim: str):
    try:
        if claim not in CLAIMS:
            raise ValueError("Unsupported episode claim.")
        fixture = validate(read_json(fixture_path), SKILL / "assets" / "episode.schema.json")
        report = validate(read_json(report_path), REPORT_SCHEMA)
    except (OSError, ValueError, TypeError, SchemaError, ValidationError) as error:
        return 2, {"claim": claim, "status": "invalid_evidence", "reason": "invalid_or_missing_report_or_fixture",
                   "error": getattr(error, "message", str(error))}
    if (report.get("fixture_sha256") != digest(fixture_path) or report.get("source_sha256") != source_identity()
            or report.get("game_id") != fixture["game_id"] or report.get("build_id") != fixture["build_id"]
            or report["case_id"] != fixture["case_id"]
            or report["physics_ticks_per_second"] != fixture["units"]["tick_rate_hz"]):
        return 2, {"claim": claim, "status": "invalid_evidence", "reason": "source_or_fixture_identity_mismatch"}
    events = report.get("events", [])
    trajectory = report.get("trajectory", [])
    if not events or not trajectory or report.get("status") != "consumer_executed":
        return 2, {"claim": claim, "status": "missing_evidence", "reason": "empty_or_unexecuted_observation"}
    threats = [event for event in events if event["kind"] == "threat_resolved"]
    if len(threats) != 2 or {event["detail"]["threat_id"] for event in threats} != {t["id"] for t in fixture["threats"]}:
        return 2, {"claim": claim, "status": "missing_evidence", "reason": "threats_not_observed"}
    received = [event for event in events if event["kind"] == "input_received"]
    injected = [event for event in events if event["kind"] == "input_injected"]
    pipeline = bool(injected) and len(received) == len(injected) and all(
        a["run_tick"] == b["run_tick"] and a["detail"]["action"] == b["detail"]["action"]
        for a, b in zip(injected, received))
    attack = [event for event in events if event["kind"] == "attack_started"]
    dodge = [event for event in events if event["kind"] == "dodge_started"]
    if claim == "escape":
        expected_line = "The winch route is ready."
        properties = {
            "input_reached_controller": pipeline,
            "committed_attack_executed": len(attack) == 1 and attack[0]["detail"]["cancellable"] is False,
            "dodge_after_recovery": len(dodge) == 1 and len(attack) == 1
                and dodge[0]["world_tick"] >= attack[0]["detail"]["recovery_until"],
            "two_threats_avoided": all(event["detail"]["hit"] is False for event in threats),
            "body_crossed": any(row["position_px"][0] >= 152 for row in trajectory),
            "native_reload_preserved_relations": report.get("restored_equal") is True,
            "restored_knowledge_used": report.get("npc_reply") == expected_line
                and "gate-crossed" in report["final_state"]["knowledge"]["keeper-ivo"],
            "owner_preserved": report["final_state"]["right_owners"] == {"winch": "bo", "archive-pass": "ava"},
            "history_not_duplicated": report["final_state"]["history"].count("archive-message") == 1,
        }
    elif claim == "recovery-blocked":
        properties = {"input_reached_controller": pipeline, "attack_executed": len(attack) == 1,
                      "dodge_refused_during_commitment": any(e["kind"] == "action_rejected"
                           and e["detail"].get("reason") == "committed_recovery" for e in events),
                      "damage_observed": any(e["detail"]["hit"] is True for e in threats),
                      "no_dodge_started": not dodge}
    elif claim == "body-blocked":
        geometry = [event["detail"] for event in events if event["kind"] == "geometry_witness"]
        properties = {"input_reached_controller": pipeline, "dodge_executed": len(dodge) == 1,
                      "point_ray_clear": len(geometry) == 1 and geometry[0]["center_ray_clear"] is True,
                      "actual_body_collision": report.get("body_collision_ticks", 0) > 0,
                      "body_not_crossed": all(row["position_px"][0] < 152 for row in trajectory)}
    else:
        warnings = [event["detail"] for event in events if event["kind"] == "warning_presented"]
        properties = {"both_warnings_observed": len(warnings) == 2,
                      "signals_inside_camera_rectangle": len(warnings) == 2 and all(w["inside_camera_rect"] is True for w in warnings)}
    code = 0 if all(properties.values()) else 1
    return code, {"claim": claim, "status": "supported" if code == 0 else "refuted",
                  "inspected_events": len(events), "inspected_physics_steps": len(trajectory),
                  "properties": properties, "report_sha256": digest(report_path)}


def suite(godot: Path, output: Path):
    output.mkdir(parents=True, exist_ok=False)
    expected = {"baseline": {"escape": 1, "recovery-blocked": 0},
                "candidate": {"escape": 0, "camera-signals": 0},
                "recovery-locked": {"escape": 1, "recovery-blocked": 0},
                "narrow-gap": {"escape": 1, "body-blocked": 0},
                "off-camera": {"escape": 0, "camera-signals": 1},
                "no-input": {"escape": 1}}
    outcomes = []
    for name, claims in expected.items():
        fixture = HERE / "fixtures" / (name + ".json")
        case_output = output / name
        operation = run(godot, fixture, case_output)
        if operation:
            outcomes.append({"case": name, "operation_exit": operation, "expected": 0})
            write_json(output / "suite.json", {"status": "unavailable", "outcomes": outcomes})
            return 2
        for claim, expected_code in claims.items():
            actual, result = assess(fixture, case_output / "report.json", claim)
            write_json(case_output / (claim + ".json"), result)
            outcomes.append({"case": name, "claim": claim, "actual": actual, "expected": expected_code})
    stale, result = assess(HERE / "fixtures" / "candidate.json", output / "baseline" / "report.json", "escape")
    outcomes.append({"case": "stale-baseline-as-candidate", "actual": stale, "expected": 2})
    write_json(output / "stale-control.json", result)
    okay = all(row.get("actual") == row.get("expected") for row in outcomes)
    write_json(output / "suite.json", {"status": "supported" if okay else "refuted", "outcomes": outcomes,
                                      "limits": "Synthetic single-process Godot execution. No rendered/audio/human or network outcome."})
    print(json.dumps({"status": "supported" if okay else "refuted", "checked_controls": len(outcomes), "output": str(output)}))
    return 0 if okay else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("run", "suite"):
        sub = commands.add_parser(name)
        sub.add_argument("--godot", required=True, type=Path)
        sub.add_argument("--out", required=True, type=Path)
        if name == "run":
            sub.add_argument("--fixture", required=True, type=Path)
    sub = commands.add_parser("assess")
    sub.add_argument("--fixture", required=True, type=Path)
    sub.add_argument("--report", required=True, type=Path)
    sub.add_argument("--claim", required=True, choices=CLAIMS)
    args = parser.parse_args()
    try:
        if args.command == "suite":
            return suite(args.godot, args.out)
        if args.command == "run":
            return run(args.godot, args.fixture, args.out)
        code, result = assess(args.fixture, args.report, args.claim)
        print(json.dumps(result, indent=2))
        return code
    except (OSError, ValueError, KeyError, TypeError, SchemaError, ValidationError) as error:
        print(json.dumps({"status": "invalid_or_missing_evidence", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
