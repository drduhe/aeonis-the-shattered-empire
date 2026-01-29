# Aeonis: The Shattered Empire (Kickstarter-bound board game)

This repo contains the working design documents for a fantasy “big strategy” board game (explicitly inspired by TI4-scale play), under the canonical name **Aeonis: The Shattered Empire**.

## Kickstarter intent (why this exists)

We’re building toward a Kickstarter to:

- **Manufacture the first copies** for distribution (the first print run).
- **Refine and clarify** the current ruleset (balance, timing clarity, onboarding).
- **Expand the roster** with many more factions/Lords and more content to support varied tables.

## What’s here today (high-level)

- **Round timing spine**: Canonical phase order and timing windows for a full round. See `rules_and_systems/Round_Structure.md`.
- **Core economy + action model**: An **Action Point (AP)** pool with rotating turns (one action per turn), variable action costs, passing, and limited AP banking. See `rules_and_systems/Actions.md`.
- **Map game**: Hex tiles with terrain production, special tiles (Cities/Ruins/Portals), and a fairly detailed **hex control / borders / ZOC** model. See `rules_and_systems/Tiles.md` and `rules_and_systems/Movement.md`.
- **Conflict**: Canon combat system with battle line + reserves (anti-doomstack) and siege rules for Cities/Fortresses. See `rules_and_systems/Combat.md`.
- **Progression**: A tiered “tech tree” style **Arcane Discoveries** system (schools, tiers, AP + resource cost) plus Lord-specific paths. See `rules_and_systems/Arcane.md`.
- **Growth constraint**: **Population** as a cap/soft limit that interacts with units and buildings, plus growth each round. See `rules_and_systems/Population.md`.
- **Politics layer**: The **High Council** defines motions, laws, and titles that can reshape borders and player power. See `rules_and_systems/High_Council.md`.
- **Victory**: VP from public/secret objectives, lord objectives, council titles, artifacts/buildings, “Throne of Power”, events, etc. See `rules_and_systems/Victory.md`.
- **Trade + upkeep**: Player-initiated trades (AP cost) plus unit/building upkeep and penalties. See `rules_and_systems/Trade_Taxes.md`.
- **Events**: Exploration/global/local/milestone events with examples. See `rules_and_systems/Events.md`.
- **Renown**: Fame/reputation unlocking bonuses and interacting with politics. See `rules_and_systems/Renown.md`.
- **Turn-order driver**: TI4-like **Strategy Cards** with initiative values, primaries, and secondaries. See `rules_and_systems/Strategy.md`.
- **Setting**: A strong lore prologue and key world “hooks” (Speaking Stones, rediscovered magic, banished lords, throne). See `rules_and_systems/Lore.md`.

## Folder map

- `rules_and_systems/`: Mechanics chapters (the “rulebook draft”).
- `marketing/`: Go-to-market docs.
  - `marketing/marketing.md`: Multi-phase campaign plan toward Kickstarter.
  - `marketing/Development_Plan.md`: High-level development phases and targets.
- `art/`: Visual references / inspiration images.
- `lore/`: Lorebook drafts and setting material (currently `lore/Lore.md`).

## Known gaps / inconsistencies to resolve next (highest impact)

- **Combat tuning**: Combat is now canonical (battle line + reserves, anti-doomstack, sieges). Next work is tuning numbers (defense bonuses, costs, siege reinforcement limits) and adding more unit types.
- **High Council integration pass**: Now that `rules_and_systems/High_Council.md` exists, update other chapters to reference its definitions (votes, motions, enactment timing) and align terminology (Influence vs IP).
- **Building system incomplete**: `rules_and_systems/Buildings.md` ends mid-sentence (Lord-specific buildings not defined).
- **Lakes / water tiles unfinished**: `rules_and_systems/Tiles.md` flags lakes as “needs work”, but movement/combat reference special traversal/portals.
- **Cost model consistency**:
  - **Population vs resource upkeep**: Canon is now “Population is the primary cap; resource upkeep is for advanced units and advanced/legendary buildings.” Ensure future unit/building additions follow this.
- **Victory system “lock-in”**: `Victory.md` offers many scoring routes and optional variants; deciding which are core vs optional will help testing and balancing.
- **Terminology**: The docs sometimes use “Influence Points (IP)” vs “Influence”.

## Suggested near-term workflow (for playability)

1. Lock a single **round structure** (council timing, strategy pick timing, production timing, event timing).
2. Lock a single **combat resolution** (and how reinforcement / unit caps interact with movement and ZOC).
3. Create a minimal “**first playable**” ruleset: 2–4 lords, 1–2 unit types, a small strategy deck, and a small event/objective set.
