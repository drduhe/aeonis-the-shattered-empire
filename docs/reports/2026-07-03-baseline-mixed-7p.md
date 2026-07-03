# bracket-c-pacing-7p-mixed-mvp

Games: 200 · Completed: 200 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 200 | 100.0% |

## Round length (completed)

- Mean: 5.3
- Median: 5

## Winning margin (completed)

- Mean: 2.5 VP
- Runaway rate (margin ≥7): 4.5%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 247 | 70 | 28.3% |
| diplomat | 252 | 30 | 11.9% |
| economist | 255 | 7 | 2.7% |
| expander | 249 | 19 | 7.6% |
| warmonger | 271 | 56 | 20.7% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 297 | 3.2% | 10.3% |
| coronation_milestone | 88 | 1.0% | 4.0% |
| objective | 8468 | 92.5% | 80.6% |
| lord_capture | 301 | 3.3% | 5.1% |

**Seat + streak combined:** 4.2% of all VP

## Combat metrics (completed)

- Battles resolved: 1670
- Attacker win rate (all): 85.7%
- Battles per player-round: 0.223
- Contested attacker win rate: 65.6%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 1670 · attacker wins 85.7%
- Uncontested captures: 978
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 692 | 454 | 65.6% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 507 | 443 | 87.4% |
| Ratio < 1.0 (att dice < def dice) | 185 | 11 | 5.9% |

**Contested attacker win rate:** 65.6% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1069
- Events per round: 1.00
- Top events: border_skirmishes (146), populist_uprising (138), winds_of_fortune (137), festival (136), supply_disruption (131)

## High Council (M2)

- Motions proposed: 7483
- Motions passed: 1995
- Motions failed: 5488
- Pass rate: 26.7%
- Yes votes: 22007 · No votes: 30374 (42.0% yes)
- Motions per round: 7.00
- Influence spent (lobby): 1386
- Avg influence spent / round: 1.30

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1069 | 14.3% |
| arcane_ascendancy | 1069 | 14.3% |
| military_maneuvers | 1069 | 14.3% |
| diplomatic_decree | 1069 | 14.3% |
| expansion_strategy | 1069 | 14.3% |
| economic_boom | 1069 | 14.3% |
| tactical_reinforcements | 577 | 7.7% |
| imperial_mandate | 492 | 6.6% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 176 | 43.7% |
| resource_surge | 159 | 39.5% |
| military_maneuvers | 68 | 16.9% |

**Secondary opt-in rate:** 100.0%

## Hypothesis evaluation (H1–H9)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=4.2 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=2.48, runaway_rate=0.045 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.806 |
| H4 | 7p timeouts are pacing not map bug | **killed** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.051 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **inconclusive** | expander_win_rate=0.076, max_persona_win_rate=0.283 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.027 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.119, mixed_4p=False |
