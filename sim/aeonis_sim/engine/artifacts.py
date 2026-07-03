"""Artifact Sites — M3 Task 2 stub (full deck in Task 3).

Sites are markers created by global/exploration events. Task 3 adds the
24-card deck, purge-draw, and VP relic scoring.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .hexmap import distance
from .types import Terrain

if TYPE_CHECKING:
    from .types import Coord, GameState


def _key(coord) -> str:
    return f"{coord[0]},{coord[1]}"


def has_site(state: GameState, coord) -> bool:
    return _key(coord) in state.artifact_sites


def place_site(state: GameState, coord) -> None:
    """Place an Artifact Site marker (card drawn in Task 3)."""
    k = _key(coord)
    if k not in state.artifact_sites:
        state.artifact_sites[k] = {"card_id": None, "owner": None}


def claim_site(state: GameState, pid: int, coord) -> bool:
    site = state.artifact_sites.get(_key(coord))
    if site is None or site.get("owner") is not None:
        return False
    site["owner"] = pid
    return True


def pick_neutral_ruins_hex(state: GameState) -> Optional[tuple]:
    for t in state.tiles.values():
        if t.terrain == Terrain.RUINS and t.controller is None:
            return t.coord
    for t in state.tiles.values():
        if t.controller is None and not t.imperial_seat:
            return t.coord
    return None


def pick_seat_adjacent_site_hex(
    state: GameState,
    speaker_home: tuple | None = None,
) -> Optional[tuple]:
    seat = next((t.coord for t in state.tiles.values() if t.imperial_seat), None)
    if seat is None:
        return None
    cands = [
        t.coord for t in state.tiles.values()
        if not has_site(state, t.coord)
    ]
    if not cands:
        return None
    if speaker_home is None:
        return min(cands, key=lambda c: distance(c, seat))
    # AL-30: tie-break clockwise from Speaker — axial sort from Speaker home.
    return min(cands, key=lambda c: (distance(c, seat), c[0] - speaker_home[0], c[1] - speaker_home[1]))
