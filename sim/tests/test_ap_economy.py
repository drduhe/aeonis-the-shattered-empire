"""Plan 2 AP economy toggles (PROPOSED; sim-only)."""
from __future__ import annotations

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.record import build_record
from aeonis_sim.engine.types import BuildingType, Terrain


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
    rec = build_record(game)
    assert "ap_economy_stats" in rec
    assert "avg_spread" in rec["ap_economy_stats"]
    assert "max_spread" in rec["ap_economy_stats"]
