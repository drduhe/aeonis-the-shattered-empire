# Rakhis balance ladder — Dial 3 (Sandstride ZOC ignore removed)

**Date:** 2026-07-12 · **Status:** sim-only · **Change:** canon + sim

## Decision

Continue after [Dial 2](2026-07-12-rakhis-ladder-dial2.md) (Hit and Run once/game).

**Dial 3:** Sandstride **no longer ignores enemy ZOC surcharges**. Keeps:
- Deserts cost **1 AP**
- Once-per-battle pre-Pre-Strike retreat

Cavalry still use the normal first-ZOC flanking exemption.

**Encoded in:** `lords/Rakhis.md`, `Movement.md`, `Tiles.md`, `move.py`, First Playable, Learn to Play, Player Aid, `rules_and_systems/INDEX.md`.

**Collateral fix (same session):** Entangling Roots bot heuristic called `warding_charm_defense_bonus` (and peers) during enumeration, which **spent** mana and could crash tournaments (`negative mana`, seed 97082). Ritual helpers now take `commit=False` for peeks. Pytest regression added.

## Gate (same Lord×persona configs / seeds)

| Bracket | Metric | Dial 0 | Dial 1 | Dial 2 | Dial 3 | Δ vs Dial 2 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Solo 4p | Rakhis win % | 51.0 | 49.5 | 48.5 | **43.3** | **−5.2** |
| Solo 4p | × warmonger | 85.0 | 70.0 | 60.0 | 60.0 | 0 |
| Solo 4p | × diplomat | 61.1 | 68.4 | 68.4 | **47.4** | −21 |
| Solo 4p | × balanced | 50.0 | 50.0 | 50.0 | 57.9 | +7.9 (noisy) |
| Mixed 4p | Rakhis win % | 36.7 | 34.7 | 42.9 | **27.5** | **−15.4** |
| Mixed 6p | Rakhis win % | 25.9 | 25.0 | 25.2 | **20.4** | −4.8 |

Solo field after Dial 3: Rakhis **43.3%**, Thal'rik **40.0%**, then ~15–24% pack. Pytest: **335 passed**.

## Verdict

**First material lever.** Mixed 4p is near the ~25–35% seated band; mixed 6p is close to neutral (~16.7%). Solo overall still high at **43%** (warmonger/balanced pairings).

Options for owner:
1. **Stop / accept** — Rakhis as a strong cavalry Lord (~40% solo, healthy mixed). Document band; move to Thal'rik / floors.
2. ~~**Dial 3b** — also drop pre-Pre-Strike retreat~~ — **tried and reverted** (see [Dial 3b](2026-07-12-rakhis-ladder-dial3b.md)).
3. **Dial 3c** — Desert 2 AP (full Sandstride cut except retreat) — last resort.

## Default-on

Still **deferred** until solo spread is acceptable or explicitly accepted.

## Regenerate

```bash
cd sim
python scripts/m4_lord_persona_sweep.py
```
