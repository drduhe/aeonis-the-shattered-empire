# bracket-6p-mixed-m3

Games: 200 · Completed: 200 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 200 | 100.0% |

## Round length (completed)

- Mean: 5.8
- Median: 6

## Winning margin (completed)

- Mean: 3.3 VP
- Runaway rate (margin ≥7): 8.5%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 225 | 48 | 21.3% |
| diplomat | 235 | 32 | 13.6% |
| economist | 229 | 6 | 2.6% |
| expander | 229 | 48 | 21.0% |
| warmonger | 222 | 56 | 25.2% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 324 | 4.5% | 11.0% |
| coronation_milestone | 104 | 1.4% | 4.5% |
| objective | 6412 | 89.2% | 76.4% |
| lord_capture | 251 | 3.5% | 4.5% |
| artifact | 101 | 1.4% | 3.5% |

**Seat + streak combined:** 6.0% of all VP

## Combat metrics (completed)

- Battles resolved: 1734
- Attacker win rate (all): 87.3%
- Battles per player-round: 0.248
- Contested attacker win rate: 76.8%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 1734 · attacker wins 87.3%
- Uncontested captures: 786
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 948 | 728 | 76.8% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 771 | 712 | 92.3% |
| Ratio < 1.0 (att dice < def dice) | 177 | 16 | 9.0% |

**Contested attacker win rate:** 76.8% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1163
- Events per round: 1.00
- Top events: council_crisis (110), ruins_unearthed (105), festival (104), populist_uprising (98), winds_of_fortune (96)

## High Council (M2)

- Motions proposed: 6978
- Motions passed: 1507
- Motions failed: 5471
- Pass rate: 21.6%
- Yes votes: 18040 · No votes: 23828 (43.1% yes)
- Motions per round: 6.00
- Influence spent (lobby): 3838
- Avg influence spent / round: 3.30

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1163 | 16.7% |
| arcane_ascendancy | 1163 | 16.7% |
| military_maneuvers | 1163 | 16.7% |
| diplomatic_decree | 1019 | 14.6% |
| expansion_strategy | 710 | 10.2% |
| economic_boom | 702 | 10.1% |
| tactical_reinforcements | 529 | 7.6% |
| imperial_mandate | 529 | 7.6% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| resource_surge | 173 | 35.9% |
| economic_boom | 170 | 35.3% |
| military_maneuvers | 70 | 14.5% |
| expansion_strategy | 36 | 7.5% |
| arcane_ascendancy | 22 | 4.6% |
| imperial_mandate | 7 | 1.5% |
| tactical_reinforcements | 4 | 0.8% |

**Secondary opt-in rate:** 100.0%

## M3 card systems

### Whispers

- Drawn: 17047 · Played: 256 · Discarded: 41 · Sabotage: 145
- Plays per round: 0.22
- Sabotage rate: 56.6% of plays
- Forced discard rate: 0.2% of draws

### Artifacts

- Games with first artifact: 104/200
- Median first-artifact round: 2
- Artifact VP share: 1.4%

### Arcane research

- Discoveries per game: 2.00
- Discoveries per player-round: 0.057

## Hypothesis evaluation (H1–H12)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=6.0 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.28, runaway_rate=0.085 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.764 |
| H4 | 8p timeouts are pacing not map bug | **inconclusive** | timeout_rate_8p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.045 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.21, max_persona_win_rate=0.252 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.026 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.136, mixed_4p=False |
| H10 | Whisper draw rate keeps hands manageable (≤7 without flooding) | **killed** | whisper_discard_rate=0.002, plays_per_round=0.22 |
| H11 | First artifact by round 3–4 (packet goal 10) | **inconclusive** | median_first_artifact_round=2.0, artifact_vp_share=0.014 |
| H12 | Merchant Lord lifts economist mixed 4p win rate ≥5% | **inconclusive** | economist_win_rate_4p=0.026, mixed_4p=False |
