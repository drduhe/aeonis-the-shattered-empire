import random

from aeonis_sim.engine.hexmap import neighbors, distance, disk, generate_map
from aeonis_sim.engine.types import Terrain, BuildingType


def test_axial_geometry():
    assert distance((0, 0), (3, -3)) == 3
    assert len(disk(3)) == 37
    assert len(neighbors((0, 0))) == 6
    assert (1, -1) in neighbors((0, 0))


def test_generate_map_4p_structure():
    rng = random.Random(42)
    tiles, homes = generate_map(4, rng)
    assert len(homes) == 4
    # Center is the Imperial Seat, a City (packet §3.1/§3.2)
    seat = tiles[(0, 0)]
    assert seat.terrain == Terrain.CITY and seat.imperial_seat
    # Each home cluster: 1 City + Plains + Forest + Mountain (packet §3.1)
    for home in homes:
        assert tiles[home].terrain == Terrain.CITY and not tiles[home].imperial_seat
    # Neutral ring contents: 2 Ruins, 2 Portals (non-adjacent), 2 Lakes, N deserts
    terrains = [t.terrain for t in tiles.values()]
    assert terrains.count(Terrain.RUINS) == 2
    assert terrains.count(Terrain.LAKE) == 2
    assert terrains.count(Terrain.DESERT) == 4
    portals = [c for c, t in tiles.items() if t.terrain == Terrain.PORTAL]
    assert len(portals) == 2
    assert distance(portals[0], portals[1]) > 1  # not adjacent
    # Whole disk is tiled
    assert len(tiles) == 37


def test_generate_map_is_seed_deterministic():
    t1, h1 = generate_map(3, random.Random(7))
    t2, h2 = generate_map(3, random.Random(7))
    assert h1 == h2
    assert {c: t.terrain for c, t in t1.items()} == {c: t.terrain for c, t in t2.items()}
