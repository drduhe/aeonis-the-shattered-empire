# Agent Playtest Simulation — Design Spec

**Date:** 2026-07-02
**Status:** Approved design; implementation not started
**Scope:** A multi-agent simulation system that plays Aeonis (First Playable Packet) against itself to produce balance data and rules validation.

---

## 1. Goals

1. **Balance data**: Lord win rates, VP-source distribution, round counts, income curves, runaway-leader/catch-up behavior — at bulk-run volume (hundreds to thousands of games).
2. **Rules validation**: surface contradictions, gaps, and undefined interactions in the `rules_and_systems/` chapters, both while encoding them and during agent play.
3. **Subjective-experience signal**: structured feedback from LLM agents (and objective proxies from bots) mapped to the 11 playtest goals in `playtest/First_Playable_Packet.md` §7.

Non-goals: replacing human playtesting (D1 pacing/fun judgments stay human); simulating free-form table talk beyond the structured negotiation protocol; 2-player support (out of scope per D4).

## 2. Decisions locked during brainstorming

- **Architecture**: engine-authoritative simulator with pluggable agents (Approach A). One coded rules engine is the sole authority; agents only ever choose among engine-enumerated legal actions.
- **Agents**: hybrid — heuristic persona bots for bulk balance runs; LLM-backed agents for rules validation and subjective feedback.
- **Engine scope**: phased content milestones (see §5), not full-packet-at-once.
- **Stack**: Python, stdlib-preferred, living at `new/sim/` beside `new/mcp/`.
- **LLM runtime**: provider-agnostic interface with adapters for **Cursor SDK** and **local models (Ollama)** as first-class targets, plus direct API as a third adapter. Selected per-agent in tournament config.
- **Negotiation**: structured typed-offer protocol enforced by the engine; no free-form chat.

## 3. Architecture

```
new/sim/
  engine/     # Game state, rules, phase machine, legal-action enumeration.
              # Knows nothing about agents. Pure, deterministic, seedable.
  agents/     # Agent interface + heuristic bots + LLM-backed agent.
              # Depends only on engine observation/action types.
  llm/        # Provider abstraction: complete(messages, json_schema) -> response.
              # Adapters: cursor-sdk, direct API, Ollama. Used only by agents/.
  runner/     # Wires agents to engine; tournaments, seeds, parallelism.
  reports/    # Aggregates game records into balance stats, playtest reports,
              # sentiment digest, ambiguity ledger updates.
```

Dependencies are one-way: `reports -> runner -> agents -> engine`, `agents -> llm`.

### Core loop

1. Engine advances to the next **decision point** (e.g., "Player 3, Action Phase turn").
2. Engine emits an **observation** (the acting player's legal view; hidden info such as other hands and face-down decks is filtered out) plus the complete list of **legal actions**.
3. The agent returns one action, optionally with annotations (§4).
4. Engine applies the action, appends it to the event-sourced **game log**, repeats.

Guarantees: no agent can create an illegal state; any game — including a crashed one — replays exactly from `(seed, action log)`.

### Ambiguity ledger

`new/playtest/Ambiguity_Ledger.md`. Each entry: the rules question, chapters consulted, the interpretation the engine encodes, and the doc that should own the fix. Sources: (a) engine implementation hitting a gap, (b) LLM-agent `rules_question` annotations (tagged with game ID), deduplicated on append.

## 4. Subjective feedback

**LLM agents** — three channels:

1. **In-move annotations**: optional `highlight` / `frustration` / `rules_question` fields on every decision response. Near-zero marginal cost.
2. **Round-end reflection**: short structured prompt at Cleanup & Checks (current plan, is it working, what felt good/bad). Sampled (default: every other round) to control token cost.
3. **Post-game exit interview**: survey keyed to the 11 playtest goals in `First_Playable_Packet.md` §7, plus "would you play again?" and free-form comments. Output fills `agents/templates/Playtest_Report_Template.md` so simulated and human sessions produce the same artifact.

**Heuristic bots** — the runner computes objective proxies filling the same report fields: downtime (decision points where Pass was the only sensible option), hopelessness (rounds with no improvement in a player's best VP path), runaway-leader and kingmaking detection.

The reports module aggregates feedback into a **sentiment digest** per batch. Every feedback item carries game ID + seed for exact replay.

Caveat (by design): LLM "feelings" are directional signal correlating with degenerate states, not a substitute for human table time.

## 5. Rules engine

- **Phase machine** mirroring `Round_Structure.md` exactly: Round Start → Event → Strategy Selection → High Council → Action Phase (rotating turns until all pass) → Production & Upkeep → Cleanup & Checks. Every timing-window rule has one unambiguous home; anywhere it doesn't is an ambiguity ledger entry.
- **State**: plain serializable structure — hex map (tiles, control, units, buildings, sites), per-player trays (AP, Gold/Mana/Influence, Renown, VP, Population, hands), shared decks/discards, council state, round marker. Hidden information explicitly marked for per-player observation filtering.
- **Randomness**: single seeded RNG; a game is fully determined by `(seed, agent decisions)`.
- **Actions**: each action type implements `enumerate(state, player)` (all legal instances, costs resolved) and `apply(state, action)`.
- **Invariants** asserted after every action: no negative resources, population within cap, unit counts within component limits, VP consistent with sources. Violation = halt + dump replayable record (always an engine bug or rules hole, never an agent error).

### Content milestones

| # | Content | Gate |
|---|---------|------|
| 1 | Core loop: map gen per packet §3; Move/Attack/Build/Recruit/Pass; baseline combat (battle line, retreats, Lord stats); production & upkeep; Imperial Seat VP; public objectives; 10 VP end | 100 consecutive crash/invariant-free bot games; milestone chapters' ledger entries triaged |
| 2 | Politics & strategy: 8 Strategy cards, VP-ordered draft + bounty gold, initiative, High Council with 8-card agenda deck, structured negotiation | same |
| 3 | Card systems: Whispers (26), global + exploration Events, Artifacts/Remnants/Sites, Arcane Tier I, secret objectives | same |
| 4 | Lord asymmetry: all 8 Lord sheets (passives, actives, unique tiles, faction discoveries, Legendary Buildings) | same |

## 6. Agents

### Interface

- `choose(observation, legal_actions) -> Decision` (one legal action + optional annotations).
- `reflect(round_summary)`, `exit_interview(game_summary)` — answered by LLM agents; no-ops for bots (proxies come from the runner).

### Heuristic bots

One scoring bot parameterized by **persona weight vectors** over features: VP progress, expected combat odds, income delta, territory, objective progress, Council leverage. Personas: *Warmonger*, *Economist*, *Expander*, *Diplomat*, *Balanced*, plus *Chaos* (uniform random; engine fuzzing only, excluded from balance stats). Deterministic given seed. Tournaments sweep Lord × persona pairings to separate "Lord is strong" from "persona suits Lord."

### LLM agents

Prompt = per-phase rules digest generated from the chapter docs + observation + legal actions (grouped/truncated when large, expandable on request) + the Lord sheet's strategy notes. Response = JSON: action + annotations. Invalid response → one retry with the validation error → fallback to heuristic bot for that move, logged (repeated fallbacks are themselves a finding: confusing observation or digest).

### LLM provider layer

`complete(messages, json_schema) -> response` with adapters: **Cursor SDK** (`cursor-sdk` Python), **direct API**, **Ollama**. Chosen per-seat in tournament config; mixed-provider games supported.

### Negotiation protocol

- Offer = bundle of *gives*/*gets*: resources, vote commitments on a named motion, non-aggression through round N, border permissions.
- Flow: propose → accept / reject / one counter → closed (bounded; no loops).
- **Binding** terms per `Diplomacy.md` binding-deal rules execute automatically (resource transfers, enforceable commitments). **Non-binding promises** are tracked, making betrayal frequency and consequences measurable.
- Bots evaluate offers with their persona scoring function; LLM agents see offers in observations and may propose wherever the phase allows (Council negotiation window, trade actions).

## 7. Data flow and outputs

- **Game record** (JSONL, one per game): seed, config (players, Lords, personas/models), full action log, per-round snapshots, feedback annotations, verdict + result. The atomic unit; everything below derives from it.
- **Tournament config** (JSON/YAML): game count, player counts, matchups, per-seat agent type/provider. Bot games run in parallel; LLM games sequential or lightly concurrent for rate limits.
- **Outputs per batch**:
  - **Balance summary** — dated markdown: win rate by Lord (+ matchup matrix), VP-source distribution, round count/length, income curves, combat frequency, Council pass rates, catch-up impact. Referenced from `playtest/Balance_Dashboard.md`.
  - **Session log rows** — appended to `playtest/session_log.csv`, tagged simulated.
  - **Playtest reports** — one per LLM game via `agents/templates/Playtest_Report_Template.md`.
  - **Sentiment digest** — aggregated feedback/proxies keyed to the packet's 11 observation goals.
  - **Ambiguity ledger updates** — deduplicated appends.

## 8. Error handling, broken games, and testing

### Structural guards (the engine cannot hang)

- **Pass is always legal**; zero enumerated actions = invariant violation (halt + dump).
- **Hard round cap** (default 25) ends the game gracefully with standings.
- **Livelock detection**: per-turn state hashing; repeated states without progress (no AP spent, no VP movement) ends the game flagged.

### Verdicts (every game record ends with one)

| Verdict | Meaning | Use |
|---|---|---|
| `completed` | VP threshold reached | Only these feed balance statistics |
| `timeout` | Round cap hit | Pacing finding (VP sources too slow/unreachable) |
| `stalled` | Livelock detected | Missing incentive or engine gap |
| `degenerate` | Completed but a monitor fired (N rounds no VP for anyone; whole-phase immediate passing; economy collapse) | Design finding |
| `crashed` | Engine bug / invariant violation | Engine backlog; record saved at point of death |

Batch reports lead with the verdict breakdown so balance is never tuned on a silently filtered subset.

### Triage loop

Group non-completed games by failure signature (verdict + similar final state); minimize one representative replay to the earliest round showing the problem; classify each signature as **engine bug** (code fix) or **design finding** (ambiguity ledger / balance report). Milestone gates force convergence before new content lands.

### Testing

- **Per-chapter unit tests**: concrete scenarios from the docs (e.g., cavalry flanking requires attack from 2+ directions; Lord capture = +1 VP + ability lockout). Doubles as an executable rules reference — doc changes surface as named test failures, supporting the canon-propagation workflow.
- **Replay/golden tests**: recorded games re-run after every engine change; final-state divergence flags unintended behavior change.
- **Fuzzing**: continuous Chaos-bot batches hunting crashes/invariant violations.
- **Determinism guard**: bot-only games run twice per seed at every milestone; any mismatch fails the build.
- **LLM failures**: timeouts/malformed output degrade to heuristic fallback, never kill a game; incident counts per provider appear in batch reports.

## 9. Defaults for implementation (revisit only if they fail)

- **Observation/action JSON schemas**: defined during implementation planning; the engine's Python types are the source of truth and the JSON forms are generated from them.
- **Rules digest**: hand-curated per-phase digest files, each citing the owning chapter; a digest is reviewed whenever its cited chapter changes (fits the canon-propagation checklist).
- **Bot lookahead**: 1-ply (score immediate successor states). Deepen only if 1-ply bots prove too weak to generate meaningful pressure on the design.
