# m2-bracket-a-4p-solo

Games: 200 · Completed: 200 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 200 | 100.0% |

## Round length (completed)

- Mean: 7.8
- Median: 6

## Winning margin (completed)

- Mean: 3.6 VP
- Runaway rate (margin ≥7): 17.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 156 | 39 | 25.0% |
| diplomat | 156 | 39 | 25.0% |
| economist | 152 | 38 | 25.0% |
| expander | 156 | 39 | 25.0% |
| warmonger | 148 | 37 | 25.0% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 347 | 6.4% | 12.9% |
| coronation_milestone | 90 | 1.6% | 3.7% |
| objective | 4762 | 87.3% | 78.0% |
| lord_capture | 258 | 4.7% | 5.4% |

**Seat + streak combined:** 8.0% of all VP

## Combat metrics (completed)

- Battles resolved: 946
- Attacker win rate (all): 81.0%
- Battles per player-round: 0.151
- Contested attacker win rate: 65.3%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 946 · attacker wins 81.0%
- Uncontested captures: 428
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 518 | 338 | 65.3% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 371 | 325 | 87.6% |
| Ratio < 1.0 (att dice < def dice) | 147 | 13 | 8.8% |

**Contested attacker win rate:** 65.3% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1562
- Events per round: 1.00
- Top events: festival (206), populist_uprising (198), mana_surge (198), supply_disruption (196), border_skirmishes (195)

## High Council (M2)

- Motions proposed: 6248
- Motions passed: 2112
- Motions failed: 4136
- Pass rate: 33.8%
- Yes votes: 12504 · No votes: 12488 (50.0% yes)
- Motions per round: 4.00
- Influence spent (lobby): 2726
- Avg influence spent / round: 1.75

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1562 | 12.5% |
| arcane_ascendancy | 1562 | 12.5% |
| military_maneuvers | 1562 | 12.5% |
| diplomatic_decree | 1562 | 12.5% |
| expansion_strategy | 1562 | 12.5% |
| economic_boom | 1562 | 12.5% |
| tactical_reinforcements | 1562 | 12.5% |
| imperial_mandate | 1562 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 156 | 43.6% |
| resource_surge | 109 | 30.4% |
| military_maneuvers | 93 | 26.0% |

**Secondary opt-in rate:** 100.0%

## Hypothesis evaluation (H1–H9)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=8.0 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.61, runaway_rate=0.17 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.78 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.054 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.25, max_persona_win_rate=0.25 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.25 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.25, mixed_4p=False |
