# Early economy sweep — conclusion (sim-only)

**Date:** 2026-07-03 · **Status:** closed · **Verdict:** **single-knob economy easing does not work** (including staged row reveal)

**Baseline:** mixed 4p/6p, Lever C expander brakes + S1 `seat_of_empire_vp: 1` (`bracket-m2-smoke.json` / `bracket-6p-mixed.json`). Economist at baseline: **10.7%** (4p), **3.6%** (6p). Mean rounds ~**6.2–6.4**.

---

## What we tested (one knob each, do not retry)

| ID | Knob | 4p economist | 6p economist | Pace | Max persona 4p |
| --- | --- | ---: | ---: | --- | --- |
| **E1** | Merchant Lord 8→6 gold | 5.4% ✗ | 1.8% ✗ | ~6.2 ✓ | warmonger 43.3% ✗ |
| **E2** | Builder 3→2 buildings | 8.1% ✗ | 3.9% ✗ | ~5.9 ✓ | warmonger 38.4% ✗ |
| **E5** | Tier-1 build 3→2 AP | 7.8% ✗ | 4.6% ✗ | ~6.4 ✓ | warmonger 42.5% ✗ |
| **E3** | Staged opening (Builder + Merchant Lord) | 10.7% ✓ | 2.2% ✗ | ~6.5–6.7 ✓ | balanced 37.5% ✗ |

Pass bars were: economist **≥10%** (4p) / **≥5%** (6p); mean rounds **6–7**; max persona **≤35%**.

---

## Conclusion

Lowering economy thresholds, production build cost, or **fixing economy cards in the opening row** helps **all** personas equally (or shifts wins to balanced/warmonger). Objectives stop discriminating; 6p economist does not lift. **Do not promote** E1/E2/E3/E5; **do not stack** without a dedicated combo study.

**E3 note:** Opening 2 public cards always Builder + Merchant Lord maintains 4p economist at baseline (10.7%) but **regresses 6p** (3.6%→2.2%) and fails the max-persona gate (balanced 37.5%). Row staging is not a viable economist lever on its own.

Remaining tracks if economy tempo is revisited: **E6** (City +1 gold), **E4** (new early economy public), **E7** (Economic Boom initiative) — see [plan](../plans/2026-07-03-plan-early-economy-impact.md).

---

## Sim toggles (kept in engine)

**Economy thresholds** — add to any bracket config under `"economy"`:

```json
"economy": {
  "merchant_lord_min_gold": 6,
  "builder_min_buildings": 2,
  "tier1_production_build_ap": 2
}
```

Defaults remain canon: **8 gold**, **3 buildings**, **3 AP** (Farm/Mine/Grove/Embassy). AL-44/45/46.

**Staged economy opening (E3)** — add under `"objectives"`:

```json
"objectives": {
  "staged_economy_opening": true
}
```

Or explicit IDs: `"opening_public_ids": ["builder", "merchant_lord"]`. Default is random 2 from the six-card public pool. AL-47.

Example re-run: copy `bracket-m2-smoke.json`, add one key block, `--report` to a new dated file.
