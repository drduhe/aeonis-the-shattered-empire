"""Arcane Tier I research (M3 Task 4)."""
from __future__ import annotations

import random

from aeonis_sim.engine.arcane import (
    TIER_I_DISCOVERY_IDS,
    apply_boundary_stones,
    apply_research,
    build_gold_cost,
    enumerate_research,
    production_golden_alchemy,
    research_resource_cost,
)
from aeonis_sim.engine.build import apply_build, enumerate_builds
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.move import apply_move, enumerate_moves
from aeonis_sim.engine.production import run_production
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain
from tests.conftest import advance_to_action_phase


def test_tier_i_ten_discoveries():
    assert len(TIER_I_DISCOVERY_IDS) == 10


def test_research_costs_ap_mana_and_grants_remnant():
    state = build_initial_state({"players": 3}, random.Random(1))
    p = state.player(0)
    p.ap = 3
    p.mana = 5
    before_r = p.remnants
    apply_research(state, 0, "golden_alchemy")
    assert "golden_alchemy" in p.discoveries
    assert p.ap == 2
    assert p.mana == 3
    assert p.remnants == before_r + 1


def test_academy_discount_once_per_round():
    state = build_initial_state({"players": 3}, random.Random(2))
    city = next(t for t in state.controlled(0) if t.terrain == Terrain.CITY)
    city.buildings.append(BuildingType.ACADEMY)
    p = state.player(0)
    p.ap = 5
    p.mana = 5
    p.gold = 5
    apply_research(state, 0, "battle_runes")
    assert p.mana == 4  # 2 cost - 1 academy discount
    assert p.arcane_round.get("academy_discount")
    p.ap = 5
    p.mana = 5
    apply_research(state, 0, "searing_salvo")
    assert p.mana == 3  # no second discount


def test_free_research_zero_cost():
    state = build_initial_state({"players": 3}, random.Random(3))
    p = state.player(0)
    p.ap = 1
    p.mana = 0
    apply_research(state, 0, "waystones", free=True, ap_waived=True)
    assert p.ap == 1
    assert "waystones" in p.discoveries


def test_sigiled_masonry_build_discount():
    state = build_initial_state({"players": 3}, random.Random(4))
    p = state.player(0)
    p.discoveries.append("sigiled_masonry")
    p.ap = 10
    p.gold = 10
    p.mana = 10
    p.pop_pool = 10
    spec = __import__("aeonis_sim.engine.types", fromlist=["BUILDING_SPECS"]).BUILDING_SPECS[
        BuildingType.FARM
    ]
    assert build_gold_cost(state, 0, BuildingType.FARM, spec.gold) == max(0, spec.gold - 1)


def test_golden_alchemy_production():
    state = build_initial_state({"players": 3}, random.Random(5))
    p = state.player(0)
    for t in state.controlled(0):
        if t.coord != p.home:
            t.controller = None
    p.discoveries.append("golden_alchemy")
    p.mana = 4
    before = p.gold
    run_production(state)
    assert p.gold == before + 3
    assert p.mana == 2


def test_waystones_move_discount():
    state = build_initial_state({"players": 3}, random.Random(6))
    p = state.player(0)
    p.discoveries.append("waystones")
    p.ap = 5
    moves = enumerate_moves(state, 0)
    if moves:
        m = moves[0]
        if m["cost"] > 1:
            apply_move(state, 0, m)
            assert p.arcane_round.get("waystones")


def test_boundary_stones_claims_neutral():
    state = build_initial_state({"players": 3}, random.Random(7))
    p = state.player(0)
    p.discoveries.append("boundary_stones")
    from aeonis_sim.engine.hexmap import neighbors
    city = next(t for t in state.controlled(0) if t.terrain == Terrain.CITY)
    for nb in neighbors(city.coord):
        tile = state.tiles.get(nb)
        if tile and tile.controller is None and not tile.imperial_seat:
            assert apply_boundary_stones(state, 0)
            assert tile.controller == 0
            return


def test_arcane_ascendancy_primary_queues_research():
    g = Game({"players": 3}, seed=42)
    dp = advance_to_action_phase(g)
    pid = dp.pid
    g.state.player(pid).held_cards = ["arcane_ascendancy"]
    g.state.player(pid).ap = 5
    g.state.player(pid).mana = 0
    g.state.player(pid).discoveries = []
    g.submit({"type": "strategy_primary", "card": "arcane_ascendancy", "cost": 1})
    rdp = g.next_decision()
    assert rdp is not None and rdp.kind == "research"
    assert rdp.context.get("free") is True
    g.submit(rdp.choices[0])
    assert len(g.state.player(pid).discoveries) == 1


def test_enumerate_research_excludes_owned():
    state = build_initial_state({"players": 3}, random.Random(8))
    state.player(0).discoveries.append("stonewright")
    opts = enumerate_research(state, 0)
    assert all(c["discovery"] != "stonewright" for c in opts)
