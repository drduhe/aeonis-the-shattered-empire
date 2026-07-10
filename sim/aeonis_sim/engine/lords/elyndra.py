"""Elyndra sheet hooks (M4)."""
from __future__ import annotations

from ..types import Terrain
from .specs import is_lord


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
