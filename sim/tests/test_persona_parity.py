"""Persona parity — design-aligned bot scoring, not arbitrary weight inflation."""
from __future__ import annotations

from aeonis_sim.agents.features import evaluate_state
from aeonis_sim.agents.persona import PERSONA_WEIGHTS, _dot, _score_draft_choice
from aeonis_sim.engine.setup import build_initial_state
import random


def test_economist_builder_need_weight_is_positive():
    assert PERSONA_WEIGHTS["economist"]["builder_need"] > 0


def test_economist_prefers_build_when_builder_objective_open():
    s = build_initial_state({"players": 4}, random.Random(1))
    s.shared_public_revealed = ["builder"]
    s.player(0).shared_scored = []
    feats = evaluate_state(s, 0)
    assert feats["builder_push"] > 0.5
    eco = _dot(PERSONA_WEIGHTS["economist"], feats)
    bal = _dot(PERSONA_WEIGHTS["balanced"], feats)
    assert eco > bal


def test_expander_has_vp_lead_brake():
    assert PERSONA_WEIGHTS["expander"]["vp_lead"] < 0
    assert PERSONA_WEIGHTS["expander"]["territory_sat"] < -4.0


def test_economist_draft_favors_economic_cards():
    s = build_initial_state({"players": 4}, random.Random(2))
    boom = _score_draft_choice(s, {"card": "economic_boom"}, "economist")
    boom_bal = _score_draft_choice(s, {"card": "economic_boom"}, "balanced")
    assert boom > boom_bal


def test_expander_draft_favors_expansion_cards():
    s = build_initial_state({"players": 4}, random.Random(3))
    exp = _score_draft_choice(s, {"card": "expansion_strategy"}, "expander")
    exp_bal = _score_draft_choice(s, {"card": "expansion_strategy"}, "balanced")
    assert exp > exp_bal
