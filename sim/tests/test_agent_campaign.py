"""Qualitative campaign assignment rotation tests."""
from __future__ import annotations

from scripts.m5_agent_playtest import game_config_for_offset


def test_lords_rotate_across_fixed_seat_personas_without_mutating_campaign():
    campaign = {
        "players": 3,
        "personas": ["diplomat", "warmonger", "economist"],
        "lord_asymmetry": {
            "enabled": True,
            "lords": ["cassian", "vharok", "thalrik"],
        },
    }

    game = game_config_for_offset(
        campaign, 1, {"lords": True, "personas": False, "step": 1},
    )

    assert game["lord_asymmetry"]["lords"] == ["vharok", "thalrik", "cassian"]
    assert game["personas"] == campaign["personas"]
    assert campaign["lord_asymmetry"]["lords"] == ["cassian", "vharok", "thalrik"]


def test_persona_rotation_is_independent_of_lord_rotation():
    campaign = {
        "players": 3,
        "personas": ["diplomat", "warmonger", "economist"],
        "lord_asymmetry": {
            "enabled": True,
            "lords": ["cassian", "vharok", "thalrik"],
        },
    }

    game = game_config_for_offset(
        campaign, 2, {"lords": False, "personas": True, "step": 1},
    )

    assert game["lord_asymmetry"]["lords"] == campaign["lord_asymmetry"]["lords"]
    assert game["personas"] == ["economist", "diplomat", "warmonger"]
