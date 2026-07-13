# Plan 5 / M4 foundation report

**Date:** 2026-07-09 · **Status:** stability gate passed · **Scope:** sim-only balance signal

Plan 5's six launch-Lord signature redesigns are promoted to canon. Nyxara and Thal'rik remain unchanged anchors. This report validates the opt-in M4 simulator foundation; it does **not** claim full Lord balance because unique tiles, remaining abilities, faction discoveries, and Legendary Buildings still belong to the full M4 milestone.

> **2026-07-13 update:** full M4 subsequently passed its architecture gate and a 520-game default review, and is now simulator-default. See `2026-07-13-m4-default-on-review.md`; this memo remains the historical foundation record.

## Encoded foundation

- Lord identity, sheet-specific starting resources, starting unit mixes, and Lord combat/movement stats.
- Cassian: one 0-AP extra Trade and binding current-motion vote promises (AL-48 timing abstraction).
- Seraphel: optional second paid Research in the same turn.
- Elyndra: one 1-AP controlled-Forest network Move per round.
- Vharok: controlled built hexes become Sieges with +1 Battle Line capacity and +1 Defense.
- Rakhis: Desert cost 1 and full ZOC-surcharge exemption.
- Nyxara: 3-card Round Start draw and hand limit 8.
- Auriel: one sanctified motion per round, double personal votes, enhanced Renown on passage.
- Thal'rik: Portal travel to enemy-controlled Portals without permission.
- Rotating Lord assignment and win-rate-by-Lord reporting for tournaments.

Deferred full-M4 effects are recorded in AL-49 rather than approximated.

## Stability result

`bracket-m4-foundation.json`: **40/40 completed**, zero crashes, zero timeouts, zero degenerate games. Mean length: **6.2 rounds**.

| Lord | Seat games | Wins | Win rate |
| --- | ---: | ---: | ---: |
| Auriel | 19 | 4 | 21.1% |
| Cassian | 18 | 3 | 16.7% |
| Elyndra | 19 | 4 | 21.1% |
| Nyxara | 20 | 2 | 10.0% |
| Rakhis | 20 | 7 | 35.0% |
| Seraphel | 18 | 5 | 27.8% |
| Thal'rik | 19 | 9 | 47.4% |
| Vharok | 19 | 4 | 21.1% |

These are small-sample, partial-implementation rates at a four-seat table (25% neutral expectation). Thal'rik's lead and Nyxara's floor are regression watch-items, not tuning instructions, until the complete sheets are encoded.

## Full-M4 entry gate

Plan 5 no longer blocks M4. The next implementation plan must encode all eight sheets' remaining passives/actives, unique tiles, faction discoveries, and Legendary Buildings, then run the architecture spec's 100-game crash/invariant-free gate. Preserve the M1–M3 default path and golden replays; M4 stays opt-in until that gate closes.
