"""Exploration events (Events.md / First Playable §4.5).

First entry to an unexplored hex draws from the exploration deck and resolves
immediately. Choice cards pause for an exploration decision point.
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

from .artifacts import claim_site, place_site
from .hexmap import distance, neighbors
from .types import Terrain, Unit, UNIT_STATS, UnitType

if TYPE_CHECKING:
    from .types import GameState

EXPLORATION_CARD_IDS: tuple[str, ...] = (
    "ancient_ruins",
    "trapped_vault",
    "speaking_stone_echo",
    "lost_cartographer",
    "wandering_mercenaries",
    "cursed_ground",
    "scattered_relics",
    "portal_instability",
    "ancient_vault_discovered",
)

CHOICE_CARDS = frozenset({
    "ancient_ruins",
    "trapped_vault",
    "ancient_vault_discovered",
})


def init_exploration_deck(rng: random.Random) -> list[str]:
    deck = list(EXPLORATION_CARD_IDS)
    rng.shuffle(deck)
    return deck


def draw_exploration(state: GameState, rng: random.Random) -> str | None:
    if not state.exploration_deck:
        state.exploration_deck = init_exploration_deck(rng)
    if not state.exploration_deck:
        return None
    card = state.exploration_deck.pop()
    state.exploration_discard.append(card)
    return card


def _nearest_city(state: GameState, pid: int, from_coord) -> Optional[tuple]:
    cities = [
        t.coord for t in state.controlled(pid)
        if t.terrain == Terrain.CITY
    ]
    if not cities:
        return None
    return min(cities, key=lambda c: distance(c, from_coord))


def _place_infantry(state: GameState, pid: int, coord) -> bool:
    p = state.player(pid)
    if p.pop_pool < 1:
        return False
    tile = state.tiles[coord]
    if any(u.owner != pid for u in tile.units):
        return False
    st = UNIT_STATS[UnitType.INFANTRY]
    tile.units.append(Unit(uid=state.new_uid(), owner=pid, type=UnitType.INFANTRY, hp=st.hp))
    p.pop_pool -= 1
    return True


def _lose_one_unit(state: GameState, pid: int, coord) -> bool:
    tile = state.tiles[coord]
    mine = [u for u in tile.units if u.owner == pid]
    if not mine:
        return False
    tile.units.remove(mine[0])
    return True


def resolve_auto(state: GameState, pid: int, coord, card_id: str, rng: random.Random) -> None:
    p = state.player(pid)
    tile = state.tiles[coord]
    if card_id == "speaking_stone_echo":
        p.influence += 1
        p.renown += 1
    elif card_id == "lost_cartographer":
        # AL-28: no fog in sim — +1 AP this round only.
        p.ap += 1
    elif card_id == "wandering_mercenaries":
        if not _place_infantry(state, pid, coord):
            city = _nearest_city(state, pid, coord)
            if city is not None:
                _place_infantry(state, pid, city)
    elif card_id == "cursed_ground":
        tile.cursed = True
    elif card_id == "scattered_relics":
        p.remnants += 2
    elif card_id == "portal_instability":
        if tile.terrain == Terrain.PORTAL:
            p.portal_instability_free = True


def exploration_choices(card_id: str, state: GameState, pid: int, coord) -> list[dict]:
    if card_id == "ancient_ruins":
        return [
            {"type": "exploration", "event": card_id, "choice": "search"},
            {"type": "exploration", "event": card_id, "choice": "leave"},
        ]
    if card_id == "trapped_vault":
        p = state.player(pid)
        out = [{"type": "exploration", "event": card_id, "choice": "lose_unit"}]
        if p.gold >= 2:
            out.append({"type": "exploration", "event": card_id, "choice": "pay_gold"})
        return out
    if card_id == "ancient_vault_discovered":
        place_site(state, coord)
        out = [{"type": "exploration", "event": card_id, "choice": "skip"}]
        if state.player(pid).ap >= 1:
            out.insert(0, {"type": "exploration", "event": card_id, "choice": "claim"})
        return out
    return []


def apply_exploration_choice(
    state: GameState,
    pid: int,
    coord,
    card_id: str,
    choice: str,
    rng: random.Random,
) -> None:
    p = state.player(pid)
    tile = state.tiles[coord]
    if card_id == "ancient_ruins":
        if choice == "leave":
            p.renown += 1
            return
        roll = rng.randint(1, 6)
        if roll >= 4:
            p.remnants += 2
        else:
            _lose_one_unit(state, pid, coord)
    elif card_id == "trapped_vault":
        if choice == "pay_gold":
            p.gold -= 2
        else:
            _lose_one_unit(state, pid, coord)
    elif card_id == "ancient_vault_discovered":
        if choice == "claim":
            p.ap -= 1
            claim_site(state, pid, coord)


def begin_exploration(
    state: GameState,
    pid: int,
    coord,
    rng: random.Random,
) -> tuple[str | None, bool]:
    """Mark explored, draw card. Returns (card_id, needs_player_choice)."""
    tile = state.tiles[coord]
    if tile.explored:
        return None, False
    tile.explored = True
    card = draw_exploration(state, rng)
    if card is None:
        return None, False
    if card in CHOICE_CARDS:
        return card, True
    resolve_auto(state, pid, coord, card, rng)
    return card, False


def enumerate_cleanse(state: GameState, pid: int) -> list[dict]:
    p = state.player(pid)
    if p.influence < 2:
        return []
    out = []
    for t in state.controlled(pid):
        if not t.cursed:
            continue
        if not any(u.owner == pid for u in t.units):
            continue
        out.append({"type": "cleanse", "hex": list(t.coord)})
    return out


def apply_cleanse(state: GameState, pid: int, coord) -> None:
    p = state.player(pid)
    tile = state.tiles[coord]
    if not tile.cursed or tile.controller != pid:
        raise ValueError("hex not cursed or not controlled")
    if p.influence < 2:
        raise ValueError("cannot afford cleanse")
    p.influence -= 2
    tile.cursed = False
