# Plan 2 AP tempo + Plan 6 bookkeeping ladder

**Date:** 2026-07-13 · **Sim-led**  
**Sample:** 910 completed games at 4p/6p/8p with audited objectives, corrected geometry, S1 Seat reward, mixed personas, and full M4 Lord asymmetry  
**Scripts:** `sim/scripts/plan2_ap_ladder.py`, `sim/scripts/plan6_bookkeeping_ladder.py`

## Verdict

- **Plan 2:** retain the current AP rules. The +2 bonus cap is nearly inert; Rally increases spread and combat heat without closing action gaps.
- **Plan 6 slim Renown:** reject this formulation. It lowers AP spread but does not close action gaps, activates too rarely, and regresses the 6p economist.
- **Plan 6 building upkeep:** promote the no-upkeep package. Price Forge, Academy, Castle, and Iron Citadel up front; buildings occupy Population but make no recurring resource payment.

## Plan 2 matched ladder

| Players | Variant | Mean rounds | Avg AP spread | Avg action gap | Builds/player | Contested attacker wins |
|---:|---|---:|---:|---:|---:|---:|
| 4 | Baseline | 6.12 | 1.02 | 2.52 | 2.45 | 65.3% |
| 4 | +2 cap | 6.12 | 0.93 | 2.54 | 2.45 | 65.8% |
| 4 | Cap + Rally | 6.36 | 1.35 | 2.46 | 2.49 | 68.8% |
| 6 | Baseline | 6.58 | 1.10 | 2.85 | 2.65 | 71.0% |
| 6 | +2 cap | 6.63 | 0.98 | 2.82 | 2.65 | 71.5% |
| 6 | Cap + Rally | 6.88 | 1.30 | 2.84 | 2.67 | 68.3% |
| 8 | Baseline | 7.23 | 1.14 | 3.39 | 2.66 | 67.9% |
| 8 | +2 cap | 7.18 | 1.04 | 3.37 | 2.62 | 68.2% |
| 8 | Cap + Rally | 7.28 | 1.37 | 3.37 | 2.70 | 68.0% |

The cap does not address banking, Event AP, or free actions, so it cannot meet the plan's stated maximum-spread target. Rally deliberately ignores the cap and therefore widens the measured start-of-round spread. Neither lever produces enough benefit to justify new rules text.

## Plan 6 matched ladder

| Players | Variant | Mean rounds | Avg AP spread | Avg action gap | Builds/player | Upkeep checks/player-round | Economist wins | Contested attacker wins |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 4 | Baseline | 6.12 | 1.02 | 2.52 | 2.45 | 0.281 | 2.6% | 65.3% |
| 4 | Slim Renown | 6.16 | 0.93 | 2.48 | 2.41 | 0.280 | 5.3% | 67.4% |
| 4 | No upkeep | 6.22 | 1.00 | 2.54 | 2.46 | **0** | 7.7% | 58.1% |
| 6 | Baseline | 6.58 | 1.10 | 2.85 | 2.65 | 0.211 | 7.9% | 71.0% |
| 6 | Slim Renown | 6.40 | 0.92 | 2.91 | 2.47 | 0.193 | 2.3% | 59.7% |
| 6 | No upkeep | 6.53 | 1.06 | 2.94 | 2.66 | **0** | 5.3% | 65.5% |
| 8 | Baseline | 7.23 | 1.14 | 3.39 | 2.66 | 0.272 | 0.0% | 67.9% |
| 8 | Slim Renown | 6.65 | 0.82 | 3.25 | 2.45 | 0.249 | 3.6% | 61.8% |
| 8 | No upkeep | 6.63 | 1.09 | 3.21 | 2.46 | **0** | 5.4% | 65.8% |

No-upkeep passes the explicit building gate: builds remain above 2 per player and Castle/Iron Citadel do not become automatic. Castle frequency moved from 0.44/0.70/0.93 to 0.48/0.90/1.43 per game at 4p/6p/8p, while Iron Citadel remained at 0.00/0.03/0.03. Pacing and winner objective share stay in their accepted bands.

Slim Renown's 5-point reward fired for only 14–18% of seats. Its action-gap movement was negligible and its persona effects were inconsistent, so the rewrite is rejected rather than promoted on bookkeeping theory alone.

## Simulator reliability note

The new action instrumentation exposed repeated 0-AP Portal hops being scored by bots as fresh expansion. A persona evaluation brake now treats a free hop into already controlled/occupied territory with no Seat progress as idle. This changes no Portal rule; it removes an agent artifact that previously inflated maximum action gaps to 98–99.

## Remaining human confirmation

When human sessions resume, time Production & Upkeep at 6p and confirm that paying the four adjusted costs up front feels cleaner than recurring maintenance. This is confirmation, not a blocker to the sim-led promotion.
