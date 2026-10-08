"""Public semantic controls; these examples are not a held-out model evaluation."""

from copy import deepcopy
import csv
from decimal import Decimal, localcontext
import json
import math
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys

from consumer import observer_view, select_content
from economy import resource_path, transfer, waiting_distribution
from state import crew_account, migrate, recover, resumed_survey, validate_state
from telemetry import query
from validate_artifact import read_json
from observe_evidence import import_observations

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def migration_contract(old, new):
    """The fixture's promised relations, independent of the migration implementation."""
    personal = {a["owner_id"]: a["amount"] for a in new["accounts"] if a["owner_kind"] == "actor"}
    actors = {actor["id"]: actor for actor in new["actors"]}
    return (personal == {"ava": 2, "bo": 0, "cy": 0}
            and crew_account(new)["amount"] == 4
            and new["rights"][0]["owner_id"] == "ava"
            and new["rights"][0]["expires_at"] == "2026-10-15T20:00:00Z"
            and actors["bo"]["unlock_ids"] == ["winch"]
            and actors["bo"]["known_fact_ids"] == ["winch-procedure"]
            and actors["ava"]["known_fact_ids"] == ["archive-code"]
            and actors["cy"]["known_fact_ids"] == ["survey-map"]
            and new["history"] == old["history"])


class ResourceAndWaitingTests(unittest.TestCase):
    def test_transfer_preserves_stock_but_changes_holder(self):
        stock = {"old-name": 2, "new-name": 0}
        self.assertEqual(transfer(stock, "old-name", "new-name", 2), {"old-name": 0, "new-name": 2})
        self.assertEqual(stock, {"old-name": 2, "new-name": 0})
        with self.assertRaises(ValueError):
            transfer(stock, "old-name", "new-name", 3)
        with self.assertRaises(ValueError):
            transfer(stock, "old-name", "old-name", 1)

    def test_recovery_conversion_has_different_units_and_source_sensitivity(self):
        model = read_json(FIXTURES / "resource-model.json")
        result = resource_path(model)
        self.assertEqual(result["rows"][-1]["scrap"], {"crew": 0, "ava": 0, "bo": 2})
        self.assertEqual(result["flow"], {"initial_scrap": 6, "source_scrap": 2,
                         "conversion_input_scrap": 6, "final_scrap": 2, "new_generators": 1})
        model["survey_yield_scrap"] = 0
        self.assertEqual(resource_path(model)["reason"], "repair_unaffordable")

    def test_waiting_known_distribution_and_guarantee(self):
        result = waiting_distribution(0.5, horizon=3, guarantee_at=3)
        self.assertEqual([row["probability"] for row in result["pmf"]], [0.5, 0.25, 0.125])
        self.assertEqual(result["tail_after_horizon"], 0.125)
        self.assertEqual(result["p95_attempts"], 5)
        self.assertEqual(result["mean_with_guarantee"], 1.75)
        certain = waiting_distribution(1, horizon=3, guarantee_at=3)
        self.assertEqual(certain["p95_attempts"], 1)
        self.assertEqual([row["probability"] for row in certain["pmf"]], [1, 0, 0])
        self.assertEqual((certain["mean_attempts"], certain["mean_with_guarantee"],
                          certain["tail_after_horizon"]), (1, 1, 0))
        self.assertLess(waiting_distribution(0.2)["tail_after_horizon"], waiting_distribution(0.1)["tail_after_horizon"])

    def test_tiny_probability_preserves_capped_waiting_or_declares_numeric_limit(self):
        for probability in (1e-18, 1e-307):
            with self.subTest(probability=probability), localcontext() as context:
                context.prec = 400
                survival = Decimal(1) - Decimal.from_float(probability)
                # Independent finite tail sum for E[min(T, 12)], avoiding the quotient formula.
                expected = float(sum(survival ** attempt for attempt in range(12)))
                result = waiting_distribution(probability, horizon=3, guarantee_at=12)
                self.assertAlmostEqual(result["mean_with_guarantee"], expected, places=12)
                self.assertLessEqual(result["mean_with_guarantee"], 12)
                self.assertTrue(math.isfinite(result["mean_attempts"]))
                self.assertGreater(result["p95_attempts"], result["mean_attempts"])
                json.dumps(result, allow_nan=False)
        for probability in (1e-308, math.nextafter(0.0, 1.0)):
            with self.subTest(probability=probability), self.assertRaisesRegex(ValueError, "finite"):
                waiting_distribution(probability)


class MigrationAndConsumersTests(unittest.TestCase):
    def setUp(self):
        self.old = read_json(FIXTURES / "save-v1.json")
        self.new = migrate(self.old)
        self.content = read_json(FIXTURES / "content.json")

    def test_migration_keeps_owned_knowledge_rights_and_history(self):
        self.assertTrue(migration_contract(self.old, self.new))
        self.assertEqual(self.new["roles"]["treasurer_id"], "bo")
        self.assertEqual(migrate(self.new), self.new)
        self.assertEqual(self.old, read_json(FIXTURES / "save-v1.json"))

    def test_equal_total_and_valid_schema_do_not_prove_owner_preservation(self):
        bad = deepcopy(self.new)
        bad["rights"][0]["owner_id"] = "bo"
        bad["accounts"][0]["amount"] = 0
        bad["accounts"][1]["amount"] = 2
        validate_state(bad)
        self.assertEqual(sum(a["amount"] for a in bad["accounts"]), sum(a["amount"] for a in self.new["accounts"]))
        self.assertFalse(migration_contract(self.old, bad))
        self.assertIn("archive-host", observer_view(bad, "bo")["right_kinds"])
        self.assertNotIn("archive-host", observer_view(self.new, "bo")["right_kinds"])

    def test_absent_or_unaccepted_authority_does_not_fund_repair(self):
        self.old["election"]["accepted"] = False
        absent = migrate(self.old)
        self.assertEqual(absent["roles"]["treasurer_id"], "ava")
        unchanged, result = recover(absent, "recovery-1")
        self.assertEqual(result["reason"], "no_active_authorized_spender")
        self.assertEqual(unchanged, absent)

    def test_recovery_then_resumed_consumer_and_replay(self):
        restored, result = recover(self.new, "recovery-1")
        self.assertEqual((result["scrap_before"], result["survey_source"], result["repair_sink"], result["scrap_after"]), (4, 2, 6, 0))
        self.assertTrue(restored["world"]["generator"])
        self.assertEqual(recover(restored, "recovery-1")[0], restored)
        resumed, _ = resumed_survey(restored, "expedition-2")
        self.assertEqual(crew_account(resumed)["amount"], 2)
        replay, status = resumed_survey(resumed, "expedition-2")
        self.assertEqual(replay, resumed)
        self.assertEqual(status["status"], "already_applied")
        self.assertEqual([e["id"] for e in replay["history"]].count("archive-message"), 1)

    def test_missing_winch_changes_feasible_group_plan(self):
        self.new["actors"][1]["status"] = "away"
        snapshot = deepcopy(self.new)
        changed, result = recover(self.new, "recovery-1")
        self.assertEqual(result["reason"], "missing_active_winch_or_route_contributor")
        self.assertEqual(changed, snapshot)

    def test_hidden_fact_does_not_enter_other_observer_or_choice(self):
        before = observer_view(self.new, "bo")
        self.new["facts"][2]["value"] = "CHANGED-SECRET"
        self.new["actors"][0]["known_fact_ids"].append("survey-map")
        after = observer_view(self.new, "bo")
        self.assertEqual(before, after)
        choice = select_content(after, self.content, "salvage")
        self.assertEqual(choice["decision"], "operate-winch")
        self.assertNotIn("archive-code", after["facts"])
        self.assertEqual(select_content(observer_view(self.new, "cy"), self.content, "salvage")["decision"], "chart-route")

    def test_zero_selected_is_refuted_and_empty_inspected_is_missing(self):
        bo = observer_view(self.new, "bo")
        archive = select_content(bo, self.content, "archive")
        self.assertEqual((archive["status"], archive["selected_count"], archive["inspected_count"]), ("refuted", 0, 1))
        self.assertEqual(select_content(bo, self.content, "absent-stage")["status"], "missing_evidence")
        selected_ids = [i["id"] for i in select_content(bo, self.content, "salvage")["selected"]]
        self.assertNotIn("first-archive-message", selected_ids)

    def test_explicit_delegation_enables_host_but_does_not_transfer_personal_right(self):
        self.new["delegations"].append({"id": "host-delegation-1", "right_id": "archive-pass-ava", "from_id": "ava", "to_id": "bo", "accepted": True})
        self.new["actors"][1]["known_fact_ids"].append("archive-code")
        self.assertEqual(select_content(observer_view(self.new, "bo"), self.content, "archive")["selected_count"], 1)
        self.assertEqual(self.new["rights"][0]["owner_id"], "ava")
        self.new["clock_utc"] = "2026-10-15T20:00:00Z"
        self.assertEqual(select_content(observer_view(self.new, "bo"), self.content, "archive")["selected_count"], 0)


class TelemetryAndObservationTests(unittest.TestCase):
    def test_missing_validator_dependency_has_distinct_status(self):
        validator = Path(__file__).resolve().parents[2] / "skills" / "game-design" / "scripts" / "validate_artifact.py"
        result = subprocess.run([sys.executable, "-S", str(validator), "--help"], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stderr)["status"], "dependency_unavailable")

    def test_build_cohort_missingness_and_reopened_database(self):
        with tempfile.TemporaryDirectory() as directory:
            result = query(FIXTURES / "sessions.csv", FIXTURES / "events.csv", FIXTURES / "event-dictionary.json",
                           "gate-episode-2", "new", Path(directory) / "data.sqlite")
        self.assertEqual(result["counts"], {"success": 1, "failure": 1, "unknown": 2, "not_attempted": 1})
        self.assertEqual(result["success_fraction_among_known_attempts"], 0.5)
        self.assertEqual(result["reopened_database"], {"sessions": 8, "events": 18})
        self.assertEqual({r["session_id"] for r in result["sessions"]}, {"s02", "s03", "s04", "s05", "s08"})

    def test_late_success_name_does_not_satisfy_deadline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "late-events.csv"
            with (FIXTURES / "events.csv").open(newline="") as stream:
                reader = csv.DictReader(stream)
                fields, rows = reader.fieldnames, list(reader)
            for row in rows:
                if row["event_id"] == "s02-e2":
                    row["run_tick"] = "40"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            result = query(FIXTURES / "sessions.csv", path, FIXTURES / "event-dictionary.json", "gate-episode-2", "new", Path(directory) / "late.sqlite")
        self.assertEqual(result["counts"]["success"], 0)
        self.assertEqual(result["counts"]["failure"], 2)

    def test_empty_cohort_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "No sessions"):
                query(FIXTURES / "sessions.csv", FIXTURES / "events.csv", FIXTURES / "event-dictionary.json",
                      "gate-episode-2", "unrecorded", Path(directory) / "empty.sqlite")

    def test_synthetic_import_retains_unknown_and_assisted_cases(self):
        result = import_observations(FIXTURES / "observations.csv", FIXTURES / "observation-manifest.json")
        self.assertEqual(result["human_claim"], "not_established")
        self.assertEqual(result["counts"], {"all": 4, "known_attempt_outcomes": 2, "unknown_outcomes": 1,
                                         "unaided_known_attempts": 1, "unaided_completed": 1})
        with tempfile.TemporaryDirectory() as directory:
            empty = Path(directory) / "empty.csv"
            empty.write_text((FIXTURES / "observations.csv").read_text().splitlines()[0] + "\n")
            with self.assertRaisesRegex(ValueError, "No observations"):
                import_observations(empty, FIXTURES / "observation-manifest.json")


if __name__ == "__main__":
    unittest.main()
