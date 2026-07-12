"""M4 faction discoveries: catalog + Research merge."""
from __future__ import annotations

import random

import pytest

from aeonis_sim.engine.arcane import apply_research, enumerate_research
from aeonis_sim.engine.lords import FACTION_DISCOVERIES, FACTION_DISCOVERY_IDS
from aeonis_sim.engine.setup import build_initial_state


def _m4(lords: list[str], *, seed: int = 2):
    """Pad to a legal 3-player map while keeping the requested lord order."""
    pad = ["vharok", "elyndra", "rakhis"]
    roster = list(lords)
    for lord in pad:
        if len(roster) >= 3:
            break
        if lord not in roster:
            roster.append(lord)
    while len(roster) < 3:
        roster.append("nyxara")
    return build_initial_state(
        {"players": len(roster), "lord_asymmetry": {"enabled": True, "lords": roster}},
        random.Random(seed),
    )


def test_sixteen_faction_discoveries_registered():
    assert len(FACTION_DISCOVERY_IDS) == 16
    assert len(FACTION_DISCOVERIES) == 16
    assert set(FACTION_DISCOVERY_IDS) == set(FACTION_DISCOVERIES)


def test_cassian_can_research_guild_contracts():
    from aeonis_sim.engine.arcane import enumerate_research, apply_research
    state = build_initial_state(
        {"players": 3, "lord_asymmetry": {"enabled": True, "lords": ["cassian", "vharok", "elyndra"]}},
        random.Random(2),
    )
    p = state.player(0)
    p.ap, p.gold, p.influence = 5, 10, 10
    choices = enumerate_research(state, 0)
    assert any(c["discovery"] == "guild_contracts" for c in choices)
    apply_research(state, 0, "guild_contracts")
    assert "guild_contracts" in p.discoveries
    assert p.remnants >= 1


def test_non_cassian_does_not_see_guild_contracts():
    state = _m4(["seraphel", "cassian"], seed=3)
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence = 5, 10, 10, 10
    choices = enumerate_research(state, 0)
    assert not any(c["discovery"] == "guild_contracts" for c in choices)
    assert any(c["discovery"] == "mana_nexus" for c in choices)


def test_wrong_lord_cannot_research_guild_contracts():
    state = _m4(["vharok"], seed=4)
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence = 5, 10, 10, 10
    with pytest.raises(ValueError, match="wrong lord"):
        apply_research(state, 0, "guild_contracts")
    assert "guild_contracts" not in p.discoveries


def test_owned_faction_discovery_excluded_from_enumerate():
    state = _m4(["cassian"], seed=5)
    p = state.player(0)
    p.ap, p.gold, p.influence = 5, 10, 10
    p.discoveries.append("guild_contracts")
    choices = enumerate_research(state, 0)
    assert not any(c["discovery"] == "guild_contracts" for c in choices)
    assert any(c["discovery"] == "diplomatic_tariffs" for c in choices)


def test_guild_contracts_charges_costs_ap_gold_influence():
    state = _m4(["cassian"], seed=6)
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence = 5, 10, 7, 10
    before_remnants = p.remnants
    apply_research(state, 0, "guild_contracts")
    assert p.ap == 4
    assert p.gold == 8
    assert p.influence == 8
    assert p.mana == 7  # faction research does not spend mana for guild_contracts
    assert p.remnants == before_remnants + 1
    assert p.discoveries.count("guild_contracts") == 1


def test_m4_off_excludes_faction_discoveries():
    state = build_initial_state({"players": 3}, random.Random(7))
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence = 5, 10, 10, 10
    choices = enumerate_research(state, 0)
    assert not any(c["discovery"] in FACTION_DISCOVERIES for c in choices)
