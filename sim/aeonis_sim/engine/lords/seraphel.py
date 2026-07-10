"""Seraphel sheet hooks (M4)."""
from __future__ import annotations

from ..types import Terrain, TERRAIN_COST, UnitType
from .specs import is_lord, mark_round_used, round_unused


def scry_top_agenda(state) -> str | None:
    """Peek the next agenda card without mutating the deck."""
    if not state.agenda_deck:
        return None
    return state.agenda_deck[-1]


def blink_step_available(state, pid: int, group: list) -> bool:
    if not is_lord(state, pid, "seraphel"):
        return False
    if not round_unused(state, pid, "blink_step"):
        return False
    if state.player(pid).mana < 2:
        return False
    return any(u.type == UnitType.LORD and u.owner == pid for u in group)


def blink_terrain_cost(terrain: Terrain) -> int | None:
    if terrain in (Terrain.MOUNTAIN, Terrain.DESERT):
        return 1
    return None


def apply_blink_step(state, pid: int) -> None:
    state.player(pid).mana -= 2
    mark_round_used(state, pid, "blink_step")
