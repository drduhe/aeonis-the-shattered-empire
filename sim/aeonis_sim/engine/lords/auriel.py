"""Auriel sheet hooks (M4)."""
from __future__ import annotations

from ..types import UnitType
from .specs import is_lord, mark_round_used, round_unused


def radiant_presence_bonus(state, battle) -> int:
    """+1 Defense while Auriel is committed on the defending side."""
    if not is_lord(state, battle.defender, "auriel"):
        return 0
    units = list(battle.def_line) + [u for _, u in battle.def_committed]
    if any(u.type == UnitType.LORD and u.owner == battle.defender for u in units):
        return 1
    return 0


def apply_exaltation(state, pid: int, rng=None) -> bool:
    """Action: spend 3 Influence for +2 Renown once/round."""
    if not is_lord(state, pid, "auriel"):
        return False
    if not round_unused(state, pid, "exaltation"):
        return False
    p = state.player(pid)
    if p.influence < 3:
        return False
    p.influence -= 3
    from .discoveries import bump_renown
    bump_renown(state, pid, 2, rng)
    mark_round_used(state, pid, "exaltation")
    return True
