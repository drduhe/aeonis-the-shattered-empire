"""Launch-Lord signatures for the M4 asymmetry layer."""
from .specs import (
    LAUNCH_LORDS,
    LORD_SPECS,
    LordSpec,
    configured_roster,
    is_lord,
    lord_attack_die,
    lord_defense_die,
    lord_hp,
    lord_id,
    lord_move,
    mark_round_used,
    round_unused,
    spec_for,
    whisper_hand_limit,
)

__all__ = [
    "LAUNCH_LORDS", "LORD_SPECS", "LordSpec", "configured_roster",
    "is_lord", "lord_attack_die", "lord_defense_die", "lord_hp",
    "lord_id", "lord_move", "mark_round_used", "round_unused",
    "spec_for", "whisper_hand_limit",
]
