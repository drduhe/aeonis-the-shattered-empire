"""Artifact deck, sites, ownership, and VP relics (M3 Task 3)."""
from __future__ import annotations

import random

from aeonis_sim.engine.artifacts import (
    ARTIFACT_CARD_IDS,
    VP_ARTIFACTS,
    apply_purge_draw,
    apply_site_claim,
    discard_lord_equipment,
    gain_artifact,
    init_artifact_deck,
    place_site,
    transfer_lord_equipment,
)
from aeonis_sim.engine.cleanup import run_cleanup
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain
from aeonis_sim.engine.production import run_production


def test_artifact_deck_twenty_four():
    deck = init_artifact_deck(random.Random(0))
    assert len(deck) == 24
    assert set(deck) == set(ARTIFACT_CARD_IDS)


def test_purge_draw_costs_three_remnants():
    state = build_initial_state({"players": 3}, random.Random(1))
    p = state.player(0)
    p.remnants = 5
    state.artifact_deck = ["wellspring_chalice"]
    pending = apply_purge_draw(state, 0)
    assert p.remnants == 2
    assert "wellspring_chalice" in p.utilities
    assert pending is None


def test_lord_equipment_carry_limit():
    state = build_initial_state({"players": 3}, random.Random(2))
    p = state.player(0)
    pending = gain_artifact(state, 0, "blade_of_the_last_emperor")
    assert pending is None
    pending = gain_artifact(state, 0, "crown_of_aeonis")
    assert pending is None
    pending = gain_artifact(state, 0, "voidwalkers_cloak")
    assert pending == "discard_lord"
    assert len(p.lord_equipment) == 3
    discard_lord_equipment(state, 0, "voidwalkers_cloak")
    assert len(p.lord_equipment) == 2
    assert state.artifact_deck[0] == "voidwalkers_cloak"


def test_site_claim_grants_artifact():
    state = build_initial_state({"players": 3}, random.Random(3))
    tile = next(t for t in state.tiles.values() if t.controller == 0)
    state.artifact_deck = ["shard_of_the_throne"]
    place_site(state, tile.coord)
    key = f"{tile.coord[0]},{tile.coord[1]}"
    assert state.artifact_sites[key]["card_id"] == "shard_of_the_throne"
    pending = apply_site_claim(state, 0, tile.coord)
    assert key not in state.artifact_sites
    assert "shard_of_the_throne" in state.player(0).utilities
    assert pending is None


def test_building_relic_attach():
    state = build_initial_state({"players": 3}, random.Random(4))
    city = next(t for t in state.controlled(0) if t.terrain == Terrain.CITY)
    city.buildings.append(BuildingType.FORGE)
    pending = gain_artifact(state, 0, "eternal_forge")
    assert pending is None
    assert city.building_relic == "eternal_forge"


def test_vp_artifact_scores_once_on_gain_not_cleanup():
    state = build_initial_state({"players": 3}, random.Random(5))
    p = state.player(0)
    p.secret_objectives = []
    state.shared_public_revealed = []
    gain_artifact(state, 0, "crown_of_aeonis")
    assert p.vp == 1
    assert p.vp_sources.get("artifact") == 1
    run_cleanup(state)
    assert p.vp == 1
    run_cleanup(state)
    assert p.vp == 1


def test_vp_artifact_steal_awards_thief_once_cap_two_players():
    state = build_initial_state({"players": 3}, random.Random(6))
    gain_artifact(state, 0, "crown_of_aeonis")
    assert state.player(0).vp_sources.get("artifact") == 1
    pending = transfer_lord_equipment(state, 0, 1)
    assert pending is None
    assert state.player(1).vp_sources.get("artifact") == 1
    assert state.player(0).vp == 1  # permanence: no refund
    # Third holder does not score (cap 2 players per artifact).
    transfer_lord_equipment(state, 1, 2)
    assert state.player(2).vp_sources.get("artifact") is None
    assert "crown_of_aeonis" in state.player(2).lord_equipment


def test_lord_capture_transfers_equipment():
    state = build_initial_state({"players": 3}, random.Random(6))
    state.player(0).lord_equipment = ["blade_of_the_last_emperor", "crown_of_aeonis"]
    pending = transfer_lord_equipment(state, 0, 1)
    assert state.player(0).lord_equipment == []
    assert set(state.player(1).lord_equipment) == {
        "blade_of_the_last_emperor", "crown_of_aeonis",
    }
    assert pending is None


def test_utility_effect_wellspring_production():
    state = build_initial_state({"players": 3}, random.Random(7))
    p = state.player(0)
    for t in state.controlled(0):
        if t.coord != p.home:
            t.controller = None
    p.utilities.append("wellspring_chalice")
    before = p.gold
    run_production(state)
    assert p.gold == before + 2


def test_vp_artifacts_set():
    assert VP_ARTIFACTS == {
        "crown_of_aeonis",
        "eternal_forge",
        "shard_of_the_throne",
        "imperial_seal",
    }
