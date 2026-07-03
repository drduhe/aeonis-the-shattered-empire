from aeonis_sim.engine.game import Game


def test_first_decision_is_action_for_player_0():
    g = Game({"players": 3}, seed=11)
    dp = g.next_decision()
    assert dp.kind == "action" and dp.pid == 0
    kinds = {c["type"] for c in dp.choices}
    assert "pass" in kinds and "move" in kinds and "recruit" in kinds


def test_pass_rotates_and_all_pass_advances_round():
    g = Game({"players": 3}, seed=11)
    for expected_pid in (0, 1, 2):
        dp = g.next_decision()
        assert dp.pid == expected_pid
        g.submit({"type": "pass"})
    # All passed -> production + cleanup ran -> round 2, player 0 again
    dp = g.next_decision()
    assert g.state.round == 2 and dp.pid == 0


def test_ap_reset_includes_city_bonus_and_banking():
    g = Game({"players": 3}, seed=11)
    for _ in range(3):
        g.next_decision()
        g.submit({"type": "pass"})   # banks min(ap,2) = 2
    g.next_decision()
    # Round 2 AP: base 5 + banked 2 + city bonus 1 (one City) = 8
    assert g.state.players[0].ap == 8


def test_round_start_flips_occupied_hexes():
    g = Game({"players": 3}, seed=11)
    state = g.state
    p0 = state.players[0]
    # Manufacture: player 0 unit alone on an enemy-controlled hex
    target = next(t for t in state.tiles.values()
                  if t.controller == 1 and not t.units)
    from aeonis_sim.engine.types import Unit, UnitType
    target.units.append(Unit(uid=state.new_uid(), owner=0,
                             type=UnitType.INFANTRY, hp=1))
    for _ in range(3):
        g.next_decision()
        g.submit({"type": "pass"})
    g.next_decision()  # round 2 has begun; Round Start ran
    assert target.controller == 0  # Tiles.md control method 1


def test_submit_rejects_unenumerated_choice():
    g = Game({"players": 3}, seed=11)
    g.next_decision()
    try:
        g.submit({"type": "recruit", "city": [9, 9], "units": ["cavalry"] * 9})
        assert False, "should have raised"
    except ValueError:
        pass


def test_seed_determinism():
    def run(seed):
        g = Game({"players": 3}, seed=seed)
        log = []
        while not g.over and len(log) < 200:
            dp = g.next_decision()
            if dp is None:
                break
            choice = sorted(dp.choices, key=lambda c: str(sorted(c.items())))[0]
            g.submit(choice)
            log.append(choice)
        return log, g.state.to_dict()

    l1, s1 = run(3)
    l2, s2 = run(3)
    assert l1 == l2 and s1 == s2
