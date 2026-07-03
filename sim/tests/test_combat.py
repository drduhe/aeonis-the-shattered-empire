import random

from aeonis_sim.engine.combat import (
    enumerate_attacks, start_battle, resolve_round, finish_battle,
    enumerate_defender_retreats,
)
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import Terrain, Unit, UnitType, UNIT_STATS


class MaxRng:
    def randint(self, a, b):
        return b


class ScriptRng:
    def __init__(self, rolls):
        self.rolls = list(rolls)

    def randint(self, a, b):
        return self.rolls.pop(0) if self.rolls else b


def blank_state():
    s = build_initial_state({"players": 3}, random.Random(5))
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


def test_enumerate_attacks_needs_adjacency_and_2ap():
    s = blank_state()
    put(s, (0, 0), 0, UnitType.INFANTRY)
    put(s, (1, 0), 1, UnitType.INFANTRY)
    s.tiles[(1, 0)].controller = 1
    s.players[0].ap = 2
    atks = enumerate_attacks(s, 0)
    assert [tuple(a["target"]) for a in atks] == [(1, 0)]
    s.players[0].ap = 1
    assert enumerate_attacks(s, 0) == []


def test_battle_attacker_wipes_defender_and_occupies():
    s = blank_state()
    for _ in range(3):
        put(s, (0, 0), 0, UnitType.CAVALRY)   # d8 attack vs d6 defense
    put(s, (1, 0), 1, UnitType.INFANTRY)
    s.tiles[(1, 0)].controller = 1
    s.players[0].ap = 2
    b = start_battle(s, 0, {"type": "attack", "target": [1, 0], "cost": 2})
    assert s.players[0].ap == 0
    resolve_round(s, b, MaxRng())   # cav rolls 8 > inf defense 6 -> dead
    assert b.winner == "attacker"
    finish_battle(s, b)
    assert s.tiles[(1, 0)].controller == 0
    assert len(s.tiles[(1, 0)].units) == 3          # occupation up to cap 3
    assert s.players[0].battle_wins == 1


def test_archer_prestrike_kills_before_reply():
    s = blank_state()
    put(s, (0, 0), 0, UnitType.ARCHER)
    put(s, (1, 0), 1, UnitType.ARCHER)
    s.tiles[(1, 0)].controller = 1
    s.players[0].ap = 2
    b = start_battle(s, 0, {"type": "attack", "target": [1, 0], "cost": 2})
    resolve_round(s, b, MaxRng())   # att archer d6=6 > def archer d4=4, dies first
    assert b.winner == "attacker"


def test_lord_capture_awards_vp_and_renown():
    s = blank_state()
    for _ in range(3):
        put(s, (0, 0), 0, UnitType.CAVALRY)
    lord = put(s, (1, 0), 1, UnitType.LORD)  # 3 HP
    s.tiles[(1, 0)].controller = 1
    s.players[0].ap = 2
    b = start_battle(s, 0, {"type": "attack", "target": [1, 0], "cost": 2})
    # Each cavalry rolls 8, lord defense rolls 1 -> 3 damage total -> captured
    resolve_round(s, b, ScriptRng([8, 1, 8, 1, 8, 1]))
    assert s.players[0].vp == 1
    assert s.players[0].vp_sources["lord_capture"] == 1
    assert s.players[0].renown == 2
    assert s.players[1].lord_captured is True
    assert s.find_lord(1) is None
    assert b.winner == "attacker"


def test_city_battle_is_siege_and_marker_persists():
    s = blank_state()
    put(s, (0, 0), 0, UnitType.INFANTRY)
    put(s, (1, 0), 1, UnitType.INFANTRY)
    s.tiles[(1, 0)].terrain = Terrain.CITY
    s.tiles[(1, 0)].controller = 1
    s.players[0].ap = 2
    b = start_battle(s, 0, {"type": "attack", "target": [1, 0], "cost": 2})
    assert b.siege is True                     # AL-7: auto Hold the Walls
    resolve_round(s, b, ScriptRng([1, 6, 1, 6]))   # all misses, undecided
    assert b.winner is None
    finish_battle(s, b)
    assert s.tiles[(1, 0)].siege is True
    assert enumerate_defender_retreats(s, b) == []  # no retreat from Cities


def test_defender_retreat_options_on_standard_hex():
    s = blank_state()
    put(s, (0, 0), 0, UnitType.INFANTRY)
    put(s, (1, 0), 1, UnitType.INFANTRY)
    s.tiles[(1, 0)].controller = 1
    s.tiles[(2, 0)].controller = 1             # retreat destination
    s.players[0].ap = 2
    b = start_battle(s, 0, {"type": "attack", "target": [1, 0], "cost": 2})
    resolve_round(s, b, ScriptRng([1, 6, 1, 6]))
    dests = {tuple(r["dest"]) for r in enumerate_defender_retreats(s, b)}
    assert (2, 0) in dests
