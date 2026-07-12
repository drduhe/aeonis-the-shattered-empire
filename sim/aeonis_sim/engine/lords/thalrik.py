"""Thal'rik sheet hooks (M4)."""
from __future__ import annotations

from .specs import is_lord
from .tiles import tile_is_portal


def threshold_ward_bonus(state, battle) -> int:
    """+1 Defense when defending a Portal hex (including Rift Anchor)."""
    if not is_lord(state, battle.defender, "thalrik"):
        return 0
    if tile_is_portal(state, battle.target, battle.defender):
        return 1
    return 0
