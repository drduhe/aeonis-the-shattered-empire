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
from .tiles import (
    UNIQUE_TILES,
    UniqueTileSpec,
    apply_unique_tile_production,
    controls_unique,
    place_unique_tiles,
    tile_is_portal,
    unique_spec_by_id,
    unique_spec_for_lord,
)
from .auriel import radiant_presence_bonus
from .thalrik import threshold_ward_bonus
from .elyndra import apply_rooted_defenses_reroll


def extra_defense_bonus(state, battle, side: str) -> int:
    """Lord-specific combat defense modifiers (Auriel, Thal'rik)."""
    if side != "def" or battle.defender is None:
        return 0
    return radiant_presence_bonus(state, battle) + threshold_ward_bonus(state, battle)


__all__ = [
    "LAUNCH_LORDS", "LORD_SPECS", "LordSpec", "configured_roster",
    "is_lord", "lord_attack_die", "lord_defense_die", "lord_hp",
    "lord_id", "lord_move", "mark_round_used", "round_unused",
    "spec_for", "whisper_hand_limit",
    "UNIQUE_TILES", "UniqueTileSpec", "apply_unique_tile_production",
    "controls_unique", "place_unique_tiles", "tile_is_portal",
    "unique_spec_by_id", "unique_spec_for_lord",
    "extra_defense_bonus", "radiant_presence_bonus", "threshold_ward_bonus",
    "apply_rooted_defenses_reroll",
]
