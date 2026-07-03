# bracket-b-high-8p-mixed-mvp

Games: 600 · Completed: 600 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 600 | 100.0% |

## Round length (completed)

- Mean: 5.4
- Median: 5

## Winning margin (completed)

- Mean: 2.5 VP
- Runaway rate (margin ≥7): 3.7%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 824 | 237 | 28.8% |
| diplomat | 838 | 75 | 8.9% |
| economist | 833 | 15 | 1.8% |
| expander | 832 | 75 | 9.0% |
| warmonger | 849 | 120 | 14.1% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 1008 | 3.4% | 12.1% |
| coronation_milestone | 322 | 1.1% | 4.8% |
| objective | 27508 | 91.7% | 78.5% |
| lord_capture | 1176 | 3.9% | 4.6% |

**Seat + streak combined:** 4.4% of all VP

## Combat metrics (completed)

- Battles resolved: 5918
- Attacker win rate (all): 85.6%
- Battles per player-round: 0.229
- Contested attacker win rate: 68.4%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 5918 · attacker wins 85.6%
- Uncontested captures: 3218
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 2700 | 1846 | 68.4% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 2055 | 1788 | 87.0% |
| Ratio < 1.0 (att dice < def dice) | 645 | 58 | 9.0% |

**Contested attacker win rate:** 68.4% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 3233
- Events per round: 1.00
- Top events: border_skirmishes (418), mana_surge (417), festival (410), migration_wave (405), populist_uprising (398)

## High Council (M2)

- Motions proposed: 25864
- Motions passed: 6734
- Motions failed: 19130
- Pass rate: 26.0%
- Yes votes: 83989 · No votes: 122923 (40.6% yes)
- Motions per round: 8.00
- Influence spent (lobby): 6928
- Avg influence spent / round: 2.14

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 3233 | 12.5% |
| arcane_ascendancy | 3233 | 12.5% |
| economic_boom | 3233 | 12.5% |
| military_maneuvers | 3233 | 12.5% |
| diplomatic_decree | 3233 | 12.5% |
| expansion_strategy | 3233 | 12.5% |
| tactical_reinforcements | 3233 | 12.5% |
| imperial_mandate | 3233 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 617 | 49.7% |
| resource_surge | 487 | 39.2% |
| military_maneuvers | 138 | 11.1% |

**Secondary opt-in rate:** 100.0%

## Hypothesis evaluation (H1–H9)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=4.4 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=2.5, runaway_rate=0.037 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.785 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.046 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **inconclusive** | expander_win_rate=0.09, max_persona_win_rate=0.288 |
| H8 | Economist viable in mixed seats (builder/gold path) | **confirmed** | economist_win_rate=0.018 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.089, mixed_4p=False |
