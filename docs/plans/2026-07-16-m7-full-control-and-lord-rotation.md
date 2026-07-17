# M7 Full-Control Agents and Lord Rotation

**Date:** 2026-07-16
**Status:** EXECUTED
**Evidence class:** sim-only

## Goal

Move from fixed-Lord, sparsely sampled qualitative games to repeatable six-player assignment rotation and a mode in which the model chooses every meaningful legal decision.

## Delivered protocol

- Campaign configs can rotate Lords and personas independently between games without mutating the source config.
- `full_control` bypasses decision-kind, round, and call-count sampling limits.
- Full-control decisions receive the complete legal menu rather than the sampled mode's presentation cap.
- Forced one-choice windows resolve automatically and are counted separately; all windows with two or more legal choices go to the model.
- The engine remains authoritative: the model selects from numbered legal choices, while validation, hidden state, and resolution stay in the simulator.
- Provider validation failure retries once when configured, then uses the seat persona only as a safety fallback.
- A per-round zero-cost Portal route guard removes an already-used directed route from later choice sets. The model still chooses among every remaining legal action, but cannot repeat the exact free route indefinitely.

## Evidence gates

1. Six canonical 10-VP games rotate six Lords one seat per game while keeping personas fixed, separating Lord assignment from persona/seat context.
2. One accelerated 4-VP full-control game verifies end-to-end feasibility; its pacing and winner are not balance evidence.
3. The unguarded trace is retained as a diagnostic baseline for model-loop behavior.
4. A guarded replay must complete without persona delegation and materially reduce the Portal/action explosion.
5. Focused tests cover full-control sampling bypass, forced choices, assignment immutability, independent rotation, and route suppression; the full simulator suite remains the regression gate.

## Interpretation boundary

Full control means every non-forced decision is model-selected from the complete engine-enumerated legal menu. It does not give a provider authority to invent actions, inspect another seat's hidden information, edit state, or bypass the rules engine. All findings remain sim-only until replicated.

## Validation

- Focused model/campaign gate: **13 passed**.
- Complete simulator suite: **368 passed**.
- Manifest validation: passed.
- Manifest-scoped relative-link check: passed.
- Terminology sweep: only allowlisted canon/history/instruction hits.
