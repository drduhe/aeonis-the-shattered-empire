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

__all__ = [
    "LAUNCH_LORDS", "LORD_SPECS", "LordSpec", "configured_roster",
    "is_lord", "lord_attack_die", "lord_defense_die", "lord_hp",
    "lord_id", "lord_move", "mark_round_used", "round_unused",
    "spec_for", "whisper_hand_limit",
    "UNIQUE_TILES", "UniqueTileSpec", "apply_unique_tile_production",
    "controls_unique", "place_unique_tiles", "tile_is_portal",
    "unique_spec_by_id", "unique_spec_for_lord",
]
