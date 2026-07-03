# M2 Events + Council — Simulation Impact Report

**Date:** 2026-07-03 · **Sim-only** (not canon)

Milestone 2 Tasks 4–5 added **global Event phase** (8-card deck, auto-resolve before
Strategy draft) and **High Council** (agenda reveal, propose/vote, speaker rotation).
All runs below use the **full M2 engine** (events + council + strategy + initiative).

## Brackets run

| Label | Config | Games | Completed | Matchmaking |
| --- | --- | ---: | ---: | --- |
| M2 mixed smoke | `sim/configs/bracket-m2-smoke.json` | 100 | 100% | mixed 4p |
| M2 solo ladder | `sim/configs/bracket-m2-4p.json` | 200 | 96.5% | solo 4p |
| Bracket A slice | `sim/configs/bracket-a-100.json` | 100 | 98% | solo 4p |

Artifacts:

- [M2 mixed markdown](2026-07-03-m2-smoke-bracket.md) · [HTML](2026-07-03-m2-smoke-bracket.html)
- [M2 solo markdown](2026-07-03-m2-bracket-4p.md) · [HTML](2026-07-03-m2-bracket-4p.html)
- [Bracket A 100 markdown](2026-07-03-bracket-a-100.md) · [HTML](2026-07-03-bracket-a-100.html)

## Headline findings (100-game mixed smoke vs 100-game solo slice)

| Metric | M2 mixed smoke | Bracket A 100 |
| --- | ---: | ---: |
| Mean rounds | **5.8** | 7.8 |
| Runaway rate (≥7 VP margin) | 18.0% | 10.2% |
| Battles / player-round | **0.217** | 0.132 |
| Attacker win % | 85.1% | 81.3% |
| Winner lord-capture VP share | 5.6% | 4.4% |
| Economist win % (mixed seats) | **0%** | 25% (solo) |
| Expander win % (mixed) | **66.2%** | 25% (solo) |
| Diplomat win % (mixed) | **15.8%** | 25% (solo) |
| Events / round | 1.00 | 1.00 |
| Council motions / round | 4.00 | 4.00 |
| Council pass rate | 100% | 100% |

### Read

- **Faster games:** Mean rounds dropped ~2 vs the Bracket A slice — catch-up events
  (`winds_of_fortune`, `populist_uprising`) and council resource motions accelerate
  tempo/objective scoring.
- **More fighting:** Battles per player-round rose (~0.13 → ~0.22) despite shorter
  games; attacker win rate still bot-hot (81–85%).
- **Persona skew in mixed M2:** Expander dominates mixed smoke (66%); economist
  still 0% in mixed — H8 remains open. Diplomat registers wins (16%) with council
  live, but is not yet competitive with expander.
- **Council bots too agreeable:** 100% pass rate and 4 motions/round (every player
  proposes every round) — Task 6/7 should add pass incentives and vote diversity.
- **M2 solo 200-game:** 193 completed, 3 timeout, 4 degenerate — gate not yet met.

## Regression gates

Plan 1/2 CI brackets unchanged; re-run after M2 stabilizes:

    cd sim && python scripts/regression_check.py --config configs/regression-plan1-baseline.json

## Next steps

- Task 6 negotiation · Task 7 persona/report polish (council pass rate, diplomat weights)
- Task 8: M2 gate (100 consecutive completed 4p mixed, zero crashes)
