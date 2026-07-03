# m2-smoke-4p-mixed

Games: 100 · Completed: 100 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 100 | 100.0% |

## Round length (completed)

- Mean: 6.4
- Median: 6

## Winning margin (completed)

- Mean: 3.2 VP
- Runaway rate (margin ≥7): 7.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 71 | 30 | 42.3% |
| diplomat | 78 | 10 | 12.8% |
| economist | 79 | 2 | 2.5% |
| expander | 76 | 22 | 28.9% |
| warmonger | 88 | 34 | 38.6% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 203 | 7.1% | 13.5% |
| coronation_milestone | 54 | 1.9% | 4.6% |
| objective | 2422 | 85.2% | 74.8% |
| lord_capture | 164 | 5.8% | 7.1% |

**Seat + streak combined:** 9.0% of all VP

## Combat metrics (completed)

- Battles resolved: 609
- Attacker win rate (all): 81.9%
- Battles per player-round: 0.236
- Contested attacker win rate: 66.8%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 609 · attacker wins 81.9%
- Uncontested captures: 278
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 331 | 221 | 66.8% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 239 | 214 | 89.5% |
| Ratio < 1.0 (att dice < def dice) | 92 | 7 | 7.6% |

**Contested attacker win rate:** 66.8% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 644
- Events per round: 1.00
- Top events: festival (84), populist_uprising (84), harsh_winter (83), mana_surge (82), winds_of_fortune (81)

## High Council (M2)

- Motions proposed: 2576
- Motions passed: 739
- Motions failed: 1837
- Pass rate: 28.7%
- Yes votes: 5049 · No votes: 5255 (49.0% yes)
- Motions per round: 4.00
- Influence spent (lobby): 932
- Avg influence spent / round: 1.45

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 644 | 12.5% |
| arcane_ascendancy | 644 | 12.5% |
| military_maneuvers | 644 | 12.5% |
| expansion_strategy | 644 | 12.5% |
| economic_boom | 644 | 12.5% |
| diplomatic_decree | 644 | 12.5% |
| tactical_reinforcements | 644 | 12.5% |
| imperial_mandate | 644 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| resource_surge | 67 | 35.3% |
| economic_boom | 64 | 33.7% |
| military_maneuvers | 59 | 31.1% |

**Secondary opt-in rate:** 100.0%

## Hypothesis evaluation (H1–H9)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=9.0 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.19, runaway_rate=0.07 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.748 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.071 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **confirmed** | expander_win_rate=0.289, max_persona_win_rate=0.423 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.025 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **killed** | diplomat_win_rate=0.128, mixed_4p=True |
