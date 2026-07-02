# Buildings Overhaul Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Overhaul the Buildings system — finalize Forge/Academy/Bank, add 8 Legendary Building faction capstones, cut the upgrade system, and bring the full building roster into First Playable.

**Architecture:** `Buildings.md` gets a major rewrite as the owning chapter. Changes propagate to 8 Lord sheets, the First Playable packet, and 5 supporting system files. The Archive of the Fallen artifact fixes a dangling "Library" reference.

**Tech Stack:** Markdown docs, JSON manifest. No code changes.

---

## Task 1: Rewrite `Buildings.md` — finalize TBD buildings, add Legendary capstones, cut upgrades

**Files:**
- Modify: `new/rules_and_systems/Buildings.md`
- Reference: `docs/plans/2026-02-19-buildings-overhaul-design.md`

**Step 1: Finalize Forge (lines 79-83)**

Replace the current Forge entry with:

```markdown
- **Forge / Arcane Forge** (Cities):
  - Build cost: 5 Gold
  - Population capacity: occupies 1 Population
  - Resource upkeep: 1 Mana per round (see `Trade_Taxes.md`)
  - Effect: Once per round, when you Recruit at this City, you may recruit **1 additional unit** beyond the normal 2-unit limit. Units recruited at this City cost **−1 Gold** (minimum 1).
```

**Step 2: Finalize Academy (lines 84-88)**

Replace the current Academy entry with:

```markdown
- **Academy** (Cities):
  - Build cost: 4 Gold, 3 Mana
  - Population capacity: occupies 2 Population
  - Resource upkeep: 1 Mana per round (see `Trade_Taxes.md`)
  - Effect: You gain a **School Specialty** of your choice (counts as +1 sigil when checking Arcane prerequisites; see `Arcane.md` section 3.3). Once per round, when you take a Research action, reduce its resource cost by **1 Mana** (minimum 0).
```

**Step 3: Finalize Bank (lines 89-93)**

Replace the current Bank entry with:

```markdown
- **Bank** (Cities):
  - Build cost: 5 Gold
  - Population capacity: occupies 1 Population
  - Resource upkeep: none
  - Effect: Once per round during **Production & Upkeep**, you may convert resources at a 2:3 rate. Choose one: **2 Mana → 3 Gold**, **2 Gold → 3 Mana**, or **2 Gold → 3 Influence**.
```

**Step 4: Replace the Legendary Building placeholder (lines 104-108)**

Replace the current stub with a full Legendary Buildings section containing:
- System rules (per design doc section 3)
- All 8 faction capstones with name, Lord, prerequisite, cost, upkeep, and effect (per design doc section 3)

**Step 5: Remove the Upgrade system (lines 110-116)**

Delete the entire "New Mechanics: Building Upgrades" section and the Upgrade Examples, Cost of Upgrades, and Upgrade Slots entries. The Advanced Forge reference in this section was already updated during the Artifact implementation.

**Step 6: Update the Lord-specific buildings section (lines 147-160)**

Replace the template with a note stating that each Lord's Legendary Building IS their unique building, and reference the Legendary Buildings section above.

**Step 7: Commit**

```bash
git add new/rules_and_systems/Buildings.md
git commit -m "feat: finalize Forge/Academy/Bank, add 8 Legendary Buildings, cut upgrade system"
```

---

## Task 2: Fix Archive of the Fallen in `Artifacts.md`

**Files:**
- Modify: `new/rules_and_systems/Artifacts.md`

**Step 1: Update eligible buildings**

Find the Archive of the Fallen entry. Change:
- "Academy or Library" → "Academy"

This appears in two places: the artifact entry in the Artifact List section, and possibly in any Building Relic reference table.

**Step 2: Commit**

```bash
git add new/rules_and_systems/Artifacts.md
git commit -m "fix: remove Library reference from Archive of the Fallen (merged into Academy)"
```

---

## Task 3: Update `Victory.md` — Legendary Building specifics

**Files:**
- Modify: `new/rules_and_systems/Victory.md`

**Step 1: Update section 4**

In the "Artifacts and Legendary Buildings" section, update the Legendary Buildings bullet. Replace:
```
- **Legendary Buildings:** Each Legendary Building is worth **2-3 VP**, depending on its construction cost and impact.
```
with:
```
- **Legendary Buildings:** Each Lord has one unique Legendary Building (faction capstone). Each is worth **2 VP** (checked at Cleanup & Checks). If the City containing a Legendary Building is captured, the captor gains control and its VP. Constructing a Legendary Building also grants **+2 Renown** immediately. See `Buildings.md`.
```

**Step 2: Commit**

```bash
git add new/rules_and_systems/Victory.md
git commit -m "fix: update Legendary Buildings VP rules with faction capstone specifics"
```

---

## Task 4: Update `Population.md` — Legendary Population cost

**Files:**
- Modify: `new/rules_and_systems/Population.md`

**Step 1: Update the building costs section**

Find the Legendary Buildings entry (around line 69) that says:
```
- **Legendary Buildings:** May require significant Population Points both to build and maintain.
```
Replace with:
```
- **Legendary Buildings:** Each occupies **3 Population** (reserved capacity while the building exists). See `Buildings.md`.
```

**Step 2: Commit**

```bash
git add new/rules_and_systems/Population.md
git commit -m "fix: set Legendary Building Population cost to 3"
```

---

## Task 5: Update `First_Playable_Packet.md` — full building roster

**Files:**
- Modify: `new/playtest/First_Playable_Packet.md`

**Step 1: Update section 4.2 (Buildings allowed)**

Replace the current building list and exclusion note. The new section should list ALL buildings as allowed:

```markdown
### 4.2 Buildings (allowed — full roster)

All buildings from `Buildings.md` are available:

**Production:** Farm, Mine, Grove, Embassy

**Military/Defensive:** Tower, Fortress, Bridge

**Advanced:** Guild Hall, Forge, Academy, Bank, Market, Castle

**Legendary (faction capstones):** Each Lord has 1 unique Legendary Building. See `Buildings.md` for prerequisites, costs, and effects. Legendary Buildings cost **4 AP** to construct, occupy **3 Population**, and are worth **2 VP**.

**Build action cost: 3 AP** for standard buildings, **4 AP** for Legendary Buildings (see `Actions.md`).
```

Remove the "Not used in First Playable" exclusion list (the line about Academy, Forge, Bank, Castle, Legendary Buildings).

**Step 2: Add playtest goal**

In section 7 (Playtest goals), add after the Artifacts goal:

```markdown
11. **Buildings (full roster)**: Do the finalized Forge/Academy/Bank feel worth their cost? Are Legendary Building prerequisites achievable by round 4-5? Does the 2 VP reward justify the 4 AP + resource investment? Do players target each other's Legendary Buildings?
```

**Step 3: Commit**

```bash
git add new/playtest/First_Playable_Packet.md
git commit -m "feat: enable full building roster in First Playable including Legendary capstones"
```

---

## Task 6: Update `INDEX.md` — resolve Legendary Buildings

**Files:**
- Modify: `new/rules_and_systems/INDEX.md`

**Step 1: Remove from remaining work**

Delete the line:
```
- **Legendary Buildings**: Mentioned in `Buildings.md` but no specific examples defined.
```

**Step 2: Remove from "next docs" list**

Delete the line:
```
- A **Legendary Buildings** catalog.
```

**Step 3: Add to resolved decisions**

After the Artifact system entry, add:
```
- **Buildings overhaul**: Forge/Academy/Bank finalized with concrete effects; upgrade system removed (covered by Arcane Discoveries + Building Relics); 8 Legendary Buildings defined as faction capstones (1 per Lord, 2 VP, +2 Renown, multi-gate prerequisites, 4 AP + resources to build); full building roster in First Playable.
```

**Step 4: Commit**

```bash
git add new/rules_and_systems/INDEX.md
git commit -m "feat: mark buildings overhaul and Legendary Buildings as resolved"
```

---

## Task 7: Update `content-manifest.json`

**Files:**
- Modify: `new/content-manifest.json`

**Step 1: Update Buildings description**

Find the Buildings entry and update its description:
```json
"description": "Full building roster: production, military, advanced, and 8 Legendary faction capstones."
```

**Step 2: Commit**

```bash
git add new/content-manifest.json
git commit -m "fix: update Buildings description in Codex manifest"
```

---

## Task 8: Add Legendary Buildings to Lord sheets (all 8)

**Files:**
- Modify: `new/lords/Cassian.md`
- Modify: `new/lords/Seraphel.md`
- Modify: `new/lords/Vharok.md`
- Modify: `new/lords/Elyndra.md`
- Modify: `new/lords/Rakhis.md`
- Modify: `new/lords/Nyxara.md`
- Modify: `new/lords/Auriel.md`
- Modify: `new/lords/Thalrik.md`

**Step 1: Add Legendary Building entry to each Lord sheet**

For each Lord, find the appropriate section (after abilities/faction mechanics, before objectives or Future Content) and add a "Legendary Building" section with:

- **Name**
- **Prerequisite**
- **Build cost** (4 AP + resources)
- **Population:** 3
- **VP:** 2 VP (checked at Cleanup & Checks)
- **Effect** (full rules text)

Use the entries from the design doc section 3. Each Lord gets their specific building:

| Lord | File | Building |
|---|---|---|
| Cassian | `Cassian.md` | Grand Exchange |
| Seraphel | `Seraphel.md` | Arcane Sanctum |
| Vharok | `Vharok.md` | Iron Citadel |
| Elyndra | `Elyndra.md` | Heartwood Sanctum |
| Rakhis | `Rakhis.md` | Windsworn Warcamp |
| Nyxara | `Nyxara.md` | Hall of Whispers |
| Auriel | `Auriel.md` | Cathedral of Radiance |
| Thal'rik | `Thalrik.md` | Dimensional Nexus |

**Step 2: Commit**

```bash
git add new/lords/*.md
git commit -m "feat: add Legendary Building entries to all 8 Lord sheets"
```

---

## Task 9: Verify `Renown.md` cross-reference

**Files:**
- Verify: `new/rules_and_systems/Renown.md`

**Step 1: Check line 33**

Verify the line reads: "Constructing unique or legendary buildings: **+2 Renown**."

This is already correct and compatible with the new Legendary Building system. No change needed unless the wording says something different.

If it says "unique or legendary" — update to: "Constructing a **Legendary Building**: **+2 Renown** (see `Buildings.md`)."

**Step 2: Commit (only if changed)**

```bash
git add new/rules_and_systems/Renown.md
git commit -m "fix: clarify Legendary Building Renown reference"
```

---

## Execution Order Summary

| Task | File(s) | Dependency |
|---|---|---|
| 1 | `Buildings.md` (major rewrite) | None (do first) |
| 2 | `Artifacts.md` (Library fix) | After Task 1 |
| 3 | `Victory.md` | After Task 1 |
| 4 | `Population.md` | After Task 1 |
| 5 | `First_Playable_Packet.md` | After Task 1 |
| 6 | `INDEX.md` | After Task 1 |
| 7 | `content-manifest.json` | After Task 1 |
| 8 | Lord sheets (8 files) | After Task 1 |
| 9 | `Renown.md` (verify) | After Task 1 |

Tasks 2-9 are independent of each other and can be parallelized after Task 1.
