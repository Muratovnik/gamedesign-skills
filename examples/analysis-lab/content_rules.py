"""One action-eligibility contract for content choice and campaign transitions."""

from pathlib import Path
import sys

SKILL = Path(__file__).resolve().parents[2] / "skills" / "game-design"
sys.path.insert(0, str(SKILL / "scripts"))
from validate_artifact import validate  # noqa: E402


def validate_content(content, game_id):
    validate(content, SKILL / "assets" / "content.schema.json")
    if content["game_id"] != game_id:
        raise ValueError("Content and observer belong to different games.")
    if len({item["id"] for item in content["items"]}) != len(content["items"]):
        raise ValueError("Content identities are duplicated.")
    return content


def rejection_reasons(view, item):
    reasons = []
    if not view["active"]:
        reasons.append("observer_away")
    for key, available in (("required_facts", view["facts"]), ("required_unlocks", view["unlock_ids"]),
                           ("required_rights", view["right_kinds"])):
        if not set(item[key]) <= set(available):
            reasons.append(key)
    if set(item["forbidden_history"]) & set(view["history_ids"]):
        reasons.append("already_emitted_history")
    return reasons
