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

    mark_game_used,

    round_unused,

    game_unused,

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

from .discoveries import (

    FACTION_DISCOVERIES,

    FACTION_DISCOVERY_IDS,

    FactionDiscoverySpec,

)

from .legendaries import (

    LEGENDARY_BUILDINGS,

    award_legendary_build_vp,

    award_legendary_capture_vp,

    can_build_legendary,

    legendary_for_lord,

    score_legendary_vp,

)

from .auriel import apply_exaltation, radiant_presence_bonus

from .cassian import apply_council_patronage, apply_letters_of_credit

from .elyndra import (

    apply_entangling_roots,

    apply_rooted_defenses_reroll,

    entangling_roots_available,

    entangling_roots_penalty,

    entangling_worthwhile,

    enumerate_entangling_roots,

    would_entangling_prevent_hit,

)

from .nyxara import apply_shadow_sight, apply_veil_of_shadows, veil_available

from .rakhis import (

    apply_desert_tempest,

    apply_hit_and_run,

    apply_sandstride_retreat,

    desert_tempest_entry_surcharge,

    enumerate_desert_tempest,

    enumerate_hit_and_run_moves,

    enumerate_sandstride_retreats,

    sandstride_retreat_available,

)

from .seraphel import apply_blink_step, blink_step_available, scry_top_agenda

from .thalrik import threshold_ward_bonus

from .vharok import apply_lock_the_line, enumerate_lock_the_line, lock_the_line_available





def extra_defense_bonus(state, battle, side: str) -> int:

    """Lord-specific combat defense modifiers (Auriel, Thal'rik)."""

    if side != "def" or battle.defender is None:

        return 0

    return radiant_presence_bonus(state, battle) + threshold_ward_bonus(state, battle)





__all__ = [

    "LAUNCH_LORDS", "LORD_SPECS", "LordSpec", "configured_roster",

    "is_lord", "lord_attack_die", "lord_defense_die", "lord_hp",

    "lord_id", "lord_move", "mark_round_used", "round_unused",
    "mark_game_used", "game_unused",
    "spec_for", "whisper_hand_limit",

    "UNIQUE_TILES", "UniqueTileSpec", "apply_unique_tile_production",

    "controls_unique", "place_unique_tiles", "tile_is_portal",

    "unique_spec_by_id", "unique_spec_for_lord",

    "FACTION_DISCOVERIES", "FACTION_DISCOVERY_IDS", "FactionDiscoverySpec",

    "LEGENDARY_BUILDINGS", "award_legendary_build_vp", "award_legendary_capture_vp", "can_build_legendary", "legendary_for_lord",

    "score_legendary_vp",

    "extra_defense_bonus", "radiant_presence_bonus", "threshold_ward_bonus",

    "apply_rooted_defenses_reroll",

    "apply_council_patronage", "apply_letters_of_credit",

    "scry_top_agenda", "blink_step_available", "apply_blink_step",

    "lock_the_line_available", "enumerate_lock_the_line", "apply_lock_the_line",

    "entangling_roots_available", "entangling_roots_penalty",

    "enumerate_entangling_roots", "entangling_worthwhile",

    "apply_entangling_roots", "would_entangling_prevent_hit",

    "sandstride_retreat_available", "enumerate_sandstride_retreats",

    "apply_sandstride_retreat", "enumerate_hit_and_run_moves", "apply_hit_and_run",

    "enumerate_desert_tempest", "apply_desert_tempest", "desert_tempest_entry_surcharge",

    "apply_shadow_sight", "veil_available", "apply_veil_of_shadows",

    "apply_exaltation",

]


