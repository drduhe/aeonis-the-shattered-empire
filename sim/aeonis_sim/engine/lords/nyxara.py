"""Nyxara sheet hooks (M4)."""
from __future__ import annotations

from ..types import UnitType
from .specs import is_lord, mark_round_used, round_unused


def apply_shadow_sight(state, whisper_pid: int) -> None:
    """AL-51: Nyxara gains an information token when another player plays a Whisper."""
    for p in state.players:
        if p.pid == whisper_pid:
            continue
        if not is_lord(state, p.pid, "nyxara"):
            continue
        if not round_unused(state, p.pid, "shadow_sight"):
            continue
        p.shadow_sight_tokens += 1
        mark_round_used(state, p.pid, "shadow_sight")


def veil_available(state, pid: int, group: list) -> bool:
    if not is_lord(state, pid, "nyxara"):
        return False
    if not round_unused(state, pid, "veil_of_shadows"):
        return False
    if state.player(pid).mana < 2:
        return False
    return any(u.type == UnitType.LORD and u.owner == pid for u in group)


def apply_veil_of_shadows(state, pid: int) -> None:
    state.player(pid).mana -= 2
    mark_round_used(state, pid, "veil_of_shadows")
