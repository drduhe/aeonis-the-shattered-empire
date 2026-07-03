"""Global Event phase (Events.md / First_Playable_Packet.md §4.5).

M2 sim subset extended in M3 Task 2: twelve First Playable global events.
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING, Callable

from .artifacts import pick_neutral_ruins_hex, pick_seat_adjacent_site_hex, place_site
from .types import BuildingType, Terrain

if TYPE_CHECKING:
    from .types import GameState

EVENT_CARD_IDS: tuple[str, ...] = (
    "harsh_winter",
    "festival",
    "migration_wave",
    "council_crisis",
    "mana_surge",
    "border_skirmishes",
    "supply_disruption",
    "open_roads",
    "populist_uprising",
    "winds_of_fortune",
    "ruins_unearthed",
    "echo_of_the_old_empire",
)


def init_event_deck(rng: random.Random) -> list[str]:
    deck = list(EVENT_CARD_IDS)
    rng.shuffle(deck)
    return deck


def draw_event(state: GameState, rng: random.Random) -> str | None:
    if not state.event_deck:
        state.event_deck = init_event_deck(rng)
    if not state.event_deck:
        return None
    card = state.event_deck.pop()
    state.last_event_id = card
    return card


def _players_with_fewest(state: GameState, key) -> list[int]:
    vals = [key(state, p.pid) for p in state.players]
    best = min(vals)
    return [p.pid for p in state.players if key(state, p.pid) == best]


def _players_with_most(state: GameState, key) -> list[int]:
    vals = [key(state, p.pid) for p in state.players]
    best = max(vals)
    return [p.pid for p in state.players if key(state, p.pid) == best]


def _hex_count(state: GameState, pid: int) -> int:
    return len(state.controlled(pid))


def _plains_count(state: GameState, pid: int) -> int:
    return sum(1 for t in state.controlled(pid) if t.terrain == Terrain.PLAINS)


def _has_farm(state: GameState, pid: int) -> bool:
    return any(t.has(BuildingType.FARM) for t in state.controlled(pid))


def _discard_resources(state: GameState, pid: int, total: int) -> None:
    p = state.player(pid)
    left = total
    for attr in ("gold", "mana", "influence"):
        take = min(left, getattr(p, attr))
        setattr(p, attr, getattr(p, attr) - take)
        left -= take
        if left <= 0:
            break


def _resolve_harsh_winter(state: GameState) -> None:
    for p in state.players:
        if _has_farm(state, p.pid):
            continue
        p.gold = max(0, p.gold - 2)


def _resolve_festival(state: GameState) -> None:
    for p in state.players:
        p.pending_ap += 1


def _resolve_migration_wave(state: GameState) -> None:
    for p in state.players:
        if _plains_count(state, p.pid) < 2:
            continue
        cap = state.pop_cap(p.pid)
        p.pop_pool = min(cap, p.pop_pool + 2)


def _resolve_mana_surge(state: GameState) -> None:
    for p in state.players:
        p.mana += 2


def _resolve_border_skirmishes(state: GameState) -> None:
    for pid in _players_with_most(state, _hex_count):
        state.player(pid).renown += 1


def _resolve_supply_disruption(state: GameState) -> None:
    for p in state.players:
        _discard_resources(state, p.pid, 2)


def _resolve_populist_uprising(state: GameState) -> None:
    for pid in _players_with_fewest(state, _hex_count):
        p = state.player(pid)
        cap = state.pop_cap(pid)
        p.pop_pool = min(cap, p.pop_pool + 2)
        p.influence += 1


def _resolve_winds_of_fortune(state: GameState) -> None:
    for pid in _players_with_fewest(state, lambda s, p: s.player(p).vp):
        state.player(pid).pending_ap += 2
        state.pending_winds_draws.append(pid)


def _resolve_council_crisis(state: GameState) -> None:
    state.council_crisis = True


def _resolve_open_roads(state: GameState) -> None:
    state.open_roads = True


def _resolve_ruins_unearthed(state: GameState) -> None:
    coord = pick_neutral_ruins_hex(state)
    if coord is not None:
        place_site(state, coord)


def _resolve_echo_of_the_old_empire(state: GameState) -> None:
    coord = pick_seat_adjacent_site_hex(state, state.player(state.speaker).home)
    if coord is not None:
        place_site(state, coord)
    for p in state.players:
        p.remnants += 1


_EVENT_HANDLERS: dict[str, Callable[[GameState], None]] = {
    "harsh_winter": _resolve_harsh_winter,
    "festival": _resolve_festival,
    "migration_wave": _resolve_migration_wave,
    "council_crisis": _resolve_council_crisis,
    "mana_surge": _resolve_mana_surge,
    "border_skirmishes": _resolve_border_skirmishes,
    "supply_disruption": _resolve_supply_disruption,
    "open_roads": _resolve_open_roads,
    "populist_uprising": _resolve_populist_uprising,
    "winds_of_fortune": _resolve_winds_of_fortune,
    "ruins_unearthed": _resolve_ruins_unearthed,
    "echo_of_the_old_empire": _resolve_echo_of_the_old_empire,
}


def resolve_event(state: GameState, card_id: str) -> None:
    handler = _EVENT_HANDLERS.get(card_id)
    if handler is None:
        raise ValueError(f"unknown event: {card_id}")
    handler(state)
    state.event_discard.append(card_id)
