"""Plan 2 AP economy toggles (PROPOSED; sim-only)."""
from __future__ import annotations

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.council import council_votes
from aeonis_sim.engine.lords.discoveries import bump_renown
from aeonis_sim.engine.production import _pay_upkeep
from aeonis_sim.engine.record import build_record
from aeonis_sim.engine.types import BuildingType, Terrain, effective_building_spec


def test_ap_bonus_cap_limits_city_and_guild_stacking():
    game = Game(
        {"players": 3, "ap_economy": {"ap_bonus_cap": 2}},
        seed=42,
    )
    s = game.state
    pid = 0
    controlled = s.controlled(pid)
    for tile in controlled[:3]:
        tile.terrain = Terrain.CITY
    controlled[0].buildings.append(BuildingType.GUILD_HALL)
    s.player(pid).renown = 6
    assert game._ap_bonus(pid) == 2


def test_rally_grants_lowest_vp_player_extra_ap():
    game = Game({"players": 3, "ap_economy": {"rally": True}}, seed=99)
    s = game.state
    s.player(1).vp = 0
    s.player(2).vp = 5
    s.player(0).vp = 10
    before = s.player(1).ap
    game._apply_rally()
    assert s.player(1).ap == before + 1


def test_ap_economy_stats_in_record():
    game = Game(
        {"players": 3, "ap_economy": {"ap_bonus_cap": 2, "rally": True}},
        seed=7,
    )
    game.action_count_log = [{0: 3, 1: 1, 2: 2}]
    game.pass_log = [{
        "round": 1, "pid": 0, "order": 1, "remaining_ap": 4,
        "banked_ap": 2, "stranded_ap": 2, "actions_before_pass": 3,
    }]
    game.build_counts[0] = 2
    rec = build_record(game)
    assert "ap_economy_stats" in rec
    assert "avg_spread" in rec["ap_economy_stats"]
    assert "max_spread" in rec["ap_economy_stats"]
    assert rec["ap_economy_stats"]["max_action_gap"] == 2
    assert rec["ap_economy_stats"]["actions_per_player_round"] == 2
    assert rec["ap_economy_stats"]["stranded_ap_per_player_round"] == 2 / 3
    assert rec["ap_economy_stats"]["builds_per_player_game"] == 2 / 3


def test_slim_renown_replaces_passive_ap_and_votes_with_once_only_rewards():
    game = Game({"players": 3, "bookkeeping": {"slim_renown": True}}, seed=15)
    state = game.state
    p = state.player(0)
    p.renown = 4
    before_hand = len(p.whisper_hand)
    before_influence = p.influence

    bump_renown(state, 0, 1, game.rng)

    assert p.renown_reward_5 is True
    assert p.influence == before_influence + 2
    assert len(p.whisper_hand) == before_hand + 2
    assert game._ap_bonus(0) == min(2, sum(
        1 for tile in state.controlled(0) if tile.terrain == Terrain.CITY
    ))
    assert council_votes(state, 0) == 1

    p.renown = 9
    before_vp = p.vp
    bump_renown(state, 0, 1, game.rng)
    bump_renown(state, 0, 1, game.rng)
    assert p.renown_reward_10 is True
    assert p.vp == before_vp + 1
    assert p.vp_sources["renown_milestone"] == 1


def test_no_building_upkeep_uses_upfront_costs_and_skips_payments():
    game = Game(
        {"players": 3, "bookkeeping": {"building_upkeep": False}},
        seed=17,
    )
    state = game.state
    p = state.player(0)
    home = state.tiles[p.home]
    home.buildings = [BuildingType.FORGE, BuildingType.CASTLE]
    p.gold = 20
    p.mana = 5

    stats = _pay_upkeep(state, p)

    assert stats["checks"] == 0
    assert (p.gold, p.mana) == (20, 5)
    assert home.active(BuildingType.FORGE)
    assert home.active(BuildingType.CASTLE)
    assert effective_building_spec(state, BuildingType.FORGE).gold == 6
    assert effective_building_spec(state, BuildingType.FORGE).mana == 1
    assert effective_building_spec(state, BuildingType.ACADEMY).mana == 4
    assert effective_building_spec(state, BuildingType.CASTLE).gold == 8
    assert effective_building_spec(state, BuildingType.IRON_CITADEL).gold == 10
