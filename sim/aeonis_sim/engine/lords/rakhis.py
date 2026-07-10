"""Rakhis sheet hooks (M4)."""
from __future__ import annotations

from ..hexmap import distance, neighbors
from ..types import BuildingType, Terrain, UnitType
from .specs import is_lord, mark_round_used, round_unused


def _rakhis_side(state, battle) -> int | None:
    if is_lord(state, battle.attacker, "rakhis"):
        return battle.attacker
    if is_lord(state, battle.defender, "rakhis"):
        return battle.defender
    return None


def sandstride_retreat_available(state, battle) -> bool:
    """Once per battle before first Pre-Strike of round 1."""
    if battle.rounds != 1 or battle.battle_flags.get("sandstride_used"):
        return False
    pid = _rakhis_side(state, battle)
    if pid is None:
        return False
    committed = (
        battle.att_committed if pid == battle.attacker else battle.def_committed
    )
    return len(committed) > 0


def _defender_retreat_blocked(state, battle) -> bool:
    t = state.tiles[battle.target]
    if t.terrain == Terrain.CITY or t.has(BuildingType.FORTRESS):
        return True
    return bool(battle.siege and t.terrain != Terrain.PLAINS)


def enumerate_sandstride_retreats(state, battle) -> list:
    if not sandstride_retreat_available(state, battle):
        return []
    pid = _rakhis_side(state, battle)
    assert pid is not None
    choices = [{"type": "sandstride_skip"}]
    if pid == battle.attacker:
        choices.append({"type": "sandstride_retreat"})
        return choices
    if _defender_retreat_blocked(state, battle):
        return choices
    for coord, tile in state.tiles.items():
        if tile.controller != pid:
            continue
        if any(u.owner != pid for u in tile.units):
            continue
        if distance(coord, battle.target) > 2 or distance(coord, battle.target) < 1:
            continue
        choices.append({"type": "sandstride_retreat", "dest": list(coord)})
    return choices


def apply_sandstride_retreat(state, battle, choice: dict) -> None:
    battle.battle_flags["sandstride_used"] = True
    if choice["type"] == "sandstride_skip":
        return
    pid = _rakhis_side(state, battle)
    assert pid is not None
    if pid == battle.attacker:
        battle.winner = None
        battle.att_retreated = True
        return
    dest = state.tiles[tuple(choice["dest"])]
    for u in list(battle.def_line):
        for origin, cu in list(battle.def_committed):
            if cu is u:
                state.tiles[origin].units.remove(u)
                dest.units.append(u)
                battle.def_committed.remove((origin, cu))
        battle.def_line.remove(u)
    battle.winner = None
    battle.def_retreated = True


def enumerate_hit_and_run_moves(state, battle) -> list:
    if not is_lord(state, battle.attacker, "rakhis"):
        return []
    if battle.winner != "attacker":
        return []
    if not round_unused(state, battle.attacker, "hit_and_run"):
        return []
    out = []
    for origin, u in battle.att_committed:
        if u.hp <= 0:
            continue
        for n in neighbors(origin):
            tile = state.tiles.get(n)
            if tile is None:
                continue
            if any(v.owner != battle.attacker for v in tile.units):
                continue
            if tile.controller not in (None, battle.attacker):
                continue
            out.append({
                "type": "hit_and_run",
                "uid": u.uid,
                "from": list(origin),
                "dest": list(n),
            })
    return out


def apply_hit_and_run(state, battle, choice: dict) -> None:
    origin = state.tiles[tuple(choice["from"])]
    dest = state.tiles[tuple(choice["dest"])]
    uid = int(choice["uid"])
    unit = next(u for u in origin.units if u.uid == uid)
    origin.units.remove(unit)
    dest.units.append(unit)
    for i, (o, u) in enumerate(battle.att_committed):
        if u.uid == uid:
            battle.att_committed[i] = (tuple(choice["dest"]), u)
            break
    mark_round_used(state, battle.attacker, "hit_and_run")


def enumerate_desert_tempest(state, pid: int) -> list:
    if not is_lord(state, pid, "rakhis"):
        return []
    if not round_unused(state, pid, "desert_tempest"):
        return []
    if state.player(pid).mana < 2:
        return []
    out = []
    for tile in state.controlled(pid):
        if tile.terrain != Terrain.DESERT:
            continue
        if not any(distance(tile.coord, c) <= 2 for c, _ in state.units_of(pid)):
            continue
        out.append({
            "type": "desert_tempest",
            "coord": list(tile.coord),
        })
    return out


def apply_desert_tempest(state, pid: int, coord: tuple) -> None:
    state.player(pid).mana -= 2
    state.desert_tempest = {
        "coord": list(coord),
        "round": state.round,
        "owner": pid,
    }
    mark_round_used(state, pid, "desert_tempest")


def desert_tempest_entry_surcharge(state, pid: int, coord: tuple) -> int:
    dt = state.desert_tempest
    if not dt or tuple(dt["coord"]) != coord:
        return 0
    if dt.get("owner") == pid or dt.get("round") != state.round:
        return 0
    return 2
