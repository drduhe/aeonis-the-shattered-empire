"""M4 combat passives: Auriel, Thal'rik, Elyndra, Vharok Forged."""
from __future__ import annotations

import random

from aeonis_sim.engine import combat
from aeonis_sim.engine.combat import (
    prepare_battle_round,
    resolve_round,
    start_battle,
)
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.lords import (
    apply_council_patronage,
    apply_letters_of_credit,
    apply_exaltation,
    apply_shadow_sight,
    apply_entangling_roots,
    entangling_roots_penalty,
    enumerate_entangling_roots,
    extra_defense_bonus,
    scry_top_agenda,
)
from aeonis_sim.engine.lords.elyndra import apply_rooted_defenses_reroll
from aeonis_sim.engine.lords.rakhis import (
    apply_desert_tempest,
    desert_tempest_entry_surcharge,
    enumerate_hit_and_run_moves,
    enumerate_sandstride_retreats,
)
from aeonis_sim.engine.lords.vharok import (
    apply_lock_the_line,
    enumerate_lock_the_line,
)
from aeonis_sim.engine.move import enumerate_moves
from aeonis_sim.engine.recruit import enumerate_recruits
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


def test_cassian_council_patronage_after_lobby():
    state = m4_state(["cassian", "vharok", "seraphel"])
    p = state.player(0)
    before = p.gold
    assert apply_council_patronage(state, 0, 2)
    assert p.gold == before + 1
    assert not apply_council_patronage(state, 0, 1)


def test_cassian_letters_of_credit_spends_influence_for_gold():
    state = m4_state(["cassian", "vharok", "seraphel"])
    p = state.player(0)
    p.influence, p.gold = 2, 1
    assert apply_letters_of_credit(state, 0)
    assert (p.influence, p.gold) == (1, 3)
    assert not apply_letters_of_credit(state, 0)


def test_seraphel_scry_peeks_without_mutating_deck():
    state = m4_state(["seraphel", "cassian", "vharok"])
    state.agenda_deck = ["realm_tax", "border_arbitration"]
    assert scry_top_agenda(state) == "border_arbitration"
    assert len(state.agenda_deck) == 2


def test_seraphel_blink_step_mountain_costs_one_ap():
    state = strip_map(m4_state(["seraphel", "vharok", "cassian"]))
    origin, dest = (0, 0), (1, 0)
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[dest].terrain = Terrain.MOUNTAIN
    state.tiles[origin].controller = 0
    put(state, origin, 0, UnitType.INFANTRY)
    put(state, origin, 0, UnitType.LORD)
    state.player(0).ap = 5
    state.player(0).mana = 4
    blink = next(m for m in enumerate_moves(state, 0) if m.get("blink_step"))
    assert blink["cost"] == 1


def test_vharok_lock_the_line_enumerates_reassignments():
    state = strip_map(m4_state(["vharok", "auriel", "cassian"]))
    target = (1, 0)
    state.tiles[target].terrain = Terrain.PLAINS
    state.tiles[target].controller = 0
    put(state, target, 0, UnitType.INFANTRY)
    put(state, target, 0, UnitType.LORD)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    put(state, (2, 0), 1, UnitType.ARCHER)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    state.player(0).mana = 2
    battle = start_battle(
        state, 1, {"type": "attack", "target": list(target), "cost": 2},
    )
    prepare_battle_round(state, battle, declare_targets=True)
    choices = enumerate_lock_the_line(state, battle)
    assert {"type": "lock_the_line_skip"} in choices
    reassign = next(c for c in choices if c["type"] == "lock_the_line")
    apply_lock_the_line(state, battle, reassign)
    assert state.player(0).mana == 1


from .conftest import advance_to_action_phase


def test_elyndra_entangling_roots_enumerates_from_game_combat_flow():
    g = Game(
        {
            "players": 3,
            "lord_asymmetry": {
                "enabled": True,
                "lords": ["vharok", "elyndra", "cassian"],
            },
        },
        seed=41,
    )
    state = strip_map(g.state)
    forest, origin = (1, 0), (2, 0)
    state.tiles[forest].terrain = Terrain.FOREST
    state.tiles[forest].controller = 1
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[origin].controller = 0
    put(state, forest, 1, UnitType.INFANTRY)
    put(state, forest, 1, UnitType.LORD)
    put(state, origin, 0, UnitType.INFANTRY)
    state.player(0).ap = 5
    state.player(1).mana = 2

    advance_to_action_phase(g)
    g._initiative_queue = [0, 1, 2]
    g._pending = None

    dp = g.next_decision()
    attack = next(c for c in dp.choices if c["type"] == "attack")
    g.submit(attack)

    dp = g.next_decision()
    while dp is not None and dp.kind != "entangling_roots":
        if dp.kind == "sandstride_retreat":
            g.submit({"type": "sandstride_skip"})
        elif dp.kind == "lock_the_line":
            g.submit({"type": "lock_the_line_skip"})
        else:
            raise AssertionError(f"unexpected decision before entangling_roots: {dp.kind}")
        dp = g.next_decision()

    assert dp is not None
    assert dp.kind == "entangling_roots"
    assert {"type": "entangling_roots_skip"} in dp.choices
    apply_choice = next(c for c in dp.choices if c["type"] == "entangling_roots")
    mana_before = g.state.player(1).mana
    g.submit(apply_choice)
    assert g.state.player(1).mana == mana_before - 1
    assert g._battle.pending_entangling == {
        "striker_uid": apply_choice["striker_uid"],
    }
    assert g._battle_lord_substage == "execute"


def test_elyndra_entangling_roots_enumerates_strikers():
    state = strip_map(m4_state(["elyndra", "vharok", "cassian"]))
    forest = (1, 0)
    state.tiles[forest].terrain = Terrain.FOREST
    state.tiles[forest].controller = 0
    put(state, forest, 0, UnitType.INFANTRY)
    put(state, forest, 0, UnitType.LORD)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    state.player(0).mana = 2
    battle = start_battle(
        state, 1, {"type": "attack", "target": list(forest), "cost": 2},
    )
    prepare_battle_round(state, battle, declare_targets=True)
    choices = enumerate_entangling_roots(state, battle)
    assert {"type": "entangling_roots_skip"} in choices
    apply_choice = next(c for c in choices if c["type"] == "entangling_roots")
    apply_entangling_roots(state, battle, apply_choice)
    assert state.player(0).mana == 1
    assert battle.pending_entangling == {"striker_uid": apply_choice["striker_uid"]}


def test_elyndra_entangling_roots_penalty_floors_at_one():
    assert entangling_roots_penalty(5) == 2
    assert entangling_roots_penalty(2) == 1
    assert entangling_roots_penalty(1) == 0


def test_elyndra_entangling_roots_changes_attack_outcome():
    state = strip_map(m4_state(["elyndra", "vharok", "cassian"]))
    forest = (1, 0)
    state.tiles[forest].terrain = Terrain.FOREST
    state.tiles[forest].controller = 0
    put(state, forest, 0, UnitType.INFANTRY)
    put(state, forest, 0, UnitType.LORD)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    state.player(0).mana = 2
    battle = start_battle(
        state, 1, {"type": "attack", "target": list(forest), "cost": 2},
    )
    prepare_battle_round(state, battle, declare_targets=True)
    striker = next(u for u in battle.att_line if u.type != UnitType.ARCHER)
    apply_entangling_roots(
        state, battle,
        {"type": "entangling_roots", "striker_uid": striker.uid},
    )
    combat.execute_battle_round(state, battle, ScriptRng([4, 1, 1, 6]))
    assert battle.winner is None
    assert battle.pending_entangling is None


def test_rakhis_sandstride_retreat_enumerates_before_pre_strike():
    state = strip_map(m4_state(["rakhis", "vharok", "cassian"]))
    target, retreat = (1, 0), (0, 1)
    state.tiles[target].terrain = Terrain.PLAINS
    state.tiles[retreat].terrain = Terrain.PLAINS
    state.tiles[target].controller = 0
    state.tiles[retreat].controller = 0
    put(state, target, 0, UnitType.INFANTRY)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    state.player(1).ap = 5
    battle = start_battle(
        state, 1, {"type": "attack", "target": list(target), "cost": 2},
    )
    prepare_battle_round(state, battle, declare_targets=True)
    choices = enumerate_sandstride_retreats(state, battle)
    assert any(c["type"] == "sandstride_retreat" for c in choices)


def test_rakhis_hit_and_run_enumerates_adjacent_moves():
    state = strip_map(m4_state(["rakhis", "vharok", "cassian"]))
    origin, dest_hex = (2, 0), (2, 1)
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[dest_hex].terrain = Terrain.PLAINS
    state.tiles[origin].controller = 0
    state.tiles[dest_hex].controller = None
    unit = put(state, origin, 0, UnitType.CAVALRY)
    battle = combat.Battle(attacker=0, defender=1, target=(1, 0), winner="attacker")
    battle.att_committed = [(origin, unit)]
    moves = enumerate_hit_and_run_moves(state, battle)
    assert any(tuple(m["dest"]) == dest_hex for m in moves)


def test_rakhis_desert_tempest_adds_ap_for_other_players():
    state = strip_map(m4_state(["rakhis", "vharok", "cassian"]))
    desert, entry = (1, 0), (0, 0)
    state.tiles[desert].terrain = Terrain.DESERT
    state.tiles[entry].terrain = Terrain.PLAINS
    state.tiles[desert].controller = 0
    put(state, entry, 1, UnitType.INFANTRY)
    put(state, desert, 0, UnitType.INFANTRY)
    state.player(0).mana = 3
    apply_desert_tempest(state, 0, desert)
    assert desert_tempest_entry_surcharge(state, 1, desert) == 2
    assert desert_tempest_entry_surcharge(state, 0, desert) == 0


def test_nyxara_shadow_sight_increments_token_without_reveal():
    state = m4_state(["nyxara", "cassian", "vharok"])
    nyx = state.player(0)
    apply_shadow_sight(state, 1)
    assert nyx.shadow_sight_tokens == 1
    apply_shadow_sight(state, 2)
    assert nyx.shadow_sight_tokens == 1


def test_nyxara_veil_ignores_zoc_on_enemy_hex_path():
    state = strip_map(m4_state(["nyxara", "vharok", "cassian"]))
    origin, through, dest = (0, 0), (1, 0), (2, 0)
    for coord in (origin, through, dest):
        state.tiles[coord].terrain = Terrain.PLAINS
    state.tiles[origin].controller = 0
    state.tiles[through].controller = 1
    state.tiles[dest].controller = None
    put(state, origin, 0, UnitType.INFANTRY)
    put(state, origin, 0, UnitType.LORD)
    state.player(0).ap = 5
    state.player(0).mana = 3
    veil_moves = [m for m in enumerate_moves(state, 0) if m.get("veil")]
    assert any(tuple(m["dest"]) == dest for m in veil_moves)


def test_auriel_exaltation_spends_influence_for_renown():
    state = m4_state(["auriel", "vharok", "cassian"])
    p = state.player(0)
    p.influence = 4
    before = p.renown
    assert apply_exaltation(state, 0)
    assert p.influence == 1
    assert p.renown == before + 2
    assert not apply_exaltation(state, 0)


def test_thalrik_rift_summon_allows_portal_recruitment():
    state = strip_map(m4_state(["thalrik", "vharok", "cassian"]))
    portal = next(
        coord for coord, tile in state.tiles.items() if tile.terrain == Terrain.PORTAL
    )
    state.tiles[portal].controller = 0
    put(state, portal, 0, UnitType.INFANTRY)
    state.player(0).ap = 3
    state.player(0).gold = 10
    state.player(0).pop_pool = 10
    recruits = enumerate_recruits(state, 0)
    assert any(tuple(r["city"]) == portal for r in recruits)
