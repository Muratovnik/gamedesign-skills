"""Measurement definitions and the shared choice/transition boundary, without model runs."""

from copy import deepcopy
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from consumer import observer_view, select_content
from state import DEFAULT_CONTENT, crew_account, migrate, recover
from telemetry import query
from validate_artifact import digest, read_json

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"


class MeasurementDefinitions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.dictionary = read_json(FIXTURES / "event-dictionary.json")

    def test_unknown_outcome_and_missing_control_definitions_fail_before_database(self):
        for index, event in enumerate(("gate_crossed", "action_accepted", "episode_end")):
            with self.subTest(event=event):
                definition = deepcopy(self.dictionary)
                definition["builds"]["gate-episode-2"]["allowed_events"].remove(event)
                path, database, output = (self.work / f"{kind}-{index}" for kind in ("dictionary", "database", "output"))
                path.write_text(json.dumps(definition))
                result = subprocess.run([sys.executable, "-B", str(HERE / "lab.py"), "telemetry",
                    "--sessions", str(FIXTURES / "sessions.csv"), "--events", str(FIXTURES / "events.csv"),
                    "--dictionary", str(path), "--build", "gate-episode-2", "--cohort", "new",
                    "--database", str(database), "--output", str(output)], capture_output=True, text=True, check=False, timeout=15)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stderr)["status"], "invalid_or_missing_evidence")
                self.assertFalse(database.exists())
                self.assertFalse(output.exists())

    def test_renamed_valid_outcome_keeps_measurement_and_unobserved_outcome_is_failure(self):
        with (FIXTURES / "events.csv").open(newline="") as stream:
            reader = csv.DictReader(stream)
            fields, original_rows = reader.fieldnames, list(reader)
        for observed in (True, False):
            with self.subTest(observed=observed):
                definition = deepcopy(self.dictionary)
                meaning = definition["builds"]["gate-episode-2"]
                meaning["outcome_event"] = "crossing_confirmed"
                meaning["allowed_events"].remove("gate_crossed")
                meaning["allowed_events"].append("crossing_confirmed")
                rows = deepcopy(original_rows)
                for row in rows:
                    if row["event_name"] == "gate_crossed":
                        row["event_name"] = "crossing_confirmed" if observed else "action_accepted"
                dictionary, events, database = (self.work / f"{kind}-{observed}" for kind in ("dictionary", "events", "database"))
                dictionary.write_text(json.dumps(definition))
                with events.open("w", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(rows)
                result = query(FIXTURES / "sessions.csv", events, dictionary, "gate-episode-2", "new", database)
                self.assertEqual(result["counts"], {"success": int(observed), "failure": 1 if observed else 2,
                                                    "unknown": 2, "not_attempted": 1})
                self.assertEqual(result["success_fraction_among_known_attempts"], 0.5 if observed else 0)
                self.assertEqual(result["input_sha256"]["dictionary"], digest(dictionary))
                self.assertEqual(result["reopened_database"], {"sessions": 8, "events": 18})


class RecoveryEligibility(unittest.TestCase):
    def setUp(self):
        self.state = migrate(read_json(FIXTURES / "save-v1.json"))
        self.content = read_json(DEFAULT_CONTENT)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def test_unknown_winch_procedure_refutes_both_consumers_but_public_knowledge_enables(self):
        bo = next(actor for actor in self.state["actors"] if actor["id"] == "bo")
        bo["known_fact_ids"] = []
        before = deepcopy(self.state)
        choice = select_content(observer_view(self.state, "bo"), self.content, "salvage")
        self.assertNotIn("operate-winch", [item["action"] for item in choice["selected"]])
        unchanged, response = recover(self.state, "repair-private")
        self.assertEqual(response["status"], "refuted")
        self.assertEqual(unchanged, before)
        self.assertEqual(self.state, before)
        next(fact for fact in self.state["facts"] if fact["id"] == "winch-procedure")["public"] = True
        self.assertEqual(select_content(observer_view(self.state, "bo"), self.content, "salvage")["decision"], "operate-winch")
        repaired, response = recover(self.state, "repair-public")
        self.assertEqual(response["status"], "supported")
        self.assertTrue(repaired["world"]["generator"])
        self.assertEqual(crew_account(repaired)["amount"], 0)

    def test_content_rights_and_history_constrain_choice_and_transition_together(self):
        for field, requirement in (("required_rights", ["archive-host"]), ("forbidden_history", ["archive-message"])):
            with self.subTest(field=field):
                content = deepcopy(self.content)
                next(item for item in content["items"] if item["id"] == "winch-route")[field] = requirement
                path = self.work / (field + ".json")
                path.write_text(json.dumps(content))
                self.assertNotIn("operate-winch", [item["action"] for item in
                    select_content(observer_view(self.state, "bo"), content, "salvage")["selected"]])
                unchanged, result = recover(self.state, "repair-constrained", path)
                self.assertEqual(result["status"], "refuted")
                self.assertEqual(unchanged, self.state)
                self.assertEqual(result["content_input"], {"path": str(path.resolve()), "sha256": digest(path)})

    def test_explicit_alternate_repertoire_is_consumed_and_identified_by_cli(self):
        next(actor for actor in self.state["actors"] if actor["id"] == "bo")["known_fact_ids"] = []
        winch = next(item for item in self.content["items"] if item["id"] == "winch-route")
        winch.update(id="assisted-winch", required_facts=[], text="The supervisor supplies the procedure.")
        source, content, output = (self.work / name for name in ("save.json", "assisted.json", "repaired.json"))
        source.write_text(json.dumps(self.state))
        content.write_text(json.dumps(self.content))
        self.assertEqual(select_content(observer_view(self.state, "bo"), self.content, "salvage")["decision"], "operate-winch")
        result = subprocess.run([sys.executable, "-B", str(HERE / "lab.py"), "recover", "--input", str(source),
            "--content", str(content), "--operation-id", "assisted", "--output", str(output)],
            capture_output=True, text=True, check=False, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        interpretation, receipt = map(json.loads, result.stdout.splitlines())
        self.assertEqual(interpretation["content_input"], {"path": str(content.resolve()), "sha256": digest(content)})
        self.assertEqual(receipt["input_sha256"], digest(source))
        self.assertEqual(crew_account(read_json(output))["amount"], 0)

    def test_missing_action_repertoire_is_invalid_and_completed_replay_needs_no_current_content(self):
        missing = deepcopy(self.content)
        missing["items"] = [item for item in missing["items"] if item["action"] != "operate-winch"]
        path = self.work / "missing-winch.json"
        path.write_text(json.dumps(missing))
        with self.assertRaisesRegex(ValueError, "no salvage action"):
            recover(self.state, "new-operation", path)
        repaired, _ = recover(self.state, "completed-operation")
        repaired["world"]["generator"] = False
        next(actor for actor in repaired["actors"] if actor["id"] == "bo")["known_fact_ids"] = []
        replay, status = recover(repaired, "completed-operation", self.work / "unavailable-content.json")
        self.assertEqual(status, {"status": "already_applied", "operation_id": "completed-operation"})
        self.assertEqual(replay, repaired)


if __name__ == "__main__":
    unittest.main()
