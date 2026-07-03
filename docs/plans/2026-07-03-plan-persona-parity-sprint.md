# Persona parity sprint (sim-only)

- **Status:** COMPLETE (v2.5 weights) — bot weights only; not canon
- **Date:** 2026-07-03
- **Trigger:** Mixed B/C MVP — Expander **43–46%** win rate; other personas **&lt;6%**

## H7 — Persona parity at mixed seats

**Hypothesis:** Expander over-indexes `territory` / `expansion` / Seat chase vs shared-row `objective` features, especially in fast 7–8p games.

**Sim kill criteria (mixed brackets, MVP combat):**

| Metric | Target | B 8p result | C 7p result |
|--------|--------|-------------|-------------|
| Expander win rate | ≤30% | **17.8%** | **22.9%** |
| Max persona win rate | ≤28% | **23.2%** (balanced) | **22.9%** (expander) |
| Winner objective VP (8p) | ≥55% | **71%** (H3 killed) | **71.4%** (H3 killed) |

**Changes (v2.5):**

- `features.py`: `territory_sat` penalty after 3 controlled hexes; lower raw `expansion` feature weights
- `persona.py`: cut Expander territory/seat weights; raise `objective` / `next_objective` on all personas; `territory_sat` negative weight on Expander only

**Reports:** `docs/reports/2026-07-03-bracket-{b,c}-mixed-parity-report.html`

**Open:** Economist still &lt;1% win rate — monitor; may need builder/economy objective alignment in a follow-up.
