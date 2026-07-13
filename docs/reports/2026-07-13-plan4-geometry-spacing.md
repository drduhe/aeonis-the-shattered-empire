# Plan 4 geometry validation + Plan 1 spacing lever

**Date:** 2026-07-13 · **Sim-only**  
**Geometry sample:** 200 maps at each count 3–8 (1,200 total)  
**Combat sample:** matched M4 mixed ladder, 50 games at 4p / 40 at 6p / 40 at 8p per Edge mode  
**Scripts:** `sim/scripts/plan4_geometry_audit.py`, `sim/scripts/plan1_prestrike_mixed_ladder.py`

## Verdict

**Promote balanced angular home spacing and guaranteed Ruins/Portal access for First Playable presets.** Treat corrected geometry as the successful non-Pre-Strike Plan 1 lever. Keep Aggressor's Edge and Pillage off.

The old generator sorted outer-ring coordinates by row, not geometric angle. That clustered high-count homes and violated the draft spacing contract in every sampled map. Correct angular placement plus coverage-aware special placement closes the geometry gates and cools 6p/8p attacker advantage into the target band.

## Geometry gate

| Players | Radius | Hexes | Old min home distance | New min | Special access after fix | Max production spread | Hexes/player |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 3 | 37 | 6 | 5 | 100% | 0 | 12.33 |
| 4 | 3 | 37 | 3 | 4 | 100% | 0 | 9.25 |
| 5 | 4 | 61 | 3 | 4 | 100% | 0 | 12.20 |
| 6 | 4 | 61 | 2 | 4 | 100% | 0 | 10.17 |
| 7 | 5 | 91 | 2 | 4 | 100% | 0 | 13.00 |
| 8 | 5 | 91 | 2 | 3 | 100% | 0 | 11.38 |

All home-to-contested-ring distances are at most 4. Contested-tile counts are 9/10/12/13/17/18 from 3p through 8p.

**8p exception:** A radius-5 perimeter has 30 positions. Eight evenly spaced Home Cities cannot all have four perimeter steps between them (32 would be required), so the validated minimum is 3. Moving to a full radius-6 disk would jump to 127 tiles. The corrected radius-5 map passes combat and expansion-room gates, so the 91-tile design stays.

## Combat rebaseline

Plan 1 target for contested attacker wins is 55–65%.

| Players | Old baseline | Corrected spacing, Edge off | Corrected + Pre-Strike | Battles/player-round | Mean rounds (off) |
|---:|---:|---:|---:|---:|---:|
| 4 | 67.6% | **66.7%** | 69.1% | 0.245 | 7.10 |
| 6 | 72.0% | **64.2%** | 65.0% | 0.262 | 6.88 |
| 8 | 72.5% | **62.3%** | 64.9% | 0.291 | 7.08 |

- 6p/8p land inside the Plan 1 band without changing combat resolution. The canonical no-upkeep rebaseline puts 4p at 66.7%, a 1.7-point watch above the narrow gate; the matched Plan 2 baseline was 65.3% and its no-upkeep arm was 58.1%, so the combined evidence does not justify a combat-rule change.
- Pre-Strike worsens attacker advantage at every count in this ladder and remains rejected.
- Mean rounds remain inside the accepted 6–8 band.

## Manufacturing consequence

The validated 8p radius-5 preset uses **91 positions**, not the stale 81-tile estimate. With all eight launch Unique Starting Tiles substituted, the physical inventory is:

- 8 Home Cities + 1 Imperial Seat
- 21 Plains, 16 Forests, 19 Mountains
- 8 Deserts, 4 Ruins, 3 Portals, 3 Lakes
- 8 Unique Starting Tiles

Total: **91**. The prior production-manifest row also summed to 77 despite displaying 81; it is replaced by the validated bill of materials.

## Remaining Plan 4 scope

Geometry is sim-validated. The Docket, reduced 6–8p Whisper draw, real-time council target, and slice-draft user experience still require human playtests and remain PROPOSED. Human confirmation should specifically check whether the 8p distance-3 neighbor pair feels cramped despite the passing sim metrics.
