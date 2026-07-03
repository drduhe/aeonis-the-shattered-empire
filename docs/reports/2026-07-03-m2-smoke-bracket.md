# m2-smoke-4p-mixed

Games: 100 · Completed: 100 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 100 | 100.0% |

## Round length (completed)

- Mean: 5.9
- Median: 5

## Winning margin (completed)

- Mean: 4.0 VP
- Runaway rate (margin ≥7): 15.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 72 | 17 | 23.6% |
| diplomat | 77 | 7 | 9.1% |
| economist | 79 | 0 | 0.0% |
| expander | 76 | 52 | 68.4% |
| warmonger | 88 | 22 | 25.0% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 232 | 8.5% | 17.6% |
| coronation_milestone | 82 | 3.0% | 7.1% |
| objective | 2288 | 83.5% | 69.3% |
| lord_capture | 138 | 5.0% | 6.0% |

**Seat + streak combined:** 11.5% of all VP

## Combat metrics (completed)

- Battles resolved: 505
- Attacker win rate (all): 84.0%
- Battles per player-round: 0.215
- Contested attacker win rate: 70.0%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 505 · attacker wins 84.0%
- Uncontested captures: 235
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 270 | 189 | 70.0% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 204 | 188 | 92.2% |
| Ratio < 1.0 (att dice < def dice) | 66 | 1 | 1.5% |

**Contested attacker win rate:** 70.0% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 586
- Events per round: 1.00
- Top events: harsh_winter (81), populist_uprising (76), winds_of_fortune (75), mana_surge (74), border_skirmishes (74)

## High Council (M2)

- Motions proposed: 2344
- Motions passed: 671
- Motions failed: 1673
- Pass rate: 28.6%
- Yes votes: 4592 · No votes: 4784 (49.0% yes)
- Motions per round: 4.00
- Influence spent (lobby): 790
- Avg influence spent / round: 1.35

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 586 | 12.5% |
| arcane_ascendancy | 586 | 12.5% |
| military_maneuvers | 586 | 12.5% |
| diplomatic_decree | 586 | 12.5% |
| expansion_strategy | 586 | 12.5% |
| economic_boom | 586 | 12.5% |
| tactical_reinforcements | 586 | 12.5% |
| imperial_mandate | 586 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 83 | 43.9% |
| resource_surge | 65 | 34.4% |
| military_maneuvers | 41 | 21.7% |

**Secondary opt-in rate:** 100.0%

## Hypothesis evaluation (H1–H9)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=11.5 |
| H2 | Winning margin >5 VP under strategic play | **inconclusive** | avg_margin=4.0, runaway_rate=0.15 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.693 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.06 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **confirmed** | expander_win_rate=0.684, max_persona_win_rate=0.684 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.0 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **killed** | diplomat_win_rate=0.091, mixed_4p=True |
