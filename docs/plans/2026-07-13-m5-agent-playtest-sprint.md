# M5 agent playtest sprint

**Date:** 2026-07-13 · **Status:** EXECUTED (infrastructure; sim-only findings)

## Outcome

Add a qualitative agent layer to the engine-authoritative simulator without allowing a language model to invent actions, see opponents' hidden information, mutate canon, or block a game when a provider fails.

This milestone implements the qualitative layer described in §4.4 and Milestone 5 of `2026-07-02-agent-playtest-simulation-design.md`. It does not change game rules.

## Execution order and gates

1. **Contract and privacy:** give a model a compact seat-specific observation, phase digest, and numbered engine-enumerated legal actions. Redact opponents' secret objectives and Whisper hands.
2. **Provider boundary:** support a deterministic CI provider and local Ollama JSON-schema responses. Validate action indices, retry within budget, then fall back to the configured persona bot.
3. **Qualitative evidence:** capture decision annotations, completed-round reflections, post-game interviews, provider latency, retries, invalid responses, and fallbacks in the game JSONL.
4. **Reporting:** generate a Markdown report with reliability, reflections, interviews, decision moments, and candidate rules questions. Never auto-write the Ambiguity Ledger or promote a design plan.
5. **Profiles:** keep a small deterministic pipeline campaign for regression and a quality-first three-persona Ollama pilot for substantive feedback.
6. **Verification:** targeted tests, full pytest, manifest/link/terminology/timing checks, deterministic campaign, then the local-model pilot.

## Safety contract

- The existing `Game` object remains the only rules authority; the model returns an index, and `Game.submit` receives the exact enumerated action.
- Failed, malformed, or out-of-range responses consume the configured decision budget and fall back safely.
- A seat sees its own hidden cards plus public summaries, never an opponent's hidden card identities.
- Model prose is stored as **directional sim-only evidence**. A reported question is a triage candidate, not canon and not an automatic Ambiguity Ledger entry.
- Deterministic-provider prose is labeled **pipeline dry run only** and is not qualitative evidence.

## Operating profiles

| Profile | Purpose | Seats | Model-owned moments |
| --- | --- | ---: | --- |
| `m5-agent-playtest-dry-run.json` | Fast repeatable orchestration/CI check | 3 | 2 decisions + 1 reflection + interview per seat |
| `m5-agent-playtest-ollama-pilot.json` | Quality-first local-model feedback | 3 | 1 decision + 1 reflection + interview per seat, with retry |

The quality-first profile intentionally permits long local inference. Persona bots resolve the other decisions so a campaign remains bounded while the sampled qualitative moments can use a 16K context window and a 2K-token response allowance.

## Reproduce

From `sim/`:

```powershell
python scripts/m5_agent_playtest.py `
  --config configs/m5-agent-playtest-dry-run.json `
  --out ../playtest/agent_sessions/2026-07-13-m5-dry-run.jsonl `
  --report ../docs/reports/2026-07-13-m5-agent-playtest-dry-run.md

python scripts/m5_agent_playtest.py `
  --config configs/m5-agent-playtest-ollama-pilot.json `
  --out ../playtest/agent_sessions/2026-07-13-m5-ollama-pilot.jsonl `
  --report ../docs/reports/2026-07-13-m5-agent-playtest-ollama-pilot.md
```

## Acceptance criteria

- [x] Model choices cannot bypass the engine's legal-action list.
- [x] Opponent hidden information is absent from model prompts.
- [x] Invalid output retries and falls back without invalidating the game.
- [x] Decision-attempt budgets cannot be bypassed by malformed responses.
- [x] Round reflections use a snapshot from the completed round, before automatic next-round refresh.
- [x] JSONL and Markdown artifacts distinguish dry-run, local-model, and sim-only claims.
- [x] Deterministic three-persona campaign completes.
- [x] Quality-first local-model campaign completes and is reviewed.
- [x] Full repository verification is green.

## Execution record

- **Deterministic gate:** seeds 7301–7302, 2/2 completed, six qualitative seat-games, zero retries/fallbacks. This validates orchestration only.
- **Local-model pilot:** seed 7311, three personas, 7 rounds, final VP 10–5–10. The three sampled decisions, three round reflections, and three exit interviews completed with one retry and zero fallbacks; provider time totaled about 134 seconds.
- **Signals to replicate:** 4/18 council motions passed and 4/18 negotiation offers were accepted. Three battles (two attacker wins) are explicitly too few for a combat conclusion.
- **Synchronization finding:** pilot review exposed an old M3 encoding error: canonical Diplomatic Decree grants 2 Influence, while the simulator spent 2. The simulator and test were corrected before the retained pilot was generated. Earlier contaminated pilot output was overwritten.
- **Verification:** 357/357 pytest; M4 CI bracket 20/20 completed with zero crash/timeout/degenerate; manifest valid; all relative Markdown links valid; terminology sweep contained only allowed historical/definition hits; timing-window lint clean.

## Promotion rule

No M5 agent comment changes canon by itself. Repeated signals may become a written hypothesis; rules changes still require an owning-doc patch, propagation, sim regression gates, and a resolved entry in `rules_and_systems/INDEX.md`.
