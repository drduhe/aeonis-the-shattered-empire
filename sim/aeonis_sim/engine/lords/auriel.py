"""Auriel sheet hooks (M4)."""
from __future__ import annotations

from ..types import UnitType
from .specs import is_lord


def radiant_presence_bonus(state, battle) -> int:
    """+1 Defense while Auriel is committed on the defending side."""
    if not is_lord(state, battle.defender, "auriel"):
        return 0
    units = list(battle.def_line) + [u for _, u in battle.def_committed]
    if any(u.type == UnitType.LORD and u.owner == battle.defender for u in units):
        return 1
    return 0
