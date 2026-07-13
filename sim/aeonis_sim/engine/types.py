from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

Coord = tuple  # axial (q, r)

# --- Global constants (First_Playable_Packet.md / Victory.md / Population.md) ---
VP_THRESHOLD = 10  # canon default; override per-game via GameState.vp_threshold (Plan 3 pacing)
FRONTIER_LORD_MIN_HEXES = 7  # canon default; override via GameState (H7 Lever B experiment)
PUBLIC_OBJECTIVE_VP = 2  # canon default for public row cards
SEAT_OF_EMPIRE_VP = 2  # canon default; override via GameState (seat sweep S1)
MERCHANT_LORD_MIN_GOLD = 8  # canon default; early-economy E1 (config["economy"])
BUILDER_MIN_BUILDINGS = 3  # canon default; early-economy E2 (config["economy"])
TIER1_PRODUCTION_BUILD_AP = 3  # Farm/Mine/Grove/Embassy; early-economy E5 (config["economy"])
DEFAULT_BUILD_AP = 3  # all other buildings (Actions.md)
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
    FORGE = "forge"
    ACADEMY = "academy"
    BANK = "bank"
    MARKET = "market"
    CASTLE = "castle"
    GRAND_EXCHANGE = "grand_exchange"
    ARCANE_SANCTUM = "arcane_sanctum"
    IRON_CITADEL = "iron_citadel"
    HEARTWOOD_SANCTUM = "heartwood_sanctum"
    WINDSWORN_WARCAMP = "windsworn_warcamp"
    HALL_OF_WHISPERS = "hall_of_whispers"
    CATHEDRAL_OF_RADIANCE = "cathedral_of_radiance"
    DIMENSIONAL_NEXUS = "dimensional_nexus"


LEGENDARY_BUILDINGS = frozenset({
    BuildingType.GRAND_EXCHANGE,
    BuildingType.ARCANE_SANCTUM,
    BuildingType.IRON_CITADEL,
    BuildingType.HEARTWOOD_SANCTUM,
    BuildingType.WINDSWORN_WARCAMP,
    BuildingType.HALL_OF_WHISPERS,
    BuildingType.CATHEDRAL_OF_RADIANCE,
    BuildingType.DIMENSIONAL_NEXUS,
})


@dataclass(frozen=True)
class BuildingSpec:
    terrain: Optional[Terrain]  # None = any land terrain
    gold: int = 0
    mana: int = 0
    influence: int = 0
    pop: int = 0
    upkeep_gold: int = 0
    upkeep_mana: int = 0


# Buildings.md standard roster (M3 Task 1 completes Forge/Academy/Bank/Market).
# Legendary capstones stay M4 (Lord sheets). Academy's Arcane effect activates
# with M3 Task 4 (Research); the building itself costs/upkeeps now.
BUILDING_SPECS = {
    BuildingType.FARM: BuildingSpec(Terrain.PLAINS, gold=2, pop=1),
    BuildingType.MINE: BuildingSpec(Terrain.MOUNTAIN, gold=3, pop=1),
    BuildingType.GROVE: BuildingSpec(Terrain.FOREST, mana=2, pop=1),
    BuildingType.EMBASSY: BuildingSpec(Terrain.DESERT, influence=3, pop=1),
    BuildingType.TOWER: BuildingSpec(None, gold=4, pop=1),
    BuildingType.FORTRESS: BuildingSpec(None, gold=5, mana=2, pop=2),
    BuildingType.BRIDGE: BuildingSpec(Terrain.LAKE, gold=4, pop=0),
    BuildingType.GUILD_HALL: BuildingSpec(Terrain.CITY, gold=4, influence=2, pop=1),
    BuildingType.FORGE: BuildingSpec(Terrain.CITY, gold=5, pop=1, upkeep_mana=1),
    BuildingType.ACADEMY: BuildingSpec(Terrain.CITY, gold=4, mana=3, pop=2,
                                       upkeep_mana=1),
    BuildingType.BANK: BuildingSpec(Terrain.CITY, gold=5, pop=1),
    BuildingType.MARKET: BuildingSpec(Terrain.CITY, gold=2, influence=2, pop=1),
    BuildingType.CASTLE: BuildingSpec(Terrain.CITY, gold=6, pop=2, upkeep_gold=2),
    BuildingType.GRAND_EXCHANGE: BuildingSpec(Terrain.CITY, gold=6, influence=3, pop=3),
    BuildingType.ARCANE_SANCTUM: BuildingSpec(Terrain.CITY, gold=4, mana=6, pop=3),
    BuildingType.IRON_CITADEL: BuildingSpec(
        Terrain.CITY, gold=8, mana=2, pop=3, upkeep_gold=2,
    ),
    BuildingType.HEARTWOOD_SANCTUM: BuildingSpec(
        Terrain.CITY, gold=3, mana=4, influence=2, pop=3,
    ),
    BuildingType.WINDSWORN_WARCAMP: BuildingSpec(Terrain.CITY, gold=5, influence=3, pop=3),
    BuildingType.HALL_OF_WHISPERS: BuildingSpec(
        Terrain.CITY, gold=4, mana=4, influence=2, pop=3,
    ),
    BuildingType.CATHEDRAL_OF_RADIANCE: BuildingSpec(
        Terrain.CITY, gold=4, mana=3, influence=3, pop=3,
    ),
    BuildingType.DIMENSIONAL_NEXUS: BuildingSpec(Terrain.CITY, gold=5, mana=5, pop=3),
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
    # Mana-upkeep buildings with unpaid upkeep this round (AL-8 pattern
    # generalized for Forge/Academy). Stores BuildingType values.
    suspended: list = field(default_factory=list)
    # Ongoing siege: unit uids still committed between Attack actions (Combat.md §6.4).
    siege_att_uids: list = field(default_factory=list)
    siege_def_uids: list = field(default_factory=list)
    explored: bool = False
    cursed: bool = False
    building_relic: Optional[str] = None  # artifact id attached to a building here
    unique_tile_id: str = ""  # M4 launch-Lord starting tile id
    void_anchor_until_round: int = 0  # Thal'rik Void Anchor: owner-only portal this round

    def has(self, b: BuildingType) -> bool:
        return b in self.buildings

    def active(self, b: BuildingType) -> bool:
        """Building present and its upkeep paid this round."""
        if b not in self.buildings:
            return False
        if b == BuildingType.CASTLE:
            return not self.castle_suspended
        return b.value not in self.suspended

    def to_dict(self) -> dict:
        out = {
            "coord": list(self.coord),
            "terrain": self.terrain.value,
            "imperial_seat": self.imperial_seat,
            "controller": self.controller,
            "units": [u.to_dict() for u in self.units],
            "buildings": [b.value for b in self.buildings],
            "siege": self.siege,
            "adj_claim": list(self.adj_claim) if self.adj_claim else None,
            "castle_suspended": self.castle_suspended,
            "suspended": list(self.suspended),
            "siege_att_uids": list(self.siege_att_uids),
            "siege_def_uids": list(self.siege_def_uids),
            "explored": self.explored,
            "cursed": self.cursed,
            "building_relic": self.building_relic,
        }
        if self.unique_tile_id:
            out["unique_tile_id"] = self.unique_tile_id
        if self.void_anchor_until_round:
            out["void_anchor_until_round"] = self.void_anchor_until_round
        return out

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
            suspended=list(d.get("suspended", [])),
            siege_att_uids=list(d.get("siege_att_uids", [])),
            siege_def_uids=list(d.get("siege_def_uids", [])),
            explored=bool(d.get("explored", True)),
            cursed=bool(d.get("cursed", False)),
            building_relic=d.get("building_relic"),
            unique_tile_id=str(d.get("unique_tile_id") or ""),
            void_anchor_until_round=int(d.get("void_anchor_until_round") or 0),
        )


@dataclass
class PlayerState:
    pid: int
    home: Coord
    lord_id: str = ""
    lord_round: dict = field(default_factory=dict)
    lord_game: dict = field(default_factory=dict)  # once-per-game Lord ability flags
    ap: int = 0
    banked: int = 0
    gold: int = 0
    mana: int = 0
    influence: int = 0
    renown: int = 0
    vp: int = 0
    pop_pool: int = 0
    passed: bool = False
    secret_objectives: list = field(default_factory=list)  # unscored secret ids held
    secrets_scored: list = field(default_factory=list)     # scored secret ids
    fortress_built: list = field(default_factory=list)     # coords where pid built Fortress
    battle_wins_at: list = field(default_factory=list)     # hexes where pid won a battle
    influence_hex_gains: list = field(default_factory=list)  # hexes gained via Influence council
    shared_scored: list = field(default_factory=list)   # public objective ids scored
    public_objective_progress: dict = field(default_factory=dict)  # revealed cumulative public cards
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
    remnants: int = 0
    portal_instability_free: bool = False  # one 0-AP portal move (AL-29)
    lord_equipment: list = field(default_factory=list)   # artifact ids, max 2
    utilities: list = field(default_factory=list)
    pending_building_relic: Optional[str] = None
    discoveries: list = field(default_factory=list)   # Tier I+ discovery ids owned
    arcane_round: dict = field(default_factory=dict)  # per-round discovery flags
    whisper_hand: list = field(default_factory=list)
    whisper_flags: dict = field(default_factory=dict)
    pending_whisper_draws: int = 0
    shadow_sight_tokens: int = 0  # AL-51: Nyxara Shadow Sight information tokens
    sacred_rite_5: bool = False
    sacred_rite_10: bool = False
    attacker_battle_wins: int = 0  # M4 Warcamp prereq
    whispers_played: int = 0  # M4 Hall of Whispers prereq

    def add_vp(self, n: int, source: str) -> None:
        self.vp += n
        self.vp_sources[source] = self.vp_sources.get(source, 0) + n
        if n > 0:
            self.pending_whisper_draws += 1

    def to_dict(self) -> dict:
        out = {
            "pid": self.pid, "home": list(self.home), "ap": self.ap, "banked": self.banked,
            "gold": self.gold, "mana": self.mana, "influence": self.influence,
            "renown": self.renown, "vp": self.vp, "pop_pool": self.pop_pool,
            "passed": self.passed,
            "secret_objectives": list(self.secret_objectives),
            "secrets_scored": list(self.secrets_scored),
            "fortress_built": [list(c) for c in self.fortress_built],
            "battle_wins_at": [list(c) for c in self.battle_wins_at],
            "influence_hex_gains": [list(c) for c in self.influence_hex_gains],
            "shared_scored": list(self.shared_scored),
            "public_objective_progress": dict(self.public_objective_progress),
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
            "remnants": self.remnants,
            "portal_instability_free": self.portal_instability_free,
            "lord_equipment": list(self.lord_equipment),
            "utilities": list(self.utilities),
            "pending_building_relic": self.pending_building_relic,
            "discoveries": list(self.discoveries),
            "arcane_round": dict(self.arcane_round),
            "whisper_hand": list(self.whisper_hand),
            "whisper_flags": dict(self.whisper_flags),
            "pending_whisper_draws": self.pending_whisper_draws,
        }
        if self.shadow_sight_tokens:
            out["shadow_sight_tokens"] = self.shadow_sight_tokens
        if self.sacred_rite_5:
            out["sacred_rite_5"] = self.sacred_rite_5
        if self.sacred_rite_10:
            out["sacred_rite_10"] = self.sacred_rite_10
        # Keep pre-M4 records byte-stable when the opt-in layer is disabled.
        if self.lord_id:
            out["lord_id"] = self.lord_id
            out["lord_round"] = dict(self.lord_round)
            if self.lord_game:
                out["lord_game"] = dict(self.lord_game)
            if self.attacker_battle_wins:
                out["attacker_battle_wins"] = self.attacker_battle_wins
            if self.whispers_played:
                out["whispers_played"] = self.whispers_played
        return out

    @staticmethod
    def from_dict(d: dict) -> "PlayerState":
        p = PlayerState(pid=d["pid"], home=tuple(d["home"]))
        p.lord_id = str(d.get("lord_id", ""))
        p.lord_round = dict(d.get("lord_round", {}))
        p.lord_game = dict(d.get("lord_game", {}))
        if "secret_objectives" in d:
            for k in ("ap", "banked", "gold", "mana", "influence", "renown", "vp", "pop_pool",
                      "passed", "public_scored_this_round",
                      "battle_wins", "used_portal_travel", "lord_captured",
                      "rite_count", "rite_bonus_scored"):
                setattr(p, k, d[k])
            p.secret_objectives = list(d.get("secret_objectives", []))
            p.secrets_scored = list(d.get("secrets_scored", []))
            p.fortress_built = [tuple(c) for c in d.get("fortress_built", [])]
            p.battle_wins_at = [tuple(c) for c in d.get("battle_wins_at", [])]
            p.influence_hex_gains = [tuple(c) for c in d.get("influence_hex_gains", [])]
            p.shared_scored = list(d.get("shared_scored", []))
            p.public_objective_progress = dict(d.get("public_objective_progress", {}))
        elif "secret_objective" in d:
            for k in ("ap", "banked", "gold", "mana", "influence", "renown", "vp", "pop_pool",
                      "passed", "public_scored_this_round",
                      "battle_wins", "used_portal_travel", "lord_captured",
                      "rite_count", "rite_bonus_scored"):
                setattr(p, k, d[k])
            if d.get("secret_objective"):
                p.secret_objectives = [d["secret_objective"]]
            if d.get("secret_scored") and p.secret_objectives:
                p.secrets_scored = [p.secret_objectives[0]]
                p.secret_objectives = []
            p.shared_scored = list(d.get("shared_scored", []))
        else:
            # Legacy pre-Plan-3-MVP records
            for k in ("ap", "banked", "gold", "mana", "influence", "renown", "vp", "pop_pool",
                      "passed", "battle_wins", "used_portal_travel", "lord_captured"):
                setattr(p, k, d[k])
            if d.get("objective"):
                p.secret_objectives = [d["objective"]]
            if d.get("objective_scored") and p.secret_objectives:
                p.secrets_scored = [p.secret_objectives[0]]
                p.secret_objectives = []
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
        p.remnants = int(d.get("remnants", 0))
        p.portal_instability_free = bool(d.get("portal_instability_free", False))
        p.lord_equipment = list(d.get("lord_equipment", []))
        p.utilities = list(d.get("utilities", []))
        p.pending_building_relic = d.get("pending_building_relic")
        p.discoveries = list(d.get("discoveries", []))
        p.arcane_round = dict(d.get("arcane_round", {}))
        p.whisper_hand = list(d.get("whisper_hand", []))
        p.whisper_flags = dict(d.get("whisper_flags", {}))
        p.pending_whisper_draws = int(d.get("pending_whisper_draws", 0))
        p.shadow_sight_tokens = int(d.get("shadow_sight_tokens", 0))
        p.sacred_rite_5 = bool(d.get("sacred_rite_5", False))
        p.sacred_rite_10 = bool(d.get("sacred_rite_10", False))
        p.attacker_battle_wins = int(d.get("attacker_battle_wins", 0))
        p.whispers_played = int(d.get("whispers_played", 0))
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
    shared_public_stage_two: list = field(default_factory=list)
    # Plan 1 combat ladder (PROPOSED; toggled via config["combat"]).
    # aggressors_edge_mode: "off" | "full" | "pre_strike"
    aggressors_edge_mode: str = "off"
    pillage: bool = False
    # Plan 2 AP economy (PROPOSED; toggled via config["ap_economy"]).
    ap_bonus_cap: Optional[int] = None  # e.g. 2 = unified +2 cap
    rally: bool = False  # +1 AP to lowest VP at Round Start (ignores cap)
    vp_threshold: int = VP_THRESHOLD  # Plan 3 pacing experiment (config["pacing"])
    frontier_lord_min_hexes: int = FRONTIER_LORD_MIN_HEXES  # Lever B row tempo (config["objectives"])
    seat_of_empire_vp: int = SEAT_OF_EMPIRE_VP  # Seat sweep S1 (config["seat_rewards"])
    merchant_lord_min_gold: int = MERCHANT_LORD_MIN_GOLD  # Early economy E1 (config["economy"])
    builder_min_buildings: int = BUILDER_MIN_BUILDINGS  # Early economy E2 (config["economy"])
    tier1_production_build_ap: int = TIER1_PRODUCTION_BUILD_AP  # Early economy E5 (config["economy"])
    speaker: int = 0
    strategy_pool: list = field(default_factory=list)      # undrafted card ids
    strategy_bounty: dict = field(default_factory=dict)    # card id -> accumulated gold
    event_deck: list = field(default_factory=list)
    event_discard: list = field(default_factory=list)
    last_event_id: Optional[str] = None
    agenda_deck: list = field(default_factory=list)
    agenda_revealed: Optional[str] = None
    active_laws: list = field(default_factory=list)
    open_roads: bool = False
    council_crisis: bool = False
    exploration_deck: list = field(default_factory=list)
    exploration_discard: list = field(default_factory=list)
    artifact_sites: dict = field(default_factory=dict)  # "q,r" -> {card_id, owner}
    artifact_deck: list = field(default_factory=list)
    secret_objective_deck: list = field(default_factory=list)
    secret_objective_discard: list = field(default_factory=list)
    pending_winds_draws: list = field(default_factory=list)
    whisper_deck: list = field(default_factory=list)
    whisper_discard: list = field(default_factory=list)
    desert_tempest: Optional[dict] = None  # {coord, round, owner}
    trades_this_round: int = 0  # M4 Grand Exchange production tracker
    # Plan 3 score-once: card_id -> pids who already scored that VP artifact (cap 2).
    artifact_vp_awarded: dict = field(default_factory=dict)
    # Legendary building type value -> scored construction VP.
    legendary_build_vp_awarded: set = field(default_factory=set)
    # "building_type:pid" -> scored capture VP.
    legendary_capture_vp_awarded: set = field(default_factory=set)

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
        out = {
            "players": [p.to_dict() for p in self.players],
            "tiles": {f"{c[0]},{c[1]}": t.to_dict() for c, t in self.tiles.items()},
            "round": self.round,
            "final_round": self.final_round,
            "next_uid": self.next_uid,
            "shared_public_revealed": list(self.shared_public_revealed),
            "shared_public_deck": list(self.shared_public_deck),
            "shared_public_stage_two": list(self.shared_public_stage_two),
            "speaker": self.speaker,
            "strategy_pool": list(self.strategy_pool),
            "strategy_bounty": dict(self.strategy_bounty),
            "event_deck": list(self.event_deck),
            "event_discard": list(self.event_discard),
            "last_event_id": self.last_event_id,
            "agenda_deck": list(self.agenda_deck),
            "agenda_revealed": self.agenda_revealed,
            "active_laws": list(self.active_laws),
            "open_roads": self.open_roads,
            "council_crisis": self.council_crisis,
            "exploration_deck": list(self.exploration_deck),
            "exploration_discard": list(self.exploration_discard),
            "artifact_sites": dict(self.artifact_sites),
            "artifact_deck": list(self.artifact_deck),
            "secret_objective_deck": list(self.secret_objective_deck),
            "secret_objective_discard": list(self.secret_objective_discard),
            "pending_winds_draws": list(self.pending_winds_draws),
            "whisper_deck": list(self.whisper_deck),
            "whisper_discard": list(self.whisper_discard),
            "artifact_vp_awarded": {
                k: list(v) for k, v in self.artifact_vp_awarded.items()
            },
            "legendary_build_vp_awarded": sorted(self.legendary_build_vp_awarded),
            "legendary_capture_vp_awarded": sorted(self.legendary_capture_vp_awarded),
        }
        if self.desert_tempest:
            out["desert_tempest"] = dict(self.desert_tempest)
        return out

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
            shared_public_stage_two=list(d.get("shared_public_stage_two", [])),
            speaker=d.get("speaker", 0),
            strategy_pool=list(d.get("strategy_pool", [])),
            strategy_bounty=dict(d.get("strategy_bounty", {})),
            event_deck=list(d.get("event_deck", [])),
            event_discard=list(d.get("event_discard", [])),
            last_event_id=d.get("last_event_id"),
            agenda_deck=list(d.get("agenda_deck", [])),
            agenda_revealed=d.get("agenda_revealed"),
            active_laws=list(d.get("active_laws", [])),
            open_roads=bool(d.get("open_roads", False)),
            council_crisis=bool(d.get("council_crisis", False)),
            exploration_deck=list(d.get("exploration_deck", [])),
            exploration_discard=list(d.get("exploration_discard", [])),
            artifact_sites=dict(d.get("artifact_sites", {})),
            artifact_deck=list(d.get("artifact_deck", [])),
            secret_objective_deck=list(d.get("secret_objective_deck", [])),
            secret_objective_discard=list(d.get("secret_objective_discard", [])),
            pending_winds_draws=list(d.get("pending_winds_draws", [])),
            whisper_deck=list(d.get("whisper_deck", [])),
            whisper_discard=list(d.get("whisper_discard", [])),
            desert_tempest=dict(d["desert_tempest"]) if d.get("desert_tempest") else None,
            trades_this_round=int(d.get("trades_this_round", 0)),
            artifact_vp_awarded={
                k: list(v) for k, v in dict(d.get("artifact_vp_awarded", {})).items()
            },
            legendary_build_vp_awarded=set(d.get("legendary_build_vp_awarded", [])),
            legendary_capture_vp_awarded=set(d.get("legendary_capture_vp_awarded", [])),
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
                suspended=list(tile.suspended),
                siege_att_uids=list(tile.siege_att_uids),
                siege_def_uids=list(tile.siege_def_uids),
                explored=tile.explored,
                cursed=tile.cursed,
                building_relic=tile.building_relic,
                unique_tile_id=tile.unique_tile_id,
                void_anchor_until_round=tile.void_anchor_until_round,
            )
            for coord, tile in self.tiles.items()
        }
        players = [
            PlayerState(
                pid=p.pid,
                home=p.home,
                lord_id=p.lord_id,
                lord_round=dict(p.lord_round),
                lord_game=dict(p.lord_game),
                ap=p.ap,
                banked=p.banked,
                gold=p.gold,
                mana=p.mana,
                influence=p.influence,
                renown=p.renown,
                vp=p.vp,
                pop_pool=p.pop_pool,
                passed=p.passed,
                secret_objectives=list(p.secret_objectives),
                secrets_scored=list(p.secrets_scored),
                fortress_built=list(p.fortress_built),
                battle_wins_at=list(p.battle_wins_at),
                influence_hex_gains=list(p.influence_hex_gains),
                shared_scored=list(p.shared_scored),
                public_objective_progress=dict(p.public_objective_progress),
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
                remnants=p.remnants,
                portal_instability_free=p.portal_instability_free,
                lord_equipment=list(p.lord_equipment),
                utilities=list(p.utilities),
                pending_building_relic=p.pending_building_relic,
                discoveries=list(p.discoveries),
                arcane_round=dict(p.arcane_round),
                whisper_hand=list(p.whisper_hand),
                whisper_flags=dict(p.whisper_flags),
                pending_whisper_draws=p.pending_whisper_draws,
                shadow_sight_tokens=p.shadow_sight_tokens,
                sacred_rite_5=p.sacred_rite_5,
                sacred_rite_10=p.sacred_rite_10,
                attacker_battle_wins=p.attacker_battle_wins,
                whispers_played=p.whispers_played,
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
            shared_public_stage_two=list(self.shared_public_stage_two),
            aggressors_edge_mode=self.aggressors_edge_mode,
            pillage=self.pillage,
            ap_bonus_cap=self.ap_bonus_cap,
            rally=self.rally,
            vp_threshold=self.vp_threshold,
            frontier_lord_min_hexes=self.frontier_lord_min_hexes,
            seat_of_empire_vp=self.seat_of_empire_vp,
            merchant_lord_min_gold=self.merchant_lord_min_gold,
            builder_min_buildings=self.builder_min_buildings,
            tier1_production_build_ap=self.tier1_production_build_ap,
            speaker=self.speaker,
            strategy_pool=list(self.strategy_pool),
            strategy_bounty=dict(self.strategy_bounty),
            event_deck=list(self.event_deck),
            event_discard=list(self.event_discard),
            last_event_id=self.last_event_id,
            agenda_deck=list(self.agenda_deck),
            agenda_revealed=self.agenda_revealed,
            active_laws=list(self.active_laws),
            open_roads=self.open_roads,
            council_crisis=self.council_crisis,
            exploration_deck=list(self.exploration_deck),
            exploration_discard=list(self.exploration_discard),
            artifact_sites=dict(self.artifact_sites),
            artifact_deck=list(self.artifact_deck),
            secret_objective_deck=list(self.secret_objective_deck),
            secret_objective_discard=list(self.secret_objective_discard),
            pending_winds_draws=list(self.pending_winds_draws),
            whisper_deck=list(self.whisper_deck),
            whisper_discard=list(self.whisper_discard),
            desert_tempest=dict(self.desert_tempest) if self.desert_tempest else None,
            trades_this_round=self.trades_this_round,
            artifact_vp_awarded={
                k: list(v) for k, v in self.artifact_vp_awarded.items()
            },
            legendary_build_vp_awarded=set(self.legendary_build_vp_awarded),
            legendary_capture_vp_awarded=set(self.legendary_capture_vp_awarded),
        )
