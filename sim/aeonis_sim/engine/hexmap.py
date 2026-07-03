from __future__ import annotations

import math
import random

from .types import Terrain, Tile

DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
# Corners of ring 3 — home-city anchor positions for 3-4 players.
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


def _map_radius(num_players: int) -> int:
    """Disk radius scaled to player count (First_Playable_Packet.md §3.1)."""
    if num_players <= 4:
        return 3
    if num_players <= 6:
        return 4
    return 5


def _outer_ring(radius: int) -> list:
    return sorted(
        [c for c in disk(radius) if distance(c, (0, 0)) == radius],
        key=lambda c: (c[1], c[0]),
    )


def _home_anchors(num_players: int, radius: int) -> list:
    if num_players <= 4:
        return [CORNERS[int(i * 6 / num_players)] for i in range(num_players)]
    ring = _outer_ring(radius)
    return [ring[int(i * len(ring) / num_players)] for i in range(num_players)]


def _neutral_counts(num_players: int) -> dict:
    if num_players <= 4:
        return {"ruins": 2, "portals": 2, "lakes": 2, "deserts": num_players}
    return {
        "ruins": (num_players + 1) // 2,
        "portals": max(2, math.ceil(num_players / 3)),
        "lakes": max(2, math.ceil(num_players / 3)),
        "deserts": num_players,
    }


def generate_map(num_players: int, rng: random.Random):
    """First_Playable_Packet.md §3.1 map for 3-8 players.

    Returns (tiles: dict[Coord, Tile], homes: list[Coord]) with homes[pid] the
    player's home City coordinate.
    """
    if not 3 <= num_players <= 8:
        raise ValueError("Milestone 1 supports 3-8 players")
    radius = _map_radius(num_players)
    coords = disk(radius)
    in_disk = set(coords)
    tiles = {}
    used = set()

    tiles[(0, 0)] = Tile((0, 0), Terrain.CITY, imperial_seat=True)
    used.add((0, 0))

    homes = []
    cluster_terrains = [Terrain.PLAINS, Terrain.FOREST, Terrain.MOUNTAIN]
    for city in _home_anchors(num_players, radius):
        homes.append(city)
        tiles[city] = Tile(city, Terrain.CITY)
        used.add(city)
        cands = [n for n in neighbors(city) if n in in_disk and n not in used]
        cands.sort(key=lambda c: (distance(c, (0, 0)), c))
        for terrain, coord in zip(cluster_terrains, cands):
            tiles[coord] = Tile(coord, terrain)
            used.add(coord)

    remaining = [c for c in coords if c not in used]
    rng.shuffle(remaining)
    counts = _neutral_counts(num_players)

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

    place(Terrain.RUINS, counts["ruins"])
    place(Terrain.PORTAL, 1)
    while sum(1 for t in tiles.values() if t.terrain == Terrain.PORTAL) < counts["portals"]:
        existing = tuple(c for c, t in tiles.items() if t.terrain == Terrain.PORTAL)
        place(
            Terrain.PORTAL,
            1,
            constraint=lambda c, ps=existing: all(distance(c, p) > 1 for p in ps),
        )
    place(Terrain.LAKE, counts["lakes"])
    # AL-3: deserts by shuffle, not "between each pair of home clusters".
    place(Terrain.DESERT, counts["deserts"])

    filler = [Terrain.PLAINS, Terrain.FOREST, Terrain.MOUNTAIN]
    for i, c in enumerate(remaining):
        tiles[c] = Tile(c, filler[i % 3])

    return tiles, homes
