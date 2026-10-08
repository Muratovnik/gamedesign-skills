"""Input and operation-identity regressions for the bounded campaign consumer."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from state import SKILL, crew_account, migrate, recover, resumed_survey
from validate_artifact import read_json, validate

HERE = Path(__file__).resolve().parent


class InputAndReplayTests(unittest.TestCase):
    def setUp(self):
        self.old = read_json(HERE / "fixtures" / "save-v1.json")
        self.state = migrate(self.old)

    def run_lab(self, command, state, operation_id=None):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / "source.json", Path(directory) / "output.json"
            original = json.dumps(state)
            source.write_text(original)
            argv = [sys.executable, "-B", str(HERE / "lab.py"), command,
                    "--input", str(source), "--output", str(output)]
            if operation_id is not None:
                argv.extend(["--operation-id", operation_id])
            result = subprocess.run(argv, capture_output=True, text=True, check=False)
            self.assertEqual(source.read_text(), original)
            return result, json.loads(output.read_text()) if output.exists() else None

    def assert_invalid_without_output(self, result, output):
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stderr)["status"], "invalid_or_missing_evidence")
        self.assertIsNone(output)
        self.assertNotIn("Traceback", result.stderr)

    def test_save_roots_and_nested_types_are_rejected_before_use(self):
        malformed = [[], None, True, 7, "save", {"schema_version": True}]
        for field, value in (("world", []), ("actors", [False]), ("history", "archive-message")):
            bad = deepcopy(self.state)
            bad[field] = value
            malformed.append(bad)
        bad_boolean = deepcopy(self.state)
        bad_boolean["world"]["generator"] = "false"
        malformed.append(bad_boolean)
        for index, state in enumerate(malformed):
            with self.subTest(case=index):
                self.assert_invalid_without_output(*self.run_lab("migrate", state))

    def test_non_finite_values_are_rejected_by_shared_json_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "numbers.json"
            for literal in ("NaN", "Infinity", "-Infinity", "1e999"):
                with self.subTest(literal=literal):
                    path.write_text('{"value":' + literal + '}')
                    with self.assertRaises(ValueError):
                        read_json(path)
        fixture = read_json(HERE.parent / "godot-episode" / "fixtures" / "candidate.json")
        fixture["actor"]["start_px"][0] = float("nan")
        with self.assertRaises(ValueError):
            validate(fixture, SKILL / "assets" / "episode.schema.json")

    def test_unrelated_history_and_incomplete_recovery_are_conflicts(self):
        cases = [("survey", self.state, "archive-message"),
                 ("survey", self.state, "generator-lost"),
                 ("recover", self.state, "archive-message")]
        for records in [
            [{"id": "old-job:repair", "kind": "generator-repaired", "actor_id": "bo", "tick": 47}],
            [{"id": "old-job:survey", "kind": "survey-completed", "actor_id": "cy", "tick": 46}],
            [{"id": "old-job:survey", "kind": "message-emitted", "actor_id": "cy", "tick": 46},
             {"id": "old-job:repair", "kind": "loss", "actor_id": "bo", "tick": 47}],
            [{"id": "old-job:survey", "kind": "survey-completed", "actor_id": "cy", "tick": 47},
             {"id": "old-job:repair", "kind": "generator-repaired", "actor_id": "bo", "tick": 46}],
        ]:
            partial = deepcopy(self.state)
            partial["history"].extend(records)
            cases.append(("recover", partial, "old-job"))
        wrong_actor = deepcopy(self.state)
        wrong_actor["history"].append({"id": "other-survey", "kind": "survey-completed", "actor_id": "bo", "tick": 46})
        cases.append(("survey", wrong_actor, "other-survey"))
        for index, (command, state, operation_id) in enumerate(cases):
            with self.subTest(case=index):
                self.assert_invalid_without_output(*self.run_lab(command, state, operation_id))

    def test_recovery_subevents_cannot_be_claimed_as_standalone_operations(self):
        completed, _ = recover(self.state, "recovery-1")
        for command, operation_id in (("survey", "recovery-1:survey"), ("recover", "new:job"), ("survey", "")):
            with self.subTest(command=command, operation_id=operation_id):
                self.assert_invalid_without_output(*self.run_lab(command, completed, operation_id))

    def test_genuine_repeats_preserve_later_world_changes_without_awards(self):
        repaired, _ = recover(self.state, "recovery-1")
        completed, _ = resumed_survey(repaired, "expedition-2")
        completed["world"].update(generator=False, survey_yield_scrap=7)
        completed["roles"]["treasurer_id"] = "ava"
        next(a for a in completed["actors"] if a["id"] == "cy")["status"] = "away"
        crew_account(completed)["amount"] = 9
        completed["history"].append({"id": "later-loss", "kind": "loss", "actor_id": "ava", "tick": 60})
        for command, operation_id in (("recover", "recovery-1"), ("survey", "expedition-2")):
            with self.subTest(command=command):
                result, output = self.run_lab(command, completed, operation_id)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout.splitlines()[0])["status"], "already_applied")
                self.assertEqual(output, completed)

    def test_fresh_survey_without_required_source_or_actor_is_refuted(self):
        result, output = self.run_lab("survey", self.state, "new-survey")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["reason"], "source_not_repaired")
        self.assertIsNone(output)
        no_route = deepcopy(self.state)
        no_route["world"]["generator"] = True
        no_route["actors"] = [a for a in no_route["actors"] if a["id"] != "cy"]
        no_route["accounts"] = [a for a in no_route["accounts"] if a["owner_id"] != "cy"]
        result, output = self.run_lab("survey", no_route, "new-survey")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["reason"], "route_decider_absent")
        self.assertIsNone(output)


if __name__ == "__main__":
    unittest.main()
