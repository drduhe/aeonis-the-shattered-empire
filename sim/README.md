# Aeonis Simulator

Engine-authoritative playtest simulator. See
`docs/plans/2026-07-02-agent-playtest-simulation-design.md` for the design spec.

## Setup

    python3.11 -m pip install -r requirements-dev.txt

## Run tests

    cd sim && python3.11 -m pytest

Golden replay fixtures: `tests/fixtures/golden_replays.jsonl`. Regenerate after
engine changes:

    cd sim && python scripts/generate_golden_replays.py

CI runs the same suite on push/PR when `sim/` changes (`.github/workflows/sim.yml`).

## Run bot games

Chaos (fuzz):

    cd sim && python3.11 -m aeonis_sim.runner.play --players 4 --seed 1 --games 10 --out games.jsonl

Persona bots:

    cd sim && python3.11 -m aeonis_sim.runner.play --players 4 --persona balanced --seed 1 --games 10

Qualitative agent playtests (M5):

    cd sim && python scripts/m5_agent_playtest.py \
      --config configs/m5-agent-playtest-dry-run.json \
      --out ../playtest/agent_sessions/m5-dry-run.jsonl \
      --report ../docs/reports/m5-dry-run.md

Use `configs/m5-agent-playtest-ollama-pilot.json` for the quality-first local Ollama profile. The model receives a redacted seat view and numbered legal actions; the engine remains authoritative. Invalid responses consume the decision budget, retry once when configured, and fall back to the seat's persona bot. Reports label all findings sim-only, and deterministic-provider comments are pipeline evidence only.

Conversational negotiation pilot (M6):

    cd sim && python scripts/m5_agent_playtest.py \
      --config configs/m6-conversational-negotiation-ollama.json \
      --out ../playtest/agent_sessions/2026-07-16-m6-conversational-negotiation.jsonl \
      --report ../docs/reports/2026-07-16-m6-conversational-negotiation-pilot.md

M6 model seats choose only engine-enumerated proposals/responses, then add a short public message. Immediate exchanges execute; future promises remain non-binding and are reported as kept, broken, or unresolved.

Tournament (balance campaign):

    cd sim && python3.11 -m aeonis_sim.runner.tournament \
      --config configs/bracket-m2-smoke.json --out /tmp/smoke.jsonl --report /tmp/smoke.md

Flags: `--players`, `--seed`, `--games`, `--out`, `--persona`, `--personas`.
Tournament: `--config`, `--report`, `--html`, `--session-log`, `--workers` (default: CPU count).

Combat variant flags (Plan 1 ladder) live in tournament config under `"combat"`:
`aggressors_edge_mode` (`off` | `full` | `pre_strike`), legacy `aggressors_edge`, `pillage`.

Rejected Plan 2 AP economy toggles remain under `"ap_economy"` for regression:
`ap_bonus_cap` (e.g. `2`), `rally` (`true` / `false`). Plan 6 experiments use
`"bookkeeping"`: `slim_renown` remains rejected/default-off; `building_upkeep`
defaults to `false` (canonical) and `true` reproduces the retired upkeep rules.

H7 calibration toggles (PROPOSED, sim-only): `"pacing"` (`vp_threshold`), `"objectives"`
(`frontier_lord_min_hexes`), `"seat_rewards"` (`seat_of_empire_vp`), `"economy"` (see
`docs/reports/2026-07-03-early-economy-sweep-conclusion.md`). Default smoke uses
`seat_of_empire_vp: 1` plus Lever C brakes in `persona.py`. See
`docs/reports/2026-07-03-current-baselines.md`.

## Regression gates (Plan 1 / Plan 2)

CI runs four 30-game Warmonger brackets with sim-calibrated metric bands
(not human playtest targets). Local:

    cd sim && python scripts/regression_check.py --config configs/regression-plan1-baseline.json

Configs: `configs/regression-plan1-baseline.json`, `regression-plan1-prestrike.json`,
`regression-plan2-baseline.json`, `regression-plan2-cap-rally.json`.

**M2 gate (CI):** `configs/bracket-m2-ci.json` — 20 mixed 4p games, zero crash/timeout/degenerate.

    cd sim && python scripts/regression_check.py --config configs/bracket-m2-ci.json

Full gate smoke: `configs/bracket-m2-smoke.json` (100 games). Solo ladder: `bracket-m2-4p.json`.

See `docs/reports/2026-07-03-plan1-combat-ladder.md` for calibration notes.

## Pacing / verdicts (sim-only)

- **`completed`** — someone reached `VP_THRESHOLD` (10) and the final round resolved, **or**
  the printed round cap (`DEFAULT_ROUND_CAP`, 25) was hit (`round_cap_finish` in the record).
- **`degenerate`** — `completed` but with `action_cap` or `no_vp_progress` while max VP stayed
  below threshold (VP drought with no winner).
- **`stalled`** — identical board state at round start (true engine loop).
- **`no_vp_progress`** is cleared if VP resumes; late-game droughts on the way to 10 VP are
  not flagged as degenerate at game end.

Milestone status and next scope: `docs/plans/INDEX.md` (sim track section);
architecture spec §5 owns milestone content.

M2 tournament configs: `configs/bracket-m2-smoke.json`, `bracket-m2-4p.json`, `bracket-6p-mixed.json`, `bracket-8p-mixed.json`.
Current baselines: `docs/reports/2026-07-03-current-baselines.md`.

## M4 Lord asymmetry (full encode)

Full M4 is the simulator default: unique tiles, remaining abilities, faction discoveries, and Legendary Buildings. Tournament runs rotate the eight launch Lords across seats. Use `"lord_asymmetry": {"enabled": false}` only for an explicit neutral/legacy comparison.

```
    cd sim && python scripts/regression_check.py --config configs/bracket-m4.json --workers 4
    cd sim && python scripts/regression_check.py --config configs/bracket-m4-ci.json --workers 4
    cd sim && python scripts/m4_default_review.py
```

## Plan 2/6 tempo + Plan 3 objectives + Plan 4 geometry

The full-deck objective audit and geometry/spacing gates are reproducible:

```bash
cd sim
python scripts/plan3_objective_audit_ladder.py
python scripts/plan4_geometry_audit.py
python scripts/plan1_prestrike_mixed_ladder.py
python scripts/plan2_ap_ladder.py
python scripts/plan6_bookkeeping_ladder.py
```

The objective ladder compares the reduced First Playable row with the audited full deck at 4p/6p/8p. The geometry audit checks 200 seeds per count for home spacing, Ruins/Portal access, starting-production parity, and tile inventory. The Plan 1 ladder is the combat rebaseline after geometry changes.

Foundation smoke remains at `configs/bracket-m4-foundation.json`. Gate report: `docs/reports/2026-07-12-m4-gate.md`. AL-49 closed; AL-50–52 resolved.

Rules questions found while encoding the docs live in
`playtest/Ambiguity_Ledger.md`.
