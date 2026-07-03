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
