# Mixed 8p M3 baseline (post H7 calibration)

**Regenerated:** 2026-07-03 · **Config:** `sim/configs/bracket-8p-mixed.json` (200 games, seed_base 38000)

**Default sim stack:** M3 engine · **Lever C** expander brakes · **S1** `seat_of_empire` 1 VP.

Prior snapshot (pre-calibration): economist **2.3%** — see git history for `2026-07-03-baseline-mixed-8p-m3.md`.

---

# bracket-8p-mixed-m3

Games: 200 · Completed: 200 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 200 | 100.0% |

## Round length (completed)

- Mean: 6.2
- Median: 6

## Winning margin (completed)

- Mean: 2.4 VP
- Runaway rate (margin ≥7): 2.5%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 296 | 67 | 22.6% |
| diplomat | 285 | 26 | 9.1% |
| economist | 293 | 6 | 2.0% |
| expander | 269 | 29 | 10.8% |
| warmonger | 289 | 51 | 17.6% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 292 | 3.0% | 9.4% |
| coronation_milestone | 102 | 1.0% | 4.5% |
| objective | 8779 | 89.8% | 75.7% |
| lord_capture | 400 | 4.1% | 5.3% |
| artifact | 200 | 2.0% | 5.1% |

**Seat + streak combined:** 4.0% of all VP

## Combat metrics (completed)

- Battles resolved: 2837
- Attacker win rate (all): 83.7%
- Battles per player-round: 0.285
- Contested attacker win rate: 68.0%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 2837 · attacker wins 83.7%
- Uncontested captures: 1391
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 1446 | 983 | 68.0% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 1037 | 958 | 92.4% |
| Ratio < 1.0 (att dice < def dice) | 409 | 25 | 6.1% |

**Contested attacker win rate:** 68.0% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1244
- Events per round: 1.00
- Top events: open_roads (116), council_crisis (114), festival (113), border_skirmishes (106), echo_of_the_old_empire (105)

## High Council (M2)

- Motions proposed: 9952
- Motions passed: 2272
- Motions failed: 7680
- Pass rate: 22.8%
- Yes votes: 32049 · No votes: 47567 (40.3% yes)
- Motions per round: 8.00
- Influence spent (lobby): 5436
- Avg influence spent / round: 4.37

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1244 | 12.5% |
| arcane_ascendancy | 1244 | 12.5% |
| military_maneuvers | 1244 | 12.5% |
| diplomatic_decree | 1244 | 12.5% |
| economic_boom | 1244 | 12.5% |
| expansion_strategy | 1244 | 12.5% |
| tactical_reinforcements | 1244 | 12.5% |
| imperial_mandate | 1244 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| resource_surge | 302 | 36.6% |
| economic_boom | 210 | 25.4% |
| military_maneuvers | 108 | 13.1% |
| expansion_strategy | 86 | 10.4% |
| imperial_mandate | 55 | 6.7% |
| arcane_ascendancy | 45 | 5.4% |
| tactical_reinforcements | 20 | 2.4% |

**Secondary opt-in rate:** 100.0%

## M3 card systems

### Whispers

- Drawn: 24317 · Played: 311 · Discarded: 20 · Sabotage: 200
- Plays per round: 0.25
- Sabotage rate: 64.3% of plays
- Forced discard rate: 0.1% of draws

### Artifacts

- Games with first artifact: 157/200
- Median first-artifact round: 2
- Artifact VP share: 2.0%

### Arcane research

- Discoveries per game: 4.50
- Discoveries per player-round: 0.091

## Hypothesis evaluation (H1–H12)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=4.0 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=2.42, runaway_rate=0.025 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.757 |
| H4 | 8p timeouts are pacing not map bug | **killed** | timeout_rate_8p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.053 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.108, max_persona_win_rate=0.226 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.02 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.091, mixed_4p=False |
| H10 | Whisper draw rate keeps hands manageable (≤7 without flooding) | **killed** | whisper_discard_rate=0.001, plays_per_round=0.25 |
| H11 | First artifact by round 3–4 (packet goal 10) | **inconclusive** | median_first_artifact_round=2, artifact_vp_share=0.02 |
| H12 | Merchant Lord lifts economist mixed 4p win rate ≥5% | **inconclusive** | economist_win_rate_4p=0.02, mixed_4p=False |
