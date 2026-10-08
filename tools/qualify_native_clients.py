#!/usr/bin/env python3
"""Qualify pinned native plugin lifecycles in an explicitly disposable Linux user environment."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import queue
import re
import subprocess
import sys
import threading
import time

PACKAGE = "game-design"
MARKETPLACE = "game-design-source"
IDENTITY = f"{PACKAGE}@{MARKETPLACE}"
SENTINEL = "qualification-sentinel"
SENTINEL_MARKETPLACE = "qualification-sentinel-source"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_result(output: str):
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        # Claude mutation commands may print progress before their final JSON line.
        for line in reversed(output.splitlines()):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    raise ValueError("The native command returned no JSON result")


def claude_skill_inventory(details: str) -> list[str]:
    match = re.search(r"^[ \t]*Skills \((\d+)\)[ \t]*(.*)$", details, re.MULTILINE)
    if not match:
        raise ValueError("Claude details contain no skill component inventory")
    names = [name.strip() for name in match.group(2).split(",") if name.strip()]
    if len(names) != int(match.group(1)) or len(names) != len(set(names)):
        raise ValueError("Claude skill count and component names differ")
    return sorted(names)


def partial_text(value) -> str:
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")


class Qualification:
    def __init__(self, args):
        self.args = args
        self.commands = []
        self.observations = []
        self.root = args.work.resolve()
        self.root.mkdir(parents=True, exist_ok=False)

    def run(self, argv, cwd, *, allowed=(0,), parse=False, timeout=120):
        command = [str(arg) for arg in argv]
        record = {"argv": command, "cwd": str(cwd), "status": "started", "exit_code": None}
        self.commands.append(record)
        try:
            result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired as error:
            record.update(status="timed_out", stdout=partial_text(error.stdout), stderr=partial_text(error.stderr),
                          timeout_seconds=timeout)
            raise
        except OSError as error:
            record.update(status="unavailable", error=str(error))
            raise
        record.update(status="completed", exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
        if result.returncode not in allowed:
            raise RuntimeError(f"Native command failed ({result.returncode}): {command}\n{result.stderr}")
        return json_result(result.stdout) if parse else result

    def codex_skills(self, project):
        command = [str(self.args.codex), "app-server", "--listen", "stdio://"]
        protocol = {"client": "codex", "operation": "app-server", "argv": command,
                    "cwd": str(project), "requests": [], "status": "started"}
        self.observations.append(protocol)
        try:
            process = subprocess.Popen(command,
                                       cwd=project, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)
        except OSError as error:
            protocol.update(status="unavailable", error=str(error))
            raise
        messages = queue.Queue()
        stderr = []

        def read_stdout():
            for line in process.stdout:
                try:
                    messages.put(json.loads(line))
                except json.JSONDecodeError:
                    messages.put({"protocol_error": line})

        def read_stderr():
            for line in process.stderr:
                stderr.append(line)

        output_reader = threading.Thread(target=read_stdout, daemon=True)
        error_reader = threading.Thread(target=read_stderr, daemon=True)
        output_reader.start()
        error_reader.start()

        def request(identity, method, params):
            attempt = {"id": identity, "method": method, "params": params}
            protocol["requests"].append(attempt)
            process.stdin.write(json.dumps({"id": identity, "method": method, "params": params}) + "\n")
            process.stdin.flush()
            deadline = time.monotonic() + 45
            while time.monotonic() < deadline:
                try:
                    response = messages.get(timeout=max(0.01, deadline - time.monotonic()))
                except queue.Empty:
                    raise TimeoutError(f"Codex app-server timed out waiting for {method}") from None
                if "protocol_error" in response:
                    attempt["invalid_response"] = response["protocol_error"]
                    raise ValueError(f"Codex app-server returned invalid JSON during {method}")
                if response.get("id") == identity:
                    attempt["response"] = response
                    if "error" in response:
                        raise RuntimeError(f"{method}: {response['error']}")
                    return response["result"]
            raise TimeoutError(method)

        try:
            request(1, "initialize", {"clientInfo": {"name": "game-design-qualification", "version": "1"},
                                       "capabilities": {"experimentalApi": True}})
            process.stdin.write(json.dumps({"method": "initialized"}) + "\n")
            process.stdin.flush()
            result = request(2, "skills/list", {"cwds": [str(project)], "forceReload": True})
            protocol["status"] = "completed"
            self.observations.append({"client": "codex", "operation": "skills/list", "result": result})
            rows = result["data"]
            if len(rows) != 1 or rows[0]["errors"]:
                raise ValueError(f"Native skill discovery failed: {rows}")
            return rows[0]["skills"]
        except Exception as error:
            protocol.update(status="incomplete", error=str(error))
            raise
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            output_reader.join(timeout=1)
            error_reader.join(timeout=1)
            protocol["stderr"] = "".join(stderr)
            protocol["exit_code"] = process.returncode

    def resource_action(self, installed, source, client, stage):
        expected = {path.relative_to(source).as_posix(): digest(path)
                    for path in (source / "skills").rglob("*") if path.is_file()
                    and "__pycache__" not in path.parts and "node_modules" not in path.parts}
        observed = {path.relative_to(installed).as_posix(): digest(path)
                    for path in (installed / "skills").rglob("*") if path.is_file()
                    and "__pycache__" not in path.parts and "node_modules" not in path.parts}
        if observed != expected:
            raise ValueError("The installed skill resources differ from the selected source")
        output = self.root / f"{client}-{stage}-observations.json"
        self.run([sys.executable, installed / "skills/game-design/scripts/observe_evidence.py",
                  "--csv", source / "examples/analysis-lab/fixtures/observations.csv",
                  "--manifest", source / "examples/analysis-lab/fixtures/observation-manifest.json",
                  "--output", output], self.root)
        report = json.loads(output.read_text(encoding="utf-8"))
        if report["human_claim"] != "not_established" or report["counts"]["all"] != 4:
            raise ValueError("The installed runtime operation did not preserve its bounded result")
        if stage == "candidate" and report.get("conditions") is None:
            raise ValueError("Candidate installation lost the observation-context correction")
        self.observations.append({"client": client, "stage": stage, "installed_root": str(installed),
                                  "verified_skill_files": expected, "operation_report": report})

    def sentinel_source(self):
        root = self.root / "sentinel-source"
        for directory in (".agents/plugins", ".claude-plugin", f"skills/{SENTINEL}"):
            (root / directory).mkdir(parents=True, exist_ok=True)
        plugin = {"name": SENTINEL, "version": "0.0.1", "description": "Disposable lifecycle control."}
        (root / "plugin.json").write_text(json.dumps(plugin), encoding="utf-8")
        (root / ".claude-plugin/plugin.json").write_text(json.dumps(plugin), encoding="utf-8")
        (root / ".agents/plugins/marketplace.json").write_text(json.dumps({"name": SENTINEL_MARKETPLACE,
            "plugins": [{"name": SENTINEL, "source": {"source": "local", "path": "./"}}]}), encoding="utf-8")
        (root / ".claude-plugin/marketplace.json").write_text(json.dumps({"name": SENTINEL_MARKETPLACE,
            "owner": {"name": "qualification"}, "plugins": [{"name": SENTINEL, "source": "./"}]}), encoding="utf-8")
        (root / f"skills/{SENTINEL}/SKILL.md").write_text(
            f"---\nname: {SENTINEL}\ndescription: Report the disposable lifecycle marker when explicitly requested.\n---\n\nReturn `sentinel-preserved`.\n",
            encoding="utf-8")
        return root

    def codex(self, sentinel):
        client = self.args.codex
        project = self.root / "codex-game"
        project.mkdir()
        self.run(["git", "init", "--quiet", project], self.root)
        self.run([client, "--version"], project)
        initial = self.run([client, "plugin", "list", "--json"], project, parse=True)
        if initial["installed"]:
            raise ValueError("Codex qualification requires a disposable user with no installed plugins")

        def add(source, name=PACKAGE, marketplace=MARKETPLACE):
            self.run([client, "plugin", "marketplace", "add", source, "--json"], project)
            self.run([client, "plugin", "add", f"{name}@{marketplace}", "--json"], project)

        def remove(name=PACKAGE, marketplace=MARKETPLACE):
            self.run([client, "plugin", "remove", f"{name}@{marketplace}", "--json"], project)
            self.run([client, "plugin", "marketplace", "remove", marketplace, "--json"], project)

        add(sentinel, SENTINEL, SENTINEL_MARKETPLACE)
        # This file belongs to the explicitly disposable runner user. Trust is
        # limited to the newly created game repository so its project flag applies.
        config = Path.home() / ".codex/config.toml"
        with config.open("a", encoding="utf-8") as stream:
            stream.write(f"\n[projects.{json.dumps(str(project))}]\ntrust_level = \"trusted\"\n")
        (project / ".codex").mkdir()

        def flag(enabled):
            (project / ".codex/config.toml").write_text(
                f'[plugins."{IDENTITY}"]\nenabled = {str(enabled).lower()}\n', encoding="utf-8")

        def inspect(source, stage, enabled=True):
            listing = self.run([client, "plugin", "list", "--json"], project, parse=True)["installed"]
            states = {item["pluginId"]: item for item in listing}
            if not states[f"{SENTINEL}@{SENTINEL_MARKETPLACE}"]["enabled"]:
                raise ValueError("An unrelated plugin was disabled")
            if states[IDENTITY]["enabled"] != enabled:
                raise ValueError("Native enable state differs from the project declaration")
            skills = self.codex_skills(project)
            own = [item for item in skills if item.get("pluginId") == IDENTITY and item["enabled"]]
            expected = sorted(f"{PACKAGE}:{path.parent.name}" for path in (source / "skills").glob("*/SKILL.md"))
            if sorted(item["name"] for item in own) != (expected if enabled else []):
                raise ValueError("Native Codex discovery differs from the enabled bundle inventory")
            if enabled:
                self.resource_action(Path(own[0]["path"]).parents[2], source, "codex", stage)

        add(self.args.previous)
        flag(True)
        inspect(self.args.previous, "baseline")
        flag(False)
        inspect(self.args.previous, "disabled", False)
        flag(True)
        inspect(self.args.previous, "reenabled")
        remove()
        add(self.args.source)
        inspect(self.args.source, "candidate")
        remove()
        add(self.args.previous)
        inspect(self.args.previous, "rollback")
        remove()
        if any(item.get("pluginId") == IDENTITY and item["enabled"] for item in self.codex_skills(project)):
            raise ValueError("Removed plugin remains in native skill discovery")
        remaining = self.run([client, "plugin", "list", "--json"], project, parse=True)["installed"]
        if [item["pluginId"] for item in remaining] != [f"{SENTINEL}@{SENTINEL_MARKETPLACE}"]:
            raise ValueError("Removal altered the unrelated registration")
        remove(SENTINEL, SENTINEL_MARKETPLACE)
        if self.run([client, "plugin", "list", "--json"], project, parse=True)["installed"]:
            raise ValueError("Owned Codex registrations were not removed")

    def claude(self, sentinel):
        client = self.args.claude
        project = self.root / "claude-game"
        project.mkdir()
        self.run(["git", "init", "--quiet", project], self.root)
        self.run([client, "--version"], project)
        if self.run([client, "plugin", "list", "--json"], project, parse=True):
            raise ValueError("Claude qualification requires a disposable user with no installed plugins")

        def add(source, name=PACKAGE, marketplace=MARKETPLACE):
            self.run([client, "plugin", "validate", source, "--json"], project)
            self.run([client, "plugin", "marketplace", "add", source, "--scope", "local", "--json"], project)
            self.run([client, "plugin", "install", f"{name}@{marketplace}", "--scope", "local", "--json"], project)

        def remove(name=PACKAGE, marketplace=MARKETPLACE):
            self.run([client, "plugin", "uninstall", f"{name}@{marketplace}", "--scope", "local", "--keep-data", "--json"], project)
            self.run([client, "plugin", "marketplace", "remove", marketplace, "--scope", "local", "--json"], project)

        def inspect(source, stage, enabled=True):
            listing = self.run([client, "plugin", "list", "--json"], project, parse=True)
            states = {item["id"]: item for item in listing}
            if not states[f"{SENTINEL}@{SENTINEL_MARKETPLACE}"]["enabled"]:
                raise ValueError("An unrelated plugin was disabled")
            item = states[IDENTITY]
            if item["scope"] != "local" or item["enabled"] != enabled:
                raise ValueError("Claude native scope or enable state differs")
            # In 2.1.289 details describes even an installed disabled plugin.
            # The native list independently reports the merged enable setting.
            details = self.run([client, "plugin", "details", PACKAGE], project)
            if enabled:
                expected = sorted(path.parent.name for path in (source / "skills").glob("*/SKILL.md"))
                if claude_skill_inventory(details.stdout) != expected:
                    raise ValueError("Claude's loaded component details omit a bundled skill")
                effective = Path(item.get("readFromFolder") or item["installPath"]).resolve()
                if item.get("readFromFolder") and effective != source.resolve():
                    raise ValueError("Claude's effective local source differs from the selected revision")
                self.observations.append({"client": "claude", "stage": stage, "native_plugin": item,
                                          "effective_source": str(effective)})
                self.resource_action(effective, source, "claude", stage)

        add(sentinel, SENTINEL, SENTINEL_MARKETPLACE)
        add(self.args.previous)
        inspect(self.args.previous, "baseline")
        self.run([client, "plugin", "disable", IDENTITY, "--scope", "local", "--json"], project)
        inspect(self.args.previous, "disabled", False)
        self.run([client, "plugin", "enable", IDENTITY, "--scope", "local", "--json"], project)
        inspect(self.args.previous, "reenabled")
        remove()
        add(self.args.source)
        inspect(self.args.source, "candidate")
        remove()
        add(self.args.previous)
        inspect(self.args.previous, "rollback")
        remove()
        remaining = self.run([client, "plugin", "list", "--json"], project, parse=True)
        if [item["id"] for item in remaining] != [f"{SENTINEL}@{SENTINEL_MARKETPLACE}"]:
            raise ValueError("Removal altered the unrelated registration")
        self.run([client, "plugin", "details", PACKAGE], project, allowed=(1,))
        remove(SENTINEL, SENTINEL_MARKETPLACE)
        if self.run([client, "plugin", "list", "--json"], project, parse=True):
            raise ValueError("Owned Claude registrations were not removed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--disposable-user", action="store_true", required=True,
                        help="Acknowledge that this dedicated user's client registries may be changed.")
    for name in ("codex", "claude", "source", "previous", "work", "receipt"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    for name in ("codex", "claude", "source", "previous", "receipt"):
        setattr(args, name, getattr(args, name).resolve())
    if platform.system() != "Linux":
        parser.error("This qualification profile is Linux only")
    if args.receipt.exists():
        parser.error("Receipt already exists")
    qualification = Qualification(args)
    errors = []
    sentinel = qualification.sentinel_source()
    for client in ("codex", "claude"):
        try:
            getattr(qualification, client)(sentinel)
        except (OSError, ValueError, RuntimeError, KeyError, IndexError, queue.Empty,
                subprocess.SubprocessError) as error:
            errors.append({"client": client, "error": str(error)})
    receipt = {"status": "supported" if not errors else "incomplete", "platform": platform.platform(),
               "python": platform.python_version(), "commands": qualification.commands,
               "observations": qualification.observations, "errors": errors,
               "limits": ["Fresh-user package lifecycle and native skill inventory are checked.",
                          "Installed resources are executed by this verifier, not by a model.",
                          "No automatic model selection, model quality, human playtest or other OS is established."]}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": receipt["status"], "errors": errors, "receipt": str(args.receipt)}))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
