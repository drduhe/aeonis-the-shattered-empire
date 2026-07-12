"""M4 Legendary Buildings — prereqs, ownership, scoring helpers."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..types import BUILDING_SPECS, BuildingType, LEGENDARY_BUILDINGS
from .specs import is_lord
from .tiles import tile_is_portal

if TYPE_CHECKING:
    from ..types import GameState

LORD_LEGENDARY: dict[str, BuildingType] = {
    "cassian": BuildingType.GRAND_EXCHANGE,
    "seraphel": BuildingType.ARCANE_SANCTUM,
    "vharok": BuildingType.IRON_CITADEL,
    "elyndra": BuildingType.HEARTWOOD_SANCTUM,
    "rakhis": BuildingType.WINDSWORN_WARCAMP,
    "nyxara": BuildingType.HALL_OF_WHISPERS,
    "auriel": BuildingType.CATHEDRAL_OF_RADIANCE,
    "thalrik": BuildingType.DIMENSIONAL_NEXUS,
}

LEGENDARY_AP = 4


def legendary_for_lord(lord_id: str) -> Optional[BuildingType]:
    return LORD_LEGENDARY.get(lord_id)


def _legendary_already_built(state: GameState, btype: BuildingType) -> bool:
    return any(btype in t.buildings for t in state.tiles.values())


def _count_markets(state: GameState, pid: int) -> int:
    return sum(
        1
        for t in state.controlled(pid)
        for b in t.buildings
        if b == BuildingType.MARKET
    )


def _count_portals(state: GameState, pid: int) -> int:
    return sum(
        1
        for t in state.controlled(pid)
        if tile_is_portal(state, t.coord, pid)
    )


def legendary_prereqs_met(state: GameState, pid: int, btype: BuildingType) -> bool:
    p = state.player(pid)
    if btype == BuildingType.GRAND_EXCHANGE:
        return _count_markets(state, pid) >= 2 and p.gold >= 8
    if btype == BuildingType.ARCANE_SANCTUM:
        return len(p.discoveries) >= 3
    if btype == BuildingType.IRON_CITADEL:
        return any(t.has(BuildingType.FORTRESS) for t in state.controlled(pid))
    if btype == BuildingType.HEARTWOOD_SANCTUM:
        return state.pop_cap(pid) >= 15
    if btype == BuildingType.WINDSWORN_WARCAMP:
        return p.attacker_battle_wins >= 2
    if btype == BuildingType.HALL_OF_WHISPERS:
        return p.whispers_played >= 4
    if btype == BuildingType.CATHEDRAL_OF_RADIANCE:
        return p.renown >= 5
    if btype == BuildingType.DIMENSIONAL_NEXUS:
        return _count_portals(state, pid) >= 2
    return False


def can_build_legendary(state: GameState, pid: int, btype: BuildingType) -> bool:
    if btype not in LEGENDARY_BUILDINGS:
        return False
    p = state.player(pid)
    expected = legendary_for_lord(p.lord_id)
    if expected is None or btype != expected:
        return False
    if not is_lord(state, pid, p.lord_id):
        return False
    if _legendary_already_built(state, btype):
        return False
    if not legendary_prereqs_met(state, pid, btype):
        return False
    if p.ap < LEGENDARY_AP:
        return False
    spec = BUILDING_SPECS[btype]
    if p.gold < spec.gold or p.mana < spec.mana or p.influence < spec.influence:
        return False
    if p.pop_pool < spec.pop:
        return False
    return True


def score_legendary_vp(state: GameState, pid: int) -> None:
    """+2 VP per controlled Legendary at Cleanup (artifact-style source key)."""
    p = state.player(pid)
    for t in state.controlled(pid):
        for b in t.buildings:
            if b in LEGENDARY_BUILDINGS:
                p.add_vp(2, "legendary")


# --- Effect helpers (Task 8) ---


def controls_legendary(state: GameState, pid: int, btype: BuildingType) -> bool:
    return any(t.active(btype) for t in state.controlled(pid))


def legendary_tile(state: GameState, pid: int, btype: BuildingType):
    for t in state.controlled(pid):
        if t.active(btype):
            return t
    return None


def iron_citadel_is_fortress(tile) -> bool:
    return tile.active(BuildingType.IRON_CITADEL)


def legendary_defense_bonus(state: GameState, battle, side: str) -> int:
    if side != "def" or battle.defender is None:
        return 0
    t = state.tiles[battle.target]
    bonus = 0
    if t.active(BuildingType.IRON_CITADEL) and t.controller == battle.defender:
        bonus += 3
    if (
        t.active(BuildingType.CATHEDRAL_OF_RADIANCE)
        and t.controller == battle.defender
    ):
        bonus += 2
    return bonus


def arcane_sanctum_lord_attack_die(state: GameState, pid: int, unit, die: int) -> int:
    from ..artifacts import _DIE_UP
    from ..types import UnitType

    if unit.type != UnitType.LORD:
        return die
    for t in state.tiles.values():
        if t.active(BuildingType.ARCANE_SANCTUM) and any(u.uid == unit.uid for u in t.units):
            return _DIE_UP.get(die, die)
    return die


def apply_grand_exchange_production(state: GameState, pid: int) -> None:
    if not controls_legendary(state, pid, BuildingType.GRAND_EXCHANGE):
        return
    trades = getattr(state, "trades_this_round", 0)
    if trades:
        state.player(pid).gold += trades


def apply_arcane_sanctum_production(state: GameState, pid: int) -> None:
    if controls_legendary(state, pid, BuildingType.ARCANE_SANCTUM):
        state.player(pid).mana += 2


def apply_heartwood_production(state: GameState, pid: int) -> None:
    """+3 pop growth at hex; adjacent controlled +1 primary resource."""
    from ..hexmap import neighbors
    from ..types import Terrain

    tile = legendary_tile(state, pid, BuildingType.HEARTWOOD_SANCTUM)
    if tile is None:
        return
    p = state.player(pid)
    room = state.pop_cap(pid) - state.pop_used(pid) - p.pop_pool
    p.pop_pool += min(3, max(0, room))
    primary = {
        Terrain.MOUNTAIN: "gold",
        Terrain.FOREST: "mana",
        Terrain.DESERT: "influence",
        Terrain.PLAINS: "gold",
    }
    for nb in neighbors(tile.coord):
        nt = state.tiles.get(nb)
        if nt is None or nt.controller != pid or nt.cursed:
            continue
        res = primary.get(nt.terrain)
        if res:
            setattr(p, res, getattr(p, res) + 1)


def apply_cathedral_speaker_renown(state: GameState, pid: int, rng=None) -> None:
    if rng is None:
        return
    if state.speaker != pid:
        return
    if not controls_legendary(state, pid, BuildingType.CATHEDRAL_OF_RADIANCE):
        return
    from .discoveries import bump_renown
    bump_renown(state, pid, 1, rng)


def apply_heartwood_round_start_hp(state: GameState) -> None:
    from ..types import UNIT_STATS, UnitType
    from .specs import lord_hp

    for p in state.players:
        tile = legendary_tile(state, p.pid, BuildingType.HEARTWOOD_SANCTUM)
        if tile is None:
            continue
        for u in tile.units:
            if u.owner != p.pid:
                continue
            base = UNIT_STATS[u.type].hp
            if u.type == UnitType.LORD:
                base = lord_hp(state, u.owner, base)
            # +1 HP at Round Start (may exceed printed max by 1 until next heal).
            u.hp = min(u.hp + 1, base + 1)


def hall_of_whispers_extra_draw(state: GameState, pid: int) -> bool:
    return controls_legendary(state, pid, BuildingType.HALL_OF_WHISPERS)


def hall_any_timing_available(state: GameState, pid: int) -> bool:
    from .specs import round_unused
    return (
        controls_legendary(state, pid, BuildingType.HALL_OF_WHISPERS)
        and round_unused(state, pid, "hall_any_timing")
    )


def mark_hall_any_timing_used(state: GameState, pid: int) -> None:
    from .specs import mark_round_used
    mark_round_used(state, pid, "hall_any_timing")


def dimensional_nexus_is_portal(tile) -> bool:
    return tile.active(BuildingType.DIMENSIONAL_NEXUS)


def enumerate_nexus_teleport(state: GameState, pid: int) -> list[dict]:
    """Once/round 0-AP teleport group from Nexus city to a portal you control/occupy."""
    from .specs import round_unused

    if not controls_legendary(state, pid, BuildingType.DIMENSIONAL_NEXUS):
        return []
    if not round_unused(state, pid, "nexus_teleport"):
        return []
    origin = legendary_tile(state, pid, BuildingType.DIMENSIONAL_NEXUS)
    if origin is None:
        return []
    my_units = [u for u in origin.units if u.owner == pid]
    if not my_units:
        return []
    dests = []
    for t in state.tiles.values():
        if t.coord == origin.coord:
            continue
        occupied_by_me = any(u.owner == pid for u in t.units)
        if not (t.controller == pid or occupied_by_me):
            continue
        if not tile_is_portal(state, t.coord, pid):
            continue
        if any(u.owner != pid for u in t.units):
            continue
        dests.append(t.coord)
    return [
        {
            "type": "nexus_teleport",
            "from": list(origin.coord),
            "to": list(dest),
            "uids": [u.uid for u in my_units],
        }
        for dest in dests
    ]

def apply_nexus_teleport(state: GameState, pid: int, choice: dict) -> None:
    from .specs import mark_round_used

    origin = state.tiles[tuple(choice["from"])]
    dest = state.tiles[tuple(choice["to"])]
    uids = set(choice["uids"])
    movers = [u for u in list(origin.units) if u.owner == pid and u.uid in uids]
    for u in movers:
        origin.units.remove(u)
        dest.units.append(u)
    if dest.controller is None:
        dest.controller = pid
    mark_round_used(state, pid, "nexus_teleport")


def enumerate_warcamp_cavalry_move(state: GameState, pid: int) -> list[dict]:
    """Once/round free 1-hex Cavalry move from/near Warcamp."""
    from .specs import round_unused
    from ..hexmap import neighbors
    from ..types import UnitType, Terrain

    if not controls_legendary(state, pid, BuildingType.WINDSWORN_WARCAMP):
        return []
    if not round_unused(state, pid, "warcamp_cavalry"):
        return []
    out = []
    for t in state.tiles.values():
        for u in t.units:
            if u.owner != pid or u.type != UnitType.CAVALRY:
                continue
            for nb in neighbors(t.coord):
                nt = state.tiles.get(nb)
                if nt is None or nt.terrain == Terrain.LAKE:
                    continue
                if any(x.owner != pid for x in nt.units):
                    continue
                out.append({
                    "type": "warcamp_cavalry_move",
                    "from": list(t.coord),
                    "to": list(nb),
                    "uid": u.uid,
                })
    return out


def apply_warcamp_cavalry_move(state: GameState, pid: int, choice: dict) -> None:
    from .specs import mark_round_used

    origin = state.tiles[tuple(choice["from"])]
    dest = state.tiles[tuple(choice["to"])]
    uid = choice["uid"]
    unit = next(u for u in origin.units if u.uid == uid and u.owner == pid)
    origin.units.remove(unit)
    dest.units.append(unit)
    if dest.controller is None or dest.controller == pid:
        dest.controller = pid
    mark_round_used(state, pid, "warcamp_cavalry")


def warcamp_recruit_move_bonus(state: GameState, pid: int, city_coord) -> int:
    """Recruits from Warcamp city get +1 move on first move this round."""
    tile = state.tiles.get(city_coord)
    if tile is None or not tile.active(BuildingType.WINDSWORN_WARCAMP):
        return 0
    if tile.controller != pid:
        return 0
    return 1
