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

Tournament (balance campaign):

    cd sim && python3.11 -m aeonis_sim.runner.tournament \
      --config configs/bracket-a.json --out /tmp/bracket-a.jsonl --report /tmp/bracket-a.md

Flags: `--players`, `--seed`, `--games`, `--out`, `--persona`, `--personas`.
Tournament: `--config`, `--report`, `--html`, `--session-log`, `--workers` (default: CPU count).

Combat variant flags (Plan 1 ladder) live in tournament config under `"combat"`:
`aggressors_edge_mode` (`off` | `full` | `pre_strike`), legacy `aggressors_edge`, `pillage`.

Rules questions found while encoding the docs live in
`playtest/Ambiguity_Ledger.md`.
