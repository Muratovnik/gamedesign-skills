import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from consumer import enter_ferry, play, view

ROOT = Path(__file__).resolve().parent


class AdaptationContract(unittest.TestCase):
    def setUp(self):
        self.target = json.loads((ROOT / "fixtures/east-gate-ru.json").read_text(encoding="utf-8"))

    def test_transferred_clue_actions_and_later_scene(self):
        result = play(self.target, "east-gate-ru-2", [1, 2, 3, 4, 5, 6], "east")
        self.assertEqual((result["gate"], result["token"]), ("open", "ferryman"))
        self.assertEqual(result["notebook"], self.target["lines"])
        self.assertIn("Восточные", result["next_scene"])

    def test_wrong_player_choice_remains_a_playable_nonterminal_state(self):
        result = play(self.target, "east-gate-ru-2", [], "north")
        self.assertEqual(result["gate"], "closed")
        self.assertIsNone(result["token"])

    def test_literal_translation_breaking_operation_is_rejected(self):
        self.target["lines"][0] = "Сумерки прячут лодки."
        with self.assertRaisesRegex(ValueError, "clue"):
            play(self.target, "east-gate-ru-2", [], "east")

    def test_stale_and_wrong_later_sign_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "revision"):
            play(self.target, "east-gate-en-1", [], "east")
        self.target["later_sign"]["direction_id"] = "west"
        with self.assertRaisesRegex(ValueError, "later sign"):
            play(self.target, "east-gate-ru-2", [], "east")

    def test_valid_rewrite_and_permanent_help_are_not_rejected(self):
        alternate = copy.deepcopy(self.target)
        alternate["lines"][0] = "Волна качает лодки."
        result = play(alternate, "east-gate-ru-2", [1, 1, 2], "east")
        self.assertEqual(result["gate"], "open")
        self.assertEqual(len(result["notebook"]), 2)

    def test_target_view_presents_one_line_and_navigation(self):
        result = view(self.target, "east-gate-ru-2", 2)
        self.assertEqual(result["visible_lines"], [self.target["lines"][1]])
        self.assertEqual(result["next_line"], 3)
        self.assertEqual(result["guide"], self.target["guide"])

    def test_later_consumer_uses_and_spends_token(self):
        state = play(self.target, "east-gate-ru-2", [], "east")
        result = enter_ferry(self.target, "east-gate-ru-2", state)
        self.assertTrue(result["voyage_started"])
        self.assertIsNone(result["token"])
        with self.assertRaisesRegex(ValueError, "unspent token"):
            enter_ferry(self.target, "east-gate-ru-2", result)
        state["actions"] = [{"choose": "west"}]
        with self.assertRaisesRegex(ValueError, "direction"):
            enter_ferry(self.target, "east-gate-ru-2", state)


class InvalidFileBoundary(unittest.TestCase):
    """An unusable file is not a playable failure or a completed operation."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.artifact = ROOT / "fixtures/east-gate-ru.json"

    def call(self, artifact, output, *extra):
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "consumer.py"),
             "--artifact", str(artifact), "--expect-revision", "east-gate-ru-2",
             "--output", str(output), *extra],
            capture_output=True, text=True, check=False, timeout=10)

    def invalid(self, result, output):
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "invalid")
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(output.exists(), "Invalid input must not create a playable result")

    def test_non_object_artifacts_fail_as_invalid(self):
        for number, value in enumerate(([], None, "verse", 7)):
            with self.subTest(value=value):
                path, output = self.work / f"input-{number}.json", self.work / f"view-{number}.json"
                path.write_text(json.dumps(value))
                self.invalid(self.call(path, output, "--operation", "view"), output)

    def test_malformed_content_records_fail_before_presentation(self):
        original = json.loads(self.artifact.read_text(encoding="utf-8"))
        changes = ({"directions": []}, {"later_sign": []},
                   {"guide": []}, {"later_sign": {"direction_id": "east", "text": False}})
        for number, change in enumerate(changes):
            with self.subTest(change=change):
                path, output = self.work / f"input-{number}.json", self.work / f"view-{number}.json"
                path.write_text(json.dumps(dict(original, **change)))
                self.invalid(self.call(path, output, "--operation", "view"), output)

    def test_malformed_saved_state_cannot_start_a_voyage(self):
        produced = self.work / "played.json"
        result = self.call(self.artifact, produced, "--choose", "east")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        valid = json.loads(produced.read_text(encoding="utf-8"))
        inputs = [[], None, "save", dict(valid, actions=["choose"]),
                  dict(valid, actions=[{"choose": ["east"]}]),
                  dict(valid, actions=[{"pin_line": True}, {"choose": "east"}])]
        for number, value in enumerate(inputs):
            with self.subTest(value=value):
                path, output = self.work / f"save-{number}.json", self.work / f"voyage-{number}.json"
                path.write_text(json.dumps(value))
                self.invalid(self.call(self.artifact, output, "--operation", "enter-ferry", "--state", str(path)), output)


if __name__ == "__main__":
    unittest.main()
