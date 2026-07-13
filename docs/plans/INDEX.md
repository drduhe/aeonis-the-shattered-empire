# Design plans — index & status

**Updated:** 2026-07-13 · This is the entry point for `docs/plans/`. Plans marked PROPOSED change nothing until playtested (sim-led for now) and registered under "Design decisions (resolved)" in `rules_and_systems/INDEX.md`.

**Mission context:** the simulator (`sim/`) is the primary feedback loop. Work streams either (a) close the gap between sim and canon rules, or (b) use sim evidence to refine game systems. See `docs/reports/INDEX.md` for current baselines and findings.

---

## Active plans

| # | Plan | Status | Sim encoding | Next gate |
|---|---|---|---|---|
| 1 | [Combat aggression](2026-07-02-plan-combat-aggression.md) | **RESOLVED 2026-07-13: no combat modifier** | Edge/Pillage toggles retained for regression; corrected Plan 4 spacing is the successful lever | Human confirmation; all counts now in band |
| 2 | [AP economy](2026-07-02-plan-ap-economy.md) | **RESOLVED 2026-07-13: no cap/Rally change** | 390/390 matched games; cap inert, Rally widened spread and heated combat | Preserve toggles for regression only |
| 3 | [VP legibility (full)](2026-07-02-plan-vp-legibility.md) | **PROMOTED 2026-07-13 (sim-validated)** | Full 24-card shared row encoded; 130/130 audited games; 74–82% winner objective share | Human confirmation when playtests resume |
| 3b | [VP legibility MVP](2026-07-03-plan-vp-legibility-mvp.md) | **PROMOTED** (sim-validated 2026-07-03, `rules_and_systems/INDEX.md`) | Fully encoded | Human confirmation when playtests resume |
| 4 | [High player count](2026-07-02-plan-high-player-count.md) | **PARTIAL — geometry promoted; social systems PROPOSED** | 1,200-map geometry gate passed; corrected anchors rebaseline combat; Docket + Whisper table remain drafts | Human Docket/Whisper + 8p spacing confirmation |
| 5 | [Core Lords parity](2026-07-02-plan-core-lords-parity.md) | **PROMOTED 2026-07-09** | **M4 full encode DONE** (2026-07-12): unique tiles, remaining abilities, faction discoveries, Legendary Buildings; gate `bracket-m4.json` 100/100 | Lord-sheet tuning **paused** 2026-07-12 (Dial 3 kept); `lord_asymmetry` stays opt-in |
| 6 | [Bookkeeping](2026-07-02-plan-bookkeeping.md) | **RESOLVED 2026-07-13** | Trade/player-board hygiene landed; building upkeep removed; slim Renown rejected after 520/520 games | Human confirmation of upkeep feel |
| 7 | [Seat reward sweep](2026-07-03-plan-seat-reward-sweep.md) | **S1 adopted** (sim default) | `seat_rewards.seat_of_empire_vp` live | S2+ if revisited — see [H7 conclusion](../reports/2026-07-03-h7-calibration-sweep-conclusion.md) |
| 8 | [Early economy impact](2026-07-03-plan-early-economy-impact.md) | **E1/E2/E3/E5 killed** | `economy.*` + `objectives.staged_economy_opening` toggles live | Next: **E6** (City gold) or **E4/E7** if revisited |

## Open design questions (sim-flagged, owner decision needed)

- **Economist viability / objective tempo** — Lever B **decided 2026-07-03**: **Merchant Lord** (public, 8+ Gold) landed PROPOSED in the First Playable row. **E1/E2/E3/E5 killed 2026-07-03**. **Post-M4 (2026-07-12):** economist **6.5% / 5.2%** at mixed 6p/8p (H8 pass) with full Lord asymmetry — see [rebaseline](../reports/2026-07-12-m4-rebaseline.md). **Lever A pacing decided 2026-07-12:** design for **6–8 mean rounds** (accept current ~6.8 pace; do not stretch toward the old 8–10 aspirational band). Registered in `rules_and_systems/INDEX.md`.
- **Attacker win rate** — corrected angular home spacing and exact four-tile starts resolve the high-count heat: the canonical no-upkeep mixed M4 Edge-off rebaseline is **66.7% / 64.2% / 62.3%** at 4p/6p/8p. 4p is a narrow watch; Pre-Strike worsens all counts and stays off. See [geometry/spacing report](../reports/2026-07-13-plan4-geometry-spacing.md).
- **M4 default-on** — deferred (not blocked on more Rakhis dials). **Owner 2026-07-12:** stop Lord-sheet tuning for now; leave Dial 3 in place (no Sandstride ZOC ignore; Hit and Run once/game; Oasis cavalry discount cut). Revisit Thal'rik / floors / default-on in a later pass — see [Dial 3](../reports/2026-07-12-rakhis-ladder-dial3.md).
- **Next sim/design focus** — Plans 1/2/3/5/6 are closed and Plan 4 geometry is promoted. The next sim-led decision is the deferred **M4 default-on review**; Docket/Whisper throughput and slice-draft feel still await humans.

## Sim track

- **Architecture (north star):** [2026-07-02-agent-playtest-simulation-design.md](2026-07-02-agent-playtest-simulation-design.md) — engine-authoritative, §5 owns milestone scope.
- **M1 core loop — DONE** (2026-07-02→03): map/move/attack/build/recruit, combat, production, objectives (Plan 3 MVP), 10 VP end; golden replays, chaos fuzz, CI; Ambiguity Ledger AL-1–20 resolved.
- **Persona bots + tournaments — DONE:** 5 personas, solo/rotate/random/mixed matchmaking, balance reports, hypothesis evaluators (H1–H9), regression gates.
- **M2 politics layer — DONE** (2026-07-03): Event phase, Strategy draft + initiative, High Council (propose/vote/lobby), structured negotiation (binding trades, tracked promises), M2 gate green (CI `bracket-m2-ci.json`, smoke 100/100).
- **M3 card systems — DONE** (2026-07-03): [2026-07-03-agent-playtest-sim-implementation-plan-m3.md](2026-07-03-agent-playtest-sim-implementation-plan-m3.md) — buildings, Remnants/exploration, Artifacts/Sites, Arcane Tier I, secrets, Whispers (26), strategy primaries, H10–H12; gate green (CI `bracket-m3-ci.json`, smoke 100/100, solo 200/200, 236 pytest). Merchant Lord H12 killed at 5.3% economist mixed 4p.
- **M4 Lord asymmetry — DONE** (2026-07-12): full eight-sheet encode behind opt-in `lord_asymmetry` (unique tiles, remaining abilities, faction discoveries, Legendary Buildings). Gate green: CI `bracket-m4-ci.json`, local `bracket-m4.json` 100/100. See [M4 gate report](../reports/2026-07-12-m4-gate.md). AL-49 closed; AL-50–52 resolved.

## Strategic context

[2026-07-02-aeonis-design-roadmap.md](2026-07-02-aeonis-design-roadmap.md) — executed project stocktake: locked positioning decisions, TI4-parity snapshot, phase log. Historical but load-bearing for "why."

---

## Executed & removed plans (summaries; full text in git history)

Recover any with: `git log --diff-filter=D --summary -- docs/plans/<file>`

| Removed plan | Outcome |
|---|---|
| `2026-02-19-artifact-system-{design,implementation}.md` | Artifact system (3 categories, Remnants, Sites, 24 relics) shipped into `rules_and_systems/Artifacts.md` + 13 dependent docs |
| `2026-02-19-buildings-overhaul-{design,implementation}.md` | Building roster finalized (Academy/Forge/Bank, 8 Legendary capstones, upgrade system cut) into `rules_and_systems/Buildings.md` |
| `2026-07-02-website-marketing-redesign-{design,implementation}.md` | Two-page site shipped (`index.html` marketing + `codex.html` browser, Kit waitlist form, Arcane Night theme) |
| `2026-07-02-agent-playtest-sim-implementation-plan-a.md` | Sim M1: engine core loop, invariants, verdicts, golden replays, chaos fuzzing, CI — gate closed 2026-07-02 |
| `2026-07-02-agent-playtest-sim-implementation-plan-b.md` | Persona bots, tournament runner, reports module; Bracket A/B/C campaigns; H1–H6 initial verdicts |
| `2026-07-03-agent-playtest-sim-implementation-plan-m2.md` | Sim M2 (all 8 tasks): events, draft, initiative, council, negotiation, agents/reports, gate + CI job `m2-gate` |
| `2026-07-03-plan-persona-parity-sprint.md` | H7 parity work at 7–8p (expander ≤30% via mixed matchmaking v2); H8 stayed open — economist <1% at 7–8p (~5-round games; builder/gold too slow). Superseded by parity diagnosis + economist memo |
| `2026-07-02-improvement-plans-index.md` | Replaced by this file |

## Rules of engagement (unchanged)

- One variable per test ladder step; log sessions in `playtest/session_log.csv` against `playtest/Balance_Dashboard.md`.
- Every adopted change propagates in one atomic sweep (owning chapter + dependents + First Playable packet + rulebook + player aid + **sim**; see `.cursor/rules/aeonis-mechanics-sim-sync.mdc`).
- Each plan carries kill criteria — rolled-back experiments get recorded in the plan file, not silently dropped.
- Sim conclusions stay **sim-only** until the owner schedules human playtests.
