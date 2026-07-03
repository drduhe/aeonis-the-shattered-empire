# m2-bracket-a-4p-solo

Games: 200 · Completed: 200 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 200 | 100.0% |

## Round length (completed)

- Mean: 6.3
- Median: 6

## Winning margin (completed)

- Mean: 3.4 VP
- Runaway rate (margin ≥7): 15.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 152 | 38 | 25.0% |
| diplomat | 148 | 37 | 25.0% |
| economist | 144 | 36 | 25.0% |
| expander | 156 | 39 | 25.0% |
| warmonger | 148 | 37 | 25.0% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 320 | 5.8% | 11.8% |
| coronation_milestone | 96 | 1.7% | 4.3% |
| objective | 4912 | 88.3% | 79.1% |
| lord_capture | 235 | 4.2% | 4.8% |

**Seat + streak combined:** 7.5% of all VP

## Combat metrics (completed)

- Battles resolved: 796
- Attacker win rate (all): 79.9%
- Battles per player-round: 0.158
- Contested attacker win rate: 66.1%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 796 · attacker wins 79.9%
- Uncontested captures: 324
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 472 | 312 | 66.1% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 339 | 304 | 89.7% |
| Ratio < 1.0 (att dice < def dice) | 133 | 8 | 6.0% |

**Contested attacker win rate:** 66.1% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1260
- Events per round: 1.00
- Top events: mana_surge (161), winds_of_fortune (160), border_skirmishes (160), harsh_winter (159), festival (158)

## High Council (M2)

- Motions proposed: 5040
- Motions passed: 1654
- Motions failed: 3386
- Pass rate: 32.8%
- Yes votes: 9971 · No votes: 10189 (49.5% yes)
- Motions per round: 4.00
- Influence spent (lobby): 1780
- Avg influence spent / round: 1.41

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1260 | 12.5% |
| arcane_ascendancy | 1260 | 12.5% |
| military_maneuvers | 1260 | 12.5% |
| diplomatic_decree | 1260 | 12.5% |
| expansion_strategy | 1260 | 12.5% |
| economic_boom | 1260 | 12.5% |
| tactical_reinforcements | 1260 | 12.5% |
| imperial_mandate | 1260 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 146 | 42.4% |
| resource_surge | 100 | 29.1% |
| military_maneuvers | 98 | 28.5% |

**Secondary opt-in rate:** 100.0%

## Hypothesis evaluation (H1–H9)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=7.5 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.44, runaway_rate=0.15 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.791 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.048 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.25, max_persona_win_rate=0.25 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.25 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.25, mixed_4p=False |
