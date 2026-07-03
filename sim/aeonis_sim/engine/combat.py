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
from .production import apply_tile_production
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
    def_side = "def" if striker_side == "att" else "att"
    for striker in sorted(strikers, key=lambda u: u.uid):
        if striker.hp <= 0:
            continue
        target = _pick_target(targets_line)
        if target is None:
            return
        atk = rng.randint(1, UNIT_STATS[striker.type].attack_die)
        dfn = rng.randint(1, UNIT_STATS[target.type].defense_die)
        dfn += _defense_bonus(state, battle, def_side)
        if _hits(striker_side, atk, dfn, state.aggressors_edge_mode, pre_strike=pre_strike):
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
    _strike(state, battle, archers(battle.att_line), battle.def_line, rng, "att", pre_strike=True)
    _strike(state, battle, archers(battle.def_line), battle.att_line, rng, "def", pre_strike=True)
    # 4.3 Attacker Strike, then Defender Counterstrike
    _strike(state, battle, others(battle.att_line), battle.def_line, rng, "att", pre_strike=False)
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
        captor = state.player(battle.attacker)
        captor.battle_wins += 1
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
        state.player(battle.defender).battle_wins += 1  # AL-10
    else:
        # Undecided: siege marker persists on Cities/Fortresses; otherwise the
        # attack simply ends (attacker units never left their origin hexes).
        t.siege = battle.siege
