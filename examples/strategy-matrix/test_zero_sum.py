"""Actual CLI calculations against mathematical oracles and invalid evidence controls."""

from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/game-systems-design/scripts/solve_zero_sum.py"
FIXTURE = HERE / "fixtures/channel-signals.json"


class ZeroSumCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.model = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.sequence = 0

    def paths(self):
        self.sequence += 1
        return self.work / f"model-{self.sequence}.json", self.work / f"report-{self.sequence}.json"

    def invoke(self, model=None, *, raw=None, isolated=False, injected=None, output=None):
        path, proposed_output = self.paths()
        output = output or proposed_output
        path.write_text(json.dumps(self.model if model is None else model) if raw is None else raw, encoding="utf-8")
        command = [sys.executable, "-B"]
        if isolated:
            command.append("-S")
        if injected:
            command.extend(["-c", injected, str(SCRIPT)])
        else:
            command.append(str(SCRIPT))
        command.extend(["--model", str(path), "--output", str(output)])
        environment = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
        result = subprocess.run(command, capture_output=True, text=True, check=False,
                                timeout=30, env=environment, cwd=self.work)
        return result, output, path

    def solved(self, *args, **kwargs):
        result, output, path = self.invoke(*args, **kwargs)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report, json.loads(result.stdout))
        self.assertEqual(report["status"], "solved")
        self.assertEqual(report["input"]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(report["input"]["bytes"], len(path.read_bytes()))
        self.assertEqual(report["adapter_sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertEqual(report["engine"]["scipy_version"], "1.17.0")
        self.assertTrue(report["engine"]["numpy_version"])
        self.assertEqual(report["engine"]["method"], "highs")
        self.assertLessEqual(abs(report["certificate"]["normalized"]["gap"]), report["numerics"]["normalized_utility_tolerance"])
        for player in ("row", "column"):
            values = [entry["probability"] for entry in report["strategies"][player]]
            self.assertTrue(all(math.isfinite(value) and value >= 0 for value in values))
            self.assertAlmostEqual(math.fsum(values), 1.0, places=12)
        return report

    def rejected(self, *args, status="invalid_model", **kwargs):
        result, output, _ = self.invoke(*args, **kwargs)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertFalse(output.exists(), "A failed calculation cannot leave a solved report")
        self.assertNotIn("Traceback", result.stderr)
        report = json.loads(result.stderr)
        self.assertEqual(report["status"], status, report)
        return report

    def with_matrix(self, matrix):
        model = deepcopy(self.model)
        model["payoffs"] = matrix
        model["row_player"]["actions"] = [f"row-{i}" for i in range(len(matrix))]
        model["column_player"]["actions"] = [f"column-{j}" for j in range(len(matrix[0]))] if matrix else []
        model["context"]["availability"] = "Every named synthetic test action is available."
        return model

    def test_unequal_cycle_matches_exact_rational_mixture(self):
        # Solving A q = 0 gives q0 = 3*q2 and q1 = 2*q2; normalization
        # gives (1/2, 1/3, 1/6). Skew symmetry gives the same row strategy.
        report = self.solved()
        for player in ("row", "column"):
            for entry, expected in zip(report["strategies"][player], (1 / 2, 1 / 3, 1 / 6)):
                self.assertAlmostEqual(entry["probability"], expected, places=10)
        self.assertAlmostEqual(report["certificate"]["expected_row_utility"], 0.0, places=10)
        self.assertAlmostEqual(report["certificate"]["row_guarantee"], 0.0, places=10)
        self.assertAlmostEqual(report["certificate"]["column_cap"], 0.0, places=10)
        self.assertEqual(report["input"]["model"]["context"], self.model["context"])
        self.assertEqual(report["input"]["model"]["utility"], self.model["utility"])

    def test_positive_affine_changes_preserve_mixture_and_change_value(self):
        for scale, offset in ((1, 5), (4, -7), (0.000001, 0), (1, 1e12)):
            with self.subTest(scale=scale, offset=offset):
                model = self.with_matrix([[scale * value + offset for value in row] for row in self.model["payoffs"]])
                report = self.solved(model)
                for player in ("row", "column"):
                    for entry, expected in zip(report["strategies"][player], (1 / 2, 1 / 3, 1 / 6)):
                        self.assertAlmostEqual(entry["probability"], expected, places=9)
                self.assertAlmostEqual(report["certificate"]["expected_row_utility"], offset, delta=max(1e-10, abs(offset) * 1e-15))

    def test_negative_rectangular_model_has_the_correct_value(self):
        # The added third column pays -2.5 to either row, so the minimizer
        # selects it; the other columns bound the row mixture to [1/4, 3/4].
        report = self.solved(self.with_matrix([[-1, -3, -2.5], [-3, -1, -2.5]]))
        p = report["strategies"]["row"][0]["probability"]
        self.assertGreaterEqual(p, 0.25 - 1e-10)
        self.assertLessEqual(p, 0.75 + 1e-10)
        self.assertAlmostEqual(report["strategies"]["column"][2]["probability"], 1.0, places=10)
        self.assertAlmostEqual(report["certificate"]["expected_row_utility"], -2.5, places=10)

    def test_rectangular_game_with_multiple_optima_does_not_require_one_column_mixture(self):
        report = self.solved(self.with_matrix([[1, -1, 0], [-1, 1, 0]]))
        p = [entry["probability"] for entry in report["strategies"]["row"]]
        self.assertAlmostEqual(p[0], 0.5, places=10)
        self.assertAlmostEqual(report["certificate"]["expected_row_utility"], 0.0, places=10)
        q = [entry["probability"] for entry in report["strategies"]["column"]]
        self.assertAlmostEqual(q[0], q[1], places=10)

    def test_intended_dominance_is_a_valid_calculation(self):
        model = json.loads((HERE / "fixtures/intended-hierarchy.json").read_text(encoding="utf-8"))
        report = self.solved(model)
        self.assertAlmostEqual(report["strategies"]["row"][0]["probability"], 1.0, places=10)
        self.assertAlmostEqual(report["certificate"]["row_guarantee"], 2.0, places=10)
        self.assertAlmostEqual(report["certificate"]["column_cap"], 2.0, places=10)

    def test_singleton_and_one_sided_choices_are_valid_limited_results(self):
        for matrix, expected in (([[-4]], -4), ([[-3, -5]], -5), ([[3], [-5]], 3), ([[0]], 0)):
            with self.subTest(matrix=matrix):
                report = self.solved(self.with_matrix(matrix))
                self.assertAlmostEqual(report["certificate"]["expected_row_utility"], expected, places=10)
                self.assertTrue(any("only one available action" in value for value in report["limitations"]))

    def test_permuting_named_axes_preserves_each_actions_probability(self):
        row_order, column_order = (2, 0, 1), (1, 2, 0)
        model = deepcopy(self.model)
        model["payoffs"] = [[self.model["payoffs"][i][j] for j in column_order] for i in row_order]
        model["row_player"]["actions"] = [self.model["row_player"]["actions"][i] for i in row_order]
        model["column_player"]["actions"] = [self.model["column_player"]["actions"][j] for j in column_order]
        report = self.solved(model)
        expected = {"Anchor": 1 / 2, "Lantern": 1 / 3, "Sail": 1 / 6}
        for player in ("row", "column"):
            for entry in report["strategies"][player]:
                self.assertAlmostEqual(entry["probability"], expected[entry["action"]], places=10)

    def test_empty_and_misaligned_axes_are_invalid(self):
        variants = (self.with_matrix([]), self.with_matrix([[]]),
                    dict(self.model, payoffs=[]), dict(self.model, payoffs=[[0], [1], [2]]),
                    dict(self.model, payoffs=[[0, -1, 2], [1, 0], [-2, 3, 0]]))
        for model in variants:
            with self.subTest(model=model):
                self.rejected(model)

    def test_nonfinite_boolean_and_nonnumeric_payoffs_are_invalid(self):
        for value in (float("nan"), float("inf"), -float("inf"), True, False, "1", None, 10 ** 400):
            with self.subTest(value=value):
                model = deepcopy(self.model)
                model["payoffs"][0][0] = value
                self.rejected(model)
        self.rejected(raw=FIXTURE.read_text(encoding="utf-8").replace("[0, -1, 2]", "[1e999, -1, 2]"))

    def test_general_sum_and_undeclared_utility_are_invalid(self):
        variants = [dict(self.model, model_type="general-sum"), dict(self.model, column_payoffs=self.model["payoffs"])]
        for key, value in (("row_objective", "maximize-score"), ("column_utility", "separate-payoff-matrix"), ("costs", "")):
            model = deepcopy(self.model)
            model["utility"][key] = value
            variants.append(model)
        for model in variants:
            with self.subTest(model=model):
                self.rejected(model)

    def test_malformed_json_and_wrong_top_level_are_invalid(self):
        for raw in ("{broken", "[]", "null", "true", '"matrix"', '{"schema_version": 1, "schema_version": 1}'):
            with self.subTest(raw=raw):
                self.rejected(raw=raw)

    def test_missing_context_and_ambiguous_axis_names_are_invalid(self):
        for mutate in (lambda m: m.pop("context"),
                       lambda m: m["context"].__setitem__("availability", " "),
                       lambda m: m["row_player"]["actions"].__setitem__(1, "Anchor"),
                       lambda m: m["column_player"].__setitem__("name", "Harbour"),
                       lambda m: m.__setitem__("schema_version", True)):
            model = deepcopy(self.model)
            mutate(model)
            self.rejected(model)

    def test_missing_optional_dependency_is_unavailable_evidence(self):
        # -S removes site-packages in this subprocess without altering any environment.
        report = self.rejected(isolated=True, status="dependency_unavailable")
        self.assertIn("sha256", report["input"])

    def test_unqualified_dependency_version_is_reported(self):
        injected = """
import runpy, sys
import scipy
scipy.__version__ = '0.0-unqualified-test-version'
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')
"""
        report = self.rejected(injected=injected, status="dependency_mismatch")
        self.assertEqual(report["engine"]["scipy_version"], "0.0-unqualified-test-version")

    def test_dense_action_limit_has_a_valid_neighbor(self):
        report = self.solved(self.with_matrix([[0]] * 256))
        self.assertEqual(len(report["strategies"]["row"]), 256)
        self.assertAlmostEqual(report["certificate"]["expected_row_utility"], 0.0, places=10)
        self.rejected(self.with_matrix([[0]] * 257))

    def test_existing_output_is_preserved_byte_for_byte(self):
        output = self.work / "existing.json"
        sentinel = b'{"preserve": "previous calculation"}\n'
        output.write_bytes(sentinel)
        result, _, _ = self.invoke(output=output)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stderr)["status"], "output_unavailable")
        self.assertEqual(output.read_bytes(), sentinel)

    def test_solver_success_cannot_hide_wrong_bounds_or_probability_residuals(self):
        # Run the actual CLI and real linprog, corrupting only its returned row
        # candidate. These are adapter failure controls, not solver fidelity tests.
        for mutation in ("result.x[:-1] = [1.0, 0.0, 0.0]", "result.x[:-1] = [0.0, 0.0, 0.0]", "result.x[-1] += 0.5", "result.x[0] = float('nan')"):
            injected = f"""
import runpy, sys
import scipy.optimize
original = scipy.optimize.linprog
calls = 0
def corrupt(*args, **kwargs):
    global calls
    result = original(*args, **kwargs)
    calls += 1
    if calls == 1:
        {mutation}
    return result
scipy.optimize.linprog = corrupt
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')
"""
            with self.subTest(mutation=mutation):
                report = self.rejected(injected=injected, status="numerical_failure")
                self.assertTrue(report["solvers"]["row"]["success"])

    def test_solver_failure_status_remains_unavailable_evidence(self):
        injected = """
import runpy, sys
import scipy.optimize
original = scipy.optimize.linprog
def fail(*args, **kwargs):
    result = original(*args, **kwargs)
    result.success = False
    result.status = 4
    result.message = 'Injected numerical solver failure'
    return result
scipy.optimize.linprog = fail
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')
"""
        report = self.rejected(injected=injected, status="solver_failure")
        self.assertEqual(report["solvers"]["row"]["status"], 4)
        self.assertNotIn("column", report["solvers"])


if __name__ == "__main__":
    unittest.main()
