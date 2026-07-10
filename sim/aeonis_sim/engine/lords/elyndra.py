"""Elyndra sheet hooks (M4)."""
from __future__ import annotations

from ..types import Terrain, UnitType
from .specs import is_lord, mark_round_used


def _elyndra_committed(state, battle) -> bool:
    if not is_lord(state, battle.defender, "elyndra"):
        return False
    units = list(battle.def_line) + [u for _, u in battle.def_committed]
    return any(u.type == UnitType.LORD and u.owner == battle.defender for u in units)


def entangling_roots_available(state, battle) -> bool:
    if not _elyndra_committed(state, battle):
        return False
    if state.tiles[battle.target].terrain != Terrain.FOREST:
        return False
    if state.player(battle.defender).mana < 1:
        return False
    key = f"entangling_r{battle.rounds}"
    return not state.player(battle.defender).lord_round.get(key)


def entangling_roots_penalty(atk_roll: int) -> int:
    return min(2, max(0, atk_roll - 1))


def would_entangling_prevent_hit(
    atk_roll: int, dfn_total: int, *, edge: bool,
) -> bool:
    """True if -2 penalty would flip a hit to a miss."""
    penalized = max(1, atk_roll - 2)
    if edge:
        return atk_roll >= dfn_total and penalized < dfn_total
    return atk_roll > dfn_total and penalized <= dfn_total


def apply_entangling_roots(state, battle) -> None:
    state.player(battle.defender).mana -= 1
    key = f"entangling_r{battle.rounds}"
    state.player(battle.defender).lord_round[key] = True


def apply_rooted_defenses_reroll(state, battle, rng, roll: int, die_max: int) -> int:
    """Once per battle round in Forest, auto-reroll one Defense die if higher."""
    if not is_lord(state, battle.defender, "elyndra"):
        return roll
    if state.tiles[battle.target].terrain != Terrain.FOREST:
        return roll
    key = f"rooted_reroll_r{battle.rounds}"
    if state.player(battle.defender).lord_round.get(key):
        return roll
    state.player(battle.defender).lord_round[key] = True
    reroll = rng.randint(1, die_max)
    return max(roll, reroll)
