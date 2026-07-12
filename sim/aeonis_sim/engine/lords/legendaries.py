"""M4 Legendary Buildings — prereqs, ownership, scoring helpers."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..types import BUILDING_SPECS, BuildingType, LEGENDARY_BUILDINGS
from .specs import is_lord
from .tiles import tile_is_portal

if TYPE_CHECKING:
    from ..types import GameState

LORD_LEGENDARY: dict[str, BuildingType] = {
    "cassian": BuildingType.GRAND_EXCHANGE,
    "seraphel": BuildingType.ARCANE_SANCTUM,
    "vharok": BuildingType.IRON_CITADEL,
    "elyndra": BuildingType.HEARTWOOD_SANCTUM,
    "rakhis": BuildingType.WINDSWORN_WARCAMP,
    "nyxara": BuildingType.HALL_OF_WHISPERS,
    "auriel": BuildingType.CATHEDRAL_OF_RADIANCE,
    "thalrik": BuildingType.DIMENSIONAL_NEXUS,
}

LEGENDARY_AP = 4


def legendary_for_lord(lord_id: str) -> Optional[BuildingType]:
    return LORD_LEGENDARY.get(lord_id)


def _legendary_already_built(state: GameState, btype: BuildingType) -> bool:
    return any(btype in t.buildings for t in state.tiles.values())


def _count_markets(state: GameState, pid: int) -> int:
    return sum(
        1
        for t in state.controlled(pid)
        for b in t.buildings
        if b == BuildingType.MARKET
    )


def _count_portals(state: GameState, pid: int) -> int:
    return sum(
        1
        for t in state.controlled(pid)
        if tile_is_portal(state, t.coord, pid)
    )


def legendary_prereqs_met(state: GameState, pid: int, btype: BuildingType) -> bool:
    p = state.player(pid)
    if btype == BuildingType.GRAND_EXCHANGE:
        return _count_markets(state, pid) >= 2 and p.gold >= 8
    if btype == BuildingType.ARCANE_SANCTUM:
        return len(p.discoveries) >= 3
    if btype == BuildingType.IRON_CITADEL:
        return any(t.has(BuildingType.FORTRESS) for t in state.controlled(pid))
    if btype == BuildingType.HEARTWOOD_SANCTUM:
        return state.pop_cap(pid) >= 15
    if btype == BuildingType.WINDSWORN_WARCAMP:
        return p.attacker_battle_wins >= 2
    if btype == BuildingType.HALL_OF_WHISPERS:
        return p.whispers_played >= 4
    if btype == BuildingType.CATHEDRAL_OF_RADIANCE:
        return p.renown >= 5
    if btype == BuildingType.DIMENSIONAL_NEXUS:
        return _count_portals(state, pid) >= 2
    return False


def can_build_legendary(state: GameState, pid: int, btype: BuildingType) -> bool:
    if btype not in LEGENDARY_BUILDINGS:
        return False
    p = state.player(pid)
    expected = legendary_for_lord(p.lord_id)
    if expected is None or btype != expected:
        return False
    if not is_lord(state, pid, p.lord_id):
        return False
    if _legendary_already_built(state, btype):
        return False
    if not legendary_prereqs_met(state, pid, btype):
        return False
    if p.ap < LEGENDARY_AP:
        return False
    spec = BUILDING_SPECS[btype]
    if p.gold < spec.gold or p.mana < spec.mana or p.influence < spec.influence:
        return False
    if p.pop_pool < spec.pop:
        return False
    return True


def score_legendary_vp(state: GameState, pid: int) -> None:
    """+2 VP per controlled Legendary at Cleanup (artifact-style source key)."""
    p = state.player(pid)
    for t in state.controlled(pid):
        for b in t.buildings:
            if b in LEGENDARY_BUILDINGS:
                p.add_vp(2, "legendary")
