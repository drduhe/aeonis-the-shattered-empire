# Aeonis Simulator

Engine-authoritative playtest simulator. See
`docs/plans/2026-07-02-agent-playtest-simulation-design.md` for the design spec.

## Setup

    python3.11 -m pip install -r requirements-dev.txt

## Run tests

    cd sim && python3.11 -m pytest

## Run bot games

Chaos (fuzz):

    cd sim && python3.11 -m aeonis_sim.runner.play --players 4 --seed 1 --games 10 --out games.jsonl

Persona bots:

    cd sim && python3.11 -m aeonis_sim.runner.play --players 4 --persona balanced --seed 1 --games 10

Tournament (balance campaign):

    cd sim && python3.11 -m aeonis_sim.runner.tournament \
      --config configs/bracket-a.json --out /tmp/bracket-a.jsonl --report /tmp/bracket-a.md

Flags: `--players`, `--seed`, `--games`, `--out`, `--persona`, `--personas`.
Tournament: `--config`, `--report`, `--session-log`.

Rules questions found while encoding the docs live in
`playtest/Ambiguity_Ledger.md`.
