"""Discriminate valid bundles and broken boundaries without invoking a model."""
from __future__ import annotations

import importlib.util
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import check
import package
import release
import smoke

SCRATCH_ROOT = ROOT / "tmp" / "release-packaging-tests"


def temporary_directory():
    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=SCRATCH_ROOT)

spec = importlib.util.spec_from_file_location("bind_assay", ROOT / "skills/game-design/scripts/bind_assay.py")
binder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(binder)


class BindingBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = temporary_directory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "renamed provider"
        self.root.mkdir()
        self.owner = "evidence-research"
        self.original_binding = binder.BINDING
        self.addCleanup(setattr, binder, "BINDING", self.original_binding)
        # Synthetic provider establishes the verifier's behavior. The separate
        # release receipt proves the real Assay checkout, never this fixture.
        import hashlib
        files = {"VERSION": b"test\n", "catalog.toml": b"test\n", "LICENSE": b"synthetic permission notice\n",
                 "skills/evidence-research/SKILL.md": b"actual method text\n",
                 "skills/evidence-research/references/claim.md": b"actual conditional reference\n"}
        for relative, data in files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        binding = {"assay": {"commit": "test", "version": "test"},
                   "identity_files": {p: hashlib.sha256(d).hexdigest() for p, d in files.items() if not p.startswith("skills/")},
                   "owners": {self.owner: {p: hashlib.sha256(d).hexdigest() for p, d in files.items() if p.startswith("skills/")}}}
        binder.BINDING = Path(self.temp.name) / "binding.json"
        binder.BINDING.write_text(json.dumps(binding))

    def resolve(self, resource="SKILL.md", state="enabled"):
        return binder.resolve(self.root, self.owner, resource, state, read=True)

    def rejects(self, reason, resource="SKILL.md", state="enabled"):
        with self.assertRaises(binder.BindingFailure) as caught:
            self.resolve(resource, state)
        self.assertEqual(caught.exception.reason, reason)

    def test_relocated_bytes_and_recursive_reference_are_read(self):
        self.assertEqual(self.resolve()["content"], "actual method text\n")
        self.assertEqual(self.resolve("references/claim.md")["content"], "actual conditional reference\n")
        self.assertFalse(self.resolve()["permission_attestation"])

    def test_disabled_route_is_not_bypassed(self):
        shutil.rmtree(self.root)
        self.rejects("provider_disabled", state="disabled")

    def test_modified_required_reference_invalidates_owner(self):
        (self.root / "skills/evidence-research/references/claim.md").write_text("changed")
        self.rejects("resource_changed")

    def test_missing_resource_cannot_pass(self):
        (self.root / "skills/evidence-research/SKILL.md").unlink()
        self.rejects("resource_unreadable")

    def test_missing_peer_is_local_failure(self):
        self.owner = "absent-method"
        self.rejects("missing_required_peer")

    def test_new_owner_code_is_not_silently_verified(self):
        (self.root / "skills/evidence-research/extra.py").write_text("pass\n")
        self.rejects("unexpected_owner_resource")

    def test_other_owner_work_is_preserved_and_irrelevant(self):
        foreign = self.root / "notes.txt"
        foreign.write_text("unrelated work")
        self.assertEqual(self.resolve()["status"], "verified")
        self.assertEqual(foreign.read_text(), "unrelated work")

    def test_symlink_and_path_escape_are_rejected(self):
        path = self.root / "skills/evidence-research/SKILL.md"
        path.unlink()
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("actual method text\n")
        path.symlink_to(outside)
        self.rejects("resource_outside_root")
        self.rejects("invalid_resource_path", "../../outside.md")


class ReleaseBoundary(unittest.TestCase):
    def test_frontmatter_uses_yaml_and_links_ignore_code(self):
        self.assertEqual(check.frontmatter("---\nname: a\nmetadata: {x: 'b:c'}\n---\nbody")["metadata"]["x"], "b:c")
        links, anchors = check.document("# Repeat\n# Repeat\n[x](exists.md)\n```\n[y](missing.md)\n```\n")
        self.assertEqual(links, ["exists.md"])
        self.assertEqual(anchors, {"repeat", "repeat-1"})

    def test_archive_is_reproducible_relocatable_and_excludes_keys(self):
        with temporary_directory() as directory:
            base = Path(directory)
            first, second = base / "first.zip", base / "second.zip"
            a, b = package.build(ROOT, first), package.build(ROOT, second)
            self.assertEqual(a["sha256"], b["sha256"])
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(archive.namelist(), ["game-design/" + item["path"] for item in a["files"]])
                self.assertFalse(any("evals" in Path(n).parts or ".git" in Path(n).parts for n in archive.namelist()))
                archive.extractall(base / "relocated")
            copied = base / "relocated/game-design"
            self.assertEqual(check.inspect(copied)["status"], "pass")
            with self.assertRaises(FileExistsError):
                package.build(ROOT, first)

    def test_missing_sibling_is_reported(self):
        with temporary_directory() as directory:
            copy = Path(directory) / "copy"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(
                ".git", ".venv", "__pycache__", ".godot", ".pytest_cache", "dist", "evals", "tmp"
            ))
            shutil.rmtree(copy / "skills/game-information-design")
            result = check.inspect(copy)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("inventory" in e for e in result["errors"]))

    def test_package_cli_preserves_the_external_receipt_contract(self):
        with temporary_directory() as directory:
            base = Path(directory)
            archive, receipt = base / "source.zip", base / "receipt.json"
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "package.py"), "--output", str(archive), "--receipt", str(receipt)],
                cwd=ROOT,
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], 1)
            self.assertEqual(manifest["archive"], archive.name)
            self.assertEqual(manifest["sha256"], hashlib.sha256(archive.read_bytes()).hexdigest())
            with zipfile.ZipFile(archive) as zipped:
                self.assertNotIn("game-design/receipt.json", zipped.namelist())


class SecurePackaging(unittest.TestCase):
    def setUp(self):
        self.temp = temporary_directory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def _source(self) -> Path:
        root = self.base / "source"
        root.mkdir()
        for name, content in {
            "README.md": "public readme\n",
            "VERSION": "0.1.0\n",
            "AGENTS.md": "public contributor contract\n",
            ".betterleaks.toml": "[scanner]\n",
            ".gitignore": "tmp/\n",
            "SECURITY.md": "public security policy\n",
            "relkit.toml": "[release]\n",
            "private-notes.txt": "private metadata\n",
            "catalog.json": "{}\n",
        }.items():
            (root / name).write_text(content, encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs/public.md").write_text("public docs\n", encoding="utf-8")
        (root / "tools").mkdir()
        (root / "tools/package.py").write_text("public tool\n", encoding="utf-8")
        (root / ".github").mkdir()
        (root / ".github/relkit.pyz").write_bytes(b"public release gate")
        (root / ".github/relkit.pyz.sha256").write_text("release gate digest\n", encoding="ascii")
        (root / ".github/private-metadata.json").write_text("private metadata", encoding="utf-8")
        (root / ".github/workflows").mkdir()
        (root / ".github/workflows/check.yml").write_text("public workflow\n", encoding="utf-8")
        for relative, content in {
            "docs/.private/secret.txt": "private sentinel",
            "docs/.cache/cache.txt": "cache sentinel",
            "docs/tmp/scratch.txt": "scratch sentinel",
            "docs/client/client.json": "client sentinel",
            "docs/local/local.json": "local sentinel",
            "docs/.env": "environment sentinel",
            "tools/credentials.secret": "secret sentinel",
        }.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return root

    def test_explicit_membership_excludes_private_scratch_and_client_sentinels(self):
        root = self._source()
        actual = {path.relative_to(root).as_posix() for path in package.members(root)}
        self.assertEqual(actual, {
            ".betterleaks.toml", ".github/relkit.pyz", ".github/relkit.pyz.sha256",
            ".github/workflows/check.yml", ".gitignore", "AGENTS.md", "README.md",
            "SECURITY.md", "VERSION", "catalog.json", "docs/public.md", "relkit.toml",
            "tools/package.py",
        })

    def test_reparse_points_in_public_roots_are_refused(self):
        root = self._source()
        target = self.base / "linked-target"
        target.mkdir()
        link = root / "docs" / "linked"
        if os.name == "nt":
            result = __import__("subprocess").run(
                ["cmd.exe", "/c", "mklink", "/J", str(link), str(target)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.addCleanup(os.rmdir, link)
        else:
            link.symlink_to(target, target_is_directory=True)
            self.addCleanup(link.unlink)
        with self.assertRaisesRegex(ValueError, "symlinks or reparse points"):
            package.members(root)

    def test_release_build_smokes_downloaded_assets_and_exact_names(self):
        assets = self.base / "assets"
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        built = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "release.py"), "build", "--output", str(assets), "--version", version],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
        result = json.loads(built.stdout)
        self.assertEqual(set(result["assets"]), {"gamedesign-skills-0.1.0-source.zip", "SHA256SUMS"})
        self.assertEqual({path.name for path in assets.iterdir()}, set(result["assets"]))
        checked = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "smoke.py"), "--assets", str(assets), "--version", version,
             "--temp", str(self.base / "smoke")],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        smoke_result = json.loads(checked.stdout)
        self.assertEqual(smoke_result["status"], "pass")
        self.assertEqual(len(smoke_result["skills"]), 7)
        self.assertEqual(smoke_result["east_gate"]["play"]["status"], "executed")
        self.assertEqual(smoke_result["east_gate"]["ferry"]["status"], "executed")

    def test_version_mismatch_and_extra_asset_are_rejected(self):
        assets = self.base / "assets"
        with self.assertRaisesRegex(ValueError, "does not match VERSION"):
            release.build(assets, "9.9.9")
        result = release.build(assets, "0.1.0")
        (assets / "unexpected.txt").write_text("third asset", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Expected exactly"):
            smoke.verify(assets, result["version"], self.base / "smoke")

    def test_release_outputs_cannot_be_written_into_public_source_paths(self):
        archive = ROOT / "docs" / "unexpected-source.zip"
        receipt = ROOT / "docs" / "unexpected-receipt.json"
        with self.assertRaisesRegex(ValueError, "outside public source roots"):
            package.build(ROOT, archive)
        with self.assertRaisesRegex(ValueError, "outside public source roots"):
            package.validate_destination(ROOT, receipt)
        with self.assertRaisesRegex(ValueError, "outside public source roots"):
            release.build(ROOT / "docs" / "assets", "0.1.0")
        self.assertFalse(archive.exists())
        self.assertFalse(receipt.exists())

    def test_corrupted_checksum_and_unsafe_downloaded_zip_are_rejected(self):
        assets = self.base / "assets"
        built = release.build(assets, "0.1.0")
        archive = assets / built["archive"]
        archive.write_bytes(archive.read_bytes() + b"corruption")
        with self.assertRaisesRegex(ValueError, "checksum"):
            smoke.verify(assets, "0.1.0", self.base / "corrupt-smoke")

        unsafe = self.base / "unsafe-assets"
        unsafe.mkdir()
        unsafe_name = "gamedesign-skills-0.1.0-source.zip"
        unsafe_archive = unsafe / unsafe_name
        info = zipfile.ZipInfo("game-design/../../outside.txt")
        info.external_attr = 0o100644 << 16
        with zipfile.ZipFile(unsafe_archive, "w") as archive_file:
            archive_file.writestr(info, b"must not escape")
        digest = hashlib.sha256(unsafe_archive.read_bytes()).hexdigest()
        (unsafe / "SHA256SUMS").write_text(f"{digest}  {unsafe_name}\n", encoding="ascii")
        with self.assertRaisesRegex(ValueError, "Unsafe archive member path"):
            smoke.verify(unsafe, "0.1.0", self.base / "unsafe-smoke")


if __name__ == "__main__":
    unittest.main()
