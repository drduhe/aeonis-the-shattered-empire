"""Tournament runner smoke tests."""
from __future__ import annotations

import json
from pathlib import Path

from aeonis_sim.runner.tournament import run_tournament


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
    for name in ("bracket-a.json", "bracket-b.json", "bracket-c.json"):
        cfg = json.loads((root / name).read_text())
        assert cfg["games"] >= 200
        assert len(cfg["personas"]) >= 1


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
