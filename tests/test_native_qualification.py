"""Protect evidence handling in the native-client verifier; not client qualification."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "tools/qualify_native_clients.py"
SPEC = importlib.util.spec_from_file_location("native_qualification", SOURCE)
native = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(native)


class NativeEvidenceTests(unittest.TestCase):
    def test_component_names_are_taken_from_inventory_not_plugin_title(self):
        details = "game-design 0.1.1\n  Source: game-design@game-design-source\n\nComponent inventory\n  Skills (1)  gameplay-design\n  Agents (0)\n"
        self.assertEqual(native.claude_skill_inventory(details), ["gameplay-design"])
        self.assertNotIn("game-design", native.claude_skill_inventory(details))
        self.assertEqual(native.claude_skill_inventory("  Skills (0)\n  Agents (0)\n"), [])
        with self.assertRaisesRegex(ValueError, "count"):
            native.claude_skill_inventory("  Skills (2)  gameplay-design\n")

    def test_a_real_timeout_preserves_the_attempt_and_partial_output(self):
        with tempfile.TemporaryDirectory() as directory:
            task = native.Qualification(SimpleNamespace(work=Path(directory) / "fresh"))
            with self.assertRaises(subprocess.TimeoutExpired):
                task.run([sys.executable, "-u", "-c", "import time; print('operation started', flush=True); time.sleep(10)"],
                         task.root, timeout=2)
            self.assertEqual(len(task.commands), 1)
            record = task.commands[0]
            self.assertEqual(record["status"], "timed_out")
            self.assertIsNone(record["exit_code"])
            self.assertIn("operation started", record["stdout"])
            self.assertEqual(record["timeout_seconds"], 2)

    def test_revision_check_detects_extra_runtime_files_after_a_valid_control(self):
        source = SOURCE.parents[1]
        with tempfile.TemporaryDirectory() as directory:
            task = native.Qualification(SimpleNamespace(work=Path(directory) / "fresh"))
            installed = task.root / "installed"
            shutil.copytree(source / "skills", installed / "skills",
                            ignore=shutil.ignore_patterns("node_modules", "__pycache__"))
            task.resource_action(installed, source, "fixture", "control")
            extra = installed / "skills/game-design/references/candidate-only.md"
            extra.write_text("A file that should be absent after rollback.\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "differ"):
                task.resource_action(installed, source, "fixture", "stale")
            self.assertFalse((task.root / "fixture-stale-observations.json").exists())


if __name__ == "__main__":
    unittest.main()
