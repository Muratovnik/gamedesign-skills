"""Exercise the binder's public JSON/exit-code contract on disposable sources."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BindingCLI(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / "tmp" / "assay-binding-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.provider = base / "provider with spaces"
        consumer = base / "consumer" / "game-design"
        self.script = consumer / "scripts" / "bind_assay.py"
        self.script.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "skills/game-design/scripts/bind_assay.py", self.script)
        files = {
            "VERSION": b"fixture\n",
            "catalog.toml": b"fixture\n",
            "LICENSE": b"Synthetic test fixture\n",
            "skills/evidence-research/SKILL.md": b"Selected method\n",
            "skills/evidence-research/references/claims.md": b"Conditional reference\n",
        }
        for relative, content in files.items():
            path = self.provider / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        hashes = {path: hashlib.sha256(content).hexdigest() for path, content in files.items()}
        binding = {
            "assay": {"commit": "fixture", "version": "fixture"},
            "identity_files": {path: digest for path, digest in hashes.items() if not path.startswith("skills/")},
            "owners": {
                "evidence-research": {path: digest for path, digest in hashes.items() if path.startswith("skills/")},
                "unused-owner": {"skills/unused-owner/SKILL.md": hashlib.sha256(b"Unused method\n").hexdigest()},
            },
        }
        (consumer / "assets").mkdir()
        (consumer / "assets/assay-binding.json").write_text(json.dumps(binding), encoding="utf-8")

    def run_cli(self, code, status, reason, *, state="enabled", method="evidence-research"):
        result = subprocess.run(
            [sys.executable, "-B", str(self.script), "--assay-root", str(self.provider),
             "--provider-state", state, "--method", method, "--read"],
            cwd=self.temp.name, capture_output=True, text=True, encoding="utf-8", check=False,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "", result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual((output["status"], output["reason"]), (status, reason))
        return output

    def test_valid_changed_missing_disabled_and_missing_owner_keep_distinct_results(self):
        output = self.run_cli(0, "verified", "matched_owner_bytes")
        self.assertEqual(output["content"], "Selected method\n")
        self.assertEqual(output["checked_files"], 5)
        self.assertFalse(output["permission_attestation"])
        reference = self.provider / "skills/evidence-research/references/claims.md"
        reference.write_text("Changed reference\n", encoding="utf-8")
        self.run_cli(1, "incompatible", "resource_changed")
        reference.unlink()
        self.run_cli(2, "unavailable", "resource_unreadable")
        self.run_cli(2, "unavailable", "provider_disabled", state="disabled")
        self.run_cli(2, "unavailable", "missing_required_peer", method="unused-owner")

    def test_cyclic_required_resource_is_unavailable_json_without_traceback(self):
        resource = self.provider / "skills/evidence-research/SKILL.md"
        resource.unlink()
        try:
            resource.symlink_to(resource.name)
        except OSError as exc:
            self.skipTest(f"Cannot create the symlink fixture on this platform: {exc}")
        self.run_cli(2, "unavailable", "resource_unreadable")


if __name__ == "__main__":
    unittest.main()
