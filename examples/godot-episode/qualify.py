#!/usr/bin/env python3
"""Run this native episode in a disposable project and assess named properties."""

import argparse
import json
import math
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


def read_fixture(path):
    fixture = validate(read_json(path), SKILL / "assets" / "episode.schema.json")
    threats = fixture["threats"]
    if len({threat["id"] for threat in threats}) != len(threats):
        raise ValueError("Threat identities must be distinct.")
    if any(not threat["warning_tick"] <= threat["resolve_tick"] <= fixture["stop_tick"] for threat in threats):
        raise ValueError("Each warning must occur no later than its resolution, within the run horizon.")
    return fixture


def validate_timeout(seconds):
    if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("The phase timeout must be a finite positive number of seconds.")
    return seconds


def run(godot: Path, fixture_path: Path, output: Path, timeout_seconds=30):
    validate_timeout(timeout_seconds)
    fixture_path = fixture_path.resolve()
    read_fixture(fixture_path)
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
               "timeout_seconds": timeout_seconds,
               "jsonschema_version": version("jsonschema")}
    commands = [
        [str(godot), "--version"],
        [str(godot), "--headless", "--path", str(project), "--editor", "--import", "--quit"],
        [str(godot), "--headless", "--path", str(project), "--", "--fixture=" + str(output / "fixture.json"),
         "--output=" + str(output / "report.json"), "--run-id=" + run_id],
    ]
    for phase, command in zip(("version", "native-import", "native-execution"), commands):
        try:
            result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=timeout_seconds, check=False)
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


def operation_evidence(fixture, report):
    """Check report completeness/consistency; this does not authenticate an engine run."""
    events = report["events"]
    if [event["sequence"] for event in events] != list(range(len(events))):
        raise ValueError("Event sequence is incomplete or out of order.")
    if any(a["run_tick"] > b["run_tick"] for a, b in zip(events, events[1:])):
        raise ValueError("Event run ticks are out of order.")
    loaded = [event for event in events if event["kind"] == "fixture_loaded"]
    if (len(loaded) != 1 or loaded[0]["sequence"] != 0 or loaded[0]["run_tick"] != 0
            or loaded[0]["detail"]["case_id"] != fixture["case_id"]
            or loaded[0]["detail"]["fixture_sha256"] != report["fixture_sha256"]):
        raise ValueError("The initial fixture observation disagrees with the report identity.")
    injected = [event for event in events if event["kind"] == "input_injected"]
    received = [event for event in events if event["kind"] == "input_received"]
    expected = [(item["tick"], item["action"]) for item in sorted(fixture["input_schedule"], key=lambda item: item["tick"])
                if item["tick"] <= fixture["stop_tick"]]
    if [(event["run_tick"], event["detail"]["action"]) for event in injected] != expected:
        raise ValueError("Injected input evidence does not cover the fixture schedule within the run horizon.")
    if report["input_received_count"] != len(received):
        raise ValueError("The received-input summary disagrees with the event population.")
    pipeline = bool(injected) and len(received) == len(injected) and all(
        a["run_tick"] == b["run_tick"] and a["detail"]["action"] == b["detail"]["action"]
        and a["sequence"] < b["sequence"] < (injected[index + 1]["sequence"] if index + 1 < len(injected) else len(events))
        for index, (a, b) in enumerate(zip(injected, received)))
    outcomes = {"save": {"state_saved", "save_failed"}, "reset": {"state_reset"},
                "load": {"state_restored", "load_failed"}, "interact": {"npc_reply"}}
    observed = []
    for index, command in enumerate(injected):
        action = command["detail"]["action"]
        if action not in outcomes:
            continue
        end = injected[index + 1]["sequence"] if index + 1 < len(injected) else len(events)
        delivery = [event for event in received if command["sequence"] < event["sequence"] < end
                    and event["run_tick"] == command["run_tick"] and event["detail"]["action"] == action]
        if len(delivery) != 1:
            raise ValueError("Missing or ambiguous controller delivery for scheduled " + action)
        results = [event for event in events if delivery[0]["sequence"] < event["sequence"] < end
                   and event["run_tick"] == command["run_tick"] and event["kind"] in outcomes[action]]
        if len(results) != 1:
            raise ValueError("Missing or ambiguous operation result for scheduled " + action)
        if results[0]["kind"] in ("save_failed", "load_failed"):
            raise ValueError("Native state operation was unavailable: " + results[0]["kind"])
        observed.append(results[0])
    kinds = set().union(*outcomes.values())
    if {event["sequence"] for event in events if event["kind"] in kinds} != {event["sequence"] for event in observed}:
        raise ValueError("An operation result has no matching scheduled controller input.")
    saves = [event for event in observed if event["kind"] == "state_saved"]
    restores = [event for event in observed if event["kind"] == "state_restored"]
    replies = [event for event in observed if event["kind"] == "npc_reply"]
    saved = report["saved_state"]
    if bool(saved) != bool(saves):
        raise ValueError("The saved snapshot and save-operation evidence disagree.")
    for snapshot in (report["final_state"], saved):
        if snapshot and (snapshot["game_id"] != fixture["game_id"] or snapshot["build_id"] != fixture["build_id"]
                         or snapshot["actor"]["id"] != fixture["actor"]["id"]):
            raise ValueError("A state snapshot belongs to a different game, build or actor.")
    if saves and saved["world_tick"] != saves[-1]["world_tick"]:
        raise ValueError("The retained snapshot does not describe the last save operation.")
    restore = restores[-1] if restores else None
    reply = replies[-1] if replies else None
    if report["restored_equal"] != (restore["detail"]["matches_saved_relations"] if restore else False):
        raise ValueError("The reload summary disagrees with the observed restore operation.")
    if report["npc_reply"] != (reply["detail"]["line"] if reply else ""):
        raise ValueError("The NPC summary disagrees with the observed reply.")
    reload_chain = bool(restore and saves and saves[-1]["sequence"] < restore["sequence"] and any(
        event["kind"] == "state_reset" and saves[-1]["sequence"] < event["sequence"] < restore["sequence"]
        for event in observed))
    reset_after_restore = bool(restore and any(event["kind"] == "state_reset"
        and event["sequence"] > restore["sequence"] for event in observed))
    if reload_chain and restore["detail"]["matches_saved_relations"] and (
            restore["world_tick"] != saved["world_tick"] or restore["detail"]["world_tick"] != saved["world_tick"]
            or restore["detail"]["actor_x_px"] != saved["actor"]["position_px"][0]):
        raise ValueError("A successful restore claim contradicts the retained saved state.")
    if reload_chain and report["restored_equal"] and not reset_after_restore:
        # This scene can append crossing history and witnessed knowledge after load.
        # Its existing owner map cannot change; pre-existing relations cannot disappear.
        later = [event for event in events if event["sequence"] > restore["sequence"]]
        expected_history = saved["history"] + ["gate-crossed" for event in later if event["kind"] == "gate_crossed"]
        expected_knowledge = {actor: list(facts) for actor, facts in saved["knowledge"].items()}
        for event in later:
            if event["kind"] == "knowledge_acquired":
                actor = event["detail"]["actor_id"]
                if actor not in expected_knowledge:
                    raise ValueError("Later knowledge refers to an actor absent from the saved knowledge map.")
                expected_knowledge[actor].append(event["detail"]["fact_id"])
        final = report["final_state"]
        if (final["right_owners"] != saved["right_owners"] or final["history"] != expected_history
                or final["knowledge"] != expected_knowledge):
            raise ValueError("Saved owners, history or knowledge contradict the downstream state and observed later effects.")
    return {"pipeline": pipeline, "reload_chain": reload_chain, "restore": restore, "reply": reply,
            "reset_after_restore": reset_after_restore}


def assess(fixture_path: Path, report_path: Path, claim: str):
    try:
        if claim not in CLAIMS:
            raise ValueError("Unsupported episode claim.")
        fixture = read_fixture(fixture_path)
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
    try:
        operations = operation_evidence(fixture, report)
    except ValueError as error:
        return 2, {"claim": claim, "status": "invalid_evidence", "reason": "invalid_or_missing_operation_evidence", "error": str(error)}
    pipeline = operations["pipeline"]
    attack = [event for event in events if event["kind"] == "attack_started"]
    dodge = [event for event in events if event["kind"] == "dodge_started"]
    if claim == "escape":
        expected_line = "The winch route is ready."
        reply = operations["reply"]
        reloaded = operations["reload_chain"] and report["restored_equal"]
        properties = {
            "input_reached_controller": pipeline,
            "committed_attack_executed": len(attack) == 1 and attack[0]["detail"]["cancellable"] is False,
            "dodge_after_recovery": len(dodge) == 1 and len(attack) == 1
                and dodge[0]["world_tick"] >= attack[0]["detail"]["recovery_until"],
            "two_threats_avoided": all(event["detail"]["hit"] is False for event in threats),
            "body_crossed": any(row["position_px"][0] >= 152 for row in trajectory),
            "native_reload_preserved_relations": reloaded,
            "restored_knowledge_used": bool(reloaded and reply and not operations["reset_after_restore"]
                and reply["sequence"] > operations["restore"]["sequence"]
                and reply["detail"]["speaker_id"] == "keeper-ivo" and reply["detail"]["line"] == expected_line
                and "gate-crossed" in reply["detail"]["known_fact_ids"]
                and "gate-crossed" in report["saved_state"]["knowledge"]["keeper-ivo"]
                and "gate-crossed" in report["final_state"]["knowledge"]["keeper-ivo"]),
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


def suite(godot: Path, output: Path, timeout_seconds=30):
    validate_timeout(timeout_seconds)
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
        operation = run(godot, fixture, case_output, timeout_seconds)
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
        sub.add_argument("--timeout-seconds", type=float, default=30,
                         help="Finite positive bound for each native phase; default 30, with no automatic retry")
        if name == "run":
            sub.add_argument("--fixture", required=True, type=Path)
    sub = commands.add_parser("assess")
    sub.add_argument("--fixture", required=True, type=Path)
    sub.add_argument("--report", required=True, type=Path)
    sub.add_argument("--claim", required=True, choices=CLAIMS)
    args = parser.parse_args()
    try:
        if args.command == "suite":
            return suite(args.godot, args.out, args.timeout_seconds)
        if args.command == "run":
            return run(args.godot, args.fixture, args.out, args.timeout_seconds)
        code, result = assess(args.fixture, args.report, args.claim)
        print(json.dumps(result, indent=2))
        return code
    except (OSError, ValueError, KeyError, TypeError, SchemaError, ValidationError) as error:
        print(json.dumps({"status": "invalid_or_missing_evidence", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
