from aeonis_sim.engine.game import Game

from .conftest import advance_past_strategy_draft, complete_strategy_draft


def test_first_decision_is_strategy_draft_then_action():
    g = Game({"players": 3}, seed=11)
    dp = g.next_decision()
    assert dp.kind == "strategy_draft"
    dp = advance_past_strategy_draft(g)
    assert dp.kind == "action" and dp.pid == 0
    kinds = {c["type"] for c in dp.choices}
    assert "pass" in kinds and "move" in kinds and "recruit" in kinds


def test_pass_rotates_and_all_pass_advances_round():
    g = Game({"players": 3}, seed=11)
    for expected_pid in (0, 1, 2):
        dp = advance_past_strategy_draft(g)
        assert dp.pid == expected_pid
        g.submit({"type": "pass"})
    assert g.state.round == 1
    dp = g.next_decision()
    assert g.state.round == 2 and dp.kind == "strategy_draft"


def test_ap_reset_includes_city_bonus_and_banking():
    g = Game({"players": 3}, seed=11)
    for _ in range(3):
        dp = advance_past_strategy_draft(g)
        g.submit({"type": "pass"})
    complete_strategy_draft(g)
    assert g.state.players[0].ap == 8


def test_round_start_flips_occupied_hexes():
    g = Game({"players": 3}, seed=11)
    state = g.state
    target = next(t for t in state.tiles.values()
                  if t.controller == 1 and not t.units)
    from aeonis_sim.engine.types import Unit, UnitType
    target.units.append(Unit(uid=state.new_uid(), owner=0,
                             type=UnitType.INFANTRY, hp=1))
    for _ in range(3):
        advance_past_strategy_draft(g)
        g.submit({"type": "pass"})
    complete_strategy_draft(g)
    assert target.controller == 0


def test_lord_heals_at_round_start():
    g = Game({"players": 3}, seed=11)
    state = g.state
    coord, lord = state.find_lord(0)
    lord.hp = 1
    for _ in range(3):
        advance_past_strategy_draft(g)
        g.submit({"type": "pass"})
    complete_strategy_draft(g)
    _, lord2 = state.find_lord(0)
    assert lord2.hp == 3


def test_submit_rejects_unenumerated_choice():
    g = Game({"players": 3}, seed=11)
    advance_past_strategy_draft(g)
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
