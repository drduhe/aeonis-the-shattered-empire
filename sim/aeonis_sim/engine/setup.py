from __future__ import annotations

import random

from .hexmap import generate_map, neighbors
from .objectives import OBJECTIVES
from .types import BASE_AP, GameState, PlayerState, Unit, UNIT_STATS, UnitType


def build_initial_state(config: dict, rng: random.Random) -> GameState:
    n = config["players"]
    tiles, homes = generate_map(n, rng)
    state = GameState(players=[], tiles=tiles)

    deck: list = []

    for pid in range(n):
        if not deck:
            deck = list(OBJECTIVES.keys())
            rng.shuffle(deck)
        p = PlayerState(pid=pid, home=homes[pid], ap=BASE_AP,
                        gold=2, mana=2, influence=1)
        p.objective = deck.pop()
        state.players.append(p)

        home = tiles[homes[pid]]
        for ut in (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.INFANTRY,
                   UnitType.ARCHER, UnitType.LORD):
            home.units.append(Unit(uid=state.new_uid(), owner=pid, type=ut,
                                   hp=UNIT_STATS[ut].hp))

        # Control the home cluster: home City + its 3 cluster tiles (§3.5)
        home.controller = pid
        for nb in neighbors(homes[pid]):
            t = tiles.get(nb)
            if t is not None and t.controller is None and not t.imperial_seat \
                    and t.terrain.value in ("plains", "forest", "mountain"):
                t.controller = pid

    for p in state.players:
        # AL-4: starting units occupy Population; pool = cap - used
        p.pop_pool = state.pop_cap(p.pid) - state.pop_used(p.pid)

    return state
