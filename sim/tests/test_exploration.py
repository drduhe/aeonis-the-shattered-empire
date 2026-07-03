"""Exploration layer, remnants, and M3 global events (Task 2)."""
from __future__ import annotations

import random

from aeonis_sim.engine.events import EVENT_CARD_IDS, resolve_event
from aeonis_sim.engine.exploration import (
    EXPLORATION_CARD_IDS,
    apply_cleanse,
    apply_exploration_choice,
    begin_exploration,
    init_exploration_deck,
    resolve_auto,
)
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.move import enumerate_moves
from aeonis_sim.engine.production import run_production
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import Terrain
from tests.conftest import advance_to_action_phase


def _neutral_unexplored(state, terrain=Terrain.PLAINS):
    for t in state.tiles.values():
        if t.controller is None and not t.explored and t.terrain == terrain:
            return t
    return None


def test_exploration_deck_has_nine_cards():
    deck = init_exploration_deck(random.Random(0))
    assert len(deck) == 9
    assert set(deck) == set(EXPLORATION_CARD_IDS)


def test_first_entry_triggers_once():
    state = build_initial_state({"players": 3}, random.Random(1))
    rng = random.Random(99)
    tile = _neutral_unexplored(state)
    assert tile is not None
    tile.explored = False
    state.exploration_deck = ["scattered_relics"]
    before = state.player(0).remnants
    card, needs = begin_exploration(state, 0, tile.coord, rng)
    assert card == "scattered_relics"
    assert needs is False
    assert state.player(0).remnants == before + 2
    assert tile.explored is True
    card2, needs2 = begin_exploration(state, 0, tile.coord, rng)
    assert card2 is None


def test_ancient_ruins_search_success():
    state = build_initial_state({"players": 3}, random.Random(2))
    tile = _neutral_unexplored(state)
    tile.explored = False
    state.exploration_deck = ["ancient_ruins"]
    begin_exploration(state, 0, tile.coord, random.Random(0))
    rng = random.Random(0)
    rng.randint = lambda a, b: 6  # force success
    before = state.player(0).remnants
    apply_exploration_choice(state, 0, tile.coord, "ancient_ruins", "search", rng)
    assert state.player(0).remnants == before + 2


def test_ancient_ruins_leave_renown():
    state = build_initial_state({"players": 3}, random.Random(2))
    tile = _neutral_unexplored(state)
    tile.explored = False
    state.exploration_deck = ["ancient_ruins"]
    begin_exploration(state, 0, tile.coord, random.Random(0))
    before = state.player(0).renown
    apply_exploration_choice(
        state, 0, tile.coord, "ancient_ruins", "leave", random.Random(0),
    )
    assert state.player(0).renown == before + 1


def test_trapped_vault_pay_gold():
    state = build_initial_state({"players": 3}, random.Random(3))
    tile = _neutral_unexplored(state)
    tile.explored = False
    p = state.player(0)
    p.gold = 5
    state.exploration_deck = ["trapped_vault"]
    begin_exploration(state, 0, tile.coord, random.Random(0))
    apply_exploration_choice(
        state, 0, tile.coord, "trapped_vault", "pay_gold", random.Random(0),
    )
    assert p.gold == 3


def test_speaking_stone_echo():
    state = build_initial_state({"players": 3}, random.Random(4))
    tile = _neutral_unexplored(state)
    tile.explored = False
    p = state.player(0)
    before = (p.influence, p.renown)
    resolve_auto(state, 0, tile.coord, "speaking_stone_echo", random.Random(0))
    assert (p.influence, p.renown) == (before[0] + 1, before[1] + 1)


def test_lost_cartographer_ap():
    state = build_initial_state({"players": 3}, random.Random(5))
    tile = _neutral_unexplored(state)
    p = state.player(0)
    ap = p.ap
    resolve_auto(state, 0, tile.coord, "lost_cartographer", random.Random(0))
    assert p.ap == ap + 1


def test_cursed_ground_and_cleanse():
    state = build_initial_state({"players": 3}, random.Random(6))
    tile = next(t for t in state.tiles.values() if t.controller == 0)
    for t in state.controlled(0):
        if t.coord != tile.coord:
            t.controller = None
    tile.cursed = True
    tile.terrain = Terrain.MOUNTAIN
    p = state.player(0)
    p.influence = 3
    before_gold = p.gold
    run_production(state)
    assert p.gold == before_gold
    apply_cleanse(state, 0, tile.coord)
    assert tile.cursed is False
    assert p.influence == 1


def test_remnants_from_ruins_each_round():
    state = build_initial_state({"players": 3}, random.Random(7))
    ruins = next(
        (t for t in state.tiles.values() if t.terrain == Terrain.RUINS), None,
    )
    if ruins is None:
        ruins = next(t for t in state.tiles.values() if t.controller == 0)
        ruins.terrain = Terrain.RUINS
    ruins.controller = 0
    p = state.player(0)
    p.remnants = 0
    run_production(state)
    assert p.remnants == 1


def test_open_roads_reduces_plains_cost():
    state = build_initial_state({"players": 3}, random.Random(8))
    state.open_roads = True
    moves = enumerate_moves(state, 0)
    plains_moves = [
        m for m in moves
        if state.tiles[tuple(m["dest"])].terrain == Terrain.PLAINS
        and m["cost"] >= 1
    ]
    if plains_moves:
        assert any(m["cost"] == 1 for m in plains_moves)


def test_event_deck_twelve_cards():
    assert len(EVENT_CARD_IDS) == 12


def test_ruins_unearthed_places_site():
    state = build_initial_state({"players": 3}, random.Random(9))
    resolve_event(state, "ruins_unearthed")
    assert len(state.artifact_sites) == 1


def test_echo_grants_remnants_and_site():
    state = build_initial_state({"players": 3}, random.Random(10))
    resolve_event(state, "echo_of_the_old_empire")
    assert all(state.player(i).remnants == 1 for i in range(3))
    assert len(state.artifact_sites) == 1


def test_council_crisis_forces_speaker_propose():
    state = build_initial_state({"players": 3}, random.Random(11))
    state.council_crisis = True
    state.speaker = 1
    state.agenda_revealed = "tax_levy"
    from aeonis_sim.engine.council import enumerate_proposal_choices

    speaker_choices = enumerate_proposal_choices(state, 1)
    assert len(speaker_choices) == 1
    assert speaker_choices[0]["type"] == "council_propose"
    other = enumerate_proposal_choices(state, 0)
    assert any(c["type"] == "council_pass" for c in other)


def test_move_into_unexplored_queues_exploration():
    g = Game({"players": 3}, seed=12345)
    dp = advance_to_action_phase(g)
    assert dp is not None
    s = g.state
    unexplored = _neutral_unexplored(s)
    if unexplored is None:
        return
    s.exploration_deck = ["speaking_stone_echo"]
    from aeonis_sim.engine.hexmap import neighbors
    for t in s.tiles.values():
        if t.controller == dp.pid and any(u.owner == dp.pid for u in t.units):
            for nb in neighbors(t.coord):
                if nb == unexplored.coord:
                    move = {
                        "type": "move",
                        "from": list(t.coord),
                        "dest": list(unexplored.coord),
                        "uids": [t.units[0].uid],
                        "cost": 1,
                        "portal": False,
                    }
                    g.submit(move)
                    edp = g.next_decision()
                    if edp and edp.kind == "exploration":
                        g.submit(edp.choices[0])
                    assert unexplored.explored is True
                    return
