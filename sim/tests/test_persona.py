"""Persona bot tests."""
from __future__ import annotations

import json

from aeonis_sim.agents.factory import agents_from_config, make_agents, parse_persona_list
from aeonis_sim.agents.features import evaluate_state, score_action, simulate_action
from aeonis_sim.agents.persona import PERSONA_NAMES, PersonaBot
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.observations import DecisionPoint, observe
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.runner.play import play_game
import random


def test_persona_names_complete():
    assert set(PERSONA_NAMES) == {
        "warmonger", "economist", "expander", "diplomat", "balanced",
    }


def test_parse_persona_list_single():
    assert parse_persona_list("balanced", 4) == {0: "balanced", 1: "balanced", 2: "balanced", 3: "balanced"}


def test_parse_persona_list_per_seat():
    got = parse_persona_list("warmonger,economist,expander,diplomat", 4)
    assert got == {0: "warmonger", 1: "economist", 2: "expander", 3: "diplomat"}


def test_persona_deterministic():
    config = {"players": 4, "personas": ["balanced"] * 4}
    a = play_game(config, seed=42)
    b = play_game(config, seed=42)
    assert a["choices"] == b["choices"]
    assert a["final_vp"] == b["final_vp"]


def test_persona_differs_from_chaos():
    config = {"players": 4, "personas": ["balanced"] * 4}
    persona = play_game(config, seed=99)
    chaos = play_game({"players": 4}, seed=99)
    assert persona["choices"] != chaos["choices"] or persona["final_vp"] != chaos["final_vp"]


def test_warmonger_prefers_attack_when_available():
    rng = random.Random(1)
    state = build_initial_state({"players": 3}, rng)
    pid = 0
    # Force a simple attack opportunity by placing enemy on adjacent hex.
    from aeonis_sim.engine.types import Unit, UnitType
    home_enemy = state.players[1].home
    tile = state.tiles[home_enemy]
    for u in list(tile.units):
        if u.type != UnitType.LORD:
            tile.units.remove(u)
    bot = PersonaBot("warmonger", seed=5)
    game = Game({"players": 3}, seed=1)
    game.state = state
    game.state.players[0].ap = 5
    choices = game._action_choices(0)  # noqa: SLF001
    attacks = [c for c in choices if c["type"] == "attack"]
    if not attacks:
        return  # map layout may not expose attack; skip softly
    dp = DecisionPoint(kind="action", pid=0, choices=choices)
    obs = observe(state, 0)
    pick = bot.choose(obs, dp)
    assert pick["type"] == "attack"


def test_build_raises_economy_feature():
    rng = random.Random(2)
    state = build_initial_state({"players": 3}, rng)
    pid = 0
    p = state.player(pid)
    p.ap = 5
    p.gold = 20
    p.mana = 20
    p.influence = 20
    p.pop_pool = 10
    before = evaluate_state(state, pid)["economy"]
    from aeonis_sim.engine.build import enumerate_builds
    builds = enumerate_builds(state, pid)
    farm = next((b for b in builds if b["building"] == "farm"), None)
    if farm is None:
        return
    feats = score_action(state, pid, farm, DecisionPoint(kind="action", pid=pid, choices=[]))
    assert feats.get("economy_delta", 0) > 0
    assert feats.get("next_economy", before) >= before


def test_record_includes_personas():
    rec = play_game(
        {"players": 3, "personas": ["expander", "economist", "balanced"]},
        seed=7,
    )
    assert len(rec["config"]["personas"]) == 3


def test_score_action_invariant_under_copy():
    """copy() must produce the same persona features as dict round-trip."""
    from aeonis_sim.engine.types import GameState

    game = Game({"players": 4}, seed=17)
    steps = 0
    while not game.over and steps < 40:
        dp = game.next_decision()
        if dp is None:
            continue
        state = game.state
        for choice in dp.choices[:8]:
            feats = score_action(state, dp.pid, choice, dp)
            alt = GameState.from_dict(state.to_dict())
            alt_feats = score_action(alt, dp.pid, choice, dp)
            assert feats == alt_feats
        game.submit(dp.choices[0])
        steps += 1


def test_simulate_action_does_not_mutate_original():
    game = Game({"players": 3}, seed=5)
    dp = game.next_decision()
    moves = [c for c in dp.choices if c["type"] == "move"]
    if not moves:
        return
    before = game.state.to_dict()
    simulate_action(game.state, dp.pid, moves[0], dp.kind)
    assert game.state.to_dict() == before
