import json
from pathlib import Path

from aeonis_sim.engine.record import replay

FIXTURE = Path(__file__).parent / "fixtures" / "golden_replays.jsonl"


def test_golden_replays_round_trip():
    for line in FIXTURE.read_text().splitlines():
        rec = json.loads(line)
        g = replay(rec)
        assert g.verdict == "completed"
        assert g.state.to_dict() == rec["final_state"]


def test_golden_replays_cover_all_player_counts():
    players = set()
    for line in FIXTURE.read_text().splitlines():
        rec = json.loads(line)
        players.add(rec["config"]["players"])
    assert players == {3, 4, 5, 6, 7, 8}
