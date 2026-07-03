# Aeonis Simulator

Engine-authoritative playtest simulator. See
`docs/plans/2026-07-02-agent-playtest-simulation-design.md` for the design spec.

## Setup

    python3 -m pip install -r requirements-dev.txt

## Run tests

    cd sim && python3 -m pytest

## Run a smoke game (after Task 14)

    cd sim && python3 -m aeonis_sim.runner.play --players 4 --seed 1
