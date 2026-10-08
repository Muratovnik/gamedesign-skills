"""Public protocol regressions around one preserved native report; no engine run."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from qualify import assess as assess_report

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


if __name__ == "__main__":
    unittest.main()
