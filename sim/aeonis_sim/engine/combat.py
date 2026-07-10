"""Combat (Combat.md).

Milestone-1 agent-capability bounds (not rules rulings):
- Both sides auto-commit all eligible units on a fresh attack.
- Ongoing sieges persist committed units and add ≤3 reinforcements per round (AL-20).
- Battle Line priority: Cavalry, Archer, Infantry, Lord last.
- Strike target: enemy line unit with (lowest hp, lowest defense die, lowest uid).
Ledger: AL-7 auto Hold the Walls; AL-10 defender win definition;
AL-11 buildings taken over intact; AL-12 archers only strike in Pre-Strike;
AL-17 forest terrain +1 Defense for defenders on Forest hexes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .hexmap import neighbors, distance
from .objectives import record_battle_win_at
from .whispers import (
    BattleWhisperMods,
    auto_apply_combat_whispers,
    combat_attack_die,
    combat_defense_mod,
    combat_iron_resolve,
    combat_pre_strike_bonus,
)
from .production import apply_tile_production
from .artifacts import attack_die, defense_die, maybe_transfer_shard, transfer_lord_equipment
from .arcane import (
    battle_augury_attack_penalty,
    battle_runes_attack_bonus,
    searing_salvo_damage,
    warding_charm_defense_bonus,
)
from .types import BuildingType, Terrain, UNIT_STATS, UnitType
from .lords import is_lord

ATTACK_AP = 2
PRESS_AP = 1
_LINE_PRIORITY = {UnitType.CAVALRY: 0, UnitType.ARCHER: 1,
                  UnitType.INFANTRY: 2, UnitType.LORD: 3}
SIEGE_REINFORCE_CAP = 3


def _find_unit(state, uid: int):
    for t in state.tiles.values():
        for u in t.units:
            if u.uid == uid:
                return t.coord, u
    return None, None


def _is_battle_adjacent(coord, target) -> bool:
    return coord == target or coord in neighbors(target)


def _commit_from_uids(state, battle, uids: list, side: str) -> None:
    committed = battle.att_committed if side == "att" else battle.def_committed
    for uid in uids:
        origin, u = _find_unit(state, uid)
        if origin is None or not _is_battle_adjacent(origin, battle.target):
            continue
        if any(cu.uid == uid for _, cu in committed):
            continue
        committed.append((origin, u))


def _full_commit(state, battle) -> None:
    target = battle.target
    defender = battle.defender
    attacker = battle.attacker
    t = state.tiles[target]
    for u in t.units:
        if u.owner == defender:
            battle.def_committed.append((target, u))
    for n in neighbors(target):
        nt = state.tiles.get(n)
        if nt is None:
            continue
        for u in nt.units:
            if u.owner == attacker:
                battle.att_committed.append((n, u))
            elif u.owner == defender:
                battle.def_committed.append((n, u))


def _reinforce_siege(state, battle) -> None:
    """Combat.md §6.4: up to 3 reinforcements per side per siege round."""
    target = battle.target
    committed_uids = {u.uid for _, u in battle.att_committed + battle.def_committed}
    added_att = added_def = 0
    for n in [target, *neighbors(target)]:
        nt = state.tiles.get(n)
        if nt is None:
            continue
        for u in nt.units:
            if u.uid in committed_uids:
                continue
            if u.owner == battle.attacker and added_att < SIEGE_REINFORCE_CAP:
                battle.att_committed.append((n, u))
                committed_uids.add(u.uid)
                added_att += 1
            elif u.owner == battle.defender and added_def < SIEGE_REINFORCE_CAP:
                battle.def_committed.append((n, u))
                committed_uids.add(u.uid)
                added_def += 1


def _save_siege_committed(tile, battle) -> None:
    tile.siege_att_uids = [u.uid for _, u in battle.att_committed]
    tile.siege_def_uids = [u.uid for _, u in battle.def_committed]


def _clear_siege_committed(tile) -> None:
    tile.siege_att_uids = []
    tile.siege_def_uids = []


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
    init_att_dice: int = 0
    init_def_dice: int = 0
    uncontested: bool = False
    whisper_mods: BattleWhisperMods = field(default_factory=BattleWhisperMods)


def _defender_of(state, target) -> Optional[int]:
    t = state.tiles[target]
    for u in t.units:
        return u.owner
    return t.controller


def enumerate_attacks(state, pid, *, attack_ap: int = ATTACK_AP) -> list:
    if state.player(pid).ap < attack_ap:
        return []
    my_hexes = {t.coord for t in state.tiles.values()
                if any(u.owner == pid for u in t.units)}
    out = []
    for coord, t in state.tiles.items():
        d = _defender_of(state, coord)
        if d is None or d == pid:
            continue
        if any(n in my_hexes for n in neighbors(coord)):
            out.append({"type": "attack", "target": list(coord), "cost": attack_ap})
    return out


def _committed_die_total(committed, die_attr: str) -> int:
    return sum(getattr(UNIT_STATS[u.type], die_attr) for _, u in committed)


def snapshot_initiation(battle: Battle) -> None:
    """Record att/def die totals at commit time for stratified combat reports."""
    battle.init_att_dice = _committed_die_total(battle.att_committed, "attack_die")
    battle.init_def_dice = _committed_die_total(battle.def_committed, "defense_die")
    battle.uncontested = len(battle.def_committed) == 0


def empty_stratified_stats() -> dict:
    return {
        "retreats": 0,
        "uncontested_captures": 0,
        "contested_gte1_battles": 0,
        "contested_gte1_att_wins": 0,
        "contested_gte1_def_wins": 0,
        "contested_lt1_battles": 0,
        "contested_lt1_att_wins": 0,
        "contested_lt1_def_wins": 0,
    }


def record_battle_outcome(stats: dict, battle: Battle) -> None:
    """Update combat_stats after a battle ends (retreat, capture, or decisive fight)."""
    strat = stats.setdefault("stratified", empty_stratified_stats())
    if battle.def_retreated:
        strat["retreats"] += 1
        return
    if battle.winner is None:
        return
    stats["battles"] = stats.get("battles", 0) + 1
    if battle.winner == "attacker":
        stats["attacker_wins"] = stats.get("attacker_wins", 0) + 1
    else:
        stats["defender_wins"] = stats.get("defender_wins", 0) + 1
    if battle.uncontested and battle.winner == "attacker":
        strat["uncontested_captures"] += 1
        return
    if battle.uncontested:
        return
    bucket = (
        "contested_gte1"
        if battle.init_att_dice >= battle.init_def_dice
        else "contested_lt1"
    )
    strat[f"{bucket}_battles"] += 1
    if battle.winner == "attacker":
        strat[f"{bucket}_att_wins"] += 1
    else:
        strat[f"{bucket}_def_wins"] += 1


def start_battle(state, pid, choice) -> Battle:
    target = tuple(choice["target"])
    t = state.tiles[target]
    defender = _defender_of(state, target)
    b = Battle(attacker=pid, defender=defender, target=target)
    bastion = (
        is_lord(state, defender, "vharok")
        and t.controller == defender
        and bool(t.buildings)
    )
    b.cap = 5 if t.terrain == Terrain.CITY or t.has(BuildingType.FORTRESS) else 3
    if bastion:
        b.whisper_mods.def_cap_bonus += 1
    # AL-7: Fortress -> siege (canon); City -> defender auto-declares Hold the Walls.
    b.siege = t.terrain == Terrain.CITY or t.has(BuildingType.FORTRESS) or bastion
    state.player(pid).ap -= choice["cost"]

    if b.siege and t.siege and (t.siege_att_uids or t.siege_def_uids):
        _commit_from_uids(state, b, t.siege_att_uids, "att")
        _commit_from_uids(state, b, t.siege_def_uids, "def")
        _reinforce_siege(state, b)
    else:
        _full_commit(state, b)
    snapshot_initiation(b)
    searing_salvo_damage(state, pid, b)
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
    if t.terrain == Terrain.FOREST:
        bonus += 1  # AL-17: Movement.md forest defensive bonus
    if t.has(BuildingType.TOWER):
        bonus += 1
    if t.has(BuildingType.FORTRESS):
        bonus += 2
    if t.has(BuildingType.CASTLE) and not t.castle_suspended:
        bonus += 2
    if (
        is_lord(state, battle.defender, "vharok")
        and t.controller == battle.defender
        and bool(t.buildings)
    ):
        bonus += 1
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
        pending = transfer_lord_equipment(state, unit.owner, captor_pid)
        # Caller (finish_battle path) cannot queue DPs here; captor trims via
        # enumerate_discard_lord on next action if over carry limit.
        _ = pending


def _hits(striker_side: str, atk: int, dfn: int, edge_mode: str, *, pre_strike: bool) -> bool:
    """Plan 1 Aggressor's Edge: attacking-side Attack rolls win ties."""
    edge = False
    if striker_side == "att":
        if edge_mode == "full":
            edge = True
        elif edge_mode == "pre_strike" and pre_strike:
            edge = True
    if edge:
        return atk >= dfn
    return atk > dfn


def _strike(state, battle, strikers, targets_line, rng, striker_side, *, pre_strike: bool) -> None:
    mods = battle.whisper_mods
    def_side = "def" if striker_side == "att" else "att"
    for striker in sorted(strikers, key=lambda u: u.uid):
        if striker.hp <= 0:
            continue
        target = _pick_target(targets_line)
        if target is None:
            return
        atk_die = combat_attack_die(mods, striker)
        if atk_die == UNIT_STATS[striker.type].attack_die:
            atk_die = attack_die(state, striker.owner, striker)
        atk = rng.randint(1, atk_die)
        if striker_side == "att" and striker.owner == battle.attacker:
            atk += battle_runes_attack_bonus(state, striker.owner, battle)
        dfn_die = defense_die(state, target.owner, target, battle.target)
        dfn = rng.randint(1, dfn_die + combat_defense_mod(mods, target.uid))
        if striker_side == "att" and target.owner == battle.defender:
            dfn += warding_charm_defense_bonus(state, battle.defender, battle)
        if striker_side == "att":
            atk = max(1, atk - battle_augury_attack_penalty(state, battle.defender, battle))
        dfn += _defense_bonus(state, battle, def_side)
        if _hits(striker_side, atk, dfn, state.aggressors_edge_mode, pre_strike=pre_strike):
            dmg = 1
            if pre_strike and striker.type == UnitType.ARCHER:
                dmg += combat_pre_strike_bonus(mods)
            target.hp -= dmg
            if target.hp <= 0:
                if combat_iron_resolve(mods, target):
                    target.hp = 1
                else:
                    _kill(state, battle, target)


def resolve_round(state, battle, rng) -> None:
    mods = battle.whisper_mods
    auto_apply_combat_whispers(state, battle, "reinforce", mods)
    if battle.siege and battle.rounds > 0:
        _reinforce_siege(state, battle)
    battle.rounds += 1
    att_cap = battle.cap + mods.att_cap_bonus
    def_cap = battle.cap + mods.def_cap_bonus
    _form_line(battle.att_committed, att_cap, battle.att_line)
    _form_line(battle.def_committed, def_cap, battle.def_line)

    def archers(line):
        return [u for u in line if u.type == UnitType.ARCHER]

    def others(line):
        return [u for u in line if u.type != UnitType.ARCHER]  # AL-12

    auto_apply_combat_whispers(state, battle, "pre_strike", mods)
    _strike(state, battle, archers(battle.att_line), battle.def_line, rng, "att", pre_strike=True)
    _strike(state, battle, archers(battle.def_line), battle.att_line, rng, "def", pre_strike=True)
    auto_apply_combat_whispers(state, battle, "pre_roll", mods)
    auto_apply_combat_whispers(state, battle, "strike", mods)
    _strike(state, battle, others(battle.att_line), battle.def_line, rng, "att", pre_strike=False)
    auto_apply_combat_whispers(state, battle, "counterstrike", mods)
    _strike(state, battle, others(battle.def_line), battle.att_line, rng, "def", pre_strike=False)

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
    max_dist = 2 if battle.whisper_mods.tactical_withdrawal else 1
    out = []
    for coord, tile in state.tiles.items():
        if tile.controller != battle.defender:
            continue
        if any(u.owner != battle.defender for u in tile.units):
            continue
        if distance(coord, battle.target) > max_dist or distance(coord, battle.target) < 1:
            continue
        out.append({"type": "retreat", "dest": list(coord)})
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
        _clear_siege_committed(t)
        captor = state.player(battle.attacker)
        captor.battle_wins += 1
        record_battle_win_at(state, battle.attacker, battle.target)
        if state.pillage:
            apply_tile_production(captor, t)
        # Occupation: move up to cap surviving committed units in (auto-pick
        # by line priority). Buildings are taken over intact (AL-11).
        movers = sorted(battle.att_committed,
                        key=lambda p: (_LINE_PRIORITY[p[1].type], p[1].uid))[:battle.cap]
        for origin, u in movers:
            state.tiles[origin].units.remove(u)
            t.units.append(u)
    elif battle.winner == "defender":
        t.siege = False
        _clear_siege_committed(t)
        state.player(battle.defender).battle_wins += 1  # AL-10
        record_battle_win_at(state, battle.defender, battle.target)
        att_lord = any(
            u.owner == battle.attacker and u.type == UnitType.LORD
            for u in t.units
        ) or any(
            u.type == UnitType.LORD for _, u in battle.att_committed
        )
        maybe_transfer_shard(state, battle.attacker, battle.defender, att_lord)
    else:
        # Undecided: siege marker persists on Cities/Fortresses; otherwise the
        # attack simply ends (attacker units never left their origin hexes).
        t.siege = battle.siege
        if battle.siege:
            _save_siege_committed(t, battle)
        else:
            _clear_siege_committed(t)
