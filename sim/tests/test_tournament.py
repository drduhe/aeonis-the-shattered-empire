"""Tournament runner smoke tests."""
from __future__ import annotations

import json
from pathlib import Path

from aeonis_sim.runner.tournament import _assign_personas, run_tournament


def test_run_tournament_small(tmp_path):
    config = {
        "name": "smoke",
        "players": 3,
        "games": 4,
        "seed_base": 500,
        "personas": ["balanced", "warmonger"],
        "matchmaking": "solo",
    }
    out = tmp_path / "out.jsonl"
    records = run_tournament(config, str(out))
    assert len(records) == 4
    assert out.exists()
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 4
    for line in lines:
        rec = json.loads(line)
        assert rec["config"]["personas"] == ["balanced"] * 3 or len(rec["config"]["personas"]) == 3


def test_bracket_configs_parse():
    root = Path(__file__).parent.parent / "configs"
    for name in (
        "bracket-a.json",
        "bracket-b.json",
        "bracket-c.json",
        "bracket-b-mixed.json",
        "bracket-c-mixed.json",
        "bracket-b-mixed-plan1.json",
        "bracket-c-mixed-plan1.json",
        "bracket-plan1-step0.json",
        "bracket-plan1-step1.json",
        "bracket-plan1-step1b.json",
        "bracket-plan1-step2.json",
    ):
        cfg = json.loads((root / name).read_text())
        assert cfg["games"] >= 100
        assert len(cfg["personas"]) >= 1


def test_mixed_matchmaking_varies_seats():
    config = {
        "players": 4,
        "seed_base": 100,
        "personas": ["balanced", "warmonger", "economist", "diplomat"],
        "matchmaking": "mixed",
    }
    a = _assign_personas(config, 0)
    b = _assign_personas(config, 1)
    assert len(a) == 4
    assert len(set(a)) == 4
    assert a != b


def test_combat_config_forwarded_in_tournament():
    config = {
        "name": "combat-forward",
        "players": 3,
        "games": 1,
        "seed_base": 700,
        "personas": ["warmonger"],
        "matchmaking": "solo",
        "combat": {"aggressors_edge": True, "pillage": True},
    }
    rec = run_tournament(config, workers=1)[0]
    assert rec["config"]["combat"]["aggressors_edge"] is True
    assert rec["config"]["combat"]["pillage"] is True
    assert rec["combat_stats"]["battles"] >= 0


def test_run_tournament_parallel_matches_sequential():
    config = {
        "name": "parallel-equiv",
        "players": 4,
        "games": 6,
        "seed_base": 900,
        "personas": ["balanced", "warmonger"],
        "matchmaking": "solo",
    }
    seq = run_tournament(config, workers=1)
    par = run_tournament(config, workers=2)
    assert len(seq) == len(par)
    for a, b in zip(seq, par):
        assert a["seed"] == b["seed"]
        assert a["choices"] == b["choices"]
        assert a["final_vp"] == b["final_vp"]
        assert a["verdict"] == b["verdict"]
