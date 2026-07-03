# Agent Playtest Simulation — Plan B: Persona Bots & Balance Reports

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Heuristic persona bots that pursue VP deliberately, a tournament runner, and a `reports/` module that produces balance summaries from JSONL game records. First meaningful output: Bracket A (4p, 5 personas, 200 games each = 1,000 games).

**Architecture:** Extends Milestone 1 per `docs/plans/2026-07-02-agent-playtest-simulation-design.md` §6–7. Persona bots score legal actions with 1-ply lookahead where simulation is deterministic (move/recruit/build/pass); combat uses heuristic odds. Chaos remains for fuzzing only — balance stats count `completed` games exclusively.

**Prerequisites:** Milestone 1 gate closed (`docs/reports/2026-07-02-milestone1-gate-plan-b-readiness.html`). Resolve AL-5/AL-1/AL-4 before tuning persona weights from data; initial weights are directional priors.

**Working directory:** Paths relative to `new/`. Pytest from `sim/`.

---

## File structure

```
sim/
  aeonis_sim/
    agents/
      features.py          # state/action feature extraction
      persona.py           # PersonaBot + PERSONA_WEIGHTS
      factory.py           # make_agents(config, seed) -> dict[pid, Agent]
      chaos.py             # unchanged; fuzz only
    reports/
      __init__.py
      summary.py           # aggregate JSONL -> balance markdown
      hypotheses.py        # H1–H6 confirm/kill/inconclusive
    runner/
      play.py              # accept persona config; record personas in output
      tournament.py        # batch runner from JSON config
  configs/
    bracket-a.json           # 4p core tournament
    bracket-b.json           # 8p high count
    bracket-c.json           # 7p pacing edge
  tests/
    test_persona.py
    test_reports.py
    test_tournament.py
```

---

## Task 1: Feature extraction

**Files:** Create `sim/aeonis_sim/agents/features.py`

- [ ] `evaluate_state(state, pid) -> dict[str, float]` — normalized features: `vp`, `vp_lead`, `territory`, `seat`, `seat_streak`, `objective`, `economy`, `military`
- [ ] `score_action(state, pid, choice, dp) -> dict[str, float]` — action deltas; 1-ply via `GameState.from_dict` + `apply_*` for move/recruit/build/pass
- [ ] `combat_heuristic(state, pid, choice, dp)` — attacker/defender unit counts for attack/press/hold/retreat
- [ ] Tests: move toward seat scores higher than random wander; build farm raises economy feature

---

## Task 2: Persona bot

**Files:** Create `sim/aeonis_sim/agents/persona.py`, `sim/aeonis_sim/agents/factory.py`

- [ ] `PERSONAS`: `warmonger`, `economist`, `expander`, `diplomat`, `balanced` weight vectors
- [ ] `PersonaBot(persona, seed)` — dot-product scoring; seeded tie-break
- [ ] `make_agents(seat_personas: dict[int, str], seed: int)` — one bot per seat
- [ ] Tests: deterministic per seed; Warmonger picks attack over pass when both legal and profitable

---

## Task 3: Runner integration

**Files:** Modify `sim/aeonis_sim/runner/play.py`, `sim/aeonis_sim/engine/record.py`

- [ ] `play_game(config, seed, agents=None)` — if `config["personas"]` present and no agents, call `make_agents`
- [ ] `build_record` includes `personas` from config
- [ ] CLI flags: `--persona balanced` (all seats) or `--personas warmonger,balanced,...`
- [ ] Fast-follow: `played_rounds = record["rounds"] - 1` helper in reports (off-by-one documented)

---

## Task 4: Reports module

**Files:** Create `sim/aeonis_sim/reports/summary.py`, `hypotheses.py`

- [ ] `load_records(path) -> list[dict]`
- [ ] `verdict_breakdown(records) -> dict`
- [ ] `balance_summary(records) -> str` — markdown: verdict table, win rate by persona, VP-source mix, round distribution, runaway rate (margin ≥7), only `completed` games for balance sections
- [ ] `evaluate_hypotheses(records) -> dict` — H1–H6 per readiness brief kill criteria
- [ ] `append_session_log(records, path)` — simulated rows in `playtest/session_log.csv`
- [ ] Tests with fixture JSONL (2–3 synthetic records)

---

## Task 5: Tournament runner

**Files:** Create `sim/aeonis_sim/runner/tournament.py`, `sim/configs/bracket-*.json`

- [ ] JSON config: `name`, `players`, `games`, `personas`, `seed_base`, optional `seat_rotation`
- [ ] `run_tournament(config) -> list[dict]` — parallel optional (stdlib: sequential first)
- [ ] CLI: `--config`, `--out`, `--report`
- [ ] Bracket A/B/C configs matching readiness brief §7

---

## Task 6: Plan B gate

- [ ] Run Bracket A: 1,000 games at 4p, zero crashes
- [ ] Generate balance summary markdown + HTML report
- [ ] Mark H1–H6 confirmed/killed/inconclusive
- [ ] 55+ tests passing; determinism test (same seed → same record)

---

## Persona weight priors (initial)

| Feature | Warmonger | Economist | Expander | Diplomat | Balanced |
|---------|-----------|-----------|----------|----------|----------|
| vp | 1.5 | 1.2 | 1.3 | 1.0 | 1.2 |
| combat | 3.0 | 0.2 | 1.0 | 0.4 | 1.0 |
| economy | 0.3 | 3.0 | 0.8 | 1.2 | 1.0 |
| territory | 0.8 | 0.6 | 3.0 | 1.0 | 1.2 |
| seat | 0.5 | 0.4 | 2.5 | 0.8 | 1.0 |
| objective | 0.6 | 1.5 | 1.2 | 1.5 | 1.3 |
| military | 2.0 | 0.5 | 1.2 | 0.6 | 1.0 |

Revisit after Bracket A data; do not canon-change from bot stats alone.

---

## Out of scope (Plan B)

- LLM agents, `llm/` provider layer (Plan C)
- Strategy cards, Council, negotiation (Milestone 2)
- Lord asymmetry (Milestone 4)
- Parallel tournament execution (fast-follow)
