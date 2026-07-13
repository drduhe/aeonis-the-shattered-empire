"""Elyndra sheet hooks (M4)."""
from __future__ import annotations

from ..types import Terrain, UNIT_STATS, UnitType
from .specs import is_lord


def _elyndra_committed(state, battle) -> bool:
    if not is_lord(state, battle.defender, "elyndra"):
        return False
    units = list(battle.def_line) + [u for _, u in battle.def_committed]
    return any(u.type == UnitType.LORD and u.owner == battle.defender for u in units)


def entangling_roots_available(state, battle) -> bool:
    if not _elyndra_committed(state, battle):
        return False
    if state.tiles[battle.target].terrain != Terrain.FOREST:
        return False
    if state.player(battle.defender).mana < 1:
        return False
    key = f"entangling_r{battle.rounds}"
    return not state.player(battle.defender).lord_round.get(key)


def _entangling_striker_candidates(battle) -> list:
    """Non-archer attacker line units (main-strike phase only)."""
    return sorted(
        [u for u in battle.att_line if u.hp > 0 and u.type != UnitType.ARCHER],
        key=lambda u: u.uid,
    )


def entangling_worthwhile(state, battle, striker_uid: int) -> bool:
    """Bot heuristic: True if penalty could flip a hit to a miss for some roll."""
    from ..arcane import (
        battle_augury_attack_penalty,
        battle_runes_attack_bonus,
        warding_charm_defense_bonus,
    )
    from ..artifacts import attack_die, defense_die
    from ..whispers import combat_attack_die, combat_defense_mod

    striker = next(
        (u for u in battle.att_line if u.uid == striker_uid and u.hp > 0),
        None,
    )
    if striker is None or striker.type == UnitType.ARCHER:
        return False
    target_uid = battle.att_targets.get(striker_uid)
    target = next(
        (u for u in battle.def_line if u.uid == target_uid and u.hp > 0),
        None,
    )
    if target is None:
        return False

    mods = battle.whisper_mods
    atk_die = combat_attack_die(mods, striker)
    if atk_die == UNIT_STATS[striker.type].attack_die:
        atk_die = attack_die(state, striker.owner, striker)
    rune_bonus = (
        battle_runes_attack_bonus(state, striker.owner, battle, commit=False)
        if striker.owner == battle.attacker
        else 0
    )
    augury_pen = battle_augury_attack_penalty(
        state, battle.defender, battle, commit=False,
    )
    dfn_die = defense_die(state, target.owner, target, battle.target)
    die_max = dfn_die + combat_defense_mod(mods, target.uid)
    ward_bonus = warding_charm_defense_bonus(
        state, battle.defender, battle, commit=False,
    )
    def_bonus = 0
    if state.tiles[battle.target].terrain == Terrain.FOREST:
        def_bonus += 1
    from . import extra_defense_bonus
    def_bonus += extra_defense_bonus(state, battle, "def")

    edge = state.aggressors_edge_mode == "full"
    for atk_roll in range(1, atk_die + 1):
        atk_eff = max(1, atk_roll + rune_bonus - augury_pen)
        for dfn_roll in range(1, die_max + 1):
            dfn_total = dfn_roll + ward_bonus + def_bonus
            hits = atk_eff >= dfn_total if edge else atk_eff > dfn_total
            if hits and would_entangling_prevent_hit(atk_eff, dfn_total, edge=edge):
                return True
    return False


def enumerate_entangling_roots(state, battle) -> list:
    """Optional DP: skip or penalize one attacker main-strike unit this round."""
    if not entangling_roots_available(state, battle):
        return []
    choices: list[dict] = [{"type": "entangling_roots_skip"}]
    for striker in _entangling_striker_candidates(battle):
        choices.append({
            "type": "entangling_roots",
            "striker_uid": striker.uid,
            "worthwhile": entangling_worthwhile(state, battle, striker.uid),
        })
    return choices


def entangling_roots_penalty(atk_roll: int) -> int:
    return min(2, max(0, atk_roll - 1))


def would_entangling_prevent_hit(
    atk_roll: int, dfn_total: int, *, edge: bool,
) -> bool:
    """True if -2 penalty would flip a hit to a miss."""
    penalized = max(1, atk_roll - 2)
    if edge:
        return atk_roll >= dfn_total and penalized < dfn_total
    return atk_roll > dfn_total and penalized <= dfn_total


def apply_entangling_roots(state, battle, choice: dict) -> None:
    key = f"entangling_r{battle.rounds}"
    if choice["type"] == "entangling_roots_skip":
        state.player(battle.defender).lord_round[key] = True
        return
    if state.player(battle.defender).mana < 1:
        state.player(battle.defender).lord_round[key] = True
        return
    state.player(battle.defender).mana -= 1
    state.player(battle.defender).lord_round[key] = True
    battle.pending_entangling = {"striker_uid": int(choice["striker_uid"])}


def apply_rooted_defenses_reroll(state, battle, rng, roll: int, die_max: int) -> int:
    """Once per battle round in Forest, auto-reroll one Defense die if higher."""
    if not is_lord(state, battle.defender, "elyndra"):
        return roll
    if state.tiles[battle.target].terrain != Terrain.FOREST:
        return roll
    key = f"rooted_reroll_r{battle.rounds}"
    if state.player(battle.defender).lord_round.get(key):
        return roll
    state.player(battle.defender).lord_round[key] = True
    reroll = rng.randint(1, die_max)
    return max(roll, reroll)
