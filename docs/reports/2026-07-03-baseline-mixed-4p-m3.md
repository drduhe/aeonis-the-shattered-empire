# m2-smoke-4p-mixed

Games: 100 · Completed: 100 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 100 | 100.0% |

## Round length (completed)

- Mean: 5.8
- Median: 6

## Winning margin (completed)

- Mean: 3.1 VP
- Runaway rate (margin ≥7): 6.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 70 | 26 | 37.1% |
| diplomat | 74 | 16 | 21.6% |
| economist | 76 | 4 | 5.3% |
| expander | 74 | 30 | 40.5% |
| warmonger | 86 | 19 | 22.1% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 146 | 5.2% | 10.5% |
| coronation_milestone | 34 | 1.2% | 2.9% |
| objective | 2458 | 88.1% | 79.5% |
| lord_capture | 125 | 4.5% | 5.1% |
| artifact | 19 | 0.7% | 1.3% |

**Seat + streak combined:** 6.5% of all VP

## Combat metrics (completed)

- Battles resolved: 639
- Attacker win rate (all): 83.6%
- Battles per player-round: 0.274
- Contested attacker win rate: 73.4%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 639 · attacker wins 83.6%
- Uncontested captures: 245
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 394 | 289 | 73.4% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 305 | 283 | 92.8% |
| Ratio < 1.0 (att dice < def dice) | 89 | 6 | 6.7% |

**Contested attacker win rate:** 73.4% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 582
- Events per round: 1.00
- Top events: harsh_winter (58), open_roads (55), supply_disruption (54), winds_of_fortune (53), festival (51)

## High Council (M2)

- Motions proposed: 2328
- Motions passed: 503
- Motions failed: 1825
- Pass rate: 21.6%
- Yes votes: 4377 · No votes: 4935 (47.0% yes)
- Motions per round: 4.00
- Influence spent (lobby): 1536
- Avg influence spent / round: 2.64

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 582 | 12.5% |
| arcane_ascendancy | 582 | 12.5% |
| military_maneuvers | 582 | 12.5% |
| expansion_strategy | 582 | 12.5% |
| economic_boom | 582 | 12.5% |
| diplomatic_decree | 582 | 12.5% |
| tactical_reinforcements | 582 | 12.5% |
| imperial_mandate | 582 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 69 | 36.5% |
| resource_surge | 52 | 27.5% |
| military_maneuvers | 28 | 14.8% |
| imperial_mandate | 18 | 9.5% |
| expansion_strategy | 17 | 9.0% |
| arcane_ascendancy | 5 | 2.6% |

**Secondary opt-in rate:** 100.0%

## M3 card systems

### Whispers

- Drawn: 5857 · Played: 159 · Discarded: 76 · Sabotage: 64
- Plays per round: 0.27
- Sabotage rate: 40.3% of plays
- Forced discard rate: 1.3% of draws

### Artifacts

- Games with first artifact: 45/100
- Median first-artifact round: 3
- Artifact VP share: 0.7%

### Arcane research

- Discoveries per game: 1.30
- Discoveries per player-round: 0.056

## Hypothesis evaluation (H1–H12)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=6.5 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.12, runaway_rate=0.06 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.795 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.051 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **confirmed** | expander_win_rate=0.405, max_persona_win_rate=0.405 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.053 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **killed** | diplomat_win_rate=0.216, mixed_4p=True |
| H10 | Whisper draw rate keeps hands manageable (≤7 without flooding) | **killed** | whisper_discard_rate=0.013, plays_per_round=0.27 |
| H11 | First artifact by round 3–4 (packet goal 10) | **killed** | median_first_artifact_round=3, artifact_vp_share=0.007 |
| H12 | Merchant Lord lifts economist mixed 4p win rate ≥5% | **killed** | economist_win_rate_4p=0.053, mixed_4p=True |
