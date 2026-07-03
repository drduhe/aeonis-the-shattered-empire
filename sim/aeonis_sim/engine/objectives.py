"""Objective predicates (First Playable §4.4, Plan 3 MVP shared row)."""
from __future__ import annotations

from .types import Terrain

# --- Public shared row (Council Power deferred until Milestone 2) ---

PUBLIC_OBJECTIVE_IDS = (
    "frontier_lord",
    "builder",
    "portal_mastery",
    "warlord",
    "seat_of_empire",
)


def _frontier_lord(state, pid) -> bool:
    return len(state.controlled(pid)) >= 7


def _builder(state, pid) -> bool:
    return sum(len(t.buildings) for t in state.controlled(pid)) >= 3


def _portal_mastery(state, pid) -> bool:
    controls_portal = any(t.terrain == Terrain.PORTAL for t in state.controlled(pid))
    return controls_portal and state.player(pid).used_portal_travel


def _warlord(state, pid) -> bool:
    return state.player(pid).battle_wins >= 2


def _seat_of_empire(state, pid) -> bool:
    return any(t.imperial_seat for t in state.controlled(pid))


PUBLIC_OBJECTIVES = {
    "frontier_lord": _frontier_lord,
    "builder": _builder,
    "portal_mastery": _portal_mastery,
    "warlord": _warlord,
    "seat_of_empire": _seat_of_empire,
}

# --- Secret objectives (M1 sim subset) ---


def _golden_hoard(state, pid) -> bool:
    return state.player(pid).gold >= 10


def _mana_flood(state, pid) -> bool:
    return state.player(pid).mana >= 10


def _architect_of_control(state, pid) -> bool:
    special = {Terrain.CITY, Terrain.RUINS, Terrain.PORTAL}
    count = sum(
        1 for t in state.controlled(pid)
        if t.imperial_seat or t.terrain in special
    )
    return count >= 2


SECRET_OBJECTIVE_IDS = ("golden_hoard", "mana_flood", "architect_of_control")

SECRET_OBJECTIVES = {
    "golden_hoard": _golden_hoard,
    "mana_flood": _mana_flood,
    "architect_of_control": _architect_of_control,
}

# Back-compat alias for tests importing OBJECTIVES
OBJECTIVES = PUBLIC_OBJECTIVES
