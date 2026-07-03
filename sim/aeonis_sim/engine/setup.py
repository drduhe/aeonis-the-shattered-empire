from __future__ import annotations

import random

from .hexmap import generate_map, neighbors
from .objectives import (
    PUBLIC_OBJECTIVE_IDS,
    SECRET_OBJECTIVE_IDS,
)
from .types import BASE_AP, GameState, PlayerState, Unit, UNIT_STATS, UnitType


def build_initial_state(config: dict, rng: random.Random) -> GameState:
    n = config["players"]
    tiles, homes = generate_map(n, rng)
    state = GameState(players=[], tiles=tiles)

    public_deck = list(PUBLIC_OBJECTIVE_IDS)
    rng.shuffle(public_deck)
    state.shared_public_revealed = [public_deck.pop(), public_deck.pop()]
    state.shared_public_deck = public_deck

    secret_deck: list = []

    for pid in range(n):
        p = PlayerState(pid=pid, home=homes[pid], ap=BASE_AP,
                        gold=2, mana=2, influence=1)
        if not secret_deck:
            secret_deck = list(SECRET_OBJECTIVE_IDS)
            rng.shuffle(secret_deck)
        p.secret_objective = secret_deck.pop()
        state.players.append(p)

        home = tiles[homes[pid]]
        for ut in (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.INFANTRY,
                   UnitType.ARCHER, UnitType.LORD):
            home.units.append(Unit(uid=state.new_uid(), owner=pid, type=ut,
                                   hp=UNIT_STATS[ut].hp))

        home.controller = pid
        for nb in neighbors(homes[pid]):
            t = tiles.get(nb)
            if t is not None and t.controller is None and not t.imperial_seat \
                    and t.terrain.value in ("plains", "forest", "mountain"):
                t.controller = pid

    for p in state.players:
        p.pop_pool = state.pop_cap(p.pid) - state.pop_used(p.pid)

    return state
