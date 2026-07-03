import json

from aeonis_sim.engine.record import build_record, replay
from aeonis_sim.runner.play import play_game


def test_same_seed_produces_identical_record():
    config = {"players": 4, "personas": ["balanced", "warmonger", "economist", "expander"]}
    a = play_game(config, seed=4242)
    b = play_game(config, seed=4242)
    assert a["choices"] == b["choices"]
    assert a["final_vp"] == b["final_vp"]
    assert a["final_state"] == b["final_state"]
    assert a["verdict"] == b["verdict"]


def test_replay_matches_recorded_final_state():
    config = {"players": 4, "personas": ["balanced"] * 4}
    rec = play_game(config, seed=9001)
    g = replay(rec)
    rebuilt = build_record(g)
    assert g.verdict == rec["verdict"]
    assert g.state.to_dict() == rec["final_state"]
    assert len(rebuilt["choices"]) == len(rec["choices"])
