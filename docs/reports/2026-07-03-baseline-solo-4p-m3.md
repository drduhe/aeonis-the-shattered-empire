# m2-bracket-a-4p-solo

Games: 200 · Completed: 200 (100.0%)

## Verdict breakdown

| Verdict | Count | % |
| --- | ---: | ---: |
| completed | 200 | 100.0% |

## Round length (completed)

- Mean: 6.0
- Median: 6

## Winning margin (completed)

- Mean: 3.6 VP
- Runaway rate (margin ≥7): 14.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 156 | 39 | 25.0% |
| diplomat | 148 | 37 | 25.0% |
| economist | 160 | 40 | 25.0% |
| expander | 148 | 37 | 25.0% |
| warmonger | 156 | 39 | 25.0% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 308 | 5.7% | 10.7% |
| coronation_milestone | 76 | 1.4% | 3.3% |
| objective | 4742 | 88.0% | 79.7% |
| lord_capture | 180 | 3.3% | 3.5% |
| artifact | 82 | 1.5% | 2.6% |

**Seat + streak combined:** 7.1% of all VP

## Combat metrics (completed)

- Battles resolved: 864
- Attacker win rate (all): 79.7%
- Battles per player-round: 0.179
- Contested attacker win rate: 66.5%

## Combat stratification (contested initiations)

Initiation quality uses committed **attack dice** vs **defense dice** at battle start. Uncontested captures (no defender units) and retreats are tracked separately and excluded from contested win rates.

- All battles (legacy): 864 · attacker wins 79.7%
- Uncontested captures: 342
- Defender retreats: 0

| Bucket | Battles | Att wins | Att win % |
| --- | ---: | ---: | ---: |
| Contested (all) | 522 | 347 | 66.5% |
| Ratio ≥ 1.0 (att dice ≥ def dice) | 373 | 339 | 90.9% |
| Ratio < 1.0 (att dice < def dice) | 149 | 8 | 5.4% |

**Contested attacker win rate:** 66.5% (Plan 1 human target: 55–65%)

## Event phase (M2)

- Events resolved: 1206
- Events per round: 1.00
- Top events: council_crisis (110), harsh_winter (105), open_roads (103), ruins_unearthed (103), winds_of_fortune (102)

## High Council (M2)

- Motions proposed: 4824
- Motions passed: 1193
- Motions failed: 3631
- Pass rate: 24.7%
- Yes votes: 9388 · No votes: 9908 (48.7% yes)
- Motions per round: 4.00
- Influence spent (lobby): 3360
- Avg influence spent / round: 2.79

## Strategy cards (M2)

### Draft pick rate

| Card | Picks | % |
| --- | ---: | ---: |
| resource_surge | 1206 | 12.5% |
| arcane_ascendancy | 1206 | 12.5% |
| military_maneuvers | 1206 | 12.5% |
| diplomatic_decree | 1206 | 12.5% |
| expansion_strategy | 1206 | 12.5% |
| economic_boom | 1206 | 12.5% |
| tactical_reinforcements | 1206 | 12.5% |
| imperial_mandate | 1206 | 12.5% |

### Primary use rate (among primaries played)

| Card | Uses | % |
| --- | ---: | ---: |
| economic_boom | 143 | 38.3% |
| resource_surge | 113 | 30.3% |
| military_maneuvers | 64 | 17.2% |
| expansion_strategy | 17 | 4.6% |
| tactical_reinforcements | 14 | 3.8% |
| imperial_mandate | 12 | 3.2% |
| arcane_ascendancy | 10 | 2.7% |

**Secondary opt-in rate:** 100.0%

## M3 card systems

### Whispers

- Drawn: 12037 · Played: 287 · Discarded: 262 · Sabotage: 79
- Plays per round: 0.24
- Sabotage rate: 27.5% of plays
- Forced discard rate: 2.2% of draws

### Artifacts

- Games with first artifact: 47/200
- Median first-artifact round: 3
- Artifact VP share: 1.5%

### Arcane research

- Discoveries per game: 0.90
- Discoveries per player-round: 0.037

## Hypothesis evaluation (H1–H12)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=7.1 |
| H2 | Winning margin >5 VP under strategic play | **killed** | avg_margin=3.56, runaway_rate=0.14 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.797 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.035 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **killed** | expander_win_rate=0.25, max_persona_win_rate=0.25 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.25 |
| H9 | Diplomat win rate ≥3% in mixed 4p M2 bracket | **inconclusive** | diplomat_win_rate=0.25, mixed_4p=False |
| H10 | Whisper draw rate keeps hands manageable (≤7 without flooding) | **killed** | whisper_discard_rate=0.022, plays_per_round=0.24 |
| H11 | First artifact by round 3–4 (packet goal 10) | **killed** | median_first_artifact_round=3, artifact_vp_share=0.015 |
| H12 | Merchant Lord lifts economist mixed 4p win rate ≥5% | **inconclusive** | economist_win_rate_4p=0.25, mixed_4p=False |
