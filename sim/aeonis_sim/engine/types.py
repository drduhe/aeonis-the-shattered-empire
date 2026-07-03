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
# per City. Canon (AL-1, Population.md): base cap 7 + 3 per controlled City = 10 at start.
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
    # Ongoing siege: unit uids still committed between Attack actions (Combat.md §6.4).
    siege_att_uids: list = field(default_factory=list)
    siege_def_uids: list = field(default_factory=list)

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
            "siege_att_uids": list(self.siege_att_uids),
            "siege_def_uids": list(self.siege_def_uids),
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
            siege_att_uids=list(d.get("siege_att_uids", [])),
            siege_def_uids=list(d.get("siege_def_uids", [])),
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
    secret_objective: Optional[str] = None
    secret_scored: bool = False
    shared_scored: list = field(default_factory=list)   # public objective ids scored
    public_scored_this_round: bool = False
    battle_wins: int = 0
    used_portal_travel: bool = False
    lord_captured: bool = False
    rite_count: int = 0
    rite_bonus_scored: bool = False
    recruited_cities: list = field(default_factory=list)  # list[Coord] this round
    vp_sources: dict = field(default_factory=dict)         # source -> total VP
    held_cards: list = field(default_factory=list)         # strategy card ids this round
    primary_used: list = field(default_factory=list)       # card ids
    secondary_used: list = field(default_factory=list)     # card ids
    pending_ap: int = 0                                    # Event-granted AP next round

    def add_vp(self, n: int, source: str) -> None:
        self.vp += n
        self.vp_sources[source] = self.vp_sources.get(source, 0) + n

    def to_dict(self) -> dict:
        return {
            "pid": self.pid, "home": list(self.home), "ap": self.ap, "banked": self.banked,
            "gold": self.gold, "mana": self.mana, "influence": self.influence,
            "renown": self.renown, "vp": self.vp, "pop_pool": self.pop_pool,
            "passed": self.passed,
            "secret_objective": self.secret_objective,
            "secret_scored": self.secret_scored,
            "shared_scored": list(self.shared_scored),
            "public_scored_this_round": self.public_scored_this_round,
            "battle_wins": self.battle_wins,
            "used_portal_travel": self.used_portal_travel,
            "lord_captured": self.lord_captured,
            "rite_count": self.rite_count,
            "rite_bonus_scored": self.rite_bonus_scored,
            "recruited_cities": [list(c) for c in self.recruited_cities],
            "vp_sources": dict(self.vp_sources),
            "held_cards": list(self.held_cards),
            "primary_used": list(self.primary_used),
            "secondary_used": list(self.secondary_used),
            "pending_ap": self.pending_ap,
        }

    @staticmethod
    def from_dict(d: dict) -> "PlayerState":
        p = PlayerState(pid=d["pid"], home=tuple(d["home"]))
        if "secret_objective" in d:
            for k in ("ap", "banked", "gold", "mana", "influence", "renown", "vp", "pop_pool",
                      "passed", "secret_objective", "secret_scored", "public_scored_this_round",
                      "battle_wins", "used_portal_travel", "lord_captured",
                      "rite_count", "rite_bonus_scored"):
                setattr(p, k, d[k])
            p.shared_scored = list(d.get("shared_scored", []))
        else:
            # Legacy pre-Plan-3-MVP records
            for k in ("ap", "banked", "gold", "mana", "influence", "renown", "vp", "pop_pool",
                      "passed", "battle_wins", "used_portal_travel", "lord_captured"):
                setattr(p, k, d[k])
            p.secret_objective = d.get("objective")
            p.secret_scored = d.get("objective_scored", False)
            p.shared_scored = []
            p.public_scored_this_round = False
            p.rite_count = d.get("seat_streak", 0)
            p.rite_bonus_scored = d.get("seat_bonus_scored", False)
        p.recruited_cities = [tuple(c) for c in d["recruited_cities"]]
        p.vp_sources = dict(d["vp_sources"])
        p.held_cards = list(d.get("held_cards", []))
        p.primary_used = list(d.get("primary_used", []))
        p.secondary_used = list(d.get("secondary_used", []))
        p.pending_ap = int(d.get("pending_ap", 0))
        return p


@dataclass
class GameState:
    players: list                         # list[PlayerState]
    tiles: dict                           # dict[Coord, Tile]
    round: int = 1
    final_round: bool = False
    next_uid: int = 1
    shared_public_revealed: list = field(default_factory=list)  # objective ids
    shared_public_deck: list = field(default_factory=list)
    # Plan 1 combat ladder (PROPOSED; toggled via config["combat"]).
    # aggressors_edge_mode: "off" | "full" | "pre_strike"
    aggressors_edge_mode: str = "off"
    pillage: bool = False
    # Plan 2 AP economy (PROPOSED; toggled via config["ap_economy"]).
    ap_bonus_cap: Optional[int] = None  # e.g. 2 = unified +2 cap
    rally: bool = False  # +1 AP to lowest VP at Round Start (ignores cap)
    speaker: int = 0
    strategy_pool: list = field(default_factory=list)      # undrafted card ids
    strategy_bounty: dict = field(default_factory=dict)    # card id -> accumulated gold
    event_deck: list = field(default_factory=list)
    event_discard: list = field(default_factory=list)
    last_event_id: Optional[str] = None
    agenda_deck: list = field(default_factory=list)
    agenda_revealed: Optional[str] = None
    active_laws: list = field(default_factory=list)
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
            "shared_public_revealed": list(self.shared_public_revealed),
            "shared_public_deck": list(self.shared_public_deck),
            "speaker": self.speaker,
            "strategy_pool": list(self.strategy_pool),
            "strategy_bounty": dict(self.strategy_bounty),
            "event_deck": list(self.event_deck),
            "event_discard": list(self.event_discard),
            "last_event_id": self.last_event_id,
            "agenda_deck": list(self.agenda_deck),
            "agenda_revealed": self.agenda_revealed,
            "active_laws": list(self.active_laws),
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
            shared_public_revealed=list(d.get("shared_public_revealed", [])),
            shared_public_deck=list(d.get("shared_public_deck", [])),
            speaker=d.get("speaker", 0),
            strategy_pool=list(d.get("strategy_pool", [])),
            strategy_bounty=dict(d.get("strategy_bounty", {})),
            event_deck=list(d.get("event_deck", [])),
            event_discard=list(d.get("event_discard", [])),
            last_event_id=d.get("last_event_id"),
            agenda_deck=list(d.get("agenda_deck", [])),
            agenda_revealed=d.get("agenda_revealed"),
            active_laws=list(d.get("active_laws", [])),
        )

    def copy(self) -> "GameState":
        """Independent clone for persona 1-ply lookahead."""
        tiles = {
            coord: Tile(
                coord=tile.coord,
                terrain=tile.terrain,
                imperial_seat=tile.imperial_seat,
                controller=tile.controller,
                units=[
                    Unit(uid=u.uid, owner=u.owner, type=u.type, hp=u.hp)
                    for u in tile.units
                ],
                buildings=list(tile.buildings),
                siege=tile.siege,
                adj_claim=tile.adj_claim,
                castle_suspended=tile.castle_suspended,
                siege_att_uids=list(tile.siege_att_uids),
                siege_def_uids=list(tile.siege_def_uids),
            )
            for coord, tile in self.tiles.items()
        }
        players = [
            PlayerState(
                pid=p.pid,
                home=p.home,
                ap=p.ap,
                banked=p.banked,
                gold=p.gold,
                mana=p.mana,
                influence=p.influence,
                renown=p.renown,
                vp=p.vp,
                pop_pool=p.pop_pool,
                passed=p.passed,
                secret_objective=p.secret_objective,
                secret_scored=p.secret_scored,
                shared_scored=list(p.shared_scored),
                public_scored_this_round=p.public_scored_this_round,
                battle_wins=p.battle_wins,
                used_portal_travel=p.used_portal_travel,
                lord_captured=p.lord_captured,
                rite_count=p.rite_count,
                rite_bonus_scored=p.rite_bonus_scored,
                recruited_cities=list(p.recruited_cities),
                vp_sources=dict(p.vp_sources),
                held_cards=list(p.held_cards),
                primary_used=list(p.primary_used),
                secondary_used=list(p.secondary_used),
                pending_ap=p.pending_ap,
            )
            for p in self.players
        ]
        return GameState(
            players=players,
            tiles=tiles,
            round=self.round,
            final_round=self.final_round,
            next_uid=self.next_uid,
            shared_public_revealed=list(self.shared_public_revealed),
            shared_public_deck=list(self.shared_public_deck),
            aggressors_edge_mode=self.aggressors_edge_mode,
            pillage=self.pillage,
            ap_bonus_cap=self.ap_bonus_cap,
            rally=self.rally,
            speaker=self.speaker,
            strategy_pool=list(self.strategy_pool),
            strategy_bounty=dict(self.strategy_bounty),
            event_deck=list(self.event_deck),
            event_discard=list(self.event_discard),
            last_event_id=self.last_event_id,
            agenda_deck=list(self.agenda_deck),
            agenda_revealed=self.agenda_revealed,
            active_laws=list(self.active_laws),
        )
