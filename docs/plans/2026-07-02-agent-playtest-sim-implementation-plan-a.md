# Agent Playtest Simulation — Plan A: Core Engine (Milestone 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A deterministic Python rules engine for Aeonis Milestone 1 (core loop: map, Move/Attack/Build/Recruit, combat, production, VP) that plays complete bot games end to end, with verdicts and replayable game records.

**Architecture:** Engine-authoritative simulator per `docs/plans/2026-07-02-agent-playtest-simulation-design.md`. The engine enumerates legal choices as plain JSON-safe dicts; agents pick one; the engine applies it. A game is fully determined by `(seed, choices)`. Milestone 1 stubs the Event/Strategy/Council phases (no-ops) and uses a generic Lord (d8/d8/3 HP/move 2) for every player.

**Tech Stack:** Python 3.11+ stdlib only for the engine; `pytest` as the sole dev dependency.

**Working directory:** All paths are relative to the repo root (`new/`). Pytest commands run from `sim/`.

**Ambiguity Ledger protocol:** Whenever a task forces a rules interpretation the docs don't settle, add an entry to `playtest/Ambiguity_Ledger.md` (created in Task 15, but keep notes as you go — Task 15 lists the entries already known from planning).

---

## File structure

```
sim/
  README.md                      # how to run tests and games
  requirements-dev.txt           # pytest
  conftest.py                    # empty; marks pytest rootdir
  aeonis_sim/
    __init__.py
    engine/
      __init__.py
      types.py                   # enums, stats tables, state dataclasses, (de)serialization
      hexmap.py                  # axial coords, map generation (First Playable §3, 3-4 players)
      setup.py                   # build_initial_state()
      observations.py            # DecisionPoint, observe()
      move.py                    # enumerate_moves / apply_move (Dijkstra w/ ZOC + flanking)
      recruit.py                 # enumerate_recruits / apply_recruit
      build.py                   # enumerate_builds / apply_build
      combat.py                  # enumerate_attacks / attack resolution / sieges / Lord capture
      production.py              # run_production (Production & Upkeep)
      cleanup.py                 # run_cleanup (claims, Imperial Seat VP, objectives, victory)
      objectives.py              # Milestone-1 public objective predicates
      game.py                    # Game: phase machine, next_decision()/submit()
      invariants.py              # check_invariants, InvariantViolation
      record.py                  # game record build/save/replay
    agents/
      __init__.py
      base.py                    # Agent protocol
      chaos.py                   # ChaosBot (uniform random; fuzzing)
    runner/
      __init__.py
      play.py                    # play_game(): wires agents to engine, verdicts, records
  tests/
    __init__.py
    test_types.py
    test_hexmap.py
    test_setup.py
    test_game_loop.py
    test_move.py
    test_recruit.py
    test_build.py
    test_production.py
    test_cleanup.py
    test_combat.py
    test_invariants_record.py
    test_chaos_smoke.py
```

Design rules that apply to every task:

- Choices and observations are **plain dicts** containing only JSON-safe values (lists, not tuples, in serialized form). Internally, coordinates are `(q, r)` tuples; serialization converts to lists.
- `submit()` only accepts a choice that is **byte-identical (after canonical JSON dump) to one of the enumerated options**. Agents cannot construct novel actions.
- All randomness flows through `Game.rng` (`random.Random(seed)`). Never use the global `random` module.
- Every mutation happens in an `apply_*` function; `enumerate_*` functions never mutate state.

---

### Task 1: Scaffolding

**Files:**
- Create: `sim/README.md`
- Create: `sim/requirements-dev.txt`
- Create: `sim/conftest.py`
- Create: `sim/aeonis_sim/__init__.py`, `sim/aeonis_sim/engine/__init__.py`, `sim/aeonis_sim/agents/__init__.py`, `sim/aeonis_sim/runner/__init__.py`
- Create: `sim/tests/__init__.py`

- [ ] **Step 1: Create the package tree**

`sim/requirements-dev.txt`:

```
pytest>=8
```

`sim/conftest.py`:

```python
# Marks the pytest rootdir; running `python3 -m pytest` from sim/ puts sim/ on sys.path
# so `import aeonis_sim` resolves.
```

`sim/README.md`:

```markdown
# Aeonis Simulator

Engine-authoritative playtest simulator. See
`docs/plans/2026-07-02-agent-playtest-simulation-design.md` for the design spec.

## Setup

    python3 -m pip install -r requirements-dev.txt

## Run tests

    cd sim && python3 -m pytest

## Run a smoke game (after Task 14)

    cd sim && python3 -m aeonis_sim.runner.play --players 4 --seed 1
```

All five `__init__.py` files are empty.

- [ ] **Step 2: Verify pytest collects (0 tests, exit code 5 is expected)**

Run: `cd sim && python3 -m pip install -r requirements-dev.txt && python3 -m pytest`
Expected: `no tests ran` (exit code 5 — that's fine at this point).

- [ ] **Step 3: Commit**

```bash
git add sim/
git commit -m "feat: scaffold aeonis_sim package for playtest simulator (plan A)"
```

---

### Task 2: Core types and serialization

**Files:**
- Create: `sim/aeonis_sim/engine/types.py`
- Test: `sim/tests/test_types.py`

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_types.py`:

```python
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


def test_derived_pop_and_constants():
    assert POP_BASE == 7 and VP_THRESHOLD == 10
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_types.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'aeonis_sim.engine.types'`

- [ ] **Step 3: Implement `types.py`**

`sim/aeonis_sim/engine/types.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

Coord = tuple  # axial (q, r)

# --- Global constants (First_Playable_Packet.md / Victory.md / Population.md) ---
VP_THRESHOLD = 10
GLOBAL_POP_CAP = 25
DEFAULT_ROUND_CAP = 25
BASE_AP = 5
# Packet §3.3 says "Population Cap: 10" at start while Population.md grants +3 cap
# per City. Engine rule (Ambiguity Ledger AL-1): cap = POP_BASE + city/building
# bonuses, with POP_BASE chosen so a starting player (1 City) has cap 10.
POP_BASE = 7


class Terrain(str, Enum):
    PLAINS = "plains"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    DESERT = "desert"
    LAKE = "lake"
    CITY = "city"
    RUINS = "ruins"
    PORTAL = "portal"


# AP cost to ENTER a hex (Movement.md §2). Lakes handled via Bridge check.
TERRAIN_COST = {
    Terrain.PLAINS: 1,
    Terrain.FOREST: 1,
    Terrain.MOUNTAIN: 2,
    Terrain.DESERT: 2,
    Terrain.LAKE: 1,      # only enterable if bridged
    Terrain.CITY: 1,
    Terrain.RUINS: 1,     # AL-2: Ruins movement cost undefined; engine uses 1
    Terrain.PORTAL: 1,    # Movement.md: enter/exit a Portal costs 1 AP
}


class UnitType(str, Enum):
    INFANTRY = "infantry"
    CAVALRY = "cavalry"
    ARCHER = "archer"
    LORD = "lord"


@dataclass(frozen=True)
class UnitStats:
    attack_die: int
    defense_die: int
    hp: int
    move: int
    pop: int
    gold: int = 0
    mana: int = 0


UNIT_STATS = {
    UnitType.INFANTRY: UnitStats(6, 6, 1, 1, 1, gold=1),
    UnitType.CAVALRY: UnitStats(8, 6, 2, 2, 2, gold=2),
    UnitType.ARCHER: UnitStats(6, 4, 1, 1, 1, gold=1, mana=1),
    # Milestone-1 generic Lord (no Lord sheets until Milestone 4).
    UnitType.LORD: UnitStats(8, 8, 3, 2, 0),
}


class BuildingType(str, Enum):
    FARM = "farm"
    MINE = "mine"
    GROVE = "grove"
    EMBASSY = "embassy"
    TOWER = "tower"
    FORTRESS = "fortress"
    BRIDGE = "bridge"
    GUILD_HALL = "guild_hall"
    CASTLE = "castle"


@dataclass(frozen=True)
class BuildingSpec:
    terrain: Optional[Terrain]  # None = any land terrain
    gold: int = 0
    mana: int = 0
    influence: int = 0
    pop: int = 0
    upkeep_gold: int = 0


# Buildings.md. Milestone 1 roster only: Forge/Academy/Bank/Market/Legendaries
# depend on systems from later milestones (Trade, Arcane, Lord sheets).
BUILDING_SPECS = {
    BuildingType.FARM: BuildingSpec(Terrain.PLAINS, gold=2, pop=1),
    BuildingType.MINE: BuildingSpec(Terrain.MOUNTAIN, gold=3, pop=1),
    BuildingType.GROVE: BuildingSpec(Terrain.FOREST, mana=2, pop=1),
    BuildingType.EMBASSY: BuildingSpec(Terrain.DESERT, influence=3, pop=1),
    BuildingType.TOWER: BuildingSpec(None, gold=4, pop=1),
    BuildingType.FORTRESS: BuildingSpec(None, gold=5, mana=2, pop=2),
    BuildingType.BRIDGE: BuildingSpec(Terrain.LAKE, gold=4, pop=0),
    BuildingType.GUILD_HALL: BuildingSpec(Terrain.CITY, gold=4, influence=2, pop=1),
    BuildingType.CASTLE: BuildingSpec(Terrain.CITY, gold=6, pop=2, upkeep_gold=2),
}


@dataclass
class Unit:
    uid: int
    owner: int
    type: UnitType
    hp: int

    def to_dict(self) -> dict:
        return {"uid": self.uid, "owner": self.owner, "type": self.type.value, "hp": self.hp}

    @staticmethod
    def from_dict(d: dict) -> "Unit":
        return Unit(uid=d["uid"], owner=d["owner"], type=UnitType(d["type"]), hp=d["hp"])


@dataclass
class Tile:
    coord: Coord
    terrain: Terrain
    imperial_seat: bool = False
    controller: Optional[int] = None
    units: list = field(default_factory=list)          # list[Unit]
    buildings: list = field(default_factory=list)      # list[BuildingType]
    siege: bool = False
    # Adjacency Claim tracker (Tiles.md control method 5): (pid, consecutive checks)
    adj_claim: Optional[tuple] = None
    castle_suspended: bool = False  # AL-8: Castle upkeep unpaid -> effects off this round

    def has(self, b: BuildingType) -> bool:
        return b in self.buildings

    def to_dict(self) -> dict:
        return {
            "coord": list(self.coord),
            "terrain": self.terrain.value,
            "imperial_seat": self.imperial_seat,
            "controller": self.controller,
            "units": [u.to_dict() for u in self.units],
            "buildings": [b.value for b in self.buildings],
            "siege": self.siege,
            "adj_claim": list(self.adj_claim) if self.adj_claim else None,
            "castle_suspended": self.castle_suspended,
        }

    @staticmethod
    def from_dict(d: dict) -> "Tile":
        return Tile(
            coord=tuple(d["coord"]),
            terrain=Terrain(d["terrain"]),
            imperial_seat=d["imperial_seat"],
            controller=d["controller"],
            units=[Unit.from_dict(u) for u in d["units"]],
            buildings=[BuildingType(b) for b in d["buildings"]],
            siege=d["siege"],
            adj_claim=tuple(d["adj_claim"]) if d["adj_claim"] else None,
            castle_suspended=d["castle_suspended"],
        )


@dataclass
class PlayerState:
    pid: int
    home: Coord
    ap: int = 0
    banked: int = 0
    gold: int = 0
    mana: int = 0
    influence: int = 0
    renown: int = 0
    vp: int = 0
    pop_pool: int = 0
    passed: bool = False
    objective: Optional[str] = None
    objective_scored: bool = False
    battle_wins: int = 0
    used_portal_travel: bool = False
    lord_captured: bool = False
    seat_streak: int = 0
    seat_bonus_scored: bool = False
    recruited_cities: list = field(default_factory=list)  # list[Coord] this round
    vp_sources: dict = field(default_factory=dict)         # source -> total VP

    def add_vp(self, n: int, source: str) -> None:
        self.vp += n
        self.vp_sources[source] = self.vp_sources.get(source, 0) + n

    def to_dict(self) -> dict:
        return {
            "pid": self.pid, "home": list(self.home), "ap": self.ap, "banked": self.banked,
            "gold": self.gold, "mana": self.mana, "influence": self.influence,
            "renown": self.renown, "vp": self.vp, "pop_pool": self.pop_pool,
            "passed": self.passed, "objective": self.objective,
            "objective_scored": self.objective_scored, "battle_wins": self.battle_wins,
            "used_portal_travel": self.used_portal_travel, "lord_captured": self.lord_captured,
            "seat_streak": self.seat_streak, "seat_bonus_scored": self.seat_bonus_scored,
            "recruited_cities": [list(c) for c in self.recruited_cities],
            "vp_sources": dict(self.vp_sources),
        }

    @staticmethod
    def from_dict(d: dict) -> "PlayerState":
        p = PlayerState(pid=d["pid"], home=tuple(d["home"]))
        for k in ("ap", "banked", "gold", "mana", "influence", "renown", "vp", "pop_pool",
                  "passed", "objective", "objective_scored", "battle_wins",
                  "used_portal_travel", "lord_captured", "seat_streak", "seat_bonus_scored"):
            setattr(p, k, d[k])
        p.recruited_cities = [tuple(c) for c in d["recruited_cities"]]
        p.vp_sources = dict(d["vp_sources"])
        return p


@dataclass
class GameState:
    players: list                         # list[PlayerState]
    tiles: dict                           # dict[Coord, Tile]
    round: int = 1
    final_round: bool = False
    next_uid: int = 1

    # --- helpers used across the engine ---
    def player(self, pid: int) -> PlayerState:
        return self.players[pid]

    def controlled(self, pid: int) -> list:
        return [t for t in self.tiles.values() if t.controller == pid]

    def units_of(self, pid: int) -> list:
        out = []
        for t in self.tiles.values():
            for u in t.units:
                if u.owner == pid:
                    out.append((t.coord, u))
        return out

    def find_lord(self, pid: int):
        for coord, u in self.units_of(pid):
            if u.type == UnitType.LORD:
                return coord, u
        return None

    def pop_used(self, pid: int) -> int:
        used = sum(UNIT_STATS[u.type].pop for _, u in self.units_of(pid))
        for t in self.controlled(pid):
            for b in t.buildings:
                used += BUILDING_SPECS[b].pop
        return used

    def pop_cap(self, pid: int) -> int:
        cap = POP_BASE
        for t in self.controlled(pid):
            if t.terrain == Terrain.CITY:
                cap += 3
            if t.has(BuildingType.FARM):
                cap += 2
            if t.has(BuildingType.CASTLE) and not t.castle_suspended:
                cap += 3
        return min(cap, GLOBAL_POP_CAP)

    def new_uid(self) -> int:
        uid = self.next_uid
        self.next_uid += 1
        return uid

    def to_dict(self) -> dict:
        return {
            "players": [p.to_dict() for p in self.players],
            "tiles": {f"{c[0]},{c[1]}": t.to_dict() for c, t in self.tiles.items()},
            "round": self.round,
            "final_round": self.final_round,
            "next_uid": self.next_uid,
        }

    @staticmethod
    def from_dict(d: dict) -> "GameState":
        tiles = {}
        for key, td in d["tiles"].items():
            q, r = key.split(",")
            tiles[(int(q), int(r))] = Tile.from_dict(td)
        return GameState(
            players=[PlayerState.from_dict(p) for p in d["players"]],
            tiles=tiles,
            round=d["round"],
            final_round=d["final_round"],
            next_uid=d["next_uid"],
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_types.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/types.py sim/tests/test_types.py
git commit -m "feat: engine core types, stats tables, and state serialization"
```

---

### Task 3: Hex grid and map generation

**Files:**
- Create: `sim/aeonis_sim/engine/hexmap.py`
- Test: `sim/tests/test_hexmap.py`

Map layout implements First_Playable_Packet.md §3.1 for **3–4 players** (5–8 player scaling is a later milestone). Deviation (Ambiguity Ledger AL-3): Deserts are placed by seeded shuffle rather than "between each pair of home clusters" — positional flavor only, flagged for later fidelity work.

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_hexmap.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_hexmap.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `hexmap.py`**

`sim/aeonis_sim/engine/hexmap.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_hexmap.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/hexmap.py sim/tests/test_hexmap.py
git commit -m "feat: hex geometry and First Playable map generation (3-4p)"
```

---

### Task 4: Initial game setup

**Files:**
- Create: `sim/aeonis_sim/engine/setup.py`
- Create: `sim/aeonis_sim/engine/objectives.py`
- Test: `sim/tests/test_setup.py`

Packet §3.3–3.5 defaults (no Lord sheets in Milestone 1). **AL-4:** packet says "Population Pool: 10 (full at start)" but starting units occupy 4 Population; engine rule: starting units DO consume Population, so the starting pool is 6 of cap 10.

Milestone-1 objective deck: the packet's 6 public objectives minus **Council Power** (needs the Council, Milestone 2) — 5 cards, 1 dealt per player.

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_setup.py`:

```python
import random

from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.objectives import OBJECTIVES
from aeonis_sim.engine.types import UnitType


def make_state(players=4, seed=1):
    return build_initial_state({"players": players}, random.Random(seed))


def test_starting_resources_and_tracks():
    s = make_state()
    for p in s.players:
        assert p.ap == 5 and p.gold == 2 and p.mana == 2 and p.influence == 1
        assert p.renown == 0 and p.vp == 0
        # AL-4: pool 6 = cap 10 minus 4 pop occupied by starting units
        assert p.pop_pool == 6
        assert s.pop_cap(p.pid) == 10
        assert s.pop_used(p.pid) == 4


def test_starting_units_and_control():
    s = make_state()
    for p in s.players:
        home = s.tiles[p.home]
        types = sorted(u.type.value for u in home.units)
        assert types == ["archer", "infantry", "infantry", "infantry", "lord"]
        assert home.controller == p.pid
        # Home cluster of 4 controlled tiles
        assert len(s.controlled(p.pid)) == 4


def test_objectives_dealt_uniquely():
    s = make_state()
    objs = [p.objective for p in s.players]
    assert len(set(objs)) == len(objs)
    assert all(o in OBJECTIVES for o in objs)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_setup.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `objectives.py` (predicates used later by cleanup) and `setup.py`**

`sim/aeonis_sim/engine/objectives.py`:

```python
from __future__ import annotations

from .types import Terrain


def _frontier_lord(state, pid) -> bool:
    return len(state.controlled(pid)) >= 7


def _builder(state, pid) -> bool:
    return sum(len(t.buildings) for t in state.controlled(pid)) >= 3


def _portal_mastery(state, pid) -> bool:
    controls_portal = any(t.terrain == Terrain.PORTAL for t in state.controlled(pid))
    return controls_portal and state.player(pid).used_portal_travel


def _warlord(state, pid) -> bool:
    return state.player(pid).battle_wins >= 2


def _seat_of_empire(state, pid) -> bool:
    return any(t.imperial_seat for t in state.controlled(pid))


# Packet §4.4 public objectives, minus Council Power (Milestone 2). All 2 VP,
# checked at Cleanup & Checks (AL-5: claim timing not specified in docs;
# engine auto-scores at Cleanup, once per card).
OBJECTIVES = {
    "frontier_lord": _frontier_lord,
    "builder": _builder,
    "portal_mastery": _portal_mastery,
    "warlord": _warlord,
    "seat_of_empire": _seat_of_empire,
}
```

`sim/aeonis_sim/engine/setup.py`:

```python
from __future__ import annotations

import random

from .hexmap import generate_map, neighbors
from .objectives import OBJECTIVES
from .types import BASE_AP, GameState, PlayerState, Unit, UNIT_STATS, UnitType


def build_initial_state(config: dict, rng: random.Random) -> GameState:
    n = config["players"]
    tiles, homes = generate_map(n, rng)
    state = GameState(players=[], tiles=tiles)

    deck = sorted(OBJECTIVES.keys())
    rng.shuffle(deck)

    for pid in range(n):
        p = PlayerState(pid=pid, home=homes[pid], ap=BASE_AP,
                        gold=2, mana=2, influence=1)
        p.objective = deck.pop()
        state.players.append(p)

        home = tiles[homes[pid]]
        for ut in (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.INFANTRY,
                   UnitType.ARCHER, UnitType.LORD):
            home.units.append(Unit(uid=state.new_uid(), owner=pid, type=ut,
                                   hp=UNIT_STATS[ut].hp))

        # Control the home cluster: home City + its 3 cluster tiles (§3.5)
        home.controller = pid
        for nb in neighbors(homes[pid]):
            t = tiles.get(nb)
            if t is not None and t.controller is None and not t.imperial_seat \
                    and t.terrain.value in ("plains", "forest", "mountain"):
                t.controller = pid

    for p in state.players:
        # AL-4: starting units occupy Population; pool = cap - used
        p.pop_pool = state.pop_cap(p.pid) - state.pop_used(p.pid)

    return state
```

Note: the cluster-control loop claims the 3 cluster tiles generated adjacent to the home City in Task 3. Filler Plains/Forest/Mountain hexes adjacent to a home City would also be claimed; that over-claims only if map generation placed filler adjacent to a home city AND it is one of the first three matching — acceptable for Milestone 1 but verify the controlled-count test (exactly 4) passes; if a seed yields 5+, tighten by tracking cluster coords explicitly in `generate_map` (return `clusters: dict[pid, list[Coord]]`) and claiming exactly those. If the test fails for the chosen seeds, do that tightening as part of this task.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_setup.py -v`
Expected: 3 passed. If `test_starting_units_and_control` fails on the controlled-count assertion, implement the explicit-cluster tightening described above and re-run.

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/setup.py sim/aeonis_sim/engine/objectives.py sim/tests/test_setup.py
git commit -m "feat: initial state setup and Milestone-1 objective deck"
```

---

### Task 5: Observations and decision points

**Files:**
- Create: `sim/aeonis_sim/engine/observations.py`

Milestone 1 has **no hidden information** (objectives are public, no card hands yet), so the observation is the full state plus viewer id. The per-player filtering hook arrives with Whispers/secret objectives in a later plan — the function signature is already viewer-aware so call sites won't change.

No standalone test file: `DecisionPoint` and `observe` are exercised by every subsequent task's tests.

- [ ] **Step 1: Implement `observations.py`**

`sim/aeonis_sim/engine/observations.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DecisionPoint:
    """A point where an agent must choose. kind is one of:
    - "action":           your Action Phase turn; choices are actions
    - "press":            attacker after a battle round: press or end
    - "defender_retreat": defender after a battle round: retreat or hold
    """
    kind: str
    pid: int
    choices: list                      # list[dict], JSON-safe
    context: dict = field(default_factory=dict)


def observe(state, viewer_pid: int) -> dict:
    """The viewer's view of the game. Milestone 1: full information."""
    return {"viewer": viewer_pid, "state": state.to_dict()}
```

- [ ] **Step 2: Verify it imports**

Run: `cd sim && python3 -c "from aeonis_sim.engine.observations import DecisionPoint, observe; print('ok')"`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add sim/aeonis_sim/engine/observations.py
git commit -m "feat: decision point and observation types"
```

---

### Task 6: Move action

**Files:**
- Create: `sim/aeonis_sim/engine/move.py`
- Test: `sim/tests/test_move.py`

Rules: `Movement.md` + `Tiles.md` ZOC. Engine decisions to encode (and their ledger tags):

- Groups enumerated are **whole stack** and **each single unit** (not all subsets) — a branching-factor bound, not a rules interpretation; noted in the module docstring.
- A unit may never enter a hex containing another player's units (attacks are declared; `Movement.md` §Combat interaction).
- ZOC surcharge: +1 AP entering a hex adjacent to ≥1 enemy military unit. A group containing Cavalry skips the surcharge on the **first** ZOC hex of the path — pathfinding therefore tracks `(hex, flank_spent)`.
- Portal travel: portal hexes are adjacent to each other at 0 AP when the destination portal is neutral or yours (Open Borders arrives with the Council in Milestone 2).
- Entering a **neutral** hex claims it immediately (`Tiles.md` control method 3); enemy-controlled hexes flip at Round Start (Task 12).

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_move.py`:

```python
import random

from aeonis_sim.engine.move import enumerate_moves, apply_move
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import Terrain, Tile, Unit, UnitType, UNIT_STATS


def make_state():
    return build_initial_state({"players": 3}, random.Random(5))


def strip_map(state):
    """Clear all units off the board for hand-built scenarios."""
    for t in state.tiles.values():
        t.units = []
        t.controller = None
    return state


def put(state, coord, owner, utype, terrain=None):
    if terrain is not None:
        state.tiles[coord].terrain = terrain
    u = Unit(uid=state.new_uid(), owner=owner, type=utype, hp=UNIT_STATS[utype].hp)
    state.tiles[coord].units.append(u)
    return u


def test_infantry_range_and_cost():
    s = strip_map(make_state())
    put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    s.players[0].ap = 5
    moves = enumerate_moves(s, 0)
    dests = {tuple(m["dest"]) for m in moves}
    # Infantry range 1: only the 6 neighbors (minus impassable), never distance 2
    assert all(
        max(abs(d[0]), abs(d[1]), abs(d[0] + d[1])) <= 1 or s.tiles[d].terrain == Terrain.PORTAL
        for d in dests
    )


def test_mountain_costs_2():
    s = strip_map(make_state())
    put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    s.tiles[(1, 0)].terrain = Terrain.MOUNTAIN
    s.players[0].ap = 5
    moves = enumerate_moves(s, 0)
    m = next(m for m in moves if tuple(m["dest"]) == (1, 0))
    assert m["cost"] == 2


def test_zoc_surcharge_and_cavalry_flanking():
    s = strip_map(make_state())
    put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    put(s, (2, -1), 1, UnitType.INFANTRY, terrain=Terrain.PLAINS)  # enemy adj to (1,0) and (1,-1)
    s.tiles[(1, 0)].terrain = Terrain.PLAINS
    s.players[0].ap = 5
    moves = enumerate_moves(s, 0)
    m = next(m for m in moves if tuple(m["dest"]) == (1, 0))
    assert m["cost"] == 2  # 1 terrain + 1 ZOC
    # Same spot with cavalry: first ZOC hex is exempt
    s2 = strip_map(make_state())
    put(s2, (0, 0), 0, UnitType.CAVALRY, terrain=Terrain.PLAINS)
    put(s2, (2, -1), 1, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    s2.tiles[(1, 0)].terrain = Terrain.PLAINS
    s2.players[0].ap = 5
    m2 = next(m for m in enumerate_moves(s2, 0) if tuple(m["dest"]) == (1, 0))
    assert m2["cost"] == 1


def test_cannot_enter_occupied_or_unbridged_lake():
    s = strip_map(make_state())
    put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    put(s, (1, 0), 1, UnitType.INFANTRY)
    s.tiles[(0, 1)].terrain = Terrain.LAKE
    s.players[0].ap = 5
    dests = {tuple(m["dest"]) for m in enumerate_moves(s, 0)}
    assert (1, 0) not in dests
    assert (0, 1) not in dests


def test_apply_move_claims_neutral_and_pays_ap():
    s = strip_map(make_state())
    u = put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    s.tiles[(1, 0)].terrain = Terrain.PLAINS
    s.players[0].ap = 5
    m = next(m for m in enumerate_moves(s, 0) if tuple(m["dest"]) == (1, 0))
    apply_move(s, 0, m)
    assert s.players[0].ap == 5 - m["cost"]
    assert any(x.uid == u.uid for x in s.tiles[(1, 0)].units)
    assert s.tiles[(1, 0)].controller == 0  # neutral hex claimed immediately


def test_portal_travel_zero_ap_and_flag():
    s = strip_map(make_state())
    portals = [c for c, t in s.tiles.items() if t.terrain == Terrain.PORTAL]
    a, b = portals[0], portals[1]
    put(s, a, 0, UnitType.INFANTRY)
    s.tiles[a].controller = 0
    s.players[0].ap = 5
    m = next(m for m in enumerate_moves(s, 0) if tuple(m["dest"]) == b)
    assert m["cost"] == 0
    apply_move(s, 0, m)
    assert s.players[0].used_portal_travel is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_move.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `move.py`**

`sim/aeonis_sim/engine/move.py`:

```python
"""Move action (Movement.md, Tiles.md ZOC).

Branching bound: groups enumerated are the WHOLE STACK and each SINGLE UNIT,
not every subset. This is an agent-capability bound, not a rules ruling.
"""
from __future__ import annotations

import heapq

from .hexmap import neighbors
from .types import BuildingType, Terrain, TERRAIN_COST, UNIT_STATS, UnitType


def _enemy_zoc(state, pid) -> set:
    """Hexes adjacent to at least one enemy military unit."""
    zoc = set()
    for t in state.tiles.values():
        if any(u.owner != pid for u in t.units):
            for n in neighbors(t.coord):
                if n in state.tiles:
                    zoc.add(n)
    return zoc


def _passable(state, pid, coord) -> bool:
    t = state.tiles.get(coord)
    if t is None:
        return False
    if t.terrain == Terrain.LAKE and not t.has(BuildingType.BRIDGE):
        return False
    if any(u.owner != pid for u in t.units):
        return False  # attacks are declared; never move into enemy units
    return True


def _portal_exits(state, pid, coord):
    """Portal-to-portal edges at 0 AP (destination neutral or yours)."""
    t = state.tiles.get(coord)
    if t is None or t.terrain != Terrain.PORTAL:
        return []
    out = []
    for c2, t2 in state.tiles.items():
        if c2 == coord or t2.terrain != Terrain.PORTAL:
            continue
        if t2.controller in (None, pid):
            out.append(c2)
    return out


def _paths_from(state, pid, start, max_range, max_cost, has_cavalry):
    """Dijkstra over (hex, flank_spent). Returns dest -> (cost, hexes_entered, used_portal)."""
    best = {}
    # (cost, hexes_entered, coord, flank_spent, used_portal)
    heap = [(0, 0, start, not has_cavalry, False)]
    seen = {}
    while heap:
        cost, steps, coord, flanked, portaled = heapq.heappop(heap)
        key = (coord, flanked)
        if key in seen and seen[key] <= (cost, steps):
            continue
        seen[key] = (cost, steps)
        if coord != start:
            prev = best.get(coord)
            if prev is None or (cost, steps) < (prev[0], prev[1]):
                best[coord] = (cost, steps, portaled)
        if steps >= max_range:
            continue
        zoc = _enemy_zoc(state, pid)
        for nxt in neighbors(coord):
            if not _passable(state, pid, nxt):
                continue
            step = TERRAIN_COST[state.tiles[nxt].terrain]
            f2 = flanked
            if nxt in zoc:
                if not flanked:
                    f2 = True  # cavalry flanking: first ZOC hex free
                else:
                    step += 1
            if cost + step <= max_cost:
                heapq.heappush(heap, (cost + step, steps + 1, nxt, f2, portaled))
        for nxt in _portal_exits(state, pid, coord):
            if _passable(state, pid, nxt) and cost <= max_cost:
                heapq.heappush(heap, (cost, steps + 1, nxt, flanked, True))
    return best


def _groups(tile, pid):
    mine = [u for u in tile.units if u.owner == pid]
    if not mine:
        return []
    groups = [mine]  # whole stack
    if len(mine) > 1:
        groups.extend([[u] for u in mine])
    return groups


def enumerate_moves(state, pid) -> list:
    p = state.player(pid)
    out = []
    for tile in state.tiles.values():
        for group in _groups(tile, pid):
            uids = sorted(u.uid for u in group)
            max_range = min(UNIT_STATS[u.type].move for u in group)
            has_cav = any(u.type == UnitType.CAVALRY for u in group)
            for dest, (cost, _steps, portaled) in _paths_from(
                    state, pid, tile.coord, max_range, p.ap, has_cav).items():
                out.append({
                    "type": "move",
                    "from": list(tile.coord),
                    "dest": list(dest),
                    "uids": uids,
                    "cost": cost,
                    "portal": portaled,
                })
    return out


def apply_move(state, pid, choice) -> None:
    p = state.player(pid)
    src = state.tiles[tuple(choice["from"])]
    dst = state.tiles[tuple(choice["dest"])]
    moving = [u for u in src.units if u.uid in set(choice["uids"])]
    src.units = [u for u in src.units if u.uid not in set(choice["uids"])]
    dst.units.extend(moving)
    p.ap -= choice["cost"]
    if choice["portal"]:
        p.used_portal_travel = True
    # Tiles.md control method 3: neutral hex claimed immediately.
    if dst.controller is None:
        dst.controller = pid
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_move.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/move.py sim/tests/test_move.py
git commit -m "feat: move action with ZOC, cavalry flanking, and portal travel"
```

---

### Task 7: Recruit action

**Files:**
- Create: `sim/aeonis_sim/engine/recruit.py`
- Test: `sim/tests/test_recruit.py`

Rules: `Actions.md` §Recruit. 1 AP; one controlled City not yet used this round; up to 2 units; pay Gold/Mana and Population.

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_recruit.py`:

```python
import random

from aeonis_sim.engine.recruit import enumerate_recruits, apply_recruit
from aeonis_sim.engine.setup import build_initial_state


def make_state():
    return build_initial_state({"players": 3}, random.Random(5))


def test_enumerates_affordable_combos_at_home_city():
    s = make_state()
    p = s.players[0]  # 2 gold, 2 mana, pool 6
    recs = enumerate_recruits(s, 0)
    assert all(tuple(r["city"]) == p.home for r in recs)
    combos = {tuple(sorted(r["units"])) for r in recs}
    # 2 gold buys: 1 inf, 2 inf, 1 cav, 1 archer(1g1m), 2 archers, inf+archer
    assert ("infantry", "infantry") in combos
    assert ("cavalry",) in combos
    assert ("archer", "infantry") in combos
    # cavalry+anything needs 3+ gold -> absent
    assert not any("cavalry" in c and len(c) == 2 for c in combos)


def test_apply_recruit_pays_and_places():
    s = make_state()
    p = s.players[0]
    rec = next(r for r in enumerate_recruits(s, 0)
               if sorted(r["units"]) == ["archer", "infantry"])
    apply_recruit(s, 0, rec)
    assert p.ap == 4 and p.gold == 0 and p.mana == 1
    assert p.pop_pool == 4  # 6 - 2
    home = s.tiles[p.home]
    assert len(home.units) == 7  # 5 starting + 2
    assert p.recruited_cities == [p.home]


def test_city_reuse_blocked_within_round():
    s = make_state()
    rec = next(r for r in enumerate_recruits(s, 0) if r["units"] == ["infantry"])
    apply_recruit(s, 0, rec)
    assert enumerate_recruits(s, 0) == []  # only city already used


def test_pop_pool_blocks_recruiting():
    s = make_state()
    s.players[0].pop_pool = 0
    assert enumerate_recruits(s, 0) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_recruit.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `recruit.py`**

`sim/aeonis_sim/engine/recruit.py`:

```python
from __future__ import annotations

from itertools import combinations_with_replacement

from .types import Terrain, Unit, UNIT_STATS, UnitType

RECRUITABLE = [UnitType.INFANTRY, UnitType.CAVALRY, UnitType.ARCHER]


def _affordable(p, unit_types) -> bool:
    gold = sum(UNIT_STATS[u].gold for u in unit_types)
    mana = sum(UNIT_STATS[u].mana for u in unit_types)
    pop = sum(UNIT_STATS[u].pop for u in unit_types)
    return p.gold >= gold and p.mana >= mana and p.pop_pool >= pop


def enumerate_recruits(state, pid) -> list:
    p = state.player(pid)
    if p.ap < 1:
        return []
    combos = [list(c) for n in (1, 2)
              for c in combinations_with_replacement(RECRUITABLE, n)]
    out = []
    for tile in state.controlled(pid):
        if tile.terrain != Terrain.CITY:
            continue
        if tile.coord in p.recruited_cities:
            continue  # Actions.md: each City at most once per round
        for combo in combos:
            if _affordable(p, combo):
                out.append({
                    "type": "recruit",
                    "city": list(tile.coord),
                    "units": sorted(u.value for u in combo),
                })
    return out


def apply_recruit(state, pid, choice) -> None:
    p = state.player(pid)
    tile = state.tiles[tuple(choice["city"])]
    p.ap -= 1
    p.recruited_cities.append(tile.coord)
    for name in choice["units"]:
        ut = UnitType(name)
        st = UNIT_STATS[ut]
        p.gold -= st.gold
        p.mana -= st.mana
        p.pop_pool -= st.pop
        tile.units.append(Unit(uid=state.new_uid(), owner=pid, type=ut, hp=st.hp))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_recruit.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/recruit.py sim/tests/test_recruit.py
git commit -m "feat: recruit action with city limits and population costs"
```

---

### Task 8: Build action

**Files:**
- Create: `sim/aeonis_sim/engine/build.py`
- Test: `sim/tests/test_build.py`

Rules: `Actions.md` (3 AP), `Buildings.md`, `Tiles.md` slots (basic terrain 1 building, City 2), `Population.md` (reserved capacity). Bridge: on a Lake, requires a controlled adjacent non-Lake hex; the Lake needn't be controlled (it can't be, while impassable). **AL-6:** whether a Bridge on an uncontrolled Lake grants control — engine: bridged Lake becomes controlled by the builder.

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_build.py`:

```python
import random

from aeonis_sim.engine.build import enumerate_builds, apply_build
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain


def make_state():
    s = build_initial_state({"players": 3}, random.Random(5))
    s.players[0].gold = 20
    s.players[0].mana = 20
    s.players[0].influence = 20
    return s


def options(state, pid):
    return {(tuple(b["hex"]), b["building"]) for b in enumerate_builds(state, pid)}


def test_terrain_matching():
    s = make_state()
    p = s.players[0]
    opts = options(s, 0)
    plains = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.PLAINS)
    mountain = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.MOUNTAIN)
    assert (plains, "farm") in opts
    assert (mountain, "mine") in opts
    assert (plains, "mine") not in opts
    assert (p.home, "guild_hall") in opts
    assert (plains, "tower") in opts  # any-terrain building


def test_apply_build_farm():
    s = make_state()
    p = s.players[0]
    plains = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.PLAINS)
    cap_before = s.pop_cap(0)
    pool_before = p.pop_pool
    choice = next(b for b in enumerate_builds(s, 0)
                  if tuple(b["hex"]) == plains and b["building"] == "farm")
    apply_build(s, 0, choice)
    assert p.ap == 2 and p.gold == 18
    assert s.tiles[plains].has(BuildingType.FARM)
    assert s.pop_cap(0) == cap_before + 2      # Farm: +2 cap
    assert p.pop_pool == pool_before - 1        # occupies 1 pop


def test_slot_limits():
    s = make_state()
    plains = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.PLAINS)
    farm = next(b for b in enumerate_builds(s, 0)
                if tuple(b["hex"]) == plains and b["building"] == "farm")
    apply_build(s, 0, farm)
    s.players[0].ap = 5
    # Basic terrain: 1 building max -> no more options on that hex
    assert not any(tuple(b["hex"]) == plains for b in enumerate_builds(s, 0))


def test_bridge_requires_adjacent_control_and_claims_lake():
    s = make_state()
    from aeonis_sim.engine.hexmap import neighbors
    lake = next(c for c, t in s.tiles.items() if t.terrain == Terrain.LAKE)
    # Give player 0 control of a neighbor of the lake (clear units to be safe)
    nb = next(c for c in neighbors(lake) if c in s.tiles
              and s.tiles[c].terrain != Terrain.LAKE)
    s.tiles[nb].controller = 0
    choice = next(b for b in enumerate_builds(s, 0)
                  if tuple(b["hex"]) == lake and b["building"] == "bridge")
    apply_build(s, 0, choice)
    assert s.tiles[lake].has(BuildingType.BRIDGE)
    assert s.tiles[lake].controller == 0  # AL-6
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_build.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `build.py`**

`sim/aeonis_sim/engine/build.py`:

```python
from __future__ import annotations

from .hexmap import neighbors
from .types import BUILDING_SPECS, BuildingType, Terrain

BUILD_AP = 3


def _slots(tile) -> int:
    return 2 if tile.terrain == Terrain.CITY else 1


def _can_afford(p, spec) -> bool:
    return (p.gold >= spec.gold and p.mana >= spec.mana
            and p.influence >= spec.influence and p.pop_pool >= spec.pop)


def enumerate_builds(state, pid) -> list:
    p = state.player(pid)
    if p.ap < BUILD_AP:
        return []
    out = []
    for btype, spec in BUILDING_SPECS.items():
        if not _can_afford(p, spec):
            continue
        if btype == BuildingType.BRIDGE:
            for coord, tile in state.tiles.items():
                if tile.terrain != Terrain.LAKE or tile.has(BuildingType.BRIDGE):
                    continue
                if any(state.tiles[n].controller == pid
                       for n in neighbors(coord) if n in state.tiles
                       and state.tiles[n].terrain != Terrain.LAKE):
                    out.append({"type": "build", "hex": list(coord),
                                "building": btype.value})
            continue
        for tile in state.controlled(pid):
            if len(tile.buildings) >= _slots(tile):
                continue
            if btype in tile.buildings:
                continue
            if spec.terrain is not None and tile.terrain != spec.terrain:
                continue
            if spec.terrain is None and tile.terrain == Terrain.LAKE:
                continue
            out.append({"type": "build", "hex": list(tile.coord),
                        "building": btype.value})
    return out


def apply_build(state, pid, choice) -> None:
    p = state.player(pid)
    tile = state.tiles[tuple(choice["hex"])]
    btype = BuildingType(choice["building"])
    spec = BUILDING_SPECS[btype]
    p.ap -= BUILD_AP
    p.gold -= spec.gold
    p.mana -= spec.mana
    p.influence -= spec.influence
    p.pop_pool -= spec.pop
    tile.buildings.append(btype)
    if btype == BuildingType.BRIDGE and tile.controller is None:
        tile.controller = pid  # AL-6
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_build.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/build.py sim/tests/test_build.py
git commit -m "feat: build action with terrain matching, slots, and bridges"
```

---

### Task 9: Combat

**Files:**
- Create: `sim/aeonis_sim/engine/combat.py`
- Test: `sim/tests/test_combat.py`

Rules: `Combat.md`. Milestone-1 bounds (agent-capability limits, documented in the module docstring, not rules rulings):

- Both sides auto-commit **all** eligible units (attacker: all units adjacent to target; defender: units in target + adjacent). Commit choices become agent decisions in a later milestone.
- Battle Line formed by fixed priority: Cavalry, Archer, Infantry, Lord last (Lords protected by default).
- Strike targeting: each striker hits the enemy line unit with (lowest HP, lowest defense die, lowest uid).

Ledger entries this task creates: **AL-7** (defender always auto-declares Hold the Walls for Cities — sieges are strictly better for Milestone-1 defenders since City retreat is banned anyway), **AL-10** (defender "wins a battle" for Warlord when all attacker committed units are eliminated), **AL-11** (captured hex's buildings are taken over intact), **AL-12** (Archers strike only in Pre-Strike, not again in the main strike).

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_combat.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_combat.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `combat.py`**

`sim/aeonis_sim/engine/combat.py`:

```python
"""Combat (Combat.md).

Milestone-1 agent-capability bounds (not rules rulings):
- Both sides auto-commit all eligible units.
- Battle Line priority: Cavalry, Archer, Infantry, Lord last.
- Strike target: enemy line unit with (lowest hp, lowest defense die, lowest uid).
Ledger: AL-7 auto Hold the Walls; AL-10 defender win definition;
AL-11 buildings taken over intact; AL-12 archers only strike in Pre-Strike.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .hexmap import neighbors
from .types import BuildingType, Terrain, UNIT_STATS, UnitType

ATTACK_AP = 2
PRESS_AP = 1
_LINE_PRIORITY = {UnitType.CAVALRY: 0, UnitType.ARCHER: 1,
                  UnitType.INFANTRY: 2, UnitType.LORD: 3}


@dataclass
class Battle:
    attacker: int
    defender: int
    target: tuple
    att_committed: list = field(default_factory=list)  # [(origin, Unit)]
    def_committed: list = field(default_factory=list)
    att_line: list = field(default_factory=list)       # [Unit]
    def_line: list = field(default_factory=list)
    siege: bool = False
    cap: int = 3
    rounds: int = 0
    winner: Optional[str] = None
    def_retreated: bool = False


def _defender_of(state, target) -> Optional[int]:
    t = state.tiles[target]
    for u in t.units:
        return u.owner
    return t.controller


def enumerate_attacks(state, pid) -> list:
    if state.player(pid).ap < ATTACK_AP:
        return []
    my_hexes = {t.coord for t in state.tiles.values()
                if any(u.owner == pid for u in t.units)}
    out = []
    for coord, t in state.tiles.items():
        d = _defender_of(state, coord)
        if d is None or d == pid:
            continue
        if any(n in my_hexes for n in neighbors(coord)):
            out.append({"type": "attack", "target": list(coord), "cost": ATTACK_AP})
    return out


def start_battle(state, pid, choice) -> Battle:
    target = tuple(choice["target"])
    t = state.tiles[target]
    defender = _defender_of(state, target)
    b = Battle(attacker=pid, defender=defender, target=target)
    b.cap = 5 if t.terrain == Terrain.CITY or t.has(BuildingType.FORTRESS) else 3
    # AL-7: Fortress -> siege (canon); City -> defender auto-declares Hold the Walls.
    b.siege = t.terrain == Terrain.CITY or t.has(BuildingType.FORTRESS)
    state.player(pid).ap -= choice["cost"]

    for u in t.units:
        if u.owner == defender:
            b.def_committed.append((target, u))
    for n in neighbors(target):
        nt = state.tiles.get(n)
        if nt is None:
            continue
        for u in nt.units:
            if u.owner == pid:
                b.att_committed.append((n, u))
            elif u.owner == defender:
                b.def_committed.append((n, u))
    return b


def _form_line(committed, cap, line) -> None:
    pool = sorted((u for _, u in committed if u not in line),
                  key=lambda u: (_LINE_PRIORITY[u.type], u.uid))
    while len(line) < cap and pool:
        line.append(pool.pop(0))


def _pick_target(line) -> Optional[object]:
    alive = [u for u in line if u.hp > 0]
    if not alive:
        return None
    return min(alive, key=lambda u: (u.hp, UNIT_STATS[u.type].defense_die, u.uid))


def _defense_bonus(state, battle, side) -> int:
    if side != "def":
        return 0
    t = state.tiles[battle.target]
    bonus = 0
    if t.has(BuildingType.TOWER):
        bonus += 1
    if t.has(BuildingType.FORTRESS):
        bonus += 2
    if t.has(BuildingType.CASTLE) and not t.castle_suspended:
        bonus += 2
    return bonus


def _kill(state, battle, unit) -> None:
    for lst in (battle.att_line, battle.def_line):
        if unit in lst:
            lst.remove(unit)
    for lst in (battle.att_committed, battle.def_committed):
        for pair in list(lst):
            if pair[1] is unit:
                lst.remove(pair)
                origin = pair[0]
                state.tiles[origin].units.remove(unit)
    if unit.type == UnitType.LORD:
        owner = state.player(unit.owner)
        owner.lord_captured = True
        captor_pid = battle.attacker if unit.owner == battle.defender else battle.defender
        captor = state.player(captor_pid)
        captor.add_vp(1, "lord_capture")     # Combat.md 2.1.4
        captor.renown += 2


def _strike(state, battle, strikers, targets_line, rng, def_side) -> None:
    for striker in sorted(strikers, key=lambda u: u.uid):
        if striker.hp <= 0:
            continue
        target = _pick_target(targets_line)
        if target is None:
            return
        atk = rng.randint(1, UNIT_STATS[striker.type].attack_die)
        dfn = rng.randint(1, UNIT_STATS[target.type].defense_die)
        dfn += _defense_bonus(state, battle, def_side)
        if atk > dfn:
            target.hp -= 1
            if target.hp <= 0:
                _kill(state, battle, target)


def resolve_round(state, battle, rng) -> None:
    battle.rounds += 1
    _form_line(battle.att_committed, battle.cap, battle.att_line)
    _form_line(battle.def_committed, battle.cap, battle.def_line)

    def archers(line):
        return [u for u in line if u.type == UnitType.ARCHER]

    def others(line):
        return [u for u in line if u.type != UnitType.ARCHER]  # AL-12

    # 4.2 Archer Pre-Strike: attacker archers first, then defender archers
    _strike(state, battle, archers(battle.att_line), battle.def_line, rng, "def")
    _strike(state, battle, archers(battle.def_line), battle.att_line, rng, "att")
    # 4.3 Attacker Strike, then Defender Counterstrike
    _strike(state, battle, others(battle.att_line), battle.def_line, rng, "def")
    _strike(state, battle, others(battle.def_line), battle.att_line, rng, "att")

    if not battle.def_committed:
        battle.winner = "attacker"
    elif not battle.att_committed:
        battle.winner = "defender"


def enumerate_defender_retreats(state, battle) -> list:
    t = state.tiles[battle.target]
    if t.terrain == Terrain.CITY or t.has(BuildingType.FORTRESS):
        return []  # Combat.md 4.4: no retreat from Cities/Fortresses
    if battle.winner is not None:
        return []
    out = []
    for n in neighbors(battle.target):
        nt = state.tiles.get(n)
        if nt is None or nt.controller != battle.defender:
            continue
        if any(u.owner != battle.defender for u in nt.units):
            continue
        out.append({"type": "retreat", "dest": list(n)})
    return out


def apply_defender_retreat(state, battle, choice) -> None:
    dest = state.tiles[tuple(choice["dest"])]
    for u in list(battle.def_line):
        for origin, cu in list(battle.def_committed):
            if cu is u:
                state.tiles[origin].units.remove(u)
                dest.units.append(u)
                battle.def_committed.remove((origin, cu))
        battle.def_line.remove(u)
    battle.winner = None  # battle simply ends; finish_battle handles the rest
    battle.def_retreated = True


def finish_battle(state, battle) -> None:
    t = state.tiles[battle.target]
    if battle.winner == "attacker":
        t.controller = battle.attacker
        t.siege = False
        state.player(battle.attacker).battle_wins += 1
        # Occupation: move up to cap surviving committed units in (auto-pick
        # by line priority). Buildings are taken over intact (AL-11).
        movers = sorted(battle.att_committed,
                        key=lambda p: (_LINE_PRIORITY[p[1].type], p[1].uid))[:battle.cap]
        for origin, u in movers:
            state.tiles[origin].units.remove(u)
            t.units.append(u)
    elif battle.winner == "defender":
        t.siege = False
        state.player(battle.defender).battle_wins += 1  # AL-10
    else:
        # Undecided: siege marker persists on Cities/Fortresses; otherwise the
        # attack simply ends (attacker units never left their origin hexes).
        t.siege = battle.siege
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_combat.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/combat.py sim/tests/test_combat.py
git commit -m "feat: combat with battle lines, sieges, retreats, and lord capture"
```

---

### Task 10: Production & Upkeep

**Files:**
- Create: `sim/aeonis_sim/engine/production.py`
- Test: `sim/tests/test_production.py`

Rules: `Tiles.md` production, `Population.md` growth, Castle upkeep from `Buildings.md`. **AL-13:** Cities' resource production is "various combinations" in `Tiles.md` — engine rule: Cities produce no Gold/Mana/Influence in Milestone 1 (they contribute +3 Pop Cap, +2 growth, +1 AP via the City AP bonus). **AL-8:** unpaid Castle upkeep suspends the Castle's effects for the round instead of destroying it.

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_production.py`:

```python
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
    # gold 0: even if the mountain's +1 lands before the City in iteration
    # order, 1 < 2 so upkeep is unpayable either way
    p.gold = 0
    run_production(s)
    assert home.castle_suspended is True   # AL-8
    p.gold = 5
    run_production(s)
    assert home.castle_suspended is False
    assert p.gold == 5 - 2 + 1  # paid upkeep, earned mountain gold
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_production.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `production.py`**

`sim/aeonis_sim/engine/production.py`:

```python
from __future__ import annotations

from .types import BuildingType, Terrain

# Tiles.md: base production, upgraded by the matching production building.
_PLAIN = {Terrain.MOUNTAIN: ("gold", 1), Terrain.FOREST: ("mana", 1),
          Terrain.DESERT: ("influence", 1)}
_UPGRADED = {BuildingType.MINE: ("gold", 3), BuildingType.GROVE: ("mana", 3),
             BuildingType.EMBASSY: ("influence", 3)}


def run_production(state) -> None:
    for p in state.players:
        growth = 1  # Population.md base growth
        for t in state.controlled(p.pid):
            # Resource production (AL-13: Cities produce no resources in M1)
            produced = None
            for b in t.buildings:
                if b in _UPGRADED:
                    produced = _UPGRADED[b]
            if produced is None:
                produced = _PLAIN.get(t.terrain)
            if produced:
                setattr(p, produced[0], getattr(p, produced[0]) + produced[1])
            # Population growth contributions
            if t.terrain == Terrain.PLAINS:
                growth += 2 if t.has(BuildingType.FARM) else 1
            elif t.terrain == Terrain.CITY:
                growth += 2
            # Castle upkeep (AL-8: suspend when unpaid)
            if t.has(BuildingType.CASTLE):
                if p.gold >= 2:
                    p.gold -= 2
                    t.castle_suspended = False
                else:
                    t.castle_suspended = True
        room = state.pop_cap(p.pid) - state.pop_used(p.pid) - p.pop_pool
        p.pop_pool += max(0, min(growth, room))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_production.py -v`
Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/production.py sim/tests/test_production.py
git commit -m "feat: production and upkeep phase"
```

---

### Task 11: Cleanup & Checks

**Files:**
- Create: `sim/aeonis_sim/engine/cleanup.py`
- Test: `sim/tests/test_cleanup.py`

Rules: `Round_Structure.md` §7, `Tiles.md` Adjacency Claim (method 5), packet §3.2 Imperial Seat VP, `Victory.md` §5 seat streak, `Combat.md` Lord release. Ledger: **AL-5** objectives auto-score at Cleanup; **AL-9** a released Lord whose Home City is enemy-held returns to the owner's nearest controlled hex without enemy units (stays captured another round if none exists); **AL-14** competing Adjacency Claims by 2+ players leave the hex neutral (Influence bidding arrives with Milestone 2).

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_cleanup.py`:

```python
import random

from aeonis_sim.engine.cleanup import run_cleanup
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain, Unit, UnitType, UNIT_STATS


def make_state():
    return build_initial_state({"players": 3}, random.Random(5))


def test_imperial_seat_vp_and_streak():
    s = make_state()
    for p in s.players:
        p.objective = None  # isolate seat VP from objective auto-scoring
    seat = next(t for t in s.tiles.values() if t.imperial_seat)
    seat.controller = 0
    for expected_vp, expected_streak in ((1, 1), (2, 2), (5, 3)):  # +2 bonus at 3
        run_cleanup(s)
        assert s.players[0].vp == expected_vp
        assert s.players[0].seat_streak == expected_streak
    assert s.players[0].vp_sources["imperial_seat"] == 3
    assert s.players[0].vp_sources["seat_streak_bonus"] == 2


def test_objective_scored_once():
    s = make_state()
    p = s.players[0]
    p.objective = "warlord"
    p.battle_wins = 2
    run_cleanup(s)
    assert p.vp == 2 and p.objective_scored
    run_cleanup(s)
    assert p.vp == 2  # not scored twice


def test_adjacency_claim_two_checks():
    s = make_state()
    p = s.players[0]
    for pl in s.players:
        pl.objective = None
    from aeonis_sim.engine.hexmap import neighbors
    # All in-disk neighbors of a corner home City are cluster tiles (controlled),
    # so manufacture a neutral one by un-claiming a cluster tile.
    neutral = next(c for c in neighbors(p.home)
                   if c in s.tiles and s.tiles[c].controller == p.pid)
    s.tiles[neutral].controller = None
    run_cleanup(s)
    assert s.tiles[neutral].controller is None
    assert s.tiles[neutral].adj_claim == (0, 1)
    run_cleanup(s)
    assert s.tiles[neutral].controller == 0  # second consecutive check


def test_lord_release():
    s = make_state()
    p1 = s.players[1]
    # Capture player 1's lord: remove from map, set flag
    coord, lord = s.find_lord(1)
    s.tiles[coord].units.remove(lord)
    p1.lord_captured = True
    run_cleanup(s)
    assert p1.lord_captured is False
    home_units = s.tiles[p1.home].units
    released = [u for u in home_units if u.type == UnitType.LORD]
    assert len(released) == 1 and released[0].hp == UNIT_STATS[UnitType.LORD].hp


def test_victory_check_sets_final():
    s = make_state()
    s.players[2].add_vp(10, "test")
    run_cleanup(s)
    assert s.final_round is True


def test_round_trackers_reset():
    s = make_state()
    p = s.players[0]
    p.recruited_cities = [p.home]
    p.passed = True
    run_cleanup(s)
    assert p.recruited_cities == [] and p.passed is False
    assert s.round == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_cleanup.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `cleanup.py`**

`sim/aeonis_sim/engine/cleanup.py`:

```python
from __future__ import annotations

from .hexmap import distance, neighbors
from .objectives import OBJECTIVES
from .types import BuildingType, Terrain, Unit, UNIT_STATS, UnitType, VP_THRESHOLD


def _influence_range(state, pid):
    """Hexes within Adjacency-Claim influence: adjacent to a controlled City,
    or within 2 of a controlled Tower (Tiles.md, Borders section)."""
    out = set()
    for t in state.controlled(pid):
        if t.terrain == Terrain.CITY:
            out.update(n for n in neighbors(t.coord) if n in state.tiles)
        if t.has(BuildingType.TOWER):
            out.update(c for c in state.tiles if 0 < distance(c, t.coord) <= 2)
    return out


def _adjacency_claims(state) -> None:
    ranges = {p.pid: _influence_range(state, p.pid) for p in state.players}
    for coord, t in state.tiles.items():
        if t.controller is not None:
            t.adj_claim = None
            continue
        if t.terrain == Terrain.LAKE and not t.has(BuildingType.BRIDGE):
            continue
        eligible = [pid for pid, rng_ in ranges.items()
                    if coord in rng_
                    and not any(u.owner != pid for u in t.units)]
        if len(eligible) != 1:
            t.adj_claim = None  # AL-14: contested claims stay neutral in M1
            continue
        pid = eligible[0]
        if t.adj_claim and t.adj_claim[0] == pid:
            t.controller = pid  # second consecutive check
            t.adj_claim = None
        else:
            t.adj_claim = (pid, 1)


def _release_lords(state) -> None:
    for p in state.players:
        if not p.lord_captured:
            continue
        home = state.tiles[p.home]
        dest = None
        if home.controller == p.pid and not any(u.owner != p.pid for u in home.units):
            dest = home
        else:  # AL-9: nearest controlled hex without enemy units
            cands = [t for t in state.controlled(p.pid)
                     if not any(u.owner != p.pid for u in t.units)]
            if cands:
                dest = min(cands, key=lambda t: (distance(t.coord, p.home), t.coord))
        if dest is None:
            continue  # stays captured; retry next round
        st = UNIT_STATS[UnitType.LORD]
        dest.units.append(Unit(uid=state.new_uid(), owner=p.pid,
                               type=UnitType.LORD, hp=st.hp))
        p.lord_captured = False


def run_cleanup(state) -> None:
    _adjacency_claims(state)
    _release_lords(state)

    for p in state.players:
        # Imperial Seat: +1 VP per round held; +2 bonus at 3 consecutive
        if any(t.imperial_seat for t in state.controlled(p.pid)):
            p.add_vp(1, "imperial_seat")
            p.seat_streak += 1
            if p.seat_streak >= 3 and not p.seat_bonus_scored:
                p.add_vp(2, "seat_streak_bonus")
                p.seat_bonus_scored = True
        else:
            p.seat_streak = 0
        # Objectives (AL-5: auto-score at Cleanup, once per card)
        if p.objective and not p.objective_scored:
            if OBJECTIVES[p.objective](state, p.pid):
                p.add_vp(2, "objective")
                p.objective_scored = True

    if any(p.vp >= VP_THRESHOLD for p in state.players):
        state.final_round = True

    for p in state.players:
        p.recruited_cities = []
        p.passed = False
    state.round += 1
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_cleanup.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/cleanup.py sim/tests/test_cleanup.py
git commit -m "feat: cleanup phase with seat VP, objectives, claims, lord release"
```

---

### Task 12: Game loop (phase machine)

**Files:**
- Create: `sim/aeonis_sim/engine/game.py`
- Test: `sim/tests/test_game_loop.py`

Milestone-1 phase order: Round Start → *(Event, Strategy, Council: no-op stubs)* → Action Phase → Production → Cleanup. Turn order = seating order (no Strategy cards until Milestone 2; note in module docstring). Round Start implements `Actions.md` AP reset and `Tiles.md` control method 1. Guards: round cap 25 (timeout), per-player 100 actions/round (forced pass; degeneracy signal), per-round state-hash repeat (stalled).

- [ ] **Step 1: Write the failing tests**

`sim/tests/test_game_loop.py`:

```python
from aeonis_sim.engine.game import Game


def test_first_decision_is_action_for_player_0():
    g = Game({"players": 3}, seed=11)
    dp = g.next_decision()
    assert dp.kind == "action" and dp.pid == 0
    kinds = {c["type"] for c in dp.choices}
    assert "pass" in kinds and "move" in kinds and "recruit" in kinds


def test_pass_rotates_and_all_pass_advances_round():
    g = Game({"players": 3}, seed=11)
    for expected_pid in (0, 1, 2):
        dp = g.next_decision()
        assert dp.pid == expected_pid
        g.submit({"type": "pass"})
    # All passed -> production + cleanup ran -> round 2, player 0 again
    dp = g.next_decision()
    assert g.state.round == 2 and dp.pid == 0


def test_ap_reset_includes_city_bonus_and_banking():
    g = Game({"players": 3}, seed=11)
    for _ in range(3):
        g.next_decision()
        g.submit({"type": "pass"})   # banks min(ap,2) = 2
    g.next_decision()
    # Round 2 AP: base 5 + banked 2 + city bonus 1 (one City) = 8
    assert g.state.players[0].ap == 8


def test_round_start_flips_occupied_hexes():
    g = Game({"players": 3}, seed=11)
    state = g.state
    p0 = state.players[0]
    # Manufacture: player 0 unit alone on an enemy-controlled hex
    target = next(t for t in state.tiles.values()
                  if t.controller == 1 and not t.units)
    from aeonis_sim.engine.types import Unit, UnitType
    target.units.append(Unit(uid=state.new_uid(), owner=0,
                             type=UnitType.INFANTRY, hp=1))
    for _ in range(3):
        g.next_decision()
        g.submit({"type": "pass"})
    g.next_decision()  # round 2 has begun; Round Start ran
    assert target.controller == 0  # Tiles.md control method 1


def test_submit_rejects_unenumerated_choice():
    g = Game({"players": 3}, seed=11)
    g.next_decision()
    try:
        g.submit({"type": "recruit", "city": [9, 9], "units": ["cavalry"] * 9})
        assert False, "should have raised"
    except ValueError:
        pass


def test_seed_determinism():
    def run(seed):
        g = Game({"players": 3}, seed=seed)
        log = []
        while not g.over and len(log) < 200:
            dp = g.next_decision()
            if dp is None:
                break
            choice = sorted(dp.choices, key=lambda c: str(sorted(c.items())))[0]
            g.submit(choice)
            log.append(choice)
        return log, g.state.to_dict()

    l1, s1 = run(3)
    l2, s2 = run(3)
    assert l1 == l2 and s1 == s2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd sim && python3 -m pytest tests/test_game_loop.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `game.py`**

`sim/aeonis_sim/engine/game.py`:

```python
"""Phase machine (Round_Structure.md).

Milestone 1: Event, Strategy Selection, and High Council phases are no-op
stubs; Action Phase turn order is seating order (Strategy-card initiative
arrives in Milestone 2 / plan B).
"""
from __future__ import annotations

import json
import random
from typing import Optional

from . import combat
from .build import apply_build, enumerate_builds
from .cleanup import run_cleanup
from .invariants import check_invariants
from .move import apply_move, enumerate_moves
from .observations import DecisionPoint
from .production import run_production
from .recruit import apply_recruit, enumerate_recruits
from .setup import build_initial_state
from .types import BASE_AP, BuildingType, DEFAULT_ROUND_CAP, Terrain

MAX_ACTIONS_PER_PLAYER_ROUND = 100


def _canon(choice: dict) -> str:
    return json.dumps(choice, sort_keys=True)


class Game:
    def __init__(self, config: dict, seed: int):
        self.config = dict(config)
        self.seed = seed
        self.rng = random.Random(seed)
        self.state = build_initial_state(config, self.rng)
        self.over = False
        self.verdict: Optional[str] = None
        self.choices_log: list = []
        self.degenerate_flags: list = []
        self._turn_idx = 0
        self._actions_taken: dict = {}
        self._battle: Optional[combat.Battle] = None
        self._battle_stage: Optional[str] = None  # "defender_retreat" | "press"
        self._round_hashes: list = []
        self._pending: Optional[DecisionPoint] = None
        self._round_start()

    # ---- phases ----
    def _round_start(self) -> None:
        s = self.state
        if s.round > DEFAULT_ROUND_CAP:
            self._end("timeout")
            return
        d = s.to_dict()
        d.pop("round")  # only the counter differs in a true stall
        h = json.dumps(d, sort_keys=True)
        if self._round_hashes and self._round_hashes[-1] == h:
            self._end("stalled")
            return
        self._round_hashes.append(h)
        # Tiles.md control method 1: sole-occupier hexes flip at Round Start
        for t in s.tiles.values():
            owners = {u.owner for u in t.units}
            if len(owners) == 1:
                t.controller = owners.pop()
        for p in s.players:
            cities = sum(1 for t in s.controlled(p.pid)
                         if t.terrain == Terrain.CITY)
            guild = sum(1 for t in s.controlled(p.pid)
                        if t.has(BuildingType.GUILD_HALL))
            p.ap = (BASE_AP + p.banked + min(2, cities) + guild
                    + (1 if p.renown >= 5 else 0))
            p.banked = 0
        self._turn_idx = 0
        self._actions_taken = {p.pid: 0 for p in s.players}
        # Event / Strategy / Council: no-ops in Milestone 1.

    def _end(self, verdict: str) -> None:
        self.over = True
        self.verdict = verdict
        self._pending = None

    def _advance_phases(self) -> None:
        """All players have passed: Production, Cleanup, next round or end."""
        run_production(self.state)
        run_cleanup(self.state)
        check_invariants(self.state)
        if self.state.final_round:
            self._end("completed")
            return
        self._round_start()

    # ---- decision loop ----
    def _active_pid(self) -> Optional[int]:
        s = self.state
        n = len(s.players)
        for i in range(n):
            pid = (self._turn_idx + i) % n
            if not s.players[pid].passed:
                self._turn_idx = pid
                return pid
        return None

    def _action_choices(self, pid: int) -> list:
        s = self.state
        if self._actions_taken[pid] >= MAX_ACTIONS_PER_PLAYER_ROUND:
            if "action_cap" not in self.degenerate_flags:
                self.degenerate_flags.append("action_cap")
            return [{"type": "pass"}]
        out = [{"type": "pass"}]
        out.extend(enumerate_moves(s, pid))
        out.extend(enumerate_recruits(s, pid))
        out.extend(enumerate_builds(s, pid))
        out.extend(combat.enumerate_attacks(s, pid))
        return out

    def next_decision(self) -> Optional[DecisionPoint]:
        if self.over:
            return None
        if self._pending is not None:
            return self._pending
        if self._battle is not None:
            self._pending = self._battle_decision()
            if self._pending is not None:
                return self._pending
        pid = self._active_pid()
        if pid is None:
            self._advance_phases()
            return None if self.over else self.next_decision()
        self._pending = DecisionPoint(kind="action", pid=pid,
                                      choices=self._action_choices(pid))
        return self._pending

    def _battle_decision(self) -> Optional[DecisionPoint]:
        b = self._battle
        if b.winner is not None or self._battle_stage == "done":
            combat.finish_battle(self.state, b)
            check_invariants(self.state)
            self._battle = None
            self._battle_stage = None
            return None
        if self._battle_stage == "defender_retreat":
            retreats = combat.enumerate_defender_retreats(self.state, b)
            if retreats:
                return DecisionPoint(kind="defender_retreat", pid=b.defender,
                                     choices=retreats + [{"type": "hold"}],
                                     context={"target": list(b.target)})
            self._battle_stage = "press"
        if self._battle_stage == "press":
            if b.rounds < 2 and self.state.player(b.attacker).ap >= combat.PRESS_AP:
                return DecisionPoint(kind="press", pid=b.attacker,
                                     choices=[{"type": "press"}, {"type": "end"}],
                                     context={"target": list(b.target)})
            self._battle_stage = "done"
            return self._battle_decision()
        return None

    def submit(self, choice: dict) -> None:
        dp = self._pending
        if dp is None:
            raise ValueError("no pending decision")
        if _canon(choice) not in {_canon(c) for c in dp.choices}:
            raise ValueError(f"illegal choice: {choice}")
        self.choices_log.append(choice)
        self._pending = None
        s = self.state
        if dp.kind == "action":
            self._actions_taken[dp.pid] += 1
            t = choice["type"]
            if t == "pass":
                p = s.player(dp.pid)
                p.passed = True
                p.banked = min(2, p.ap)  # Actions.md banking
                self._turn_idx = (dp.pid + 1) % len(s.players)
            elif t == "move":
                apply_move(s, dp.pid, choice)
                self._turn_idx = (dp.pid + 1) % len(s.players)
            elif t == "recruit":
                apply_recruit(s, dp.pid, choice)
                self._turn_idx = (dp.pid + 1) % len(s.players)
            elif t == "build":
                apply_build(s, dp.pid, choice)
                self._turn_idx = (dp.pid + 1) % len(s.players)
            elif t == "attack":
                self._battle = combat.start_battle(s, dp.pid, choice)
                combat.resolve_round(s, self._battle, self.rng)
                self._battle_stage = "defender_retreat"
                self._turn_idx = (dp.pid + 1) % len(s.players)
        elif dp.kind == "defender_retreat":
            if choice["type"] == "retreat":
                combat.apply_defender_retreat(s, self._battle, choice)
                self._battle_stage = "done"
            else:
                self._battle_stage = "press"
        elif dp.kind == "press":
            if choice["type"] == "press":
                s.player(self._battle.attacker).ap -= combat.PRESS_AP
                combat.resolve_round(s, self._battle, self.rng)
                self._battle_stage = "defender_retreat"
            else:
                self._battle_stage = "done"
        check_invariants(s)
```

- [ ] **Step 4: Run tests (they will fail on the missing `invariants` module — implement Task 13's `invariants.py` stub NOW as part of this task if running out of order is a problem; the intended order is: write this file, then immediately do Task 13, then run both test files together)**

The clean sequence:

1. Write `game.py` (this task).
2. Write `invariants.py` + `record.py` and their tests (Task 13).
3. Run: `cd sim && python3 -m pytest tests/test_game_loop.py tests/test_invariants_record.py -v`
Expected: all passed.

- [ ] **Step 5: Commit (after Task 13's files exist and both test files pass)**

```bash
git add sim/aeonis_sim/engine/game.py sim/tests/test_game_loop.py
git commit -m "feat: phase-machine game loop with decision points and guards"
```

---

### Task 13: Invariants and game records

**Files:**
- Create: `sim/aeonis_sim/engine/invariants.py`
- Create: `sim/aeonis_sim/engine/record.py`
- Test: `sim/tests/test_invariants_record.py`

- [ ] **Step 1: Implement `invariants.py`**

`sim/aeonis_sim/engine/invariants.py`:

```python
from __future__ import annotations

from .types import GLOBAL_POP_CAP, UnitType


class InvariantViolation(AssertionError):
    pass


def check_invariants(state) -> None:
    seen_uids = set()
    lords = {}
    for coord, t in state.tiles.items():
        for u in t.units:
            if u.uid in seen_uids:
                raise InvariantViolation(f"duplicate uid {u.uid}")
            seen_uids.add(u.uid)
            if u.hp < 1:
                raise InvariantViolation(f"dead unit on board at {coord}")
            if u.type == UnitType.LORD:
                lords[u.owner] = lords.get(u.owner, 0) + 1
    for pid, n in lords.items():
        if n > 1:
            raise InvariantViolation(f"player {pid} has {n} lords")
    for p in state.players:
        for attr in ("gold", "mana", "influence", "ap", "pop_pool", "vp", "renown"):
            if getattr(p, attr) < 0:
                raise InvariantViolation(f"player {p.pid} negative {attr}")
        if p.lord_captured and state.find_lord(p.pid) is not None:
            raise InvariantViolation(f"player {p.pid} captured lord on board")
        if state.pop_used(p.pid) > GLOBAL_POP_CAP:
            raise InvariantViolation(f"player {p.pid} over global pop cap")
        if sum(p.vp_sources.values()) != p.vp:
            raise InvariantViolation(f"player {p.pid} vp/source mismatch")
```

- [ ] **Step 2: Implement `record.py`**

`sim/aeonis_sim/engine/record.py`:

```python
from __future__ import annotations

import json
from pathlib import Path


def build_record(game) -> dict:
    s = game.state
    return {
        "seed": game.seed,
        "config": game.config,
        "choices": game.choices_log,
        "verdict": game.verdict,
        "degenerate_flags": game.degenerate_flags,
        "rounds": s.round,
        "final_vp": {p.pid: p.vp for p in s.players},
        "vp_sources": {p.pid: p.vp_sources for p in s.players},
        "final_state": s.to_dict(),
    }


def save_record(record: dict, path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def replay(record: dict):
    """Re-run a recorded game; returns the reconstructed Game. Raises if any
    recorded choice is no longer legal (i.e., engine behavior changed)."""
    from .game import Game
    g = Game(record["config"], record["seed"])
    for choice in record["choices"]:
        dp = g.next_decision()
        while dp is None and not g.over:
            dp = g.next_decision()
        if g.over:
            break
        g.submit(choice)
    while not g.over and g.next_decision() is None:
        pass
    return g
```

- [ ] **Step 3: Write the tests**

`sim/tests/test_invariants_record.py`:

```python
import random

import pytest

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.invariants import InvariantViolation, check_invariants
from aeonis_sim.engine.record import build_record, replay
from aeonis_sim.engine.setup import build_initial_state


def test_invariants_pass_on_fresh_state():
    s = build_initial_state({"players": 4}, random.Random(2))
    check_invariants(s)


def test_invariants_catch_negative_gold():
    s = build_initial_state({"players": 3}, random.Random(2))
    s.players[0].gold = -1
    with pytest.raises(InvariantViolation):
        check_invariants(s)


def _play_short_game(seed):
    g = Game({"players": 3}, seed=seed)
    while not g.over:
        dp = g.next_decision()
        if dp is None:
            continue
        # Deterministic policy: first choice in canonical order
        choice = sorted(dp.choices, key=lambda c: str(sorted(c.items())))[0]
        g.submit(choice)
    return g


def test_record_replay_reproduces_final_state():
    g = _play_short_game(21)
    rec = build_record(g)
    g2 = replay(rec)
    assert g2.verdict == g.verdict
    assert g2.state.to_dict() == g.state.to_dict()
```

- [ ] **Step 4: Run the Task 12 + 13 tests together**

Run: `cd sim && python3 -m pytest tests/test_game_loop.py tests/test_invariants_record.py -v`
Expected: all passed (6 + 3). Debug here until green — this is the first time full games run.

- [ ] **Step 5: Commit (both tasks' files)**

```bash
git add sim/aeonis_sim/engine/invariants.py sim/aeonis_sim/engine/record.py sim/tests/test_invariants_record.py
git commit -m "feat: invariant checks and replayable game records"
```

---

### Task 14: Agents and runner

**Files:**
- Create: `sim/aeonis_sim/agents/base.py`
- Create: `sim/aeonis_sim/agents/chaos.py`
- Create: `sim/aeonis_sim/runner/play.py`
- Test: `sim/tests/test_chaos_smoke.py`

- [ ] **Step 1: Write the failing test**

`sim/tests/test_chaos_smoke.py`:

```python
from aeonis_sim.runner.play import play_game


def test_chaos_games_finish_with_verdicts():
    for seed in range(5):
        record = play_game({"players": 3}, seed=seed)
        assert record["verdict"] in ("completed", "timeout", "stalled", "degenerate")
        assert record["rounds"] >= 2


def test_same_seed_same_record():
    r1 = play_game({"players": 4}, seed=99)
    r2 = play_game({"players": 4}, seed=99)
    assert r1 == r2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd sim && python3 -m pytest tests/test_chaos_smoke.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement agents and runner**

`sim/aeonis_sim/agents/base.py`:

```python
from __future__ import annotations

from typing import Protocol


class Agent(Protocol):
    """One seat at the table. Milestone 1: choose() only; reflect() and
    exit_interview() join in plan C (LLM agents)."""

    def choose(self, observation: dict, decision_point) -> dict:
        """Return exactly one of decision_point.choices."""
        ...
```

`sim/aeonis_sim/agents/chaos.py`:

```python
from __future__ import annotations

import random


class ChaosBot:
    """Uniform-random agent for fuzzing the engine. Excluded from balance
    stats by design (see the design spec, Agents section)."""

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def choose(self, observation: dict, decision_point) -> dict:
        return self.rng.choice(decision_point.choices)
```

`sim/aeonis_sim/runner/play.py`:

```python
from __future__ import annotations

import argparse
import json

from ..agents.chaos import ChaosBot
from ..engine.game import Game
from ..engine.observations import observe
from ..engine.record import build_record, save_record

# Degeneracy monitor: no player gains VP for this many consecutive rounds.
NO_VP_ROUNDS_FLAG = 8


def play_game(config: dict, seed: int, agents=None) -> dict:
    game = Game(config, seed)
    if agents is None:
        agents = {p.pid: ChaosBot(seed * 1000 + p.pid)
                  for p in game.state.players}
    last_vp_round, last_vp_total = 1, 0
    while not game.over:
        dp = game.next_decision()
        if dp is None:
            continue
        vp_total = sum(p.vp for p in game.state.players)
        if vp_total > last_vp_total:
            last_vp_total, last_vp_round = vp_total, game.state.round
        elif (game.state.round - last_vp_round >= NO_VP_ROUNDS_FLAG
              and "no_vp_progress" not in game.degenerate_flags):
            game.degenerate_flags.append("no_vp_progress")
        obs = observe(game.state, dp.pid)
        game.submit(agents[dp.pid].choose(obs, dp))
    record = build_record(game)
    if record["verdict"] == "completed" and record["degenerate_flags"]:
        record["verdict"] = "degenerate"
    return record


def main() -> None:
    ap = argparse.ArgumentParser(description="Run chaos-bot Aeonis games")
    ap.add_argument("--players", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--games", type=int, default=1)
    ap.add_argument("--out", default=None, help="JSONL path to append records")
    args = ap.parse_args()
    counts = {}
    for i in range(args.games):
        rec = play_game({"players": args.players}, seed=args.seed + i)
        counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1
        if args.out:
            save_record(rec, args.out)
        print(f"seed={args.seed + i} verdict={rec['verdict']} "
              f"rounds={rec['rounds']} vp={rec['final_vp']}")
    print("verdicts:", counts)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd sim && python3 -m pytest tests/test_chaos_smoke.py -v`
Expected: 2 passed. Chaos games will surface engine bugs the unit tests missed (this is their job) — fix any `InvariantViolation` or crash before proceeding; each fix gets its own commit.

- [ ] **Step 5: Run the full suite**

Run: `cd sim && python3 -m pytest`
Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add sim/aeonis_sim/agents/ sim/aeonis_sim/runner/ sim/tests/test_chaos_smoke.py
git commit -m "feat: agent interface, chaos bot, and game runner"
```

---

### Task 15: Milestone gate — 100-game fuzz run and the Ambiguity Ledger

**Files:**
- Create: `playtest/Ambiguity_Ledger.md`
- Modify: `sim/README.md` (usage section already written in Task 1; update if CLI flags changed)

- [ ] **Step 1: Run the 100-game fuzz gate**

Run: `cd sim && python3 -m aeonis_sim.runner.play --players 4 --seed 1000 --games 100`
Expected: 100 lines of verdicts and a final `verdicts:` summary containing **no crashes** (a crash = Python traceback; `timeout`/`stalled`/`degenerate` verdicts are findings, not failures). If any game crashes, reproduce with its seed, fix, commit the fix, and re-run the full 100 until clean.

- [ ] **Step 2: Record the verdict distribution**

Copy the final `verdicts:` line into the Ambiguity Ledger header (Step 3) as the Milestone-1 baseline. A high `timeout` share is expected — chaos bots don't pursue VP; that's Plan B's persona-bot job to interpret.

- [ ] **Step 3: Write `playtest/Ambiguity_Ledger.md`**

```markdown
# Ambiguity Ledger

Rules questions found while encoding the docs into the simulator
(`sim/`). Each entry: the question, the interpretation the engine uses, and
the doc that should own the canonical answer. Triage by either patching the
owning doc (then the engine) or accepting the engine interpretation into
canon.

**Milestone-1 fuzz baseline (100 chaos games, seeds 1000-1099):** _paste the
verdicts summary from the gate run here_

| ID | Question | Engine interpretation | Owning doc | Status |
|---|---|---|---|---|
| AL-1 | Packet §3.3 says starting Pop Cap 10, but `Population.md` grants +3 cap per City — a starting player (1 City) would exceed 10 with any base ≥ 8. What is the base cap? | Base cap 7, so 1 starting City yields exactly 10 | `Population.md` | Open |
| AL-2 | Movement cost of Ruins hexes is undefined in `Movement.md` §2 | 1 AP (treated as easy terrain) | `Movement.md` | Open |
| AL-3 | (Sim fidelity, not rules) Deserts placed by shuffle, not "between each pair of home clusters" | Positional flavor only in M1 | `First_Playable_Packet.md` | Sim-only |
| AL-4 | Packet §3.3 says "Population Pool: 10 (full at start)" but starting units occupy 4 Population — is the pool 10 or 6? | Starting units consume Population: pool 6 of cap 10 | `First_Playable_Packet.md` | Open |
| AL-5 | When are objectives claimed/scored? No timing window in packet §4.4 or `Victory.md` | Auto-scored at Cleanup & Checks, once per card | `Victory.md` | Open |
| AL-6 | Does building a Bridge on a neutral Lake grant control of the Lake hex? | Yes — builder controls the bridged Lake | `Tiles.md` | Open |
| AL-7 | (Sim bound) Defender choice to Hold the Walls for Cities | M1 auto-declares Hold the Walls (strictly better: City retreat is banned anyway) | `Combat.md` | Sim-only |
| AL-8 | What happens when Castle upkeep (2 Gold) cannot be paid? `Trade_Taxes.md`/`Buildings.md` don't say | Castle effects suspended for the round; building persists | `Buildings.md` | Open |
| AL-9 | Lord release "returns to Home City" — what if the Home City is enemy-held or contains enemy units? | Returns to nearest controlled hex without enemy units; stays captured another round if none | `Combat.md` | Open |
| AL-10 | "Warlord: win 2 battles (attacker or defender)" — what counts as a defender win? | All attacker committed units eliminated | `Combat.md` | Open |
| AL-11 | Captured hex buildings "may be destroyed, downgraded, or taken over, depending on the circumstances" — which? | Taken over intact | `Tiles.md` / `Buildings.md` | Open |
| AL-12 | Do Archers strike again in the main Strike step after their Pre-Strike? | No — Pre-Strike is their strike for the round | `Combat.md` | Open |
| AL-13 | Cities produce "+2 Population and various combinations of resources" — which resources? | No Gold/Mana/Influence in M1 (cap, growth, and AP bonuses only) | `Tiles.md` | Open |
| AL-14 | Competing Adjacency Claims resolve by Influence bidding — a decision the M1 bots can't make | Contested claims stay neutral in M1 | `Tiles.md` | Sim-only |
```

- [ ] **Step 4: Update `sim/README.md` if needed**

Confirm the CLI example matches the implemented flags (`--players --seed --games --out`). Fix if drifted.

- [ ] **Step 5: Final full test run and commit**

Run: `cd sim && python3 -m pytest`
Expected: all tests pass.

```bash
git add playtest/Ambiguity_Ledger.md sim/README.md
git commit -m "feat: ambiguity ledger with Milestone-1 rulings and fuzz baseline"
```

---

## Follow-on plans (not in this document)

- **Plan B — Persona bots + balance reports:** heuristic scoring bots (Warmonger/Economist/Expander/Diplomat/Balanced), tournament configs, parallel bulk runs, the balance summary + session-log + verdict-breakdown reports, Strategy cards + Council (engine Milestone 2).
- **Plan C — LLM agents:** provider layer (Cursor SDK / direct API / Ollama), rules digests, annotations, reflections, exit interviews, playtest reports, sentiment digest.
- **Plan D — Content milestones 3–4:** Whispers, Events, Artifacts, Arcane Tier I, secret objectives, the 8 Lord sheets, negotiation protocol.

Sequencing note: Plan B before Plan C — LLM agents are only worth their cost once the engine survives persona-bot play, and personas provide the fallback policy LLM agents degrade to.

