"""Vharok sheet hooks (M4)."""
from __future__ import annotations

from itertools import combinations

from ..types import UnitType
from .specs import is_lord, mark_round_used


def _vharok_committed(state, battle) -> bool:
    if not is_lord(state, battle.defender, "vharok"):
        return False
    units = list(battle.def_line) + [u for _, u in battle.def_committed]
    return any(u.type == UnitType.LORD and u.owner == battle.defender for u in units)


def lock_the_line_available(state, battle) -> bool:
    if not _vharok_committed(state, battle):
        return False
    if state.player(battle.defender).mana < 1:
        return False
    key = f"lock_line_r{battle.rounds}"
    if state.player(battle.defender).lord_round.get(key):
        return False
    return bool(battle.att_targets)


def _legal_def_line_targets(battle) -> list:
    return [u for u in battle.def_line if u.hp > 0]


def enumerate_lock_the_line(state, battle) -> list:
    """Optional DP: skip or reassign up to two attacker targets."""
    if not lock_the_line_available(state, battle):
        return []
    choices = [{"type": "lock_the_line_skip"}]
    strikers = sorted(
        [u for u in battle.att_line if u.hp > 0],
        key=lambda u: u.uid,
    )
    legal = _legal_def_line_targets(battle)
    if not strikers or not legal:
        return choices
    for count in (1, 2):
        if count > len(strikers):
            break
        for combo in combinations(strikers, count):
            for targets in combinations(legal, count):
                reassign = [
                    {"striker": s.uid, "target": t.uid}
                    for s, t in zip(combo, targets)
                ]
                choices.append({"type": "lock_the_line", "reassign": reassign})
    return choices


def apply_lock_the_line(state, battle, choice: dict) -> None:
    if choice["type"] == "lock_the_line_skip":
        key = f"lock_line_r{battle.rounds}"
        state.player(battle.defender).lord_round[key] = True
        return
    for pair in choice.get("reassign", []):
        battle.att_targets[int(pair["striker"])] = int(pair["target"])
    state.player(battle.defender).mana -= 1
    key = f"lock_line_r{battle.rounds}"
    state.player(battle.defender).lord_round[key] = True
