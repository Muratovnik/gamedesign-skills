"""Public protocol regressions around one preserved native report; no engine run."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from qualify import assess as assess_report, digest, read_fixture, validate_timeout

HERE = Path(__file__).resolve().parent
RECORDED = HERE / "fixtures" / "test_recorded_candidate_report.json"


class ReportContractTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads(RECORDED.read_text(encoding="utf-8"))

    def assess(self, report, claim="escape", fixture="candidate.json", raw=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            path.write_text(json.dumps(report) if raw is None else raw)
            return assess_report(HERE / "fixtures" / fixture, path, claim)

    def assert_invalid(self, result):
        code, response = result
        self.assertEqual(code, 2, response)
        self.assertIn(response["status"], ("invalid_evidence", "invalid_or_missing_evidence", "missing_evidence"))

    def renumber(self, report):
        for index, event in enumerate(report["events"]):
            event["sequence"] = index
        report["input_received_count"] = sum(event["kind"] == "input_received" for event in report["events"])

    def test_scheduled_state_operations_cannot_disappear_behind_positive_summaries(self):
        for missing in ("state_saved", "state_reset", "state_restored", "npc_reply", "whole-state-pipeline"):
            with self.subTest(missing=missing):
                report = deepcopy(self.report)
                if missing == "whole-state-pipeline":
                    report["events"] = [event for event in report["events"]
                        if event["kind"] not in ("state_saved", "state_reset", "state_restored", "npc_reply")
                        and not (event["kind"] in ("input_injected", "input_received")
                                 and event["detail"]["action"] in ("save", "reset", "load", "interact"))]
                else:
                    report["events"] = [event for event in report["events"] if event["kind"] != missing]
                self.renumber(report)
                self.assert_invalid(self.assess(report))

    def test_operation_summaries_and_snapshot_must_match_observed_events(self):
        mutations = [
            lambda report: report.__setitem__("saved_state", {}),
            lambda report: report.__setitem__("input_received_count", report["input_received_count"] + 1),
            lambda report: report.__setitem__("restored_equal", False),
            lambda report: report.__setitem__("npc_reply", "A summary without its matching reply."),
            lambda report: next(event for event in report["events"] if event["kind"] == "state_restored")["detail"].__setitem__("actor_x_px", 40),
            lambda report: report["events"][0]["detail"].__setitem__("fixture_sha256", "0" * 64),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index):
                report = deepcopy(self.report)
                mutate(report)
                self.assert_invalid(self.assess(report))

    def test_observed_reload_and_reply_failures_refute_while_unavailable_save_is_invalid(self):
        changed = deepcopy(self.report)
        changed["restored_equal"] = False
        next(event for event in changed["events"] if event["kind"] == "state_restored")["detail"]["matches_saved_relations"] = False
        code, response = self.assess(changed)
        self.assertEqual(code, 1, response)
        self.assertFalse(response["properties"]["native_reload_preserved_relations"])
        changed = deepcopy(self.report)
        reply = next(event for event in changed["events"] if event["kind"] == "npc_reply")
        reply["detail"].update(known_fact_ids=[], line="I have not seen a crossing.")
        changed["npc_reply"] = reply["detail"]["line"]
        code, response = self.assess(changed)
        self.assertEqual(code, 1, response)
        self.assertFalse(response["properties"]["restored_knowledge_used"])
        changed = deepcopy(self.report)
        saved = next(event for event in changed["events"] if event["kind"] == "state_saved")
        saved.update(kind="save_failed", detail={"error": 1})
        self.assert_invalid(self.assess(changed))

    def test_saved_owners_history_and_knowledge_cannot_contradict_successful_reload(self):
        mutations = [
            lambda report: report["saved_state"]["right_owners"].__setitem__("winch", "cy"),
            lambda report: report["saved_state"]["history"].remove("archive-message"),
            lambda report: report["saved_state"]["history"].append("archive-message"),
            lambda report: report["saved_state"]["knowledge"]["bo"].clear(),
            lambda report: report["final_state"]["knowledge"]["bo"].clear(),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(case=index):
                report = deepcopy(self.report)
                mutate(report)
                self.assert_invalid(self.assess(report))

    def test_observed_post_load_additions_are_valid_but_are_not_restored_knowledge(self):
        # Synthetic protocol control permits this scene's later knowledge/history effects.
        report = deepcopy(self.report)
        report["saved_state"]["history"].remove("gate-crossed")
        report["saved_state"]["knowledge"]["keeper-ivo"] = []
        additions = [event for event in report["events"] if event["kind"] in ("knowledge_acquired", "gate_crossed")]
        report["events"] = [event for event in report["events"] if event not in additions]
        index = next(index for index, event in enumerate(report["events"]) if event["kind"] == "state_restored") + 1
        for event in additions:
            event.update(run_tick=47, world_tick=43, game_time_s=43 / 60)
        report["events"][index:index] = additions
        self.renumber(report)
        code, response = self.assess(report)
        self.assertEqual(code, 1, response)
        self.assertTrue(response["properties"]["native_reload_preserved_relations"])
        self.assertFalse(response["properties"]["restored_knowledge_used"])

    def test_empty_scheduled_input_is_a_valid_refutation_of_escape(self):
        # Synthetic protocol control: these altered bytes are not a new native run.
        changed = deepcopy(self.report)
        fixture_path = HERE / "fixtures" / "no-input.json"
        fixture = json.loads(fixture_path.read_text())
        changed.update(case_id=fixture["case_id"], build_id=fixture["build_id"], fixture_sha256=digest(fixture_path),
                       saved_state={}, restored_equal=False, npc_reply="", run_id="synthetic-no-input-contract-control")
        changed["final_state"]["build_id"] = fixture["build_id"]
        changed["events"] = [event for event in changed["events"] if event["kind"] not in (
            "input_injected", "input_received", "attack_started", "dodge_started", "state_saved", "state_reset", "state_restored", "npc_reply")]
        changed["events"][0]["detail"].update(case_id=fixture["case_id"], fixture_sha256=digest(fixture_path))
        self.renumber(changed)
        code, response = self.assess(changed, fixture="no-input.json")
        self.assertEqual(code, 1, response)
        self.assertFalse(response["properties"]["input_reached_controller"])

    def test_recorded_success_and_typed_negative_observations(self):
        self.report["inspection_note"] = "Additional diagnostic metadata does not change the observation."
        self.assertEqual(self.assess(self.report)[0], 0)
        hit = deepcopy(self.report)
        next(e for e in hit["events"] if e["kind"] == "threat_resolved")["detail"]["hit"] = True
        self.assertEqual(self.assess(hit)[0], 1)
        off_camera = deepcopy(self.report)
        next(e for e in off_camera["events"] if e["kind"] == "warning_presented")["detail"]["inside_camera_rect"] = False
        self.assertEqual(self.assess(off_camera, "camera-signals")[0], 1)

    def test_cli_wrong_root_has_structured_exit_two(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            path.write_text("[]")
            result = subprocess.run(
                [sys.executable, "-B", str(HERE / "qualify.py"), "assess",
                 "--fixture", str(HERE / "fixtures" / "candidate.json"), "--report", str(path), "--claim", "escape"],
                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn(json.loads(result.stderr or result.stdout)["status"], ("invalid_evidence", "invalid_or_missing_evidence"))
        self.assertNotIn("Traceback", result.stderr)

    def test_wrong_report_roots_are_invalid_evidence(self):
        for value in ([], None, True, 7, "report"):
            with self.subTest(root=value):
                self.assert_invalid(self.assess(value))

    def test_malformed_observation_records_cannot_support_or_refute(self):
        mutations = [
            ("event record", lambda r: r["events"].__setitem__(0, []), "escape"),
            ("detail record", lambda r: r["events"][0].__setitem__("detail", []), "escape"),
            ("position dimension", lambda r: r["trajectory"][0].__setitem__("position_px", [160]), "escape"),
            ("position boolean", lambda r: r["trajectory"][0].__setitem__("position_px", [True, 90]), "escape"),
            ("position infinity", lambda r: r["trajectory"][0].__setitem__("position_px", [float("inf"), 90]), "escape"),
            ("time NaN", lambda r: r["events"][0].__setitem__("game_time_s", float("nan")), "escape"),
            ("tick boolean", lambda r: r["trajectory"][0].__setitem__("run_tick", True), "escape"),
            ("state record", lambda r: r.__setitem__("final_state", []), "escape"),
            ("knowledge string", lambda r: r["final_state"]["knowledge"].__setitem__("keeper-ivo", "gate-crossed"), "escape"),
            ("history string", lambda r: r["final_state"].__setitem__("history", "archive-message"), "escape"),
            ("restore numeric", lambda r: r.__setitem__("restored_equal", 1), "escape"),
            ("collision boolean", lambda r: r.__setitem__("body_collision_ticks", True), "body-blocked"),
        ]
        for field, kind, key, value, claim in [
            ("hit list", "threat_resolved", "hit", [], "escape"),
            ("hit zero", "threat_resolved", "hit", 0, "escape"),
            ("hit null", "threat_resolved", "hit", None, "escape"),
            ("hit string", "threat_resolved", "hit", "false", "escape"),
            ("camera string", "warning_presented", "inside_camera_rect", "false", "camera-signals"),
            ("ray list", "geometry_witness", "center_ray_clear", [], "body-blocked"),
            ("recovery boolean", "attack_started", "recovery_until", True, "escape"),
        ]:
            mutations.append((field, lambda r, k=kind, f=key, v=value:
                              next(e for e in r["events"] if e["kind"] == k)["detail"].__setitem__(f, v), claim))
        for name, mutate, claim in mutations:
            with self.subTest(field=name):
                report = deepcopy(self.report)
                mutate(report)
                self.assert_invalid(self.assess(report, claim))
        raw = json.dumps(self.report).replace('"body_collision_ticks": 0', '"body_collision_ticks": 1e999')
        self.assert_invalid(self.assess(None, raw=raw))

    def test_empty_and_stale_evidence_keep_distinct_non_success_status(self):
        empty = deepcopy(self.report)
        empty["events"] = []
        self.assert_invalid(self.assess(empty))
        self.assert_invalid(self.assess(self.report, fixture="baseline.json"))


class FixtureAndRunnerBoundaryTests(unittest.TestCase):
    def test_first_tick_and_warning_resolution_order_are_checked_before_run(self):
        original = json.loads((HERE / "fixtures" / "candidate.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            for warning, resolution, valid in ((0, 26, False), (1, 26, True), (1, 1, True),
                                                (27, 26, False), (1, original["stop_tick"] + 1, False)):
                with self.subTest(warning=warning, resolution=resolution):
                    fixture = deepcopy(original)
                    fixture["threats"][0].update(warning_tick=warning, resolve_tick=resolution)
                    path.write_text(json.dumps(fixture))
                    if valid:
                        self.assertEqual(read_fixture(path)["threats"][0]["warning_tick"], warning)
                    else:
                        result = subprocess.run([sys.executable, "-B", str(HERE / "qualify.py"), "run",
                            "--fixture", str(path), "--godot", str(Path(directory) / "absent-godot"),
                            "--out", str(Path(directory) / "uncreated")], capture_output=True, text=True, check=False, timeout=15)
                        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                        self.assertNotIn("Traceback", result.stderr)
                        self.assertNotIn("absent-godot", result.stderr, "Reject the fixture before attempting the engine boundary")
                        self.assertFalse((Path(directory) / "uncreated").exists())

    def test_timeout_bound_is_finite_positive_and_invalid_cli_has_no_side_effect(self):
        self.assertEqual(validate_timeout(30), 30)
        self.assertEqual(validate_timeout(55.5), 55.5)
        for invalid in (0, -1, float("inf"), float("nan"), True):
            with self.subTest(value=invalid), self.assertRaisesRegex(ValueError, "finite positive"):
                validate_timeout(invalid)
        with tempfile.TemporaryDirectory() as directory:
            for command in ("run", "suite"):
                output = Path(directory) / command
                argv = [sys.executable, "-B", str(HERE / "qualify.py"), command, "--godot", "missing-godot",
                        "--out", str(output), "--timeout-seconds", "nan"]
                if command == "run":
                    argv.extend(["--fixture", str(HERE / "fixtures" / "candidate.json")])
                result = subprocess.run(argv, capture_output=True, text=True, check=False, timeout=15)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("finite positive", json.loads(result.stderr)["error"])
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
