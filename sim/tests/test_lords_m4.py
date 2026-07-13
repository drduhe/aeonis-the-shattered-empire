"""M4 foundation: launch-Lord setup, stats, and Plan 5 signatures."""
from __future__ import annotations

import random

from aeonis_sim.engine import combat
from aeonis_sim.engine.council import tally_votes
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.move import apply_move, enumerate_moves
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import (
    BuildingType,
    Terrain,
    Unit,
    UnitType,
    UNIT_STATS,
)
from aeonis_sim.engine.whispers import hand_over_limit

from .conftest import advance_to_action_phase


ROSTER = [
    "cassian", "seraphel", "vharok", "elyndra",
    "rakhis", "nyxara", "auriel", "thalrik",
]


def m4_state(players: int = 8):
    return build_initial_state(
        {
            "players": players,
            "lord_asymmetry": {"enabled": True, "lords": ROSTER[:players]},
        },
        random.Random(19),
    )


def test_m4_is_default_on_with_explicit_neutral_escape_hatch():
    game = Game({"players": 3}, seed=21)
    default = game.state
    neutral = build_initial_state(
        {"players": 3, "lord_asymmetry": {"enabled": False}},
        random.Random(21),
    )

    assert [p.lord_id for p in default.players] == ROSTER[:3]
    assert game.config["lord_asymmetry"]["lords"] == ROSTER[:3]
    assert [p.lord_id for p in neutral.players] == ["", "", ""]


def strip_map(state):
    for tile in state.tiles.values():
        tile.units = []
        tile.controller = None
        tile.buildings = []
    return state


def put(state, coord, owner, unit_type):
    unit = Unit(
        uid=state.new_uid(), owner=owner, type=unit_type,
        hp=UNIT_STATS[unit_type].hp,
    )
    state.tiles[coord].units.append(unit)
    return unit


def test_m4_setup_uses_sheet_resources_units_and_lord_hp():
    state = m4_state()
    cassian = state.player(0)
    vharok = state.player(2)
    rakhis = state.player(4)
    assert (cassian.gold, cassian.mana, cassian.influence) == (3, 2, 2)
    assert [u.type for u in state.tiles[vharok.home].units].count(UnitType.ARCHER) == 0
    assert [u.type for u in state.tiles[rakhis.home].units].count(UnitType.CAVALRY) == 1
    vharok_lord = next(
        u for u in state.tiles[vharok.home].units if u.type == UnitType.LORD
    )
    assert vharok_lord.hp == 4


def test_elyndra_deep_roots_is_one_ap_and_once_per_round():
    state = strip_map(m4_state(4))
    state.player(3).ap = 5
    coords = list(state.tiles)[:2]
    for coord in coords:
        state.tiles[coord].terrain = Terrain.FOREST
        state.tiles[coord].controller = 3
    put(state, coords[0], 3, UnitType.INFANTRY)
    root = next(m for m in enumerate_moves(state, 3) if m.get("root_network"))
    assert root["cost"] == 1
    apply_move(state, 3, root)
    assert not any(m.get("root_network") for m in enumerate_moves(state, 3))


def test_rakhis_desert_costs_one_without_zoc():
    """Sandstride Dial 3 keeps Desert = 1 AP; ZOC is normal."""
    state = strip_map(m4_state(5))
    origin, dest = (0, 0), (1, 0)
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[dest].terrain = Terrain.DESERT
    put(state, origin, 4, UnitType.INFANTRY)
    state.player(4).ap = 5
    move = next(m for m in enumerate_moves(state, 4) if tuple(m["dest"]) == dest)
    assert move["cost"] == 1


def test_rakhis_pays_normal_zoc_surcharge():
    """Dial 3 (2026-07-12): Sandstride no longer ignores enemy ZOC surcharges."""
    state = strip_map(m4_state(5))
    origin, dest, enemy = (0, 0), (1, 0), (2, -1)
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[dest].terrain = Terrain.DESERT
    state.tiles[enemy].terrain = Terrain.PLAINS
    put(state, origin, 4, UnitType.INFANTRY)
    put(state, enemy, 0, UnitType.INFANTRY)
    state.player(4).ap = 5
    move = next(m for m in enumerate_moves(state, 4) if tuple(m["dest"]) == dest)
    # Desert 1 + infantry ZOC surcharge 1
    assert move["cost"] == 2


def test_thalrik_can_use_enemy_controlled_portal():
    state = strip_map(m4_state())
    portals = [coord for coord, tile in state.tiles.items() if tile.terrain == Terrain.PORTAL]
    origin, dest = portals[:2]
    state.tiles[origin].controller = 7
    state.tiles[dest].controller = 0
    put(state, origin, 7, UnitType.INFANTRY)
    state.player(7).ap = 0
    moves = enumerate_moves(state, 7)
    assert any(tuple(m["dest"]) == dest and m["cost"] == 0 for m in moves)


def test_vharok_built_hex_becomes_larger_siege():
    state = strip_map(m4_state(4))
    origin, target = (0, 0), (1, 0)
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[target].terrain = Terrain.MOUNTAIN
    state.tiles[target].controller = 2
    state.tiles[target].buildings = [BuildingType.MINE]
    put(state, origin, 0, UnitType.INFANTRY)
    put(state, target, 2, UnitType.INFANTRY)
    state.player(0).ap = 5
    battle = combat.start_battle(
        state, 0, {"type": "attack", "target": list(target), "cost": 2},
    )
    assert battle.siege is True
    assert battle.cap == 3
    assert battle.whisper_mods.def_cap_bonus == 1


def test_nyxara_hand_limit_is_eight():
    state = m4_state()
    state.player(5).whisper_hand = [str(i) for i in range(8)]
    assert not hand_over_limit(state, 5)
    state.player(5).whisper_hand.append("ninth")
    assert hand_over_limit(state, 5)


def test_auriel_sanctify_doubles_her_votes():
    state = m4_state()
    state.player(6).renown = 5  # two Council Votes before sanctification
    ballots = [
        {"pid": 6, "support": True, "lobby": 0, "sanctify": True},
        {"pid": 0, "support": False, "lobby": 0},
        {"pid": 1, "support": False, "lobby": 0},
        {"pid": 2, "support": False, "lobby": 0},
    ]
    assert tally_votes(state, "realm_tax", ballots)


def test_seraphel_gets_optional_second_paid_research():
    g = Game(
        {
            "players": 3,
            "lord_asymmetry": {
                "enabled": True,
                "lords": ["seraphel", "cassian", "vharok"],
            },
        },
        seed=31,
    )
    advance_to_action_phase(g)
    g._initiative_queue = [0, 1, 2]
    g._pending = None
    g.state.player(0).ap = 10
    g.state.player(0).gold = 10
    g.state.player(0).mana = 10
    dp = g.next_decision()
    first = next(c for c in dp.choices if c["type"] == "research")
    g.submit(first)
    followup = g.next_decision()
    assert followup.kind == "research"
    assert any(c["type"] == "research_skip" for c in followup.choices)


def test_cassian_free_trade_does_not_rotate_his_turn():
    g = Game(
        {
            "players": 3,
            "lord_asymmetry": {
                "enabled": True,
                "lords": ["cassian", "seraphel", "vharok"],
            },
        },
        seed=37,
    )
    advance_to_action_phase(g)
    g._initiative_queue = [0, 1, 2]
    g._pending = None
    g.state.player(0).gold = 5
    g.state.player(1).mana = 5
    dp = g.next_decision()
    trade = next(c for c in dp.choices if c["type"] == "trade")
    before_ap = g.state.player(0).ap
    g.submit(trade)
    response = g.next_decision()
    g.submit(next(c for c in response.choices if c["type"] == "negotiation_reject"))
    assert g.state.player(0).ap == before_ap
    assert g.next_decision().pid == 0
