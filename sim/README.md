# Aeonis Simulator

Engine-authoritative playtest simulator. See
`docs/plans/2026-07-02-agent-playtest-simulation-design.md` for the design spec.

## Setup

    python3.11 -m pip install -r requirements-dev.txt

## Run tests

    cd sim && python3.11 -m pytest

## Run chaos-bot games

    cd sim && python3.11 -m aeonis_sim.runner.play --players 4 --seed 1 --games 10 --out games.jsonl

Flags: `--players` (default 4), `--seed` (base seed; game N uses seed+N),
`--games` (default 1), `--out` (optional JSONL path to append game records).
Prints one verdict line per game and a final `verdicts:` tally.

Rules questions found while encoding the docs live in
`playtest/Ambiguity_Ledger.md`.
