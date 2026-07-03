# Design plans — index & status

**Updated:** 2026-07-03 · This is the entry point for `docs/plans/`. Plans marked PROPOSED change nothing until playtested (sim-led for now) and registered under "Design decisions (resolved)" in `rules_and_systems/INDEX.md`.

**Mission context:** the simulator (`sim/`) is the primary feedback loop. Work streams either (a) close the gap between sim and canon rules, or (b) use sim evidence to refine game systems. See `docs/reports/INDEX.md` for current baselines and findings.

---

## Active plans

| # | Plan | Status | Sim encoding | Next gate |
|---|---|---|---|---|
| 1 | [Combat aggression](2026-07-02-plan-combat-aggression.md) | PROPOSED | Toggles live (`combat.aggressors_edge_mode`, `pillage`); ladder run — all variants exceed 55–65% human target (bots over-attack) | Human playtest; sim recommends **Pre-Strike Edge** first (`docs/reports/2026-07-03-plan1-combat-ladder.md`) |
| 2 | [AP economy](2026-07-02-plan-ap-economy.md) | PROPOSED | Toggles live (`ap_economy.ap_bonus_cap`, `rally`); regression gates green in CI | Human playtest of cap + Rally |
| 3 | [VP legibility (full)](2026-07-02-plan-vp-legibility.md) | PARTIAL — MVP promoted | MVP encoded (shared row, Coronation Rite, VP permanence) | Remaining: D4 purchased-VP cut, D5 event audit, artifact/building score-once, 24-card audit |
| 3b | [VP legibility MVP](2026-07-03-plan-vp-legibility-mvp.md) | **PROMOTED** (sim-validated 2026-07-03, `rules_and_systems/INDEX.md`) | Fully encoded | Human confirmation when playtests resume |
| 4 | [High player count](2026-07-02-plan-high-player-count.md) | PROPOSED | Not encoded (Docket, Whisper scaling, map construction) | Docket text + `Map_Construction.md` authoring can start anytime; 6p/8p tables gate promotion |
| 5 | [Core Lords parity](2026-07-02-plan-core-lords-parity.md) | PROPOSED | Not encoded — **blocks sim M4** (Lord asymmetry needs redesigned sheets) | Redesign briefs → sheets → sim M4 encode |
| 6 | [Bookkeeping](2026-07-02-plan-bookkeeping.md) | PROPOSED | Not encoded | `Trade_Taxes.md` rewrite + Renown milestone track are no-gate hygiene; start anytime |

## Open design questions (sim-flagged, owner decision needed)

- **Economist viability / objective tempo** — Lever B **decided 2026-07-03**: **Merchant Lord** (public, 8+ Gold) landed PROPOSED in the First Playable row; first sim read lifted economist 2.5% → 6.4% mixed 4p (memo §6). Still open: **Lever A pacing** — mean rounds drifted 6.4 → 6.1 (target 8–10); H12 confirmation at M3 gate.
- **Attacker win rate** — contested 64.3% post-Merchant-Lord, now inside Plan 1's 55–65% band; keep watching, sim-only signal.
- **Council pass rate** — ~29% after motion-aware voting; acceptable band TBD (40–60% suggested).

## Sim track

- **Architecture (north star):** [2026-07-02-agent-playtest-simulation-design.md](2026-07-02-agent-playtest-simulation-design.md) — engine-authoritative, §5 owns milestone scope.
- **M1 core loop — DONE** (2026-07-02→03): map/move/attack/build/recruit, combat, production, objectives (Plan 3 MVP), 10 VP end; golden replays, chaos fuzz, CI; Ambiguity Ledger AL-1–20 resolved.
- **Persona bots + tournaments — DONE:** 5 personas, solo/rotate/random/mixed matchmaking, balance reports, hypothesis evaluators (H1–H9), regression gates.
- **M2 politics layer — DONE** (2026-07-03): Event phase, Strategy draft + initiative, High Council (propose/vote/lobby), structured negotiation (binding trades, tracked promises), M2 gate green (CI `bracket-m2-ci.json`, smoke 100/100).
- **M3 card systems — ACTIVE:** [2026-07-03-agent-playtest-sim-implementation-plan-m3.md](2026-07-03-agent-playtest-sim-implementation-plan-m3.md) — building roster completion, Remnants/exploration, Artifacts/Sites, Arcane Tier I, secret-objective completion, Whispers (26), strategy primaries completion, H10–H12 gate. Merchant Lord experiment landed with the plan.
- **M4 Lord asymmetry:** blocked on Plan 5 redesigns.

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
