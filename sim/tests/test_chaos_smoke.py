from aeonis_sim.runner.play import play_game


def test_chaos_games_finish_with_verdicts():
    for seed in range(5):
        rec = play_game({"players": 3}, seed=seed, agent_names=["chaos"] * 3)
        assert rec["verdict"] in ("completed", "timeout", "stalled", "degenerate")
        assert rec["rounds"] >= 1
        assert len(rec["choices"]) > 0


def test_seed_reproducibility_of_play_game():
    r1 = play_game({"players": 3}, seed=9, agent_names=["chaos"] * 3)
    r2 = play_game({"players": 3}, seed=9, agent_names=["chaos"] * 3)
    assert r1["choices"] == r2["choices"]
    assert r1["final_vp"] == r2["final_vp"]
