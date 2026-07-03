"""Stratified combat metrics (initiation quality, retreats, uncontested)."""
from __future__ import annotations

from aeonis_sim.engine.combat import (
    empty_stratified_stats,
    record_battle_outcome,
    resolve_round,
    start_battle,
)
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import Terrain, Unit, UnitType, UNIT_STATS
from aeonis_sim.reports.summary import (
    format_stratified_combat_section,
    stratified_combat_metrics,
)


class MaxRng:
    def randint(self, a, b):
        return b


def blank_state():
    s = build_initial_state({"players": 3}, __import__("random").Random(5))
    for t in s.tiles.values():
        t.units = []
        t.controller = None
        t.terrain = Terrain.PLAINS
        t.imperial_seat = False
        t.buildings = []
    return s


def put(s, coord, owner, utype):
    u = Unit(uid=s.new_uid(), owner=owner, type=utype, hp=UNIT_STATS[utype].hp)
    s.tiles[coord].units.append(u)
    return u


def test_snapshot_marks_uncontested_when_no_defender_units():
    s = blank_state()
    put(s, (0, 0), 0, UnitType.INFANTRY)
    s.tiles[(1, 0)].controller = 1
    s.players[0].ap = 2
    b = start_battle(s, 0, {"type": "attack", "target": [1, 0], "cost": 2})
    assert b.uncontested is True
    assert b.init_def_dice == 0


def test_record_uncontested_capture_excluded_from_contested_buckets():
    stats = {"battles": 0, "attacker_wins": 0, "defender_wins": 0}
    b = type("B", (), {
        "def_retreated": False,
        "winner": "attacker",
        "uncontested": True,
        "init_att_dice": 6,
        "init_def_dice": 0,
    })()
    record_battle_outcome(stats, b)
    st = stats["stratified"]
    assert st["uncontested_captures"] == 1
    assert st["contested_gte1_battles"] == 0
    assert stats["battles"] == 1


def test_record_contested_buckets_by_die_ratio():
    stats = {"battles": 0, "attacker_wins": 0, "defender_wins": 0}

    favorable = type("B", (), {
        "def_retreated": False,
        "winner": "attacker",
        "uncontested": False,
        "init_att_dice": 12,
        "init_def_dice": 6,
    })()
    underdog = type("B", (), {
        "def_retreated": False,
        "winner": "defender",
        "uncontested": False,
        "init_att_dice": 6,
        "init_def_dice": 12,
    })()
    record_battle_outcome(stats, favorable)
    record_battle_outcome(stats, underdog)
    st = stats["stratified"]
    assert st["contested_gte1_battles"] == 1
    assert st["contested_gte1_att_wins"] == 1
    assert st["contested_lt1_battles"] == 1
    assert st["contested_lt1_def_wins"] == 1


def test_record_retreat_tracked_separately():
    stats = {"battles": 0, "attacker_wins": 0, "defender_wins": 0}
    b = type("B", (), {
        "def_retreated": True,
        "winner": None,
        "uncontested": False,
        "init_att_dice": 6,
        "init_def_dice": 6,
    })()
    record_battle_outcome(stats, b)
    assert stats["stratified"]["retreats"] == 1
    assert stats["battles"] == 0


def test_contested_fight_integration():
    s = blank_state()
    for _ in range(3):
        put(s, (0, 0), 0, UnitType.CAVALRY)
    put(s, (1, 0), 1, UnitType.INFANTRY)
    s.tiles[(1, 0)].controller = 1
    s.players[0].ap = 2
    b = start_battle(s, 0, {"type": "attack", "target": [1, 0], "cost": 2})
    assert b.uncontested is False
    assert b.init_att_dice > b.init_def_dice
    resolve_round(s, b, MaxRng())
    stats = {"battles": 0, "attacker_wins": 0, "defender_wins": 0}
    record_battle_outcome(stats, b)
    assert stats["stratified"]["contested_gte1_battles"] == 1


def test_summary_aggregates_stratified_from_records():
    records = [
        {
            "verdict": "completed",
            "config": {"players": 4},
            "rounds": 5,
            "combat_stats": {
                "battles": 3,
                "attacker_wins": 3,
                "defender_wins": 0,
                "stratified": {
                    **empty_stratified_stats(),
                    "uncontested_captures": 1,
                    "contested_gte1_battles": 2,
                    "contested_gte1_att_wins": 2,
                },
            },
        }
    ]
    scm = stratified_combat_metrics(records)
    assert scm["uncontested_captures"] == 1
    assert scm["contested_battles"] == 2
    assert scm["contested_attacker_win_rate"] == 1.0
    lines = format_stratified_combat_section(records)
    assert any("Ratio ≥ 1.0" in line for line in lines)
    assert any("Uncontested captures: 1" in line for line in lines)
