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

- Mean: 4.1 VP
- Runaway rate (margin ≥7): 18.0%

## Win rate by persona (seat games, completed only)

| Persona | Games | Wins | Win % |
| --- | ---: | ---: | ---: |
| balanced | 70 | 11 | 15.7% |
| diplomat | 76 | 12 | 15.8% |
| economist | 77 | 0 | 0.0% |
| expander | 77 | 51 | 66.2% |
| warmonger | 88 | 23 | 26.1% |

## VP sources (all VP in completed games)

| Source | VP | % of total | % of winner VP (avg) |
| --- | ---: | ---: | ---: |
| coronation_rite | 240 | 8.8% | 18.4% |
| coronation_milestone | 92 | 3.4% | 8.1% |
| objective | 2270 | 83.1% | 68.0% |
| lord_capture | 130 | 4.8% | 5.6% |

**Seat + streak combined:** 12.2% of all VP

## Combat metrics (completed)

- Battles resolved: 505
- Attacker win rate: 85.1%
- Battles per player-round: 0.217

## Event phase (M2)

- Events resolved: 583
- Events per round: 1.00
- Top events: harsh_winter (82), winds_of_fortune (78), populist_uprising (77), border_skirmishes (75), festival (72)

## High Council (M2)

- Motions proposed: 2332
- Motions passed: 2332
- Pass rate: 100.0%
- Motions per round: 4.00
- Influence spent (lobby): 2144
- Avg influence spent / round: 3.68

## Hypothesis evaluation (H1–H8)

| ID | Hypothesis | Status | Detail |
| --- | --- | --- | --- |
| H1 | Seat+streak >50% of all VP under contest | **killed** | seat_streak_pct=12.2 |
| H2 | Winning margin >5 VP under strategic play | **inconclusive** | avg_margin=4.06, runaway_rate=0.18 |
| H3 | Objectives can reach ≥60% of winner VP | **killed** | winner_objective_share=0.68 |
| H4 | 7p timeouts are pacing not map bug | **inconclusive** | timeout_rate_7p=0.0 |
| H5 | Combat VP marginal even for Warmonger | **inconclusive** | winner_lord_capture_share=0.056 |
| H6 | no_vp_progress is chaos artifact | **killed** | degenerate_rate=0.0 |
| H7 | No persona dominates mixed-seat win rate | **confirmed** | expander_win_rate=0.662, max_persona_win_rate=0.662 |
| H8 | Economist viable in mixed seats (builder/gold path) | **inconclusive** | economist_win_rate=0.0 |
