import random

from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.objectives import (
    PUBLIC_OBJECTIVES,
    PUBLIC_OBJECTIVE_IDS,
    SECRET_OBJECTIVES,
    draw_public_to_row,
    record_public_progress,
)
from aeonis_sim.engine.types import BuildingType, UnitType


def make_state(players=4, seed=1):
    return build_initial_state(
        {"players": players, "lord_asymmetry": {"enabled": False}},
        random.Random(seed),
    )


def test_starting_resources_and_tracks():
    s = make_state()
    for p in s.players:
        assert p.ap == 5 and p.gold == 2 and p.mana == 2 and p.influence == 1
        assert p.renown == 0 and p.vp == 0
        assert p.pop_pool == 6
        assert s.pop_cap(p.pid) == 10
        assert s.pop_used(p.pid) == 4


def test_starting_units_and_control():
    s = make_state()
    for p in s.players:
        home = s.tiles[p.home]
        types = sorted(u.type.value for u in home.units)
        assert types == ["archer", "infantry", "infantry", "infantry", "lord"]
        assert home.controller == p.pid
        assert len(s.controlled(p.pid)) == 4


def test_staged_economy_opening_from_objectives_config():
    s = build_initial_state(
        {"players": 4, "objectives": {"staged_economy_opening": True}},
        random.Random(99),
    )
    assert set(s.shared_public_revealed) == {"builder", "merchant_lord"}
    assert len(s.shared_public_deck) == 4
    assert not {"builder", "merchant_lord"} & set(s.shared_public_deck)


def test_shared_public_row_and_secrets():
    s = make_state()
    assert len(s.shared_public_revealed) == 2
    assert all(o in PUBLIC_OBJECTIVES for o in s.shared_public_revealed)
    secrets = [p.secret_objectives[0] for p in s.players if p.secret_objectives]
    assert all(o in SECRET_OBJECTIVES for o in secrets)


def test_full_public_deck_has_twelve_cards_per_stage():
    s = build_initial_state(
        {"players": 4, "objectives": {"full_public_deck": True}},
        random.Random(44),
    )
    assert len(PUBLIC_OBJECTIVE_IDS) == 24
    assert len(s.shared_public_revealed) == 2
    assert len(s.shared_public_deck) == 10
    assert len(s.shared_public_stage_two) == 12


def test_stage_two_merges_at_round_four():
    s = build_initial_state(
        {
            "players": 4,
            "objectives": {
                "full_public_deck": True,
                "exclude_public_ids": ["archmage"],
            },
        },
        random.Random(45),
    )
    s.round = 3
    assert draw_public_to_row(s, random.Random(1), round_start=True)
    assert s.shared_public_stage_two
    s.round = 4
    assert draw_public_to_row(s, random.Random(2), round_start=True)
    assert not s.shared_public_stage_two


def test_public_progress_starts_only_after_reveal():
    s = make_state()
    s.shared_public_revealed = []
    record_public_progress(s, 0, "warlord")
    assert s.player(0).public_objective_progress == {}
    s.shared_public_revealed = ["warlord"]
    record_public_progress(s, 0, "warlord")
    assert s.player(0).public_objective_progress["warlord"] == 1


def test_prosperous_realm_requires_buildings_and_population_cap():
    s = make_state()
    home = s.tiles[s.player(0).home]
    home.buildings = [
        BuildingType.FARM,
        BuildingType.MARKET,
        BuildingType.BANK,
        BuildingType.ACADEMY,
        BuildingType.FORGE,
    ]
    assert s.pop_cap(0) >= 12
    assert PUBLIC_OBJECTIVES["prosperous_realm"](s, 0)
