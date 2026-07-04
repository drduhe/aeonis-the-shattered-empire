# Mixed 6p M3 baseline (post H7 calibration)

**Regenerated:** 2026-07-03 · **Config:** `sim/configs/bracket-6p-mixed.json` (200 games, seed_base 36000)

**Default sim stack:** M3 engine · **Lever C** expander brakes · **S1** `seat_of_empire` 1 VP.

Prior snapshot (pre-calibration): economist **2.6%** — see git history for `2026-07-03-baseline-mixed-6p-m3.md`.

---

# bracket-6p-mixed-m3

Games: 200 · Completed: 200 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 200 | 100.0% |

## Round length (completed)

- Mean: 6.4
- Median: 6

## Winning margin (completed)

- Mean: 3.0 VP
- Runaway rate (margin ≥7): 6.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 216 | 51 | 23.6% |
| diplomat | 228 | 34 | 14.9% |
| economist | 221 | 8 | 3.6% |
| expander | 222 | 32 | 14.4% |
| warmonger | 217 | 59 | 27.2% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 318 | 4.3% | 11.3% |
| coronation_milestone | 108 | 1.4% | 4.8% |
| objective | 6595 | 88.3% | 74.5% |
| lord_capture | 304 | 4.1% | 4.7% |
| artifact | 140 | 1.9% | 4.8% |

**Seat + streak combined:** 5.7% of all VP

## Combat metrics (completed)

- Battles resolved: 2126
- Attacker win rate (all): 84.9%
- Battles per player-round: 0.277
- Contested attacker win rate: 71.6%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 2126 · attacker wins 84.9%
- Uncontested captures: 994
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 1132 | 811 | 71.6% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 863 | 790 | 91.5% |
| Ratio < 1.0 (att dice < def dice) | 269 | 21 | 7.8% |

**Contested attacker win rate:** 71.6% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1281
- Events per round: 1.00
- Top events: council_crisis (120), border_skirmishes (112), festival (111), open_roads (110), ruins_unearthed (110)

## High Council (M2)

- Motions proposed: 7686
- Motions passed: 1619
- Motions failed: 6067
- Pass rate: 21.1%
- Yes votes: 19534 · No votes: 26582 (42.4% yes)
- Motions per round: 6.00
- Influence spent (lobby): 4444
- Avg influence spent / round: 3.47

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1281 | 16.7% |
| arcane_ascendancy | 1281 | 16.7% |
| military_maneuvers | 1281 | 16.7% |
| diplomatic_decree | 1119 | 14.6% |
| economic_boom | 780 | 10.1% |
| expansion_strategy | 764 | 9.9% |
| imperial_mandate | 590 | 7.7% |
| tactical_reinforcements | 590 | 7.7% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| resource_surge | 232 | 34.8% |
| economic_boom | 196 | 29.4% |
| military_maneuvers | 101 | 15.1% |
| expansion_strategy | 64 | 9.6% |
| arcane_ascendancy | 43 | 6.4% |
| imperial_mandate | 26 | 3.9% |
| tactical_reinforcements | 5 | 0.7% |

**Secondary opt-in rate:** 100.0%

## M3 card systems

### Whispers

- Drawn: 18789 · Played: 318 · Discarded: 78 · Sabotage: 187
- Plays per round: 0.25
- Sabotage rate: 58.8% of plays
- Forced discard rate: 0.4% of draws

### Artifacts

- Games with first artifact: 117/200
- Median first-artifact round: 2
- Artifact VP share: 1.9%

### Arcane research

- Discoveries per game: 3.04
- Discoveries per player-round: 0.079

## Hypothesis evaluation (H1–H12)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=5.7 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.02, runaway_rate=0.06 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.745 |
| H4 | 8p timeouts are pacing not map bug | **inconclusive** | timeout_rate_8p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.047 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.144, max_persona_win_rate=0.272 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.036 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.149, mixed_4p=False |
| H10 | Whisper draw rate keeps hands manageable (≤7 without flooding) | **killed** | whisper_discard_rate=0.004, plays_per_round=0.25 |
| H11 | First artifact by round 3–4 (packet goal 10) | **inconclusive** | median_first_artifact_round=2, artifact_vp_share=0.019 |
| H12 | Merchant Lord lifts economist mixed 4p win rate ≥5% | **inconclusive** | economist_win_rate_4p=0.036, mixed_4p=False |
