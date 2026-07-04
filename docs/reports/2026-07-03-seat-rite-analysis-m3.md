# Seat / Coronation Rite analysis — mixed 4p M3

**Date:** 2026-07-03 · **Sim-only**  
**Data:** `bracket-m2-smoke.json` (100 games, seed_base 70000) · M3 engine, pre–Lever C persona weights  
**Tool:** `sim/scripts/analyze_seat_rite.py`

---

## 1. Bottom line

**Expander does not monopolize the Imperial Seat.** Balanced holds the seat more often, scores `seat_of_empire` more often, and earns a higher share of VP from seat sources. Expander dominance correlates with **conversion efficiency** (winning when seated, and winning without the seat), not seat access.

Seat rewards are nonetheless **material** (~15.5% of all VP). See [seat reward sweep plan](../plans/2026-07-03-plan-seat-reward-sweep.md) for PROPOSED one-knob tests.

---

## 2. Seat access by persona (all seat-games)

| Persona | Win % | Rite VP/game | Milestone VP/game | `seat_of_empire` % | End-seat hold % | Seat VP % of total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Expander | 41.0% | 0.76 | 0.18 | 41% | **34.6%** | 23.3% |
| **Balanced** | 37.0% | 0.71 | 0.16 | **63%** | **53.4%** | **28.0%** |
| Warmonger | 22.2% | 0.17 | 0.04 | 33% | 25.6% | 12.9% |
| Diplomat | 21.5% | 0.22 | 0.03 | 15% | 10.1% | 7.0% |
| Economist | 5.0% | 0.04 | 0.03 | 8% | 3.8% | 4.1% |

**End-game seat holder (all games):** balanced 39 · expander 27 · warmonger 23 · diplomat 8 · economist 3.

---

## 3. Conditional win rate (end-seat control)

| Persona | Win when held seat | Win when did not |
| --- | ---: | ---: |
| Expander | **74%** (20/27) | **24%** (12/51) |
| Balanced | 62% (24/39) | 9% (3/34) |
| Warmonger | 57% (13/23) | 10% (7/67) |
| Diplomat | 88% (7/8) | 14% (10/71) |
| Economist | 33% (1/3) | 4% (3/77) |

Expander wins **38%** of the time without end-game seat control; balanced **11%**.

---

## 4. Winners and seat VP

| Winner | n | Avg seat VP | % of winner VP | Held seat at end |
| --- | ---: | ---: | ---: | ---: |
| Balanced | 27 | 3.85 | 36.0% | **89%** |
| Expander | 32 | 3.16 | 29.2% | 62% |
| Warmonger | 20 | 2.10 | 18.8% | 65% |
| Diplomat | 17 | 1.65 | 15.6% | 41% |

Balanced wins are **seat-dependent**; expander wins are **less so**.

---

## 5. Bot weights (context)

| Persona | `seat_pull` | `seat` | `rite_ready` |
| --- | ---: | ---: | ---: |
| Balanced | **0.90** | **0.95** | — |
| Expander | 0.55 | 0.55 | 0.55 |

Expander reaches the seat via **map tempo**, not highest seat-chase weights.

---

## 6. Global

- Seat-related VP (rite + milestone + `seat_of_empire`): **432 / 2789 (15.5%)**
- Per-game average across all players: **4.32 VP**

Regenerate:

```bash
cd sim
py -3.11 -m aeonis_sim.runner.tournament --config configs/bracket-m2-smoke.json --out ../docs/reports/_seat.jsonl --workers 4
py -3.11 scripts/analyze_seat_rite.py ../docs/reports/_seat.jsonl
```
