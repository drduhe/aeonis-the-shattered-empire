import json
from pathlib import Path

from aeonis_sim.engine.record import replay
from aeonis_sim.runner.play import play_game

FIXTURE = Path(__file__).parent / "fixtures" / "golden_replays.jsonl"


def test_golden_replays_round_trip():
    for line in FIXTURE.read_text().splitlines():
        rec = json.loads(line)
        g = replay(rec)
        assert g.verdict == "completed"
        assert g.state.to_dict() == rec["final_state"]


def test_golden_replays_cover_all_player_counts():
    players = set()
    personas = set()
    for line in FIXTURE.read_text().splitlines():
        rec = json.loads(line)
        players.add(rec["config"]["players"])
        personas.update(rec["config"].get("personas", []))
    assert players == {3, 4, 5, 6, 7, 8}
    assert len(personas) >= 3  # balanced + at least two specialist personas


def test_replay_migrates_pre_m4_record_without_flag():
    record = play_game(
        {
            "players": 3,
            "personas": ["balanced"] * 3,
            "lord_asymmetry": {"enabled": False},
        },
        seed=911,
    )
    del record["config"]["lord_asymmetry"]

    game = replay(record)

    assert game.verdict == "completed"
    assert all(not player.lord_id for player in game.state.players)
    assert game.state.to_dict() == record["final_state"]
