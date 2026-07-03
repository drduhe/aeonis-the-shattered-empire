from __future__ import annotations

from .types import Terrain


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


# Packet §4.4 public objectives, minus Council Power (Milestone 2). All 2 VP,
# checked at Cleanup & Checks (AL-5: claim timing not specified in docs;
# engine auto-scores at Cleanup, once per card).
OBJECTIVES = {
    "frontier_lord": _frontier_lord,
    "builder": _builder,
    "portal_mastery": _portal_mastery,
    "warlord": _warlord,
    "seat_of_empire": _seat_of_empire,
}
