"""The original Lantern Crew save migration and recovery operation."""

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import sys

SKILL = Path(__file__).resolve().parents[2] / "skills" / "game-design"
sys.path.insert(0, str(SKILL / "scripts"))
from validate_artifact import validate  # noqa: E402


def unique_ids(values, label):
    ids = [value["id"] for value in values]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate " + label + " identity.")
    return set(ids)


def validate_state(state):
    if not isinstance(state, dict):
        raise ValueError("Save root must be a JSON object.")
    version = state.get("schema_version")
    if type(version) is not int or version not in (1, 2):
        raise ValueError("Unsupported save version.")
    validate(state, SKILL / "assets" / ("save-v" + str(version) + ".schema.json"))
    if datetime.fromisoformat(state["clock_utc"]).utcoffset() is None:
        raise ValueError("The shared rights clock needs a UTC offset.")
    actors = state["members"] if version == 1 else state["actors"]
    actors_by_id = {a["id"]: a for a in actors}
    actor_ids = unique_ids(actors, "actor")
    fact_ids = unique_ids(state["facts"], "fact")
    unique_ids(state["history"], "history")
    unique_ids(state["delegations"], "delegation")
    if any(not set(a["known_fact_ids"]) <= fact_ids for a in actors):
        raise ValueError("Actor knowledge refers to an unknown fact.")
    if any(event["actor_id"] not in actor_ids for event in state["history"]):
        raise ValueError("History refers to an unknown actor.")
    if state["election"]["candidate_id"] not in actor_ids:
        raise ValueError("Election candidate is not an actor.")
    if version == 1:
        rights = [dict(r, owner_id=a["id"]) for a in actors for r in a["rights"]]
        if state["crew"]["treasurer_id"] not in actor_ids:
            raise ValueError("Treasurer is not an actor.")
    else:
        rights = state["rights"]
        unique_ids(state["accounts"], "account")
        owners = [(a["owner_id"], a["resource_id"]) for a in state["accounts"]]
        if len(owners) != len(set(owners)):
            raise ValueError("Duplicate resource account for an owner.")
        if state["crew_id"] in actor_ids or {a["owner_id"] for a in state["accounts"]} != actor_ids | {state["crew_id"]}:
            raise ValueError("Every actor and the distinct crew need one owned scrap account.")
        for account in state["accounts"]:
            valid_owner = account["owner_id"] in actor_ids if account["owner_kind"] == "actor" else account["owner_id"] == state["crew_id"]
            if not valid_owner:
                raise ValueError("Account owner is unknown or has the wrong kind.")
        if state["roles"]["treasurer_id"] not in actor_ids:
            raise ValueError("Treasurer is not an actor.")
    right_ids = unique_ids(rights, "right")
    by_right = {r["id"]: r for r in rights}
    for right in rights:
        if right["owner_id"] not in actors_by_id:
            raise ValueError("A right lost its owner.")
        if datetime.fromisoformat(right["expires_at"]).utcoffset() is None:
            raise ValueError("A timed right needs a UTC offset.")
    for delegation in state["delegations"]:
        if (delegation["right_id"] not in right_ids or delegation["to_id"] not in actor_ids
                or delegation["from_id"] != by_right[delegation["right_id"]]["owner_id"]
                or not by_right[delegation["right_id"]]["delegable"]):
            raise ValueError("Delegation has no valid owner, recipient or delegable right.")
    return state


def migrate(state):
    validate_state(state)
    if state["schema_version"] == 2:
        return deepcopy(state)
    common = ("game_id", "save_id", "world_id", "clock_utc", "facts", "history", "delegations", "election")
    changed = {key: deepcopy(state[key]) for key in common}
    changed.update(schema_version=2, build_id="lantern-crew-2", crew_id=state["crew"]["id"],
                   actors=[], accounts=[], rights=[],
                   world={"generator": state["crew"]["generator"], "survey_yield_scrap": 2},
                   roles={"treasurer_id": state["election"]["candidate_id"] if state["election"]["accepted"] else state["crew"]["treasurer_id"]},
                   migration={"from_schema": 1, "operation": "lantern-save-1-to-2"})
    for actor in state["members"]:
        changed["actors"].append({"id": actor["id"], "status": actor["status"],
                                  "unlock_ids": list(actor["unlocks"]), "known_fact_ids": list(actor["known_fact_ids"])})
        changed["accounts"].append({"id": actor["id"] + "-scrap", "owner_id": actor["id"],
            "owner_kind": "actor", "resource_id": "scrap", "amount": actor["scrap"], "unit": "piece"})
        changed["rights"].extend(dict(deepcopy(right), owner_id=actor["id"]) for right in actor["rights"])
    changed["accounts"].append({"id": state["crew"]["id"] + "-scrap", "owner_id": state["crew"]["id"],
        "owner_kind": "crew", "resource_id": "scrap", "amount": state["crew"]["scrap"], "unit": "piece"})
    return validate_state(changed)


def crew_account(state):
    matches = [a for a in state["accounts"] if a["owner_kind"] == "crew" and a["owner_id"] == state["crew_id"]]
    if len(matches) != 1:
        raise ValueError("The crew needs exactly one scrap account.")
    return matches[0]


def operation_history(state, operation_id):
    if not isinstance(operation_id, str) or not operation_id or ":" in operation_id:
        raise ValueError("Operation ID must be nonempty and contain no ':'; this example reserves it for recovery subevents.")
    return {event["id"]: event for event in state["history"]}


def recover(state, operation_id):
    validate_state(state)
    if state["schema_version"] != 2:
        raise ValueError("Recovery consumer requires schema 2.")
    prior = operation_history(state, operation_id)
    if operation_id in prior:
        raise ValueError("Operation ID conflicts with another history event.")
    survey = prior.get(operation_id + ":survey")
    repair = prior.get(operation_id + ":repair")
    if survey is not None or repair is not None:
        if (survey is None or repair is None or survey["kind"] != "survey-completed"
                or survey["actor_id"] != "cy" or repair["kind"] != "generator-repaired"
                or repair["tick"] != survey["tick"] + 1):
            raise ValueError("Recovery history is incomplete or conflicts with the requested operation.")
        # Historical completion survives later loss, changed stock and a new treasurer.
        return deepcopy(state), {"status": "already_applied", "operation_id": operation_id}
    changed = deepcopy(state)
    if changed["world"]["generator"]:
        return state, {"status": "refuted", "reason": "generator_already_operational"}
    actors = {actor["id"]: actor for actor in changed["actors"]}
    if ("bo" not in actors or actors["bo"]["status"] != "active" or "winch" not in actors["bo"]["unlock_ids"]
            or "cy" not in actors or actors["cy"]["status"] != "active"
            or "survey-map" not in {f["id"] for f in changed["facts"] if f["public"]} | set(actors["cy"]["known_fact_ids"])):
        return state, {"status": "refuted", "reason": "missing_active_winch_or_route_contributor"}
    treasurer = changed["roles"]["treasurer_id"]
    if actors[treasurer]["status"] != "active":
        return state, {"status": "refuted", "reason": "no_active_authorized_spender"}
    account = crew_account(changed)
    before = account["amount"]
    yield_scrap = changed["world"]["survey_yield_scrap"]
    if before + yield_scrap < 6:
        return state, {"status": "refuted", "reason": "survey_does_not_fund_repair"}
    account["amount"] += yield_scrap
    account["amount"] -= 6
    changed["world"]["generator"] = True
    tick = max(event["tick"] for event in changed["history"]) + 1
    changed["history"].extend([{"id": operation_id + ":survey", "kind": "survey-completed", "actor_id": "cy", "tick": tick},
                               {"id": operation_id + ":repair", "kind": "generator-repaired", "actor_id": treasurer, "tick": tick + 1}])
    validate_state(changed)
    return changed, {"status": "supported", "operation_id": operation_id, "scrap_before": before,
                     "survey_source": yield_scrap, "repair_sink": 6, "scrap_after": account["amount"],
                     "operator": "bo", "route_decider": "cy", "spender": treasurer}


def resumed_survey(state, operation_id):
    validate_state(state)
    if state["schema_version"] != 2:
        raise ValueError("Survey consumer requires schema 2.")
    prior = operation_history(state, operation_id)
    if operation_id + ":survey" in prior or operation_id + ":repair" in prior:
        raise ValueError("Operation ID conflicts with recovery history.")
    completed = prior.get(operation_id)
    if completed is not None:
        if completed["kind"] != "survey-completed" or completed["actor_id"] != "cy":
            raise ValueError("Operation ID conflicts with another history event or survey actor.")
        return deepcopy(state), {"status": "already_applied", "operation_id": operation_id}
    changed = deepcopy(state)
    if not changed["world"]["generator"]:
        return state, {"status": "refuted", "reason": "source_not_repaired"}
    actor = next((a for a in changed["actors"] if a["id"] == "cy"), None)
    if actor is None or actor["status"] != "active":
        return state, {"status": "refuted", "reason": "route_decider_absent"}
    account = crew_account(changed)
    before = account["amount"]
    account["amount"] += changed["world"]["survey_yield_scrap"]
    changed["history"].append({"id": operation_id, "kind": "survey-completed", "actor_id": "cy",
                               "tick": max(e["tick"] for e in changed["history"]) + 1})
    return validate_state(changed), {"status": "supported", "operation_id": operation_id,
                                     "scrap_before": before, "scrap_after": account["amount"]}
