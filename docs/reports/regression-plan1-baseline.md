# regression-plan1-baseline-4p

Games: 30 · Completed: 30 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 30 | 100.0% |

## Round length (completed)

- Mean: 6.6
- Median: 7

## Winning margin (completed)

- Mean: 3.0 VP
- Runaway rate (margin ≥7): 10.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| warmonger | 120 | 30 | 25.0% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 38 | 4.4% | 7.5% |
| coronation_milestone | 4 | 0.5% | 0.4% |
| objective | 724 | 83.8% | 79.9% |
| lord_capture | 98 | 11.3% | 12.2% |

**Seat + streak combined:** 4.9% of all VP

## Combat metrics (completed)

- Battles resolved: 409
- Attacker win rate (all): 84.8%
- Battles per player-round: 0.514
- Contested attacker win rate: 69.5%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 409 · attacker wins 84.8%
- Uncontested captures: 206
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 203 | 141 | 69.5% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 151 | 137 | 90.7% |
| Ratio < 1.0 (att dice < def dice) | 52 | 4 | 7.7% |

**Contested attacker win rate:** 69.5% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 199
- Events per round: 1.00
- Top events: populist_uprising (29), supply_disruption (28), border_skirmishes (26), migration_wave (26), harsh_winter (24)

## High Council (M2)

- Motions proposed: 796
- Motions passed: 796
- Pass rate: 100.0%
- Motions per round: 4.00
- Influence spent (lobby): 782
- Avg influence spent / round: 3.93

## Hypothesis evaluation (H1–H8)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=4.9 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.0, runaway_rate=0.1 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.799 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **killed** | winner_lord_capture_share=0.122 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.0, max_persona_win_rate=0.25 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.0 |
