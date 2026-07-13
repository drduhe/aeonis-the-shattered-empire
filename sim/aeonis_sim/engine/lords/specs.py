"""Launch-Lord signatures for the M4 asymmetry layer.

The module is deliberately data-first: setup/stat differences and small
cross-system predicates live here, while each owning engine module applies
the relevant rule. Full M4 is the canonical default; neutral M1-M3 behavior
remains available through config["lord_asymmetry"]["enabled"] = false.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..types import UnitType


@dataclass(frozen=True)
class LordSpec:
    id: str
    attack_die: int
    defense_die: int
    hp: int
    move: int
    gold: int
    mana: int
    influence: int
    start_units: tuple[UnitType, ...]


LAUNCH_LORDS: tuple[str, ...] = (
    "cassian", "seraphel", "vharok", "elyndra",
    "rakhis", "nyxara", "auriel", "thalrik",
)

LORD_SPECS: dict[str, LordSpec] = {
    "cassian": LordSpec("cassian", 6, 8, 3, 2, 3, 2, 2,
                         (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.ARCHER)),
    "seraphel": LordSpec("seraphel", 10, 6, 3, 2, 1, 4, 1,
                          (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.ARCHER)),
    "vharok": LordSpec("vharok", 8, 10, 4, 1, 4, 1, 1,
                        (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.INFANTRY)),
    "elyndra": LordSpec("elyndra", 6, 8, 4, 2, 2, 3, 1,
                         (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.ARCHER)),
    "rakhis": LordSpec("rakhis", 8, 6, 3, 3, 3, 1, 2,
                        (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.CAVALRY)),
    "nyxara": LordSpec("nyxara", 10, 4, 2, 2, 2, 2, 2,
                        (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.ARCHER)),
    "auriel": LordSpec("auriel", 6, 10, 3, 2, 1, 2, 3,
                        (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.ARCHER)),
    "thalrik": LordSpec("thalrik", 8, 8, 3, 2, 2, 3, 1,
                         (UnitType.INFANTRY, UnitType.INFANTRY, UnitType.ARCHER)),
}


def lord_id(state, pid: int) -> str:
    return getattr(state.player(pid), "lord_id", "")


def is_lord(state, pid: int | None, expected: str) -> bool:
    return pid is not None and lord_id(state, pid) == expected


def spec_for(state, pid: int) -> LordSpec | None:
    return LORD_SPECS.get(lord_id(state, pid))


def round_unused(state, pid: int, key: str) -> bool:
    return not bool(state.player(pid).lord_round.get(key))


def mark_round_used(state, pid: int, key: str) -> None:
    state.player(pid).lord_round[key] = True


def game_unused(state, pid: int, key: str) -> bool:
    return not bool(state.player(pid).lord_game.get(key))


def mark_game_used(state, pid: int, key: str) -> None:
    state.player(pid).lord_game[key] = True


def configured_roster(config: dict, players: int) -> list[str]:
    block = config.get("lord_asymmetry", {})
    if not block.get("enabled", True):
        return [""] * players
    roster = list(block.get("lords") or LAUNCH_LORDS[:players])
    if len(roster) != players:
        raise ValueError("lord_asymmetry.lords must contain one Lord per player")
    unknown = [name for name in roster if name not in LORD_SPECS]
    if unknown:
        raise ValueError(f"unknown launch Lord(s): {unknown}")
    if len(set(roster)) != len(roster):
        raise ValueError("launch Lords must be unique within one game")
    return roster


def lord_attack_die(state, pid: int, fallback: int) -> int:
    spec = spec_for(state, pid)
    return spec.attack_die if spec else fallback


def lord_defense_die(state, pid: int, fallback: int) -> int:
    spec = spec_for(state, pid)
    return spec.defense_die if spec else fallback


def lord_hp(state, pid: int, fallback: int) -> int:
    spec = spec_for(state, pid)
    return spec.hp if spec else fallback


def lord_move(state, pid: int, fallback: int) -> int:
    spec = spec_for(state, pid)
    return spec.move if spec else fallback


def whisper_hand_limit(state, pid: int, fallback: int) -> int:
    return 8 if is_lord(state, pid, "nyxara") else fallback
