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
