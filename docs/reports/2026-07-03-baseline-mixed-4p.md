# m2-smoke-4p-mixed

Games: 100 · Completed: 100 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 100 | 100.0% |

## Round length (completed)

- Mean: 6.1
- Median: 6

## Winning margin (completed)

- Mean: 3.2 VP
- Runaway rate (margin ≥7): 7.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 71 | 24 | 33.8% |
| diplomat | 75 | 18 | 24.0% |
| economist | 78 | 5 | 6.4% |
| expander | 74 | 25 | 33.8% |
| warmonger | 86 | 24 | 27.9% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 167 | 5.9% | 11.5% |
| coronation_milestone | 40 | 1.4% | 3.6% |
| objective | 2468 | 87.5% | 79.5% |
| lord_capture | 145 | 5.1% | 5.4% |

**Seat + streak combined:** 7.3% of all VP

## Combat metrics (completed)

- Battles resolved: 542
- Attacker win rate (all): 81.4%
- Battles per player-round: 0.224
- Contested attacker win rate: 64.3%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 542 · attacker wins 81.4%
- Uncontested captures: 259
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 283 | 182 | 64.3% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 196 | 174 | 88.8% |
| Ratio < 1.0 (att dice < def dice) | 87 | 8 | 9.2% |

**Contested attacker win rate:** 64.3% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 606
- Events per round: 1.00
- Top events: populist_uprising (82), harsh_winter (78), winds_of_fortune (78), mana_surge (78), border_skirmishes (76)

## High Council (M2)

- Motions proposed: 2424
- Motions passed: 699
- Motions failed: 1725
- Pass rate: 28.8%
- Yes votes: 4739 · No votes: 4957 (48.9% yes)
- Motions per round: 4.00
- Influence spent (lobby): 788
- Avg influence spent / round: 1.30

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 606 | 12.5% |
| arcane_ascendancy | 606 | 12.5% |
| military_maneuvers | 606 | 12.5% |
| expansion_strategy | 606 | 12.5% |
| economic_boom | 606 | 12.5% |
| diplomatic_decree | 606 | 12.5% |
| tactical_reinforcements | 606 | 12.5% |
| imperial_mandate | 606 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 75 | 41.2% |
| resource_surge | 69 | 37.9% |
| military_maneuvers | 38 | 20.9% |

**Secondary opt-in rate:** 100.0%

## Hypothesis evaluation (H1–H9)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=7.3 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.23, runaway_rate=0.07 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.795 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.054 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **inconclusive** | expander_win_rate=0.338, max_persona_win_rate=0.338 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.064 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **killed** | diplomat_win_rate=0.24, mixed_4p=True |
