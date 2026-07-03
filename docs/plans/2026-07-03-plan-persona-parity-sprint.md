# Persona parity sprint (sim-only)

- **Status:** H7 **pass** at 8p (v2.5 + full-roster mixed). H8 **open** — economist &lt;1% at 7–8p.
- **Date:** 2026-07-03

## H7 — Persona parity at mixed seats

| Metric | Target | B 8p (v2) | C 7p (v2) |
|--------|--------|-----------|-----------|
| Expander win rate | ≤30% | **20.3%** | 31.4% (inconclusive) |
| Max persona win rate | ≤28% | **26.1%** | 31.4% (inconclusive) |
| Winner objective VP | ≥55% | **72%** | **72%** |

**Mixed matchmaking (v2):** every roster persona appears **at least once** per game when `players ≥ len(roster)`.

## H8 — Economist viability (open)

**Hypothesis:** Economist can win ≥5% of mixed seat-games via builder/gold objectives.

| Result | B 8p | C 7p | Solo 8p (sanity) |
|--------|------|------|------------------|
| Economist win % | **0.2%** | **0.4%** | **12.5%** (= random) |

**Sim read:** Economist scores ~random alone but loses every mixed race to objective-fast personas at 7–8p (~5 round games). Builder (3×3 AP) + `golden_hoard` (10 gold) do not complete in time. **Not a weight-tuning-only fix** — needs longer games (Plan 4 pacing) or economist-specific objective hook (future).

**Shipped anyway:** `builder_track`, `builder_delta`, `builder_need`, `gold_track`, `catch_up`, `production_bonus` features; economist weight + feature boosts; H8 evaluator in reports.

**Reports:** `docs/reports/2026-07-03-bracket-{b,c}-mixed-parity-v2-report.html`
