# M4 default-on review

**Date:** 2026-07-13 · **Status:** sim-led promotion  
**Sample:** 520/520 completed matched games at 4p/6p/8p  
**Stack:** canonical no-building-upkeep rules, audited public objectives, corrected geometry, S1 Seat reward, mixed personas  
**Script:** `sim/scripts/m4_default_review.py`

## Decision

**Make full M4 Lord asymmetry the simulator default.** Use `"lord_asymmetry": {"enabled": false}` only for explicit neutral/legacy regression comparisons.

M4 is already canonical game content. Default-on therefore means the simulator models the actual launch Lords unless a test deliberately requests a synthetic symmetric baseline; it does not declare the current Lord sheets perfectly balanced.

## Matched results

| Players | M4 | Mean rounds | Winner objective share | Contested attacker wins | Actions/player-round | Economist wins |
|---:|---|---:|---:|---:|---:|---:|
| 4 | Off | 6.60 | 78.9% | 60.3% | 3.39 | 8.9% |
| 4 | **On** | **6.70** | **84.5%** | **56.6%** | **3.49** | **12.2%** |
| 6 | Off | 7.15 | 79.1% | 62.1% | 3.29 | 2.3% |
| 6 | **On** | **6.66** | **78.5%** | **62.6%** | **3.37** | **5.4%** |
| 8 | Off | 7.00 | 79.5% | 63.4% | 3.24 | 0.8% |
| 8 | **On** | **6.38** | **72.5%** | **63.3%** | **3.34** | **0.8%** |

All primary default gates pass: 100% completion, 6–8 mean rounds, at least 60% winner objective share, and 55–65% contested attacker wins. M4 improves the 6p economist above the 5% watch floor. The 8p economist remains below that floor in both arms, so it is not an M4-default regression.

## Lord and persona watches

Default-on exposes balance signals that a neutral baseline cannot show:

- **4p:** Auriel won 51.1% when seated and Rakhis 36.7%; warmonger won 44.4%. This is the clearest follow-up watch.
- **6p:** Lord results were comparatively compact at 10.5–23.2% around a 16.7% neutral seat expectation.
- **8p:** Auriel led at 23.9% and Vharok trailed at 7.0% around a 12.5% expectation. The 8p economist remained 0.8% with M4 both off and on.

These remain sim-only balance signals. They belong in later one-dial ladders, not in the default-fidelity decision.

## Implementation contract

- Omitted `lord_asymmetry` now means full M4 enabled.
- Tournament runs rotate the eight launch Lords across seats.
- Direct engine games use the first available launch Lords unless a roster is supplied.
- Explicit `"enabled": false` preserves neutral M1–M3 fixtures and historical comparisons.

## Next sim focus

Return to economist viability, beginning with the 8p floor and persona/objective fit before applying another economy knob. Keep Auriel/warmonger at 4p as a paired regression watch.
