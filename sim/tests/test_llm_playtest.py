"""M5 engine-bounded qualitative playtest tests."""
from __future__ import annotations

from aeonis_sim.agents.factory import agents_from_config
from aeonis_sim.agents.llm import LLMPlaytestAgent, compact_observation
from aeonis_sim.agents.providers import DeterministicProvider
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.observations import DecisionPoint, observe
from aeonis_sim.reports.qualitative import qualitative_report
from aeonis_sim.runner.play import play_game


class FirstChoiceFallback:
    def choose(self, observation, decision_point):
        return decision_point.choices[0]


class InvalidProvider:
    name = "invalid-test"

    def complete(self, messages, json_schema):
        return {"action_index": 99}


class WrongTypeProvider(DeterministicProvider):
    name = "wrong-type-test"

    def complete(self, messages, json_schema):
        result = super().complete(messages, json_schema)
        if json_schema.get("title") == "AeonisDecision":
            result["action_index"] = "0"
        return result


def test_compact_observation_redacts_opponent_hidden_information():
    game = Game({"players": 3}, seed=4)
    game.state.player(0).secret_objectives = ["own_secret"]
    game.state.player(0).whisper_hand = ["own_whisper"]
    game.state.player(1).secret_objectives = ["opponent_secret"]
    game.state.player(1).whisper_hand = ["opponent_whisper"]
    dp = game.next_decision()

    compact = compact_observation(observe(game.state, 0), dp)
    own = compact["players"][0]
    opponent = compact["players"][1]

    assert own["secret_objectives"] == ["own_secret"]
    assert own["whisper_hand"] == ["own_whisper"]
    assert "secret_objectives" not in opponent
    assert "whisper_hand" not in opponent
    assert opponent["whisper_count"] == 1
    assert "opponent_secret" not in str(compact)
    assert "opponent_whisper" not in str(compact)


def test_deterministic_agent_returns_an_enumerated_legal_choice():
    game = Game({"players": 3}, seed=5)
    dp = game.next_decision()
    agent = LLMPlaytestAgent(
        provider=DeterministicProvider(action_index=1),
        fallback=FirstChoiceFallback(),
        persona="balanced",
        seat=dp.pid,
        decision_kinds=[dp.kind],
        max_decision_calls=1,
        max_round_reflections=0,
    )

    choice = agent.choose(observe(game.state, dp.pid), dp)

    assert choice == dp.choices[1]
    assert agent.stats["model_decisions"] == 1
    assert agent.annotations[0]["action"] == choice


def test_negotiation_agent_emits_bounded_public_message():
    game = Game({"players": 3}, seed=15)
    dp = DecisionPoint(
        kind="negotiation",
        phase="action",
        pid=0,
        choices=[{"type": "negotiation_reject"}, {"type": "negotiation_accept"}],
        context={"window": "trade", "deal_kind": "protection_payment"},
    )
    agent = LLMPlaytestAgent(
        provider=DeterministicProvider(action_index=1),
        fallback=FirstChoiceFallback(),
        persona="diplomat",
        seat=0,
        decision_kinds=["negotiation"],
        max_decision_calls=1,
    )

    assert agent.choose(observe(game.state, 0), dp) == dp.choices[1]
    utterance = agent.pop_negotiation_utterance()
    assert utterance is not None
    assert utterance["message"]
    assert "message" in agent.annotations[0]


def test_invalid_provider_retries_then_falls_back_safely():
    game = Game({"players": 3}, seed=6)
    dp = game.next_decision()
    agent = LLMPlaytestAgent(
        provider=InvalidProvider(),
        fallback=FirstChoiceFallback(),
        persona="balanced",
        seat=dp.pid,
        decision_kinds=[dp.kind],
        max_decision_calls=1,
        retries=1,
    )

    choice = agent.choose(observe(game.state, dp.pid), dp)

    assert choice == dp.choices[0]
    assert agent.stats["provider_calls"] == 2
    assert agent.stats["model_decision_attempts"] == 1
    assert agent.stats["retries"] == 1
    assert agent.stats["fallbacks"] == 1
    assert len(agent.errors) == 2
    assert all(error["stage"] == "decision" for error in agent.errors)
    assert agent.annotations[0]["fallback"] is True


def test_full_control_ignores_sampling_limits_but_skips_forced_choices():
    game = Game({"players": 3}, seed=16)
    agent = LLMPlaytestAgent(
        provider=DeterministicProvider(action_index=1),
        fallback=FirstChoiceFallback(),
        persona="balanced",
        seat=0,
        decision_kinds=["never_this_kind"],
        max_decision_calls=0,
        decision_round_min=99,
        full_control=True,
    )
    decision = DecisionPoint(
        kind="action",
        phase="action",
        pid=0,
        choices=[{"type": "pass"}, {"type": "build"}],
        context={},
    )

    assert agent.choose(observe(game.state, 0), decision) == {"type": "build"}
    assert agent.stats["model_decisions"] == 1
    assert agent.stats["persona_delegations"] == 0

    forced = DecisionPoint(
        kind="scry_ack",
        phase="council",
        pid=0,
        choices=[{"type": "scry_ack"}],
        context={},
    )
    assert agent.choose(observe(game.state, 0), forced) == {"type": "scry_ack"}
    assert agent.stats["provider_calls"] == 1
    assert agent.stats["forced_choices"] == 1


def test_full_control_suppresses_repeated_zero_cost_portal_route():
    game = Game({"players": 3}, seed=17)
    agent = LLMPlaytestAgent(
        provider=DeterministicProvider(action_index=1),
        fallback=FirstChoiceFallback(),
        persona="expander",
        seat=0,
        full_control=True,
    )
    portal_out = {
        "type": "move", "from": [0, 0], "dest": [2, -1],
        "cost": 0, "portal": True,
    }
    portal_back = {
        "type": "move", "from": [2, -1], "dest": [0, 0],
        "cost": 0, "portal": True,
    }
    decision = DecisionPoint(
        kind="action", phase="action", pid=0,
        choices=[{"type": "pass"}, portal_out, portal_back], context={},
    )

    assert agent.choose(observe(game.state, 0), decision) == portal_out
    assert agent.choose(observe(game.state, 0), decision) == portal_back
    assert agent.choose(observe(game.state, 0), decision) == {"type": "pass"}
    assert agent.stats["provider_calls"] == 2
    assert agent.stats["loop_guard_activations"] == 2
    assert agent.stats["loop_choices_suppressed"] == 3


def test_full_control_presents_the_complete_legal_menu():
    game = Game({"players": 3}, seed=18)
    provider = DeterministicProvider(action_index=4)
    agent = LLMPlaytestAgent(
        provider=provider,
        fallback=FirstChoiceFallback(),
        persona="balanced",
        seat=0,
        max_presented_choices=2,
        full_control=True,
    )
    choices = [{"type": "choice", "id": index} for index in range(5)]
    decision = DecisionPoint(
        kind="action", phase="action", pid=0,
        choices=choices, context={},
    )

    assert agent.choose(observe(game.state, 0), decision) == choices[4]
    assert agent.stats["shortlisted_decisions"] == 0


def test_schema_type_error_falls_back_instead_of_coercing():
    game = Game({"players": 3}, seed=10)
    dp = game.next_decision()
    agent = LLMPlaytestAgent(
        provider=WrongTypeProvider(),
        fallback=FirstChoiceFallback(),
        persona="balanced",
        seat=dp.pid,
        decision_kinds=[dp.kind],
        max_decision_calls=1,
        retries=0,
    )

    assert agent.choose(observe(game.state, dp.pid), dp) == dp.choices[0]
    assert agent.stats["model_decisions"] == 0
    assert agent.stats["fallbacks"] == 1
    assert "must be integer" in agent.errors[0]["error"]


def test_factory_can_wrap_default_chaos_seats():
    config = {
        "players": 3,
        "llm_playtest": {
            "enabled": True,
            "seats": [0],
            "provider": {"type": "deterministic"},
        },
    }

    agents = agents_from_config(config, seed=7)

    assert isinstance(agents[0], LLMPlaytestAgent)
    assert agents[0].persona == "chaos"
    assert not isinstance(agents[1], LLMPlaytestAgent)


def test_seat_override_delays_and_shortlists_model_decision():
    config = {
        "players": 3,
        "personas": ["warmonger", "economist", "diplomat"],
        "llm_playtest": {
            "enabled": True,
            "seats": [0],
            "provider": {"type": "deterministic"},
            "seat_overrides": {
                "0": {
                    "decision_kinds": ["action"],
                    "decision_round_min": 3,
                    "max_presented_choices": 5,
                }
            },
        },
    }

    agent = agents_from_config(config, seed=9)[0]
    assert agent.decision_kinds == {"action"}
    assert agent.decision_round_min == 3
    assert agent.max_presented_choices == 5

    choices = [
        {"type": "move", "id": i} for i in range(8)
    ] + [
        {"type": "build", "id": i} for i in range(8)
    ]
    shortlist = agent._shortlist(choices)  # noqa: SLF001
    assert len(shortlist) == 5
    assert {choice["type"] for choice in shortlist} == {"move", "build"}


def test_play_game_emits_qualitative_record_and_dry_run_label():
    config = {
        "players": 3,
        "personas": ["warmonger", "economist", "diplomat"],
        "llm_playtest": {
            "enabled": True,
            "seats": [0],
            "provider": {"type": "deterministic", "action_index": 0},
            "decision_kinds": ["strategy_draft"],
            "max_decision_calls_per_seat": 1,
            "max_round_reflections_per_seat": 1,
        },
    }

    record = play_game(config, seed=8)
    payload = record["agent_playtest"]["seats"][0]
    report = qualitative_report([record])

    assert record["agent_playtest"]["sim_only"] is True
    assert payload["stats"]["model_decisions"] == 1
    assert payload["stats"]["model_decision_attempts"] == 1
    assert payload["exit_interview"]["pacing"].startswith("Dry-run only")
    assert "Pipeline dry run only" in report
    assert "not automatic canon" in report
