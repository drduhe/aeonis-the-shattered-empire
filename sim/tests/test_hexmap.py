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


def test_deserts_between_adjacent_home_pairs():
    rng = random.Random(42)
    tiles, homes = generate_map(4, rng)
    from aeonis_sim.engine.hexmap import _hex_angle
    ordered = sorted(homes, key=_hex_angle)
    deserts = [c for c, t in tiles.items() if t.terrain == Terrain.DESERT]
    assert len(deserts) == 4
    for d in deserts:
        assert all(distance(d, h) > 1 for h in homes)
    assigned = set()
    for i in range(4):
        h1, h2 = ordered[i], ordered[(i + 1) % 4]
        slot = min(
            (c for c in deserts if c not in assigned),
            key=lambda c: (distance(c, h1) + distance(c, h2), c),
        )
        assigned.add(slot)
    assert len(assigned) == 4


def test_generate_map_is_seed_deterministic():
    t1, h1 = generate_map(3, random.Random(7))
    t2, h2 = generate_map(3, random.Random(7))
    assert h1 == h2
    assert {c: t.terrain for c, t in t1.items()} == {c: t.terrain for c, t in t2.items()}


def test_generate_map_6p_and_8p_structure():
    for n, radius, ruins, portals, lakes in (
        (6, 4, 3, 2, 2),
        (8, 5, 4, 3, 3),
    ):
        rng = random.Random(99)
        tiles, homes = generate_map(n, rng)
        assert len(homes) == n
        assert len(tiles) == len(disk(radius))
        seat = tiles[(0, 0)]
        assert seat.imperial_seat
        terrains = [t.terrain for t in tiles.values()]
        assert terrains.count(Terrain.RUINS) == ruins
        assert terrains.count(Terrain.PORTAL) == portals
        assert terrains.count(Terrain.LAKE) == lakes
        assert terrains.count(Terrain.DESERT) == n
        portal_coords = [c for c, t in tiles.items() if t.terrain == Terrain.PORTAL]
        for i, a in enumerate(portal_coords):
            for b in portal_coords[i + 1:]:
                assert distance(a, b) > 1
        for home in homes:
            assert tiles[home].terrain == Terrain.CITY
