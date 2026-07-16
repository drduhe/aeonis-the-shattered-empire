# M6 Conversational Negotiation Sprint

**Date:** 2026-07-16
**Status:** EXECUTED
**Evidence class:** sim-only

## Goal

Let model-driven seats bargain directly during legal negotiation windows while preserving an engine-authoritative game and the binding/non-binding distinction in `rules_and_systems/Diplomacy.md`.

## Delivered protocol

- One typed proposal, accept/reject, and at most one typed counter.
- Public model-authored message on each sampled negotiation decision.
- Immediate resource exchanges are binding; future vote, non-aggression, named-attack, and payment promises are logged but not enforced.
- Promise outcomes resolve on the relevant vote, attack, later payment, or at Cleanup & Checks.
- First Playable keeps ordinary deals but excludes formal Accords.
- Trade resources match canon: Gold, Mana, Influence, and Remnants; Population is excluded.

## Safety and evidence gates

- Prose cannot add legal terms or override the indexed choice.
- Hidden seat information remains redacted.
- The transcript, typed offer, promise log, provider errors, and fallback counts are retained in JSONL and qualitative reports.
- Deterministic-provider runs validate orchestration only. Local-model observations remain sim-only and require replication before any balance conclusion.

## Validation

Run focused negotiation/model tests, the complete simulator suite from `sim/`, the M2 regression gate, manifest/link/terminology/timing checks, and one three-seat local-model pilot configured at `sim/configs/m6-conversational-negotiation-ollama.json`.
