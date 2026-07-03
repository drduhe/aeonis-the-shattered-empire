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

- Mean: 3.7 VP
- Runaway rate (margin ≥7): 16.5%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 160 | 40 | 25.0% |
| diplomat | 148 | 37 | 25.0% |
| economist | 152 | 38 | 25.0% |
| expander | 160 | 40 | 25.0% |
| warmonger | 152 | 38 | 25.0% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 331 | 6.1% | 12.3% |
| coronation_milestone | 90 | 1.7% | 4.0% |
| objective | 4736 | 87.5% | 78.7% |
| lord_capture | 256 | 4.7% | 5.0% |

**Seat + streak combined:** 7.8% of all VP

## Combat metrics (completed)

- Battles resolved: 875
- Attacker win rate (all): 80.7%
- Battles per player-round: 0.141
- Contested attacker win rate: 67.1%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 875 · attacker wins 80.7%
- Uncontested captures: 362
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 513 | 344 | 67.1% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 380 | 337 | 88.7% |
| Ratio < 1.0 (att dice < def dice) | 133 | 7 | 5.3% |

**Contested attacker win rate:** 67.1% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1555
- Events per round: 1.00
- Top events: festival (205), mana_surge (198), harsh_winter (198), populist_uprising (197), supply_disruption (194)

## High Council (M2)

- Motions proposed: 6220
- Motions passed: 2017
- Motions failed: 4203
- Pass rate: 32.4%
- Yes votes: 12185 · No votes: 12695 (49.0% yes)
- Motions per round: 4.00
- Influence spent (lobby): 2902
- Avg influence spent / round: 1.87

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1555 | 12.5% |
| arcane_ascendancy | 1555 | 12.5% |
| military_maneuvers | 1555 | 12.5% |
| diplomatic_decree | 1555 | 12.5% |
| expansion_strategy | 1555 | 12.5% |
| economic_boom | 1555 | 12.5% |
| tactical_reinforcements | 1555 | 12.5% |
| imperial_mandate | 1555 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 123 | 41.6% |
| resource_surge | 92 | 31.1% |
| military_maneuvers | 81 | 27.4% |

**Secondary opt-in rate:** 100.0%

## Hypothesis evaluation (H1–H9)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=7.8 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.68, runaway_rate=0.165 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.787 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.05 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.25, max_persona_win_rate=0.25 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.25 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.25, mixed_4p=False |
