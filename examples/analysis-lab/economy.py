"""Lantern Crew's bounded resource transitions and an exact waiting model."""

from copy import deepcopy
import math


def transfer(scrap, from_id, to_id, amount):
    if from_id not in scrap or to_id not in scrap or from_id == to_id:
        raise ValueError("Transfer needs two existing, distinct owners.")
    if type(amount) is not int or amount < 0 or scrap[from_id] < amount:
        raise ValueError("Transfer amount is invalid or unaffordable.")
    changed = dict(scrap)
    changed[from_id] -= amount
    changed[to_id] += amount
    return changed


def resource_path(model):
    scrap = deepcopy(model["initial_scrap"])
    if "crew" not in scrap:
        raise ValueError("The recovery path requires the crew account.")
    initial_total = sum(scrap.values())
    rows = [{"operation": "initial", "scrap": dict(scrap), "generators": model["initial_generators"]}]
    move = model["transfer"]
    scrap = transfer(scrap, move["from_id"], move["to_id"], move["amount"])
    rows.append({"operation": "personal_transfer", "scrap": dict(scrap), "generators": model["initial_generators"]})
    scrap["crew"] += model["survey_yield_scrap"]
    rows.append({"operation": "free_survey_source", "scrap": dict(scrap), "generators": model["initial_generators"]})
    if scrap["crew"] < model["repair_cost_scrap"]:
        return {"status": "refuted", "reason": "repair_unaffordable", "rows": rows,
                "required_scrap": model["repair_cost_scrap"], "available_scrap": scrap["crew"]}
    scrap["crew"] -= model["repair_cost_scrap"]
    rows.append({"operation": "scrap_to_generator", "scrap": dict(scrap), "generators": model["initial_generators"] + 1})
    return {"status": "supported", "game_id": model["game_id"], "rows": rows,
            "units": {"scrap": "piece", "generators": "device"},
            "flow": {"initial_scrap": initial_total, "source_scrap": model["survey_yield_scrap"],
                     "conversion_input_scrap": model["repair_cost_scrap"], "final_scrap": sum(scrap.values()),
                     "new_generators": 1},
            "interpretation": "Transfer preserves stock and changes its holder; repair consumes scrap to produce a different resource."}


def waiting_distribution(probability, horizon=30, guarantee_at=12):
    if (not 0 < probability <= 1 or type(horizon) is not int or type(guarantee_at) is not int
            or horizon < 1 or guarantee_at < 1):
        raise ValueError("Need 0 < p <= 1 and positive integer horizons.")
    tail = 1 - probability
    mean = 1 / probability
    # Subtracting a tiny p from one erases it before the logarithm or capped mean.
    survival_log = None if probability == 1 else math.log1p(-probability)
    p95_estimate = 1 if probability == 1 else math.log(0.05) / survival_log
    if not math.isfinite(mean) or not math.isfinite(p95_estimate):
        raise ValueError("Probability is too small for a finite floating-point mean and p95; use a larger p.")
    capped_mean = (1 if probability == 1 else
                   min(guarantee_at, -math.expm1(guarantee_at * survival_log) / probability))
    p95 = math.ceil(p95_estimate)
    pmf = [{"attempt": attempt, "probability": tail ** (attempt - 1) * probability}
           for attempt in range(1, horizon + 1)]
    return {"model": "Independent identical attempts; first desired result ends waiting.",
            "unit": "attempt", "p": probability, "horizon": horizon, "pmf": pmf,
            "tail_after_horizon": tail ** horizon, "mean_attempts": mean,
            "p95_attempts": p95, "guarantee_at": guarantee_at,
            "mean_with_guarantee": capped_mean,
            "guarantee_probability_mass": tail ** (guarantee_at - 1),
            "evidence_kind": "exact_model_calculation", "observed_player_frequency": None}
