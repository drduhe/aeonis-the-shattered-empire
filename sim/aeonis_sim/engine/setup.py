from __future__ import annotations

import random

from .hexmap import generate_map, neighbors
from .objectives import (
    SECRET_OBJECTIVE_IDS,
    deal_secret_draw,
    deal_round3_secrets,
    setup_shared_public_row,
)
from .artifacts import init_artifact_deck
from .exploration import init_exploration_deck
from .whispers import draw_whispers, init_whisper_deck
from .council import init_agenda_deck
from .events import init_event_deck
from .types import BASE_AP, GameState, PlayerState, Unit, UNIT_STATS, UnitType


def build_initial_state(config: dict, rng: random.Random) -> GameState:
    n = config["players"]
    tiles, homes = generate_map(n, rng)
    state = GameState(players=[], tiles=tiles)
    combat = config.get("combat", {})
    if combat.get("aggressors_edge_mode"):
        state.aggressors_edge_mode = str(combat["aggressors_edge_mode"])
    elif combat.get("aggressors_edge"):
        state.aggressors_edge_mode = "full"
    else:
        state.aggressors_edge_mode = "off"
    state.pillage = bool(combat.get("pillage", False))

    economy = config.get("ap_economy", {})
    cap = economy.get("ap_bonus_cap")
    state.ap_bonus_cap = int(cap) if cap is not None else None
    state.rally = bool(economy.get("rally", False))

    pacing = config.get("pacing", {})
    vp = pacing.get("vp_threshold")
    if vp is not None:
        state.vp_threshold = int(vp)

    objectives = config.get("objectives", {})
    fl = objectives.get("frontier_lord_min_hexes")
    if fl is not None:
        state.frontier_lord_min_hexes = int(fl)

    seat_rewards = config.get("seat_rewards", {})
    sov = seat_rewards.get("seat_of_empire_vp")
    if sov is not None:
        state.seat_of_empire_vp = int(sov)

    economy_exp = config.get("economy", {})
    ml = economy_exp.get("merchant_lord_min_gold")
    if ml is not None:
        state.merchant_lord_min_gold = int(ml)
    bb = economy_exp.get("builder_min_buildings")
    if bb is not None:
        state.builder_min_buildings = int(bb)
    t1 = economy_exp.get("tier1_production_build_ap")
    if t1 is not None:
        state.tier1_production_build_ap = int(t1)

    state.speaker = int(rng.randrange(n))
    state.event_deck = init_event_deck(rng)
    state.agenda_deck = init_agenda_deck(rng)
    state.exploration_deck = init_exploration_deck(rng)
    state.artifact_deck = init_artifact_deck(rng)
    state.whisper_deck = init_whisper_deck(rng)

    secret_deck = list(SECRET_OBJECTIVE_IDS)
    rng.shuffle(secret_deck)
    state.secret_objective_deck = secret_deck

    revealed, public_deck = setup_shared_public_row(rng, objectives)
    state.shared_public_revealed = revealed
    state.shared_public_deck = public_deck

    for pid in range(n):
        p = PlayerState(pid=pid, home=homes[pid], ap=BASE_AP,
                        gold=2, mana=2, influence=1)
        state.players.append(p)
        cap = deal_secret_draw(state, pid, rng)
        if cap:
            raise RuntimeError("unexpected cap draw at setup")

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

    for p in state.players:
        draw_whispers(state, p.pid, 2, rng)

    for t in tiles.values():
        if t.controller is not None:
            t.explored = True

    return state
