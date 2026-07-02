# Artifact System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the Artifact system designed in `docs/plans/2026-02-19-artifact-system-design.md` across all Aeonis game design docs — creating the new system chapter and propagating changes to 13 existing files.

**Architecture:** A new `Artifacts.md` system chapter defines the canonical rules. Existing chapters receive targeted insertions (new actions, component entries, event cards, fragment hooks, trade rules) referencing back to `Artifacts.md`. The First Playable packet is updated to include the full system.

**Tech Stack:** Markdown docs, JSON manifest. No code changes.

---

## Task 1: Create `rules_and_systems/Artifacts.md` (core system chapter)

**Files:**
- Create: `new/rules_and_systems/Artifacts.md`
- Reference: `docs/plans/2026-02-19-artifact-system-design.md` (sections 1-10)

**Step 1: Write the Artifacts chapter**

Create `new/rules_and_systems/Artifacts.md` with the following structure. Use the design doc as source material, but format as rules text (short, testable rules with timing windows per `aeonis-authoring.mdc`):

```markdown
# Aeonis: Artifacts

## Overview

Artifacts are rare, named, unique relics of the fallen Eternal Empire. Each is a card drawn from a shared Artifact Deck (20-24 cards). No two are alike.

---

## Definitions

- **Artifact Deck**: A shared face-down deck of 20-24 unique Artifact Cards, shuffled during setup.
- **Remnant**: A generic token. Players collect fragments and purge 3 to draw an artifact.
- **Artifact Site**: A temporary marker placed on an existing hex by an Event. The top card of the Artifact Deck is placed face-up on the marker. Any player with a unit there may spend 1 AP to claim it.
- **Purge**: Return a card or token permanently to its supply/bottom of deck.

---

## Artifact Categories

[Include the 3-category table from design doc section 2]

### Lord Equipment
- Attaches to your Lord token.
- A Lord may carry at most **2** Lord Equipment artifacts.
- If you gain a third, you must immediately return one of your choice to the bottom of the Artifact Deck.
- Transfers to the captor when your Lord is captured (see `Combat.md`).

### Building Relics
- Must be assigned to an eligible building you control when gained.
- If you have no eligible building, hold the relic in your player area (no effect until attached).
- If the hex changes control, the new controller claims the relic (it stays attached to the building).
- If the building is destroyed with no occupier, return the relic to the bottom of the Artifact Deck.

### Utility Artifacts
- Held in your player area. No attachment limit.
- Not contestable unless the card specifies a transfer condition.

---

## Acquisition

### Artifact Sites (event-driven)

During play, specific Global Events and Exploration Events place an **Artifact Site marker** on an existing hex. When a marker is placed:

1. Draw the top card of the Artifact Deck and place it **face-up** on the marked hex.
2. Any player with a unit on that hex may spend **1 AP** during the Action Phase to claim the artifact (timing: ACTION).
3. Once claimed, remove the Artifact Site marker. The hex returns to its normal function.
4. Multiple Artifact Sites may exist simultaneously.
5. If the Artifact Deck is empty when a site would be created, no marker is placed.

### Remnants

At any time during your turn in the Action Phase, you may **purge 3 Remnants** (return them to the shared supply) to draw the top card of the Artifact Deck. This is a **free action** (0 AP).

If the Artifact Deck is empty, you cannot purge fragments to draw.

### Fragment Sources

| Source | Fragments | Timing |
|---|---|---|
| Exploration Events (specific cards) | 0-2 | Immediately on trigger |
| Controlling a Ruins hex | 1 per Ruins | Production & Upkeep |
| Completing an Arcane Discovery | 1 (Tier I) or 2 (Tier II+) | Immediately on completion |
| Specific Whisper Cards | 1-2 | Per card timing |
| Specific Global Events | 0-2 | Event Phase |
| Council motion rewards | 1 | Council Phase resolution |

---

## Losing and Transferring Artifacts

| Trigger | Result |
|---|---|
| Lord captured | Captor takes all Lord Equipment from the captured Lord. |
| Hex control changes | New controller claims any Building Relic attached to a building on that hex. |
| Building destroyed (no occupier) | Building Relic returns to bottom of Artifact Deck. |
| Specific card text | Follow the card (e.g., Shard of the Throne transfers on combat loss). |
| Voluntary trade | Players may trade Utility Artifacts and Remnants during a Trade action (see `Trade_Taxes.md`). Lord Equipment and Building Relics cannot be traded. |

---

## VP-Bearing Artifacts

Only these 4 artifacts award VP (1 VP each while controlled):

1. **Crown of Aeonis** (Lord Equipment)
2. **Eternal Forge** (Building Relic)
3. **Shard of the Throne** (Utility)
4. **Imperial Seal** (Utility)

All other artifacts provide mechanical effects but no VP. See `Victory.md` for VP integration.

---

## Timing

- Persistent artifact effects are always active while controlled.
- Artifacts that say "PRODUCTION" resolve during Production & Upkeep (see `Round_Structure.md`, phase 6).
- Artifacts with timing windows (ACTION, COMBAT, COUNCIL, WHEN) follow the same rules as Whisper Card timing (see `Whispers.md`).

---

## Artifact List

### Lord Equipment (7)

[Full table from design doc section 5.1]

### Building Relics (6)

[Full table from design doc section 5.2]

### Utility Artifacts (11)

[Full table from design doc section 5.3]

---

## Setup

1. Shuffle all Artifact Cards into a face-down **Artifact Deck**. Place near the play area.
2. Place **Remnant tokens** (30-40) in a shared supply.
3. Set aside **Artifact Site markers** (5-6 tokens) near the Event deck.
4. No player starts with artifacts or fragments.
```

Use the full artifact tables from the design doc (all 24 artifacts with complete effect text). Format each artifact entry consistently with: name, category, effect text including timing windows, and type tag.

**Step 2: Verify cross-references**

Check that every rules reference in the new chapter (`Combat.md`, `Trade_Taxes.md`, `Victory.md`, `Round_Structure.md`, `Whispers.md`) is accurate.

**Step 3: Commit**

```bash
git add new/rules_and_systems/Artifacts.md
git commit -m "feat: add Artifacts system chapter (24 unique relics, fragment acquisition, 3 categories)"
```

---

## Task 2: Update `Victory.md` — replace blanket VP rule

**Files:**
- Modify: `new/rules_and_systems/Victory.md:50-56`

**Step 1: Replace section 4 content**

Replace the current "Artifacts and Legendary Buildings" section (lines 50-56) with:

```markdown
### 4. Artifacts and Legendary Buildings

- **Artifact VP:** Only specific named artifacts award VP. Each VP-bearing artifact is worth **1 VP** while you control it (checked at Cleanup & Checks). VP-bearing artifacts:
  - **Crown of Aeonis** (Lord Equipment) — transfers when your Lord is captured.
  - **Eternal Forge** (Building Relic) — transfers when the attached hex changes control.
  - **Shard of the Throne** (Utility) — transfers to the combat winner when you lose a battle where your Lord was present. May also be freely traded.
  - **Imperial Seal** (Utility) — may be purged to prevent a Law or Decree from being repealed.
- **Legendary Buildings:** Each Legendary Building is worth **2-3 VP**, depending on its construction cost and impact.
- See `Artifacts.md` for the full artifact system.

*Why It Works:* VP-bearing artifacts are high-value targets that drive conflict and negotiation. Most artifacts provide power, not points, preventing snowball scoring.
```

**Step 2: Update the summary list**

At line 119, change:
```
4. **Artifacts and Legendary Buildings:** Encourages exploration and long-term control.
```
to:
```
4. **Artifacts and Legendary Buildings:** VP-bearing artifacts drive conflict; others provide power (see `Artifacts.md`).
```

**Step 3: Commit**

```bash
git add new/rules_and_systems/Victory.md
git commit -m "fix: replace blanket artifact VP rule with named VP-bearing artifacts"
```

---

## Task 3: Update `Components.md` — add artifact components

**Files:**
- Modify: `new/components/Components.md:71-86`

**Step 1: Add artifact components**

After the "Cards (print-and-play)" section header (line 73), add a new section before the card list:

```markdown
- **Artifact system**:
  - 24x Artifact Cards (print-and-play; see `rules_and_systems/Artifacts.md`)
  - 30-40x Remnant tokens (shared supply; small coin or shard-shaped)
  - 5-6x Artifact Site markers (placed on hexes when Events create sites; removed when claimed)
```

**Step 2: Update the Cards section**

Add to the card list (after Whisper Cards, line 85):
```markdown
- **Artifact Cards (24)**: unique relic cards drawn from a shared deck (see `rules_and_systems/Artifacts.md`)
```

**Step 3: Commit**

```bash
git add new/components/Components.md
git commit -m "feat: add artifact components to First Playable checklist"
```

---

## Task 4: Update `Actions.md` — add Claim Artifact action

**Files:**
- Modify: `new/rules_and_systems/Actions.md:16-26` (action costs list)
- Modify: `new/rules_and_systems/Actions.md:49` (artifact AP reference)
- Modify: `new/rules_and_systems/Actions.md:98-108` (spending AP list)

**Step 1: Add Claim Artifact to canonical action costs**

After the "Trade" entry at line 24, add:
```markdown
        - **Claim Artifact**: 1 AP to claim a face-up artifact from an Artifact Site (see `Artifacts.md`).
```

**Step 2: Update the artifact AP reference**

Replace line 49:
```
- **Artifacts:** Acquiring specific artifacts may grant temporary or permanent AP boosts.
```
with:
```
- **Artifacts:** Specific artifacts grant AP boosts (e.g., Scepter of Command grants a free Move order). See `Artifacts.md`.
```

**Step 3: Add Claim Artifact to spending list**

After the "Play an ACTION Whisper" entry at line 108, add:
```markdown
- **Claim Artifact:** 1 AP at an Artifact Site hex (see `Artifacts.md`).
```

**Step 4: Commit**

```bash
git add new/rules_and_systems/Actions.md
git commit -m "feat: add Claim Artifact action (1 AP) to Actions chapter"
```

---

## Task 5: Update `Events.md` — add artifact events and fragment rewards

**Files:**
- Modify: `new/rules_and_systems/Events.md:117-122` (Ancient Ruins example)
- Modify: `new/rules_and_systems/Events.md` (add new events at end of examples section)

**Step 1: Update the Ancient Ruins exploration event**

Replace lines 117-122 (Ancient Ruins) with:
```markdown
### Exploration Event: Ancient Ruins

- **Description:** You stumble upon the remains of a forgotten temple.
- **Options:**
    1. Search the ruins. Roll a die: On a 4+, gain 2 Remnants (see `Artifacts.md`). On 3 or less, lose 1 unit to a trap.
    2. Leave the ruins untouched. Gain +1 Renown for your caution.
```

**Step 2: Add new Artifact Site events at end of examples**

After the Rebellion example (line 133), add:

```markdown
### Global Event: Ruins Unearthed

- **Description:** An earthquake reveals the entrance to an ancient imperial vault.
- **Effect:** Place an **Artifact Site marker** on a neutral or uncontrolled Ruins hex (if none available, place on any neutral hex). Draw the top Artifact Card and place it face-up on the marker. Any player with a unit there may spend 1 AP to claim it (see `Artifacts.md`).

### Global Event: Echo of the Old Empire

- **Description:** A Speaking Stone resonates with a frequency not heard in a hundred years, guiding seekers to buried treasure.
- **Effect:** Place an **Artifact Site marker** on the hex closest to the Imperial Seat that does not already have one (break ties clockwise from Speaker). Draw the top Artifact Card and place it face-up on the marker (see `Artifacts.md`). All players gain 1 Remnant.

### Exploration Event: Ancient Vault Discovered

- **Description:** Behind a collapsed wall, you find a sealed chamber marked with imperial insignia.
- **Effect:** Place an **Artifact Site marker** on this hex. Draw the top Artifact Card and place it face-up here. You may immediately spend 1 AP to claim it (see `Artifacts.md`). If you do not, it remains for any player to claim.

### Exploration Event: Scattered Relics

- **Description:** Fragments of an ancient artifact litter the ground around a shattered monument.
- **Effect:** Gain 2 Remnants (see `Artifacts.md`).
```

**Step 3: Add artifact reference to Synergy section**

After the Population System synergy entry (line 111), add:

```markdown
### 6. Artifact System

- Events are the primary way Artifact Sites appear on the map. Global and Exploration events that create Artifact Sites drive territorial conflict around valuable relic locations. See `Artifacts.md`.
```

**Step 4: Commit**

```bash
git add new/rules_and_systems/Events.md
git commit -m "feat: add artifact site events and fragment rewards to Events chapter"
```

---

## Task 6: Update `Arcane.md` — add fragment generation hook

**Files:**
- Modify: `new/rules_and_systems/Arcane.md:91-96` (after gaining discovery)

**Step 1: Add fragment generation to Research action**

After step 5 in section 4.2 ("Gain the discovery: its effect becomes active immediately..."), add:

```markdown
6. **Gain Remnants**: When you complete a Research action, gain Remnants:
   - **Tier I**: 1 Remnant.
   - **Tier II**: 2 Remnants.
   - **Tier III**: 3 Remnants.
   See `Artifacts.md` for fragment rules.
```

**Step 2: Add artifact reference to integration hooks**

In section 6 (line 119-124), add a new bullet:

```markdown
- **Artifacts** (`Artifacts.md`): Completing any research generates Remnants. Some artifacts grant School Specialties or research bonuses.
```

**Step 3: Commit**

```bash
git add new/rules_and_systems/Arcane.md
git commit -m "feat: add Remnant generation to Arcane Discovery completion"
```

---

## Task 7: Update `Buildings.md` — add Building Relic rules

**Files:**
- Modify: `new/rules_and_systems/Buildings.md:111-116` (Upgrades section)

**Step 1: Add Building Relic attachment rules**

After the existing Upgrades section, add a new section:

```markdown
## Building Relics (Artifact Attachments)

Certain artifacts in the Artifact Deck are **Building Relics** — ancient power sources that attach to a specific building type. See `Artifacts.md` for the full system.

- When you gain a Building Relic, assign it to an eligible building you control.
- A building may hold at most **1 Building Relic** at a time.
- The relic's effect activates immediately upon attachment.
- If the attached building's hex changes control, the new controller claims the relic.
- If the attached building is destroyed and no player occupies the hex, the relic returns to the bottom of the Artifact Deck.

Building Relics that reference specific building types:

| Relic | Eligible Buildings |
|---|---|
| Ley Line Conduit | Academy, Mana-producing building |
| Titan's Cornerstone | Fortress, Tower |
| Eternal Forge | Forge |
| Verdant Hearthstone | Farm, City |
| Astral Beacon | Any building on a Portal hex |
| Archive of the Fallen | Academy, Library |
```

**Step 2: Update the Advanced Forge reference**

Replace line 114:
```
- **Upgrade Examples:** Improved Farm: Increases Population production to +4. Reinforced Tower: Adds +1 defense bonus to adjacent units. Advanced Forge: Unlocks a new tier of artifacts and unit upgrades.
```
with:
```
- **Upgrade Examples:** Improved Farm: Increases Population production to +4. Reinforced Tower: Adds +1 defense bonus to adjacent units. Advanced Forge: Unlocks advanced unit upgrades. For artifact interaction, see `Artifacts.md` (Building Relics).
```

**Step 3: Commit**

```bash
git add new/rules_and_systems/Buildings.md
git commit -m "feat: add Building Relic attachment rules to Buildings chapter"
```

---

## Task 8: Update `Trade_Taxes.md` — add artifacts and fragments as tradeable

**Files:**
- Modify: `new/rules_and_systems/Trade_Taxes.md`

**Step 1: Find the section on tradeable goods and add**

Add a note to the trade rules specifying what artifact items can be traded:

```markdown
### Artifact Trade

During a Trade action, players may also exchange:

- **Remnants**: Any number may be offered or received.
- **Utility Artifacts**: May be freely traded between players.
- **Lord Equipment and Building Relics**: Cannot be traded. Lord Equipment transfers only via Lord capture; Building Relics transfer only via hex control change.

See `Artifacts.md` for full artifact rules.
```

**Step 2: Commit**

```bash
git add new/rules_and_systems/Trade_Taxes.md
git commit -m "feat: add artifact and fragment trade rules to Trade & Taxes chapter"
```

---

## Task 9: Update `Tiles.md` — add Artifact Site marker note

**Files:**
- Modify: `new/rules_and_systems/Tiles.md:219` (special hex table)

**Step 1: Update the Artifact Sites entry in the control benefits table**

Replace:
```
| **Artifact Sites** | Grants control over a powerful artifact when occupied.             |
```
with:
```
| **Artifact Sites** | Temporary markers placed by Events. A face-up Artifact Card is displayed; spend 1 AP to claim (see `Artifacts.md`). |
```

**Step 2: Commit**

```bash
git add new/rules_and_systems/Tiles.md
git commit -m "fix: update Artifact Sites hex description to match event-driven system"
```

---

## Task 10: Update `Round_Structure.md` — confirm artifact timing

**Files:**
- Modify: `new/rules_and_systems/Round_Structure.md:136-139`

**Step 1: Update the Production & Upkeep artifact reference**

The existing text at line 139 already reads:
```
   - Any laws, artifacts, or discoveries that say "each round" resolve here unless they specify a different window.
```

This is already compatible. Add a parenthetical cross-reference:

Replace with:
```
   - Any laws, artifacts, or discoveries that say "each round" resolve here unless they specify a different window (see `Artifacts.md` for artifact-specific timing).
```

**Step 2: Add fragment generation to Production & Upkeep**

After the line about "end of round resource effects," add:
```markdown
5. **Artifact fragment generation**:
   - Each Ruins hex you control generates **1 Remnant** (see `Artifacts.md`).
```

**Step 3: Commit**

```bash
git add new/rules_and_systems/Round_Structure.md
git commit -m "feat: add artifact timing and fragment generation to Round Structure"
```

---

## Task 11: Update `Whispers.md` — add artifact-interacting cards

**Files:**
- Modify: `new/rules_and_systems/Whispers.md`

**Step 1: Add 2 new Whisper Cards to the deck**

Find the card list section and add these to the appropriate categories:

**Economic category:**
```markdown
- **Relic Hunter** (ACTION / WHEN you enter an unexplored hex): Gain 1 Remnant immediately, in addition to any Exploration Event rewards. *(Fragment/artifact synergy.)*
```

**Subterfuge category:**
```markdown
- **Relic Thief** (WHEN another player claims an artifact from an Artifact Site): Cancel their claim. You claim the artifact instead (you must have a unit in an adjacent hex). *(Artifact denial.)*
```

**Step 2: Update the deck count**

Update the deck count reference from "24-card" to "26-card" in any headers or summaries within the file.

**Step 3: Commit**

```bash
git add new/rules_and_systems/Whispers.md
git commit -m "feat: add Relic Hunter and Relic Thief Whisper Cards for artifact interaction"
```

---

## Task 12: Update `First_Playable_Packet.md` — add artifact system

**Files:**
- Modify: `new/playtest/First_Playable_Packet.md`

**Step 1: Add Artifacts to "What rules are on" (section 1)**

After the Whispers.md entry (line 24), add:
```markdown
- `Artifacts.md` (full artifact system: 24-card deck, Remnants, event-driven Artifact Sites)
```

**Step 2: Add section 4.8 — Artifacts**

After section 4.7 (Whisper Cards), add:

```markdown
### 4.8 Artifacts (full system)

Use `rules_and_systems/Artifacts.md` as written. The Artifact system is fully enabled for First Playable.

**Setup:**
- Shuffle all 24 Artifact Cards into a face-down deck.
- Place 30-40 Remnant tokens in a shared supply.
- Set aside 5-6 Artifact Site markers near the Event deck.
- No player starts with artifacts or fragments.

**Artifact Sites:** Created during play by specific Global Events (Ruins Unearthed, Echo of the Old Empire) and Exploration Events (Ancient Vault Discovered). See `Events.md` for the event cards.

**Remnants:** Earned from exploration, Ruins control, Arcane research, Whisper Cards, and Events. Purge 3 at any time on your turn to draw an artifact (free action).

**VP:** Only 4 specific artifacts award VP (1 VP each): Crown of Aeonis, Eternal Forge, Shard of the Throne, Imperial Seal.

**Card summary by category:**
- Lord Equipment (7): Blade of the Last Emperor, Crown of Aeonis, Voidwalker's Cloak, Emberstone Gauntlet, Warden's Aegis, Whisperer's Mask, Scepter of Command
- Building Relics (6): Ley Line Conduit, Titan's Cornerstone, Eternal Forge, Verdant Hearthstone, Astral Beacon, Archive of the Fallen
- Utility (11): Shard of the Throne, Cartographer's Glass, Scroll of Dominion, Tome of Forbidden Rites, Mask of Many Faces, Wellspring Chalice, Imperial Seal, Echo of the World Tree, Mercenary Contract, Windcaller's Horn, Shroud of Nightfall
```

**Step 3: Add playtest goal**

Add to section 7 (Playtest goals), after item 9:

```markdown
10. **Artifacts**: Do Remnants feel attainable without being trivial (target: first artifact drawn by round 3-4)? Do Artifact Site events create interesting territorial conflict? Do VP-bearing artifacts feel like high-value targets? Is the Lord Equipment carry limit (2) restrictive enough?
```

**Step 4: Update Exploration Events list (section 4.5)**

Replace the "Remnant" exploration event (line 217):
```
- **Remnant**: Gain 1 VP immediately.
```
with:
```
- **Scattered Relics**: Gain 2 Remnants (see `Artifacts.md`).
```

And add the new exploration events:
```markdown
- **Ancient Vault Discovered**: Place an Artifact Site marker on this hex. Draw the top Artifact Card face-up. You may spend 1 AP to claim it immediately (see `Artifacts.md`).
```

**Step 5: Update Global Events list (section 4.5)**

Add the 2 new global events to the list:
```markdown
- **Ruins Unearthed**: Place an Artifact Site marker on a neutral/uncontrolled Ruins hex (or any neutral hex). Draw the top Artifact Card face-up on it (see `Artifacts.md`).
- **Echo of the Old Empire**: Place an Artifact Site marker on the hex closest to the Imperial Seat without one. Draw the top Artifact Card face-up. All players gain 1 Remnant (see `Artifacts.md`).
```

**Step 6: Commit**

```bash
git add new/playtest/First_Playable_Packet.md
git commit -m "feat: add full artifact system to First Playable packet"
```

---

## Task 13: Update `content-manifest.json` — add Artifacts entry

**Files:**
- Modify: `new/content-manifest.json`

**Step 1: Add Artifacts.md to the Rules & Systems category**

In the `"rules"` category `docs` array, after the Events entry (around line 166), add:

```json
{
  "title": "Artifacts",
  "path": "rules_and_systems/Artifacts.md",
  "description": "Relic deck, fragment acquisition, three artifact categories, and VP-bearing relics.",
  "status": "playtest",
  "minutes": 10,
  "tags": ["rules", "artifacts", "exploration"]
}
```

**Step 2: Update the Whispers.md entry**

The Whispers description should note the updated card count. Find the Whispers entry in the manifest — no change needed unless we want to update the description (optional).

**Step 3: Commit**

```bash
git add new/content-manifest.json
git commit -m "feat: add Artifacts chapter to Codex manifest"
```

---

## Task 14: Update `INDEX.md` — update chapter listing and remaining work

**Files:**
- Modify: `new/rules_and_systems/INDEX.md`

**Step 1: Add Artifacts to chapter listing**

After the Whispers entry (line 24), add:
```markdown
- **`Artifacts.md`**: Artifact deck (24 unique relics), Remnants, event-driven Artifact Sites, three categories (Lord Equipment, Building Relics, Utility), and VP-bearing artifacts.
```

**Step 2: Remove Artifacts from remaining work**

Delete line 49:
```
- **Artifacts**: Referenced in Lore, Victory, and Events but no dedicated system chapter yet.
```

**Step 3: Remove Artifacts from "next docs" list**

Delete line 57:
```
- An **Artifacts** system chapter.
```

**Step 4: Add Artifacts to resolved decisions**

After the Lord roster entry (line 43), add:
```markdown
- **Artifact system**: 24 unique relics in a shared deck; Remnant acquisition (3 fragments = 1 artifact); event-driven Artifact Sites; 3 categories (Lord Equipment, Building Relics, Utility); 4 VP-bearing artifacts; full system in First Playable.
```

**Step 5: Commit**

```bash
git add new/rules_and_systems/INDEX.md
git commit -m "feat: mark artifact system as resolved in INDEX"
```

---

## Execution Order Summary

| Task | File(s) | Dependency |
|---|---|---|
| 1 | Create `Artifacts.md` | None (do first) |
| 2 | `Victory.md` | After Task 1 |
| 3 | `Components.md` | After Task 1 |
| 4 | `Actions.md` | After Task 1 |
| 5 | `Events.md` | After Task 1 |
| 6 | `Arcane.md` | After Task 1 |
| 7 | `Buildings.md` | After Task 1 |
| 8 | `Trade_Taxes.md` | After Task 1 |
| 9 | `Tiles.md` | After Task 1 |
| 10 | `Round_Structure.md` | After Task 1 |
| 11 | `Whispers.md` | After Task 1 |
| 12 | `First_Playable_Packet.md` | After Tasks 5, 11 (needs event names and Whisper count) |
| 13 | `content-manifest.json` | After Task 1 |
| 14 | `INDEX.md` | Last (confirms everything is done) |

Tasks 2-11 and 13 are independent of each other and can be parallelized.
