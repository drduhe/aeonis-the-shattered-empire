from aeonis_sim.runner.play import play_game


def test_chaos_games_finish_with_verdicts():
    for seed in range(5):
        record = play_game({"players": 3}, seed=seed)
        assert record["verdict"] in ("completed", "timeout", "stalled", "degenerate")
        assert record["rounds"] >= 2


def test_same_seed_same_record():
    r1 = play_game({"players": 4}, seed=99)
    r2 = play_game({"players": 4}, seed=99)
    assert r1 == r2
