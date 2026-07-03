from __future__ import annotations

import random

from .types import Terrain, Tile

DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
# Corners of ring 3 — home-city anchor positions.
CORNERS = [(3, 0), (3, -3), (0, -3), (-3, 0), (-3, 3), (0, 3)]


def neighbors(c):
    return [(c[0] + dq, c[1] + dr) for dq, dr in DIRS]


def distance(a, b) -> int:
    dq, dr = a[0] - b[0], a[1] - b[1]
    return max(abs(dq), abs(dr), abs(dq + dr))


def disk(radius: int):
    return [
        (q, r)
        for q in range(-radius, radius + 1)
        for r in range(-radius, radius + 1)
        if max(abs(q), abs(r), abs(q + r)) <= radius
    ]


def generate_map(num_players: int, rng: random.Random):
    """First_Playable_Packet.md §3.1 map for 3-4 players on a radius-3 disk.

    Returns (tiles: dict[Coord, Tile], homes: list[Coord]) with homes[pid] the
    player's home City coordinate.
    """
    if not 3 <= num_players <= 4:
        raise ValueError("Milestone 1 supports 3-4 players")
    coords = disk(3)
    in_disk = set(coords)
    tiles = {}
    used = set()

    tiles[(0, 0)] = Tile((0, 0), Terrain.CITY, imperial_seat=True)
    used.add((0, 0))

    anchor_idxs = [int(i * 6 / num_players) for i in range(num_players)]
    homes = []
    cluster_terrains = [Terrain.PLAINS, Terrain.FOREST, Terrain.MOUNTAIN]
    for idx in anchor_idxs:
        city = CORNERS[idx]
        homes.append(city)
        tiles[city] = Tile(city, Terrain.CITY)
        used.add(city)
        # The 3 cluster tiles: neighbors of the home City, preferring inward hexes
        # so every cluster touches the neutral ring (packet §3.1).
        cands = [n for n in neighbors(city) if n in in_disk and n not in used]
        cands.sort(key=lambda c: (distance(c, (0, 0)), c))
        for terrain, coord in zip(cluster_terrains, cands):
            tiles[coord] = Tile(coord, terrain)
            used.add(coord)

    remaining = [c for c in coords if c not in used]
    rng.shuffle(remaining)

    def place(terrain, n, constraint=None):
        placed = 0
        i = 0
        while placed < n and i < len(remaining):
            c = remaining[i]
            if constraint is None or constraint(c):
                remaining.pop(i)
                tiles[c] = Tile(c, terrain)
                placed += 1
            else:
                i += 1
        if placed < n:
            raise RuntimeError(f"could not place {n}x {terrain}")

    place(Terrain.RUINS, 2)
    place(Terrain.PORTAL, 1)
    portal1 = next(c for c, t in tiles.items() if t.terrain == Terrain.PORTAL)
    place(Terrain.PORTAL, 1, constraint=lambda c: distance(c, portal1) > 1)
    place(Terrain.LAKE, 2)
    # AL-3: deserts by shuffle, not "between each pair of home clusters".
    place(Terrain.DESERT, num_players)

    filler = [Terrain.PLAINS, Terrain.FOREST, Terrain.MOUNTAIN]
    for i, c in enumerate(remaining):
        tiles[c] = Tile(c, filler[i % 3])

    return tiles, homes
