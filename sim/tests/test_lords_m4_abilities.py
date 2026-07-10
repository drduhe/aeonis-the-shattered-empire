"""M4 combat passives: Auriel, Thal'rik, Elyndra, Vharok Forged."""
from __future__ import annotations

import random

from aeonis_sim.engine import combat
from aeonis_sim.engine.combat import resolve_round
from aeonis_sim.engine.lords import extra_defense_bonus
from aeonis_sim.engine.lords.elyndra import apply_rooted_defenses_reroll
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain, Unit, UnitType, UNIT_STATS


class ScriptRng:
    def __init__(self, rolls):
        self.rolls = list(rolls)

    def randint(self, a, b):
        return self.rolls.pop(0) if self.rolls else b


def _pad_lords(lords: list[str]) -> list[str]:
    roster = list(lords)
    fillers = ["cassian", "seraphel", "vharok"]
    while len(roster) < 3:
        for name in fillers:
            if name not in roster:
                roster.append(name)
                break
        else:
            roster.append("cassian")
    return roster


def m4_state(lords: list[str]):
    padded = _pad_lords(lords)
    return build_initial_state(
        {
            "players": len(padded),
            "lord_asymmetry": {"enabled": True, "lords": padded},
        },
        random.Random(11),
    )


def strip_map(state):
    for tile in state.tiles.values():
        tile.units = []
        tile.controller = None
        tile.buildings = []
        tile.unique_tile_id = ""
    return state


def put(state, coord, owner, unit_type):
    unit = Unit(
        uid=state.new_uid(), owner=owner, type=unit_type,
        hp=UNIT_STATS[unit_type].hp,
    )
    state.tiles[coord].units.append(unit)
    return unit


def test_auriel_radiant_presence_adds_defense_when_committed():
    state = strip_map(m4_state(["auriel", "vharok"]))
    hex_ = (1, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    put(state, hex_, 0, UnitType.INFANTRY)
    put(state, hex_, 0, UnitType.LORD)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    battle = combat.start_battle(
        state, 1, {"type": "attack", "target": list(hex_), "cost": 2},
    )
    assert extra_defense_bonus(state, battle, "def") >= 1
    assert combat._defense_bonus(state, battle, "def") >= 1


def test_auriel_radiant_presence_absent_without_committed_lord():
    state = strip_map(m4_state(["auriel", "vharok"]))
    hex_ = (1, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    put(state, hex_, 0, UnitType.INFANTRY)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    battle = combat.start_battle(
        state, 1, {"type": "attack", "target": list(hex_), "cost": 2},
    )
    assert extra_defense_bonus(state, battle, "def") == 0


def test_thalrik_threshold_ward_on_portal_hex():
    state = strip_map(m4_state(["thalrik", "vharok"]))
    portal = (1, 0)
    state.tiles[portal].terrain = Terrain.PORTAL
    state.tiles[portal].controller = 0
    put(state, portal, 0, UnitType.INFANTRY)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    battle = combat.start_battle(
        state, 1, {"type": "attack", "target": list(portal), "cost": 2},
    )
    assert extra_defense_bonus(state, battle, "def") == 1
    assert combat._defense_bonus(state, battle, "def") == 1


def test_thalrik_threshold_ward_on_rift_anchor_unique_tile():
    state = strip_map(m4_state(["thalrik", "vharok"]))
    anchor = (1, 0)
    state.tiles[anchor].terrain = Terrain.FOREST
    state.tiles[anchor].unique_tile_id = "rift_anchor"
    state.tiles[anchor].controller = 0
    put(state, anchor, 0, UnitType.INFANTRY)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    battle = combat.start_battle(
        state, 1, {"type": "attack", "target": list(anchor), "cost": 2},
    )
    assert extra_defense_bonus(state, battle, "def") == 1


def test_elyndra_rooted_defenses_reroll_takes_higher_roll():
    state = strip_map(m4_state(["elyndra", "vharok"]))
    battle = combat.Battle(attacker=1, defender=0, target=(1, 0), rounds=1)
    state.tiles[(1, 0)].terrain = Terrain.FOREST
    rng = ScriptRng([5])
    result = apply_rooted_defenses_reroll(state, battle, rng, 2, 6)
    assert result == 5
    assert state.player(0).lord_round["rooted_reroll_r1"] is True


def test_elyndra_rooted_defenses_reroll_keeps_original_when_lower():
    state = strip_map(m4_state(["elyndra", "vharok"]))
    battle = combat.Battle(attacker=1, defender=0, target=(1, 0), rounds=2)
    state.tiles[(1, 0)].terrain = Terrain.FOREST
    rng = ScriptRng([5, 2])
    result = apply_rooted_defenses_reroll(state, battle, rng, 5, 6)
    assert result == 5


def test_elyndra_rooted_defenses_once_per_battle_round():
    state = strip_map(m4_state(["elyndra", "vharok"]))
    battle = combat.Battle(attacker=1, defender=0, target=(1, 0), rounds=1)
    state.tiles[(1, 0)].terrain = Terrain.FOREST
    rng = ScriptRng([6])
    first = apply_rooted_defenses_reroll(state, battle, rng, 1, 6)
    second = apply_rooted_defenses_reroll(state, battle, rng, 1, 6)
    assert first == 6
    assert second == 1


def test_elyndra_rooted_defenses_combat_path_uses_reroll():
    state = strip_map(m4_state(["elyndra", "vharok"]))
    forest = (1, 0)
    state.tiles[forest].terrain = Terrain.FOREST
    state.tiles[forest].controller = 0
    put(state, forest, 0, UnitType.INFANTRY)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    battle = combat.start_battle(
        state, 1, {"type": "attack", "target": list(forest), "cost": 2},
    )
    # att 3 vs def 2 rerolled to 5 + forest +1 = 6 -> miss on 3
    resolve_round(state, battle, ScriptRng([3, 5, 1, 6]))
    assert battle.winner is None


def test_vharok_forged_documents_existing_defense_bonus():
    state = strip_map(m4_state(["vharok", "auriel"]))
    built = (1, 0)
    state.tiles[built].terrain = Terrain.MOUNTAIN
    state.tiles[built].controller = 0
    state.tiles[built].buildings = [BuildingType.MINE]
    put(state, built, 0, UnitType.INFANTRY)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    battle = combat.start_battle(
        state, 1, {"type": "attack", "target": list(built), "cost": 2},
    )
    # Forged in Battle (+1 Def) is encoded in _defense_bonus, not doubled with Bastion cap.
    assert combat._defense_bonus(state, battle, "def") == 1
    assert extra_defense_bonus(state, battle, "def") == 0
