"""CLI input and serialized media contracts; no playback or audience evaluation."""

from copy import deepcopy
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import wave

HERE = Path(__file__).resolve().parent


class LoomInputAndOutput(unittest.TestCase):
    def setUp(self):
        self.score = json.loads((HERE / "loom-score.json").read_text(encoding="utf-8"))
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def call(self, score, name):
        source, output = self.work / (name + ".json"), self.work / name
        original = json.dumps(score)
        source.write_text(original, encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", str(HERE / "render_loom.py"), "--score", str(source),
                                 "--output-dir", str(output)], capture_output=True, text=True, check=False, timeout=15)
        self.assertEqual(source.read_text(encoding="utf-8"), original)
        return result, output

    def test_wrong_container_types_and_missing_identity_fail_before_output_directory(self):
        malformed = [[], None, "score", True]
        for field, value in (("phrases", {}), ("phrases", ["phrase-a", "phrase-b"]),
                             ("revision", None), ("revision", " "), ("beat_seconds", True)):
            value_score = deepcopy(self.score)
            value_score[field] = value
            malformed.append(value_score)
        missing_revision = deepcopy(self.score)
        del missing_revision["revision"]
        malformed.append(missing_revision)
        for value in ({}, [None], ["section"], []):
            value_score = deepcopy(self.score)
            value_score["phrases"][0]["sections"] = value
            malformed.append(value_score)
        for index, score in enumerate(malformed):
            with self.subTest(case=index):
                result, output = self.call(score, "invalid-" + str(index))
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("Loom render stopped:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(output.exists())

    def test_valid_numeric_beat_writes_reopenable_media_with_declared_rests(self):
        self.score["beat_seconds"] = 1.0
        self.score["annotation"] = "Additional authored metadata is allowed."
        result, output = self.call(self.score, "valid")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        receipt = json.loads((output / "receipt.json").read_text())
        self.assertEqual(receipt["score_revision"], "tabletop-score-1")
        self.assertEqual(len(receipt["outputs"]), 2)
        for phrase in ("phrase-a", "phrase-b"):
            with self.subTest(phrase=phrase), wave.open(str(output / (phrase + ".wav")), "rb") as wav:
                self.assertEqual((wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes()), (1, 2, 24_000, 288_000))
                pcm = wav.readframes(288_000)
                self.assertEqual(len(pcm), 576_000)
                self.assertTrue(any(pcm[:48_000]))
                self.assertFalse(any(pcm[9 * 48_000:10 * 48_000]))
                self.assertEqual(any(pcm[10 * 48_000:]), phrase == "phrase-a")
            with (output / (phrase + "-visual-timeline.csv")).open(newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 12)
            self.assertEqual((rows[0]["start_seconds"], rows[-1]["end_seconds"]), ("0", "12"))
            self.assertEqual(rows[9]["sound"], "false")


if __name__ == "__main__":
    unittest.main()
