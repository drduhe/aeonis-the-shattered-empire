"""Cassian sheet hooks (M4)."""
from __future__ import annotations

from .specs import is_lord, mark_round_used, round_unused


def apply_council_patronage(state, pid: int, lobby_spent: int) -> bool:
    """+1 Gold once/round after lobbying on a resolved council vote."""
    if lobby_spent <= 0 or not is_lord(state, pid, "cassian"):
        return False
    if not round_unused(state, pid, "patronage"):
        return False
    state.player(pid).gold += 1
    mark_round_used(state, pid, "patronage")
    return True


def apply_letters_of_credit(state, pid: int) -> bool:
    """High Council: spend 1 Influence for +2 Gold once/round."""
    if not is_lord(state, pid, "cassian"):
        return False
    if not round_unused(state, pid, "letters_of_credit"):
        return False
    p = state.player(pid)
    if p.influence < 1:
        return False
    p.influence -= 1
    p.gold += 2
    mark_round_used(state, pid, "letters_of_credit")
    return True
