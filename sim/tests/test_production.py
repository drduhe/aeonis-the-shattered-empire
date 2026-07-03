import random

from aeonis_sim.engine.production import run_production
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain


def make_state():
    return build_initial_state({"players": 3}, random.Random(5))


def test_terrain_and_building_production():
    s = make_state()
    p = s.players[0]
    p.gold = p.mana = p.influence = 0
    # Home cluster: City + Plains + Forest + Mountain
    run_production(s)
    assert p.gold == 1       # mountain
    assert p.mana == 1       # forest
    assert p.influence == 0
    # Add a Mine: mountain now +3
    mountain = next(t for t in s.controlled(0) if t.terrain == Terrain.MOUNTAIN)
    mountain.buildings.append(BuildingType.MINE)
    p.gold = 0
    run_production(s)
    assert p.gold == 3


def test_population_growth():
    s = make_state()
    p = s.players[0]
    p.pop_pool = 0
    run_production(s)
    # growth = base 1 + plains 1 + city 2 = 4, cap allows it (used 4, cap 10)
    assert p.pop_pool == 4


def test_growth_capped():
    s = make_state()
    p = s.players[0]
    p.pop_pool = s.pop_cap(0) - s.pop_used(0)  # already full
    run_production(s)
    assert p.pop_pool == s.pop_cap(0) - s.pop_used(0)  # surplus lost


def test_castle_upkeep_suspension():
    s = make_state()
    p = s.players[0]
    home = s.tiles[p.home]
    home.buildings.append(BuildingType.CASTLE)
    # gold 0: production runs first (mountain +1), but 1 < 2 so upkeep
    # is still unpayable
    p.gold = 0
    run_production(s)
    assert home.castle_suspended is True   # AL-8
    p.gold = 5
    run_production(s)
    assert home.castle_suspended is False
    assert p.gold == 5 - 2 + 1  # paid upkeep, earned mountain gold
