"""M3 Task 1 — Forge, Academy, Bank, Market (Buildings.md)."""
from __future__ import annotations

import random

from aeonis_sim.engine.build import apply_build, enumerate_builds
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.production import _bank_conversion, _pay_upkeep
from aeonis_sim.engine.recruit import apply_recruit, enumerate_recruits
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BUILDING_SPECS, BuildingType, Terrain

from .conftest import advance_to_action_phase


def make_state():
    s = build_initial_state({"players": 3}, random.Random(5))
    p = s.players[0]
    p.gold = 20
    p.mana = 20
    p.influence = 20
    p.ap = 5
    return s


def _build_on_home(s, pid: int, btype: BuildingType) -> None:
    choice = next(
        b for b in enumerate_builds(s, pid)
        if tuple(b["hex"]) == s.player(pid).home and b["building"] == btype.value
    )
    apply_build(s, pid, choice)


def test_advanced_buildings_city_only():
    s = make_state()
    opts = {(tuple(b["hex"]), b["building"]) for b in enumerate_builds(s, 0)}
    home = s.players[0].home
    plains = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.PLAINS)
    for b in ("forge", "academy", "bank", "market"):
        assert (home, b) in opts
        assert (plains, b) not in opts


def test_building_specs_match_canon():
    forge = BUILDING_SPECS[BuildingType.FORGE]
    assert forge.terrain == Terrain.CITY and forge.gold == 6 and forge.mana == 1
    assert forge.upkeep_mana == 0
    academy = BUILDING_SPECS[BuildingType.ACADEMY]
    assert academy.gold == 4 and academy.mana == 4 and academy.pop == 2
    bank = BUILDING_SPECS[BuildingType.BANK]
    assert bank.gold == 5 and bank.upkeep_mana == 0
    market = BUILDING_SPECS[BuildingType.MARKET]
    assert market.gold == 2 and market.influence == 2


def test_forge_allows_third_unit_and_discount():
    s = make_state()
    _build_on_home(s, 0, BuildingType.FORGE)
    home = s.tiles[s.players[0].home]
    assert home.active(BuildingType.FORGE)
    recs = enumerate_recruits(s, 0)
    triple = [r for r in recs if len(r["units"]) == 3]
    assert triple
    p = s.players[0]
    p.gold = 10
    p.mana = 10
    p.pop_pool = 10
    rec = next(r for r in recs if sorted(r["units"]) == ["infantry", "infantry", "infantry"])
    apply_recruit(s, 0, rec)
    # Forge: 3 infantry at 1g each (min 1, -1 discount from 1 -> still 1)
    assert p.gold == 7


def test_legacy_forge_upkeep_toggle_suspends_without_mana():
    s = make_state()
    s.building_upkeep = True
    _build_on_home(s, 0, BuildingType.FORGE)
    p = s.players[0]
    p.mana = 0
    _pay_upkeep(s, p)
    home = s.tiles[p.home]
    assert "forge" in home.suspended
    assert not home.active(BuildingType.FORGE)
    assert not any(len(r["units"]) == 3 for r in enumerate_recruits(s, 0))


def test_bank_converts_surplus_mana_to_gold():
    s = make_state()
    _build_on_home(s, 0, BuildingType.BANK)
    p = s.players[0]
    p.gold = 0
    p.mana = 4
    assert _bank_conversion(s, p) == "mana_to_gold"
    assert p.mana == 2 and p.gold == 3


def test_market_trade_costs_zero_ap():
    g = Game({"players": 3}, seed=204)
    advance_to_action_phase(g)
    pid = 0
    home = g.state.players[pid].home
    g.state.tiles[home].buildings.append(BuildingType.MARKET)
    g.state.player(pid).ap = 5
    dp = g.next_decision()
    while dp is not None and dp.pid != pid:
        g.submit(dp.choices[0])
        dp = g.next_decision()
    assert dp is not None and dp.kind == "action"
    trade = next(c for c in dp.choices if c["type"] == "trade")
    before = g.state.player(pid).ap
    g.submit(trade)
    dp2 = g.next_decision()
    assert dp2 is not None and dp2.kind == "negotiation"
    g.submit({"type": "negotiation_accept"})
    assert g.state.player(pid).ap == before
    assert g.building_stats["market_trades"] == 1
