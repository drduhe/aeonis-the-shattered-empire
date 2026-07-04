# Mixed 4p M3 baseline (post H7 calibration)

**Regenerated:** 2026-07-03 · **Config:** `sim/configs/bracket-m2-smoke.json` (100 games, seed_base 70000)

**Default sim stack:** M3 engine · **Lever C** expander lead brakes (`persona.py`) · **S1** `seat_of_empire` 1 VP (`seat_rewards.seat_of_empire_vp`).

Prior snapshot (pre-calibration, expander 40.5%): see [H7 report](2026-07-03-h7-expander-dominance-m3.md).

---

# m2-smoke-4p-mixed

Games: 100 · Completed: 100 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 100 | 100.0% |

## Round length (completed)

- Mean: 6.2
- Median: 6

## Winning margin (completed)

- Mean: 3.2 VP
- Runaway rate (margin ≥7): 7.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 68 | 23 | 33.8% |
| diplomat | 75 | 20 | 26.7% |
| economist | 75 | 8 | 10.7% |
| expander | 73 | 17 | 23.3% |
| warmonger | 85 | 26 | 30.6% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 128 | 4.5% | 7.7% |
| coronation_milestone | 20 | 0.7% | 1.3% |
| objective | 2506 | 88.8% | 82.6% |
| lord_capture | 138 | 4.9% | 6.5% |
| artifact | 27 | 1.0% | 1.8% |

**Seat + streak combined:** 5.2% of all VP

## Combat metrics (completed)

- Battles resolved: 745
- Attacker win rate (all): 78.4%
- Battles per player-round: 0.298
- Contested attacker win rate: 65.0%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 745 · attacker wins 78.4%
- Uncontested captures: 285
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 460 | 299 | 65.0% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 306 | 288 | 94.1% |
| Ratio < 1.0 (att dice < def dice) | 154 | 11 | 7.1% |

**Contested attacker win rate:** 65.0% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 625
- Events per round: 1.00
- Top events: harsh_winter (60), supply_disruption (59), festival (58), open_roads (55), winds_of_fortune (54)

## High Council (M2)

- Motions proposed: 2500
- Motions passed: 544
- Motions failed: 1956
- Pass rate: 21.8%
- Yes votes: 4764 · No votes: 5236 (47.6% yes)
- Motions per round: 4.00
- Influence spent (lobby): 1738
- Avg influence spent / round: 2.78

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 625 | 12.5% |
| arcane_ascendancy | 625 | 12.5% |
| military_maneuvers | 625 | 12.5% |
| expansion_strategy | 625 | 12.5% |
| economic_boom | 625 | 12.5% |
| diplomatic_decree | 625 | 12.5% |
| tactical_reinforcements | 625 | 12.5% |
| imperial_mandate | 625 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| resource_surge | 117 | 37.3% |
| economic_boom | 72 | 22.9% |
| military_maneuvers | 56 | 17.8% |
| expansion_strategy | 32 | 10.2% |
| imperial_mandate | 19 | 6.1% |
| arcane_ascendancy | 12 | 3.8% |
| tactical_reinforcements | 6 | 1.9% |

**Secondary opt-in rate:** 100.0%

## M3 card systems

### Whispers

- Drawn: 6305 · Played: 183 · Discarded: 122 · Sabotage: 79
- Plays per round: 0.29
- Sabotage rate: 43.2% of plays
- Forced discard rate: 1.9% of draws

### Artifacts

- Games with first artifact: 51/100
- Median first-artifact round: 3
- Artifact VP share: 1.0%

### Arcane research

- Discoveries per game: 2.21
- Discoveries per player-round: 0.088

## Hypothesis evaluation (H1–H12)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=5.2 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.25, runaway_rate=0.07 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.826 |
| H4 | 8p timeouts are pacing not map bug | **inconclusive** | timeout_rate_8p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.065 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **inconclusive** | expander_win_rate=0.233, max_persona_win_rate=0.338 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.107 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **killed** | diplomat_win_rate=0.267, mixed_4p=True |
| H10 | Whisper draw rate keeps hands manageable (≤7 without flooding) | **killed** | whisper_discard_rate=0.019, plays_per_round=0.29 |
| H11 | First artifact by round 3–4 (packet goal 10) | **killed** | median_first_artifact_round=3, artifact_vp_share=0.01 |
| H12 | Merchant Lord lifts economist mixed 4p win rate ≥5% | **killed** | economist_win_rate_4p=0.107, mixed_4p=True |
