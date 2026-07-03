from aeonis_sim.engine.types import (
    Terrain, UnitType, BuildingType, UNIT_STATS, BUILDING_SPECS,
    Unit, Tile, PlayerState, GameState, POP_BASE, VP_THRESHOLD,
)


def test_unit_stats_match_canon():
    # Combat.md §2 + Actions.md recruit table
    inf = UNIT_STATS[UnitType.INFANTRY]
    assert (inf.attack_die, inf.defense_die, inf.hp, inf.move, inf.pop, inf.gold, inf.mana) == (6, 6, 1, 1, 1, 1, 0)
    cav = UNIT_STATS[UnitType.CAVALRY]
    assert (cav.attack_die, cav.defense_die, cav.hp, cav.move, cav.pop, cav.gold) == (8, 6, 2, 2, 2, 2)
    arc = UNIT_STATS[UnitType.ARCHER]
    assert (arc.attack_die, arc.defense_die, arc.hp, arc.mana) == (6, 4, 1, 1)
    lord = UNIT_STATS[UnitType.LORD]  # Milestone-1 generic Lord
    assert (lord.attack_die, lord.defense_die, lord.hp, lord.move, lord.pop) == (8, 8, 3, 2, 0)


def test_building_specs_match_canon():
    farm = BUILDING_SPECS[BuildingType.FARM]
    assert farm.terrain == Terrain.PLAINS and farm.gold == 2 and farm.pop == 1
    fortress = BUILDING_SPECS[BuildingType.FORTRESS]
    assert fortress.gold == 5 and fortress.mana == 2 and fortress.pop == 2
    castle = BUILDING_SPECS[BuildingType.CASTLE]
    assert castle.terrain == Terrain.CITY and castle.upkeep_gold == 2


def test_state_round_trips_through_dict():
    u = Unit(uid=1, owner=0, type=UnitType.CAVALRY, hp=2)
    t = Tile(coord=(1, -1), terrain=Terrain.CITY, imperial_seat=True,
             controller=0, units=[u], buildings=[BuildingType.CASTLE])
    p = PlayerState(pid=0, home=(1, -1))
    s = GameState(players=[p], tiles={(1, -1): t}, round=3)
    s2 = GameState.from_dict(s.to_dict())
    assert s2.tiles[(1, -1)].units[0].type == UnitType.CAVALRY
    assert s2.tiles[(1, -1)].imperial_seat is True
    assert s2.players[0].home == (1, -1)
    assert s2.round == 3
    assert s.to_dict() == s2.to_dict()


def test_state_copy_matches_dict_round_trip():
    u = Unit(uid=1, owner=0, type=UnitType.CAVALRY, hp=2)
    t = Tile(coord=(1, -1), terrain=Terrain.CITY, imperial_seat=True,
             controller=0, units=[u], buildings=[BuildingType.CASTLE])
    p = PlayerState(pid=0, home=(1, -1))
    s = GameState(players=[p], tiles={(1, -1): t}, round=3)
    assert s.copy().to_dict() == s.to_dict()


def test_derived_pop_and_constants():
    assert POP_BASE == 7 and VP_THRESHOLD == 10
