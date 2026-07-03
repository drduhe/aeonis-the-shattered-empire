# bracket-8p-mixed-m3

Games: 200 · Completed: 200 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 200 | 100.0% |

## Round length (completed)

- Mean: 5.8
- Median: 6

## Winning margin (completed)

- Mean: 2.7 VP
- Runaway rate (margin ≥7): 4.5%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 306 | 67 | 21.9% |
| diplomat | 296 | 34 | 11.5% |
| economist | 309 | 7 | 2.3% |
| expander | 287 | 33 | 11.5% |
| warmonger | 306 | 47 | 15.4% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 251 | 2.6% | 8.3% |
| coronation_milestone | 68 | 0.7% | 3.0% |
| objective | 8642 | 90.7% | 78.6% |
| lord_capture | 390 | 4.1% | 4.8% |
| artifact | 176 | 1.8% | 5.2% |

**Seat + streak combined:** 3.3% of all VP

## Combat metrics (completed)

- Battles resolved: 2482
- Attacker win rate (all): 83.8%
- Battles per player-round: 0.267
- Contested attacker win rate: 69.0%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 2482 · attacker wins 83.8%
- Uncontested captures: 1182
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 1300 | 897 | 69.0% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 955 | 872 | 91.3% |
| Ratio < 1.0 (att dice < def dice) | 345 | 25 | 7.2% |

**Contested attacker win rate:** 69.0% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1160
- Events per round: 1.00
- Top events: festival (110), council_crisis (102), border_skirmishes (100), populist_uprising (99), supply_disruption (98)

## High Council (M2)

- Motions proposed: 9280
- Motions passed: 2039
- Motions failed: 7241
- Pass rate: 22.0%
- Yes votes: 29249 · No votes: 44991 (39.4% yes)
- Motions per round: 8.00
- Influence spent (lobby): 4982
- Avg influence spent / round: 4.29

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1160 | 12.5% |
| arcane_ascendancy | 1160 | 12.5% |
| military_maneuvers | 1160 | 12.5% |
| diplomatic_decree | 1160 | 12.5% |
| economic_boom | 1160 | 12.5% |
| expansion_strategy | 1160 | 12.5% |
| tactical_reinforcements | 1160 | 12.5% |
| imperial_mandate | 1160 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| resource_surge | 230 | 37.2% |
| economic_boom | 217 | 35.1% |
| military_maneuvers | 60 | 9.7% |
| expansion_strategy | 42 | 6.8% |
| imperial_mandate | 35 | 5.7% |
| arcane_ascendancy | 22 | 3.6% |
| tactical_reinforcements | 12 | 1.9% |

**Secondary opt-in rate:** 100.0%

## M3 card systems

### Whispers

- Drawn: 22645 · Played: 267 · Discarded: 8 · Sabotage: 171
- Plays per round: 0.23
- Sabotage rate: 64.0% of plays
- Forced discard rate: 0.0% of draws

### Artifacts

- Games with first artifact: 122/200
- Median first-artifact round: 3
- Artifact VP share: 1.8%

### Arcane research

- Discoveries per game: 2.64
- Discoveries per player-round: 0.057

## Hypothesis evaluation (H1–H12)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=3.3 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=2.66, runaway_rate=0.045 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.786 |
| H4 | 8p timeouts are pacing not map bug | **killed** | timeout_rate_8p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.048 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.115, max_persona_win_rate=0.219 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.023 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.115, mixed_4p=False |
| H10 | Whisper draw rate keeps hands manageable (≤7 without flooding) | **killed** | whisper_discard_rate=0.0, plays_per_round=0.23 |
| H11 | First artifact by round 3–4 (packet goal 10) | **killed** | median_first_artifact_round=3.0, artifact_vp_share=0.018 |
| H12 | Merchant Lord lifts economist mixed 4p win rate ≥5% | **inconclusive** | economist_win_rate_4p=0.023, mixed_4p=False |
