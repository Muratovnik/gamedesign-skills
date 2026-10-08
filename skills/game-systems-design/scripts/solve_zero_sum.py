#!/usr/bin/env python3
"""Calculate and certify one declared finite two-player zero-sum utility model."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import sys


SCIPY_VERSION = "1.17.0"
PROBABILITY_TOLERANCE = 1e-8
UTILITY_TOLERANCE = 1e-7
SOLVER_TOLERANCE = 1e-9
MAX_ACTIONS = 256
MAX_INPUT_BYTES = 4 * 1024 * 1024


class AnalysisError(Exception):
    def __init__(self, status, message, **details):
        super().__init__(message)
        self.status = status
        self.details = details


def invalid(message):
    raise AnalysisError("invalid_model", message)


def require_fields(value, fields, location):
    if not isinstance(value, dict):
        invalid(f"{location} must be an object")
    missing, unknown = set(fields) - value.keys(), value.keys() - set(fields)
    if missing or unknown:
        invalid(f"{location}: missing fields {sorted(missing)}; unsupported fields {sorted(unknown)}")


def require_text(value, location):
    if not isinstance(value, str) or not value.strip():
        invalid(f"{location} must be a nonempty string")


def validate_model(model):
    require_fields(model, {"schema_version", "model_id", "model_type", "context",
                           "row_player", "column_player", "utility", "payoffs"}, "model")
    if type(model["schema_version"]) is not int or model["schema_version"] != 1:
        invalid("schema_version must be the integer 1")
    if model["model_type"] != "two-player-zero-sum":
        invalid("Only an explicitly declared two-player-zero-sum utility model is supported")
    require_text(model["model_id"], "model_id")
    require_fields(model["context"], {"situation", "availability", "horizon"}, "context")
    for key, value in model["context"].items():
        require_text(value, f"context.{key}")
    for axis in ("row_player", "column_player"):
        player = model[axis]
        require_fields(player, {"name", "actions"}, axis)
        require_text(player["name"], f"{axis}.name")
        actions = player["actions"]
        if not isinstance(actions, list) or not 1 <= len(actions) <= MAX_ACTIONS:
            invalid(f"{axis}.actions must list 1 to {MAX_ACTIONS} available actions")
        for action in actions:
            require_text(action, f"{axis}.actions entry")
        if len(set(actions)) != len(actions):
            invalid(f"{axis}.actions must have unique names within that axis")
    if model["row_player"]["name"] == model["column_player"]["name"]:
        invalid("row_player.name and column_player.name must distinguish the two players")
    utility = model["utility"]
    require_fields(utility, {"meaning", "unit", "costs", "row_objective", "column_utility"}, "utility")
    for key in ("meaning", "unit", "costs"):
        require_text(utility[key], f"utility.{key}")
    if utility["row_objective"] != "maximize-expected-utility":
        invalid("utility.row_objective must explicitly be maximize-expected-utility")
    if utility["column_utility"] != "negative-of-row":
        invalid("utility.column_utility must explicitly be negative-of-row; no general-sum conversion is performed")
    m, n = len(model["row_player"]["actions"]), len(model["column_player"]["actions"])
    payoffs = model["payoffs"]
    if not isinstance(payoffs, list) or len(payoffs) != m:
        invalid("payoffs must contain one row for every named row action")
    matrix = []
    for i, row in enumerate(payoffs):
        if not isinstance(row, list) or len(row) != n:
            invalid(f"payoffs[{i}] must contain one value for every named column action")
        values = []
        for j, value in enumerate(row):
            if type(value) not in (int, float):
                invalid(f"payoffs[{i}][{j}] must be a finite number, not a boolean or string")
            try:
                number = float(value)
            except OverflowError:
                invalid(f"payoffs[{i}][{j}] is outside finite floating-point range")
            if not math.isfinite(number):
                invalid(f"payoffs[{i}][{j}] must be finite")
            values.append(number)
        matrix.append(values)
    return matrix


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Nonfinite JSON constant: {value}")


def read_model(path, report):
    try:
        with path.open("rb") as stream:
            raw = stream.read(MAX_INPUT_BYTES + 1)
    except OSError as exc:
        raise AnalysisError("input_unavailable", str(exc)) from exc
    if len(raw) > MAX_INPUT_BYTES:
        invalid(f"Model file exceeds the {MAX_INPUT_BYTES}-byte input limit")
    report["input"] = {"path": str(path.resolve()), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    try:
        model = json.loads(raw.decode("utf-8"), parse_constant=reject_constant, object_pairs_hook=unique_object)
    except (UnicodeError, ValueError, RecursionError) as exc:
        invalid(f"Cannot read an unambiguous finite JSON model: {exc}")
    matrix = validate_model(model)
    report["input"]["model"] = model
    return model, matrix


def probability_residuals(values):
    return {"sum_error": abs(math.fsum(values) - 1.0),
            "negative_mass": math.fsum(max(0.0, -x) for x in values),
            "upper_bound_violation": max(0.0, max(values) - 1.0)}


def checked_strategy(values, count, player):
    if len(values) != count or not all(math.isfinite(x) for x in values):
        raise AnalysisError("numerical_failure", f"{player}: solver returned nonfinite or mis-sized probabilities")
    raw = probability_residuals(values)
    if max(raw.values()) > PROBABILITY_TOLERANCE:
        raise AnalysisError("numerical_failure", f"{player}: probabilities fail simplex checks", probability_residuals=raw)
    # Repair only accepted floating-point drift, then certify the reported mixture.
    clipped = [max(0.0, x) for x in values]
    total = math.fsum(clipped)
    probabilities = [x / total for x in clipped]
    residuals = {"raw": raw, "reported": probability_residuals(probabilities),
                 "maximum_adjustment": max(abs(x - y) for x, y in zip(values, probabilities))}
    if max(residuals["reported"].values()) > PROBABILITY_TOLERANCE:
        raise AnalysisError("numerical_failure", f"{player}: reported probabilities fail simplex checks", probability_residuals=residuals)
    return probabilities, residuals


def certificate(matrix, row, column, row_value, column_value):
    """Recompute best responses from payoffs, independently of LP constraints/status."""
    row_against_columns = [math.fsum(row[i] * matrix[i][j] for i in range(len(row)))
                           for j in range(len(column))]
    rows_against_column = [math.fsum(matrix[i][j] * column[j] for j in range(len(column)))
                           for i in range(len(row))]
    lower, upper = min(row_against_columns), max(rows_against_column)
    expected = math.fsum(row[i] * rows_against_column[i] for i in range(len(row)))
    gap = upper - lower
    residuals = {"row_value_vs_guarantee": abs(row_value - lower),
                 "column_value_vs_cap": abs(column_value - upper),
                 "value_disagreement": abs(row_value - column_value)}
    checked = [*row_against_columns, *rows_against_column, expected, gap, *residuals.values()]
    if not all(math.isfinite(value) for value in checked):
        raise AnalysisError("numerical_failure", "Best-response calculation produced nonfinite quantities")
    details = {"row_guarantee": lower, "column_cap": upper, "expected_row_utility": expected,
               "gap": gap, "row_regret": upper - expected, "column_regret": expected - lower,
               "row_against_columns": row_against_columns, "rows_against_column": rows_against_column,
               "solver_value_residuals": residuals}
    if (abs(gap) > UTILITY_TOLERANCE or max(residuals.values()) > UTILITY_TOLERANCE
            or expected < lower - UTILITY_TOLERANCE or expected > upper + UTILITY_TOLERANCE):
        raise AnalysisError("numerical_failure", "Solver candidates fail independent best-response bounds", normalized_certificate=details)
    return details


def solve(model, matrix, report, time_limit):
    try:
        import numpy as np
        import scipy
        from scipy.optimize import linprog
    except (ImportError, OSError) as exc:
        raise AnalysisError("dependency_unavailable", f"Install the optional scripts/requirements.txt in the Python environment running this command: {exc}") from exc
    report["engine"] = {"api": "scipy.optimize.linprog", "method": "highs", "scipy_version": scipy.__version__,
                        "numpy_version": np.__version__, "python_version": platform.python_version(),
                        "python_implementation": platform.python_implementation()}
    if scipy.__version__ != SCIPY_VERSION:
        raise AnalysisError("dependency_mismatch", f"This adapter is qualified for scipy=={SCIPY_VERSION}; found {scipy.__version__}")

    smallest, largest = min(map(min, matrix)), max(map(max, matrix))
    # A positive affine change preserves preferences; centering also retains small
    # payoff differences when all utilities share a large common offset.
    offset = smallest if smallest == largest else smallest / 2.0 + largest / 2.0
    scale = max(abs(value - offset) for row in matrix for value in row) or 1.0
    normalized = [[(value - offset) / scale for value in row] for row in matrix]
    options = {"time_limit": time_limit, "primal_feasibility_tolerance": SOLVER_TOLERANCE,
               "dual_feasibility_tolerance": SOLVER_TOLERANCE, "ipm_optimality_tolerance": SOLVER_TOLERANCE}
    report["numerics"] = {"payoff_offset": offset, "payoff_scale": scale,
                          "probability_tolerance": PROBABILITY_TOLERANCE,
                          "normalized_utility_tolerance": UTILITY_TOLERANCE,
                          "utility_tolerance": UTILITY_TOLERANCE * scale, "linprog_options": options}
    a = np.asarray(normalized, dtype=float)
    m, n = a.shape
    problems = {
        "row": {"c": np.r_[np.zeros(m), -1.0], "A_ub": np.column_stack((-a.T, np.ones(n))),
                "b_ub": np.zeros(n), "A_eq": [np.r_[np.ones(m), 0.0]], "b_eq": [1.0],
                "bounds": [(0.0, None)] * m + [(None, None)]},
        "column": {"c": np.r_[np.zeros(n), 1.0], "A_ub": np.column_stack((a, -np.ones(m))),
                   "b_ub": np.zeros(m), "A_eq": [np.r_[np.ones(n), 0.0]], "b_eq": [1.0],
                   "bounds": [(0.0, None)] * n + [(None, None)]},
    }
    report["solvers"] = {}
    vectors = {}
    for player, problem in problems.items():
        result = linprog(**problem, method="highs", options=options)
        report["solvers"][player] = {"success": bool(result.success), "status": int(result.status),
                                      "message": str(result.message), "iterations": int(result.nit)}
        if not result.success or result.status != 0:
            raise AnalysisError("solver_failure", f"{player}: linprog did not return an optimum; this is not a game-design verdict")
        expected_length = (m if player == "row" else n) + 1
        if result.x is None or np.shape(result.x) != (expected_length,):
            raise AnalysisError("numerical_failure", f"{player}: solver returned a missing or mis-sized vector")
        vector = [float(value) for value in result.x]
        if not all(math.isfinite(value) for value in vector):
            raise AnalysisError("numerical_failure", f"{player}: solver returned a nonfinite vector")
        report["solvers"][player]["normalized_value"] = vector[-1]
        vectors[player] = vector
    row, row_residuals = checked_strategy(vectors["row"][:-1], m, "row")
    column, column_residuals = checked_strategy(vectors["column"][:-1], n, "column")
    checked = certificate(normalized, row, column, vectors["row"][-1], vectors["column"][-1])
    def in_units(value):
        restored = math.fsum((offset, scale * value))
        if not math.isfinite(restored):
            raise AnalysisError("numerical_failure", "Utility bounds could not be represented as finite output numbers")
        return restored
    report["strategies"] = {
        "row": [{"action": action, "probability": probability}
                for action, probability in zip(model["row_player"]["actions"], row)],
        "column": [{"action": action, "probability": probability}
                   for action, probability in zip(model["column_player"]["actions"], column)],
    }
    report["certificate"] = {
        "row_guarantee": in_units(checked["row_guarantee"]), "column_cap": in_units(checked["column_cap"]),
        "expected_row_utility": in_units(checked["expected_row_utility"]),
        "expected_column_utility": -in_units(checked["expected_row_utility"]),
        "gap": scale * checked["gap"], "row_regret": scale * checked["row_regret"],
        "column_regret": scale * checked["column_regret"],
        "row_against_columns": [in_units(value) for value in checked["row_against_columns"]],
        "rows_against_column": [in_units(value) for value in checked["rows_against_column"]],
        "normalized": checked, "probability_residuals": {"row": row_residuals, "column": column_residuals},
    }
    limits = ["This calculation concerns only the declared expected-utility model, not observed play or game quality."]
    if m == 1 or n == 1:
        limits.append("At least one player has only one available action; this does not establish strategic diversity.")
    report["limitations"] = limits
    report["status"] = "solved"


def positive_seconds(value):
    try:
        seconds = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("time limit must be a finite positive number") from exc
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("time limit must be a finite positive number")
    return seconds


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="Explicit utility model JSON")
    parser.add_argument("--output", type=Path, required=True, help="New JSON report path; existing paths are never overwritten")
    parser.add_argument("--time-limit", type=positive_seconds, default=10.0, help="HiGHS seconds per LP, default 10")
    args = parser.parse_args(argv)
    report = {"schema_version": 1, "status": "unavailable"}
    try:
        # Exclusive creation below also protects against an output appearing during
        # the solve. Do not reserve or truncate a report before the model succeeds.
        if args.output.exists() or args.output.is_symlink():
            raise AnalysisError("output_unavailable", f"Output already exists: {args.output}")
        model, matrix = read_model(args.model, report)
        report["adapter_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        solve(model, matrix, report, args.time_limit)
        encoded = json.dumps(report, indent=2, allow_nan=False) + "\n"
        try:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(encoded)
        except OSError as exc:
            raise AnalysisError("output_unavailable", str(exc)) from exc
        print(encoded, end="")
        return 0
    except AnalysisError as exc:
        report.update(status=exc.status, error=str(exc), **exc.details)
    except (ValueError, TypeError, ArithmeticError, RuntimeError) as exc:
        report.update(status="numerical_failure", error=f"No certified result: {exc}")
    except OSError as exc:
        report.update(status="input_unavailable", error=str(exc))
    print(json.dumps(report, allow_nan=False), file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
