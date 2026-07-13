"""Validate First Playable map generation against Plan 4 geometry gates."""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.engine.hexmap import distance, generate_map  # noqa: E402
from aeonis_sim.engine.production import tile_printed_production  # noqa: E402
from aeonis_sim.engine.setup import build_initial_state  # noqa: E402
from aeonis_sim.engine.types import Terrain  # noqa: E402


SEEDS = 200
SPECIAL = {Terrain.RUINS, Terrain.PORTAL}
CONTESTED = {Terrain.DESERT, Terrain.RUINS, Terrain.PORTAL, Terrain.LAKE}


def _pairwise_min(homes: list[tuple]) -> int:
    return min(
        distance(a, b)
        for i, a in enumerate(homes)
        for b in homes[i + 1 :]
    )


def _production_total(state, pid: int) -> int:
    return sum(
        sum(tile_printed_production(t).values())
        for t in state.controlled(pid)
    )


def audit_count(players: int) -> dict:
    failures = Counter()
    min_home_distance = 99
    max_home_to_ring = 0
    min_special_coverage = 1.0
    max_production_spread = 0
    min_tiles_per_player = 99.0
    contested_counts = Counter()
    terrain_inventory = Counter()
    homes_example = None
    for seed in range(SEEDS):
        tiles, homes = generate_map(players, random.Random(seed))
        homes_example = homes_example or homes
        pair_min = _pairwise_min(homes)
        min_home_distance = min(min_home_distance, pair_min)
        if pair_min < 4:
            failures["home_distance"] += 1

        home_to_ring = max(max(0, distance(h, (0, 0)) - 1) for h in homes)
        max_home_to_ring = max(max_home_to_ring, home_to_ring)
        if home_to_ring > 4:
            failures["seat_ring_distance"] += 1

        covered = sum(
            1 for h in homes
            if any(t.terrain in SPECIAL and distance(h, t.coord) <= 2 for t in tiles.values())
        )
        coverage = covered / players
        min_special_coverage = min(min_special_coverage, coverage)
        if coverage < 1.0:
            failures["special_access"] += 1

        state = build_initial_state({"players": players}, random.Random(seed))
        totals = [_production_total(state, pid) for pid in range(players)]
        spread = max(totals) - min(totals)
        max_production_spread = max(max_production_spread, spread)
        if spread > 1:
            failures["production_spread"] += 1

        min_tiles_per_player = min(min_tiles_per_player, len(tiles) / players)
        contested_counts[sum(1 for t in tiles.values() if t.terrain in CONTESTED)] += 1
        if seed == 0:
            terrain_inventory.update(t.terrain.value for t in state.tiles.values() if not t.unique_tile_id)
            terrain_inventory["unique"] = sum(1 for t in state.tiles.values() if t.unique_tile_id)

    return {
        "players": players,
        "samples": SEEDS,
        "homes_axial": [list(h) for h in homes_example],
        "map_tiles": sum(terrain_inventory.values()),
        "tiles_per_player": round(min_tiles_per_player, 3),
        "min_home_distance": min_home_distance,
        "max_home_to_contested_ring": max_home_to_ring,
        "min_special_access_rate": round(min_special_coverage, 3),
        "max_starting_production_spread": max_production_spread,
        "contested_tile_counts": dict(contested_counts),
        "seed0_physical_inventory": dict(sorted(terrain_inventory.items())),
        "failure_seeds": dict(failures),
    }


def main() -> None:
    results = {str(p): audit_count(p) for p in range(3, 9)}
    dest = ROOT / "tmp-plan4-geometry-audit.json"
    dest.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    print(f"WROTE {dest}")


if __name__ == "__main__":
    main()
