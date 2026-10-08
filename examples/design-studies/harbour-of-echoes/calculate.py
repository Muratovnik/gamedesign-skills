"""Replay the declared arithmetic and set relationships of the paper studies.

This is an author calculator, not a game engine, player, narrative interpreter
or skill evaluator. Run with Python 3 from any directory. It reads cases.json
beside this file and writes calculation-output.json beside it. Missing or empty
families stop the operation instead of reporting a clean result.
"""

import hashlib
import json
from fractions import Fraction
from pathlib import Path


def choose_smaller(left, right):
    return "left" if left < right else "right" if right < left else "equal"


here = Path(__file__).resolve().parent
raw = (here / "cases.json").read_bytes()
data = json.loads(raw)
quay = data["quay"]
for label, values in (
    ("quay", quay["cases"]),
    ("inference", data["inference"]["cases"]),
    ("loom-u", data["loom"]["u_values"]),
    ("loom-v", data["loom"]["v_values"]),
    ("lenses", data["lenses"]),
):
    if not values:
        raise ValueError(f"No declared cases for {label}")

quay_rows = []
required_width = Fraction(str(quay["body_width_m"])) + 2 * Fraction(
    str(quay["clearance_each_side_m"])
)
for case in quay["cases"]:
    status = "accepted"
    arrival = None
    start = None
    press = case["press_tick"]
    if Fraction(str(case["width_m"])) < required_width:
        status = "unreachable"
    elif press is None:
        status = "no-command"
    elif press < case["cue_tick"]:
        status = "input-precedes-available-cue"
    elif press < case["control_tick"] - 2:
        status = "expired-before-buffer"
    else:
        start = max(press, case["control_tick"])
        distance = Fraction(str(case["length_m"]))
        speed = Fraction(str(quay["speed_m_per_tick"]))
        if distance <= 0 or speed <= 0:
            raise ValueError("Travel needs positive distance and speed")
        duration = -(-distance // speed)
        arrival = start + duration
    safe = (
        arrival is not None
        and arrival <= quay["sweep_tick"]
        and case["target"] == "alcove"
    )
    quay_rows.append({
        "case": case["id"], "command": status, "start_tick": start,
        "arrival_tick": arrival, "outcome": "safe-at-32" if safe else "hit-at-30",
        "stamina_after_commitment": 2,
    })

spec = data["inference"]
inference_rows = []
for case in spec["cases"]:
    possible = set(spec["universe"])
    for evidence in case["encountered"]:
        possible &= set(spec["compatible_with"][evidence])
    status = "unique-under-declared-premises" if len(possible) == 1 else "underdetermined"
    if not case["encountered"]:
        status = "no-evidence"
    if not possible:
        status = "inconsistent-evidence"
    inference_rows.append({
        "case": case["id"], "encountered_count": len(case["encountered"]),
        "possible": sorted(possible), "status": status,
    })

loom_rows = []
for u in data["loom"]["u_values"]:
    for v in data["loom"]["v_values"]:
        loom_rows.append({
            "u": u, "v": v, "prototype_pulses": min(4, 2**u * 2**v),
            "altered_pulses": 2**v,
        })
phrase_lengths = {
    "a": sum(data["loom"]["phrase_a_beats"]),
    "b": sum(data["loom"]["phrase_b_beats"]),
}

lens_rows = []
for case in data["lenses"]:
    left_n, left_d = case["left"]
    right_n, right_d = case["right"]
    if not 0 <= left_n <= left_d or not 0 <= right_n <= right_d:
        raise ValueError("Counts must describe inspected lots")
    left, right = Fraction(left_n, left_d), Fraction(right_n, right_d)
    correct = choose_smaller(left, right)
    raw_count_choice = choose_smaller(left_n, right_n)
    lens_rows.append({
        "case": case["id"], "left_fraction": str(left), "right_fraction": str(right),
        "accepted": ["left", "right", "equal"] if correct == "equal" else [correct],
        "smaller_count_choice": raw_count_choice,
        "smaller_count_succeeds": correct == "equal" or raw_count_choice == correct,
    })

stock = data["reserve"]["start_batches"]
reserve_rows = []
for request in range(1, data["reserve"]["requested_batches_before_repair"] + 1):
    allowed = stock > 0
    if allowed:
        stock -= 1
    reserve_rows.append({"request": request, "allowed": allowed, "remaining": stock})

output = {
    "identity": data["identity"],
    "evidence_kind": "executed-author-calculation-of-declared-paper-models",
    "input_sha256": hashlib.sha256(raw).hexdigest(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "limits": ["No native-engine run", "No human participants", "No narrative VM", "No behavioral skill evaluation"],
    "quay": quay_rows,
    "recovery": {"first_clear_tick": quay["wash_last_tick"] + 1,
                 "first_next_threat_tick": quay["wash_last_tick"] + 4},
    "inference": inference_rows,
    "loom": loom_rows,
    "phrase_lengths_beats": phrase_lengths,
    "lenses": lens_rows,
    "reserve_before_repair": reserve_rows,
}
target = here / "calculation-output.json"
target.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "output": target.name,
    "input_sha256": output["input_sha256"],
    "case_counts": {"quay": len(quay_rows), "inference": len(inference_rows),
                    "loom": len(loom_rows), "lenses": len(lens_rows), "reserve": len(reserve_rows)},
    "quay_outcomes": {row["case"]: row["outcome"] for row in quay_rows},
    "phrase_lengths_beats": phrase_lengths,
}, indent=2))
