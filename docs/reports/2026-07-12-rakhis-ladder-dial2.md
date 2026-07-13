# Rakhis balance ladder — Dial 2 (Hit and Run once/game)

**Date:** 2026-07-12 · **Status:** sim-only · **Change:** canon + sim

## Decision

Continue ladder after [Dial 1](2026-07-12-rakhis-ladder-dial1.md) (Oasis Cavalry −1 Gold) proved weak.

**Dial 2:** Hit and Run is **once per game** (was once per round). Destinations and free 1-hex group reposition unchanged. Sandstride unchanged.

**Encoded in:** `lords/Rakhis.md`, `sim/aeonis_sim/engine/lords/rakhis.py`, `game.py` (gate uses `game_unused`), `PlayerState.lord_game`, `rules_and_systems/INDEX.md`.

## Gate (same Lord×persona configs / seeds)

| Bracket | Metric | Dial 0 | Dial 1 | Dial 2 | Δ vs Dial 1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Solo 4p | Rakhis win % | 51.0 | 49.5 | **48.5** | −1.0 |
| Solo 4p | × warmonger | 85.0 | 70.0 | **60.0** | −10 |
| Solo 4p | × balanced | 50.0 | 50.0 | 50.0 | 0 |
| Solo 4p | × diplomat | 61.1 | 68.4 | 68.4 | 0 |
| Mixed 4p | Rakhis win % | 36.7 | 34.7 | **42.9** | +8.2 (noisy) |
| Mixed 6p | Rakhis win % | 25.9 | 25.0 | 25.2 | ~0 |

Pytest: **333 passed**.

## Verdict

**Still not enough.** Overall solo spike barely moved (~51% → ~48.5%). Warmonger pairing improved (85% → 60%) but diplomat/balanced still ~50–68%. Mixed 4p moved the wrong way within noise — do not treat as regression without a larger sample.

**Dial 3 (next):** touch **Sandstride** — softest Sandstride step first:

1. **Prefer:** drop “ignore all ZOC surcharges” (keep Desert 1 AP + once/battle pre-Pre-Strike retreat), **or**
2. Remove pre-Pre-Strike retreat only, **or**
3. Full Sandstride cut (last resort).

Target band remains ~**25–35%** solo seated win rate.

## Default-on

Still **deferred**.

## Regenerate

```bash
cd sim
python scripts/m4_lord_persona_sweep.py
```
