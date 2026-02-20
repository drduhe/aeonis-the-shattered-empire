# Aeonis: Artifacts

## Overview

Artifacts are rare, named, unique relics of the fallen Eternal Empire. Each is a card drawn from a shared **Artifact Deck** (24 cards). No two are alike. They represent enchanted weapons, ancient regalia, forbidden tomes, and embedded warding stones scattered across Aeonis after the empire's collapse.

---

## Definitions

- **Artifact Deck**: A shared face-down deck of 24 unique Artifact Cards, shuffled during setup.
- **Remnant**: A generic token. Players collect Remnants and purge 3 to draw an artifact.
- **Artifact Site**: A temporary marker placed on an existing hex by an Event. The top card of the Artifact Deck is placed face-up on the marker.
- **Purge**: Return a card or token permanently to its supply or the bottom of the Artifact Deck.

---

## Artifact Categories

| Category | Attached to | Limit | Contestable via |
|---|---|---|---|
| **Lord Equipment** | Your Lord token | Max 2 per Lord | Lord capture in combat |
| **Building Relic** | A specific building you control | 1 per building | Hex control change or building destruction |
| **Utility** | Your player area | No limit | Specific card text, or not at all |

### Lord Equipment

- Attaches to your Lord token immediately when gained.
- A Lord may carry at most **2** Lord Equipment artifacts. If you gain a third, you must immediately return one of your choice to the bottom of the Artifact Deck.
- When your Lord is captured in combat (see [Combat](Combat.md)), the captor takes **all** Lord Equipment from the captured Lord.

### Building Relics

- When you gain a Building Relic, you must assign it to an eligible building you control.
- If you have no eligible building, hold the relic in your player area with no effect until you attach it to an eligible building (free action on your turn).
- A building may hold at most **1** Building Relic.
- If the attached building's hex changes control, the new controller claims the relic (it stays attached to the building).
- If the attached building is destroyed and no player occupies the hex, return the relic to the bottom of the Artifact Deck.

### Utility Artifacts

- Held in your player area. No attachment required. No limit.
- Not contestable unless the card specifies a transfer condition.

---

## Acquisition

### Artifact Sites (event-driven)

Artifact Sites are **not** a fixed tile type. They are created during play when specific Events resolve (see [Events](Events.md)).

1. When an Event creates an Artifact Site, place an **Artifact Site marker** on the specified hex.
2. Draw the top card of the Artifact Deck and place it **face-up** on the marked hex.
3. Any player with a unit on that hex may spend **1 AP** to claim the artifact. Timing: **ACTION** (on your turn during the Action Phase).
4. Once claimed, remove the Artifact Site marker. The hex returns to its normal function.
5. Multiple Artifact Sites may exist simultaneously.
6. If the Artifact Deck is empty when a site would be created, do not place the marker.

### Remnants

At any time during your turn in the Action Phase, you may **purge 3 Remnants** (return them to the shared supply) to draw the top card of the Artifact Deck. This is a **free action** (costs 0 AP).

If the Artifact Deck is empty, you may not purge Remnants to draw.

### Remnant Sources

| Source | Remnants | Timing |
|---|---|---|
| Exploration Events (specific cards) | 0–2 per event | Immediately on trigger |
| Controlling a Ruins hex | 1 per Ruins hex | Production & Upkeep |
| Completing an Arcane Discovery | 1 (Tier I), 2 (Tier II), or 3 (Tier III) | Immediately on completion |
| Specific Whisper Cards | 1–2 per card | Per card timing window |
| Specific Global Events | 0–2 per event | Event Phase |
| Council motion rewards | 1 | Council Phase resolution |

---

## Losing and Transferring Artifacts

| Trigger | Result |
|---|---|
| **Lord captured** | Captor takes all Lord Equipment from the captured Lord. Other artifact types unaffected. |
| **Hex control changes** | New controller claims any Building Relic attached to a building on that hex. |
| **Building destroyed (no occupier)** | Building Relic returns to bottom of Artifact Deck. |
| **Specific card text** | Follow the card (e.g., Shard of the Throne transfers on combat loss). |
| **Voluntary trade** | Players may trade Utility Artifacts and Remnants during a Trade action (see [Trade & Taxes](Trade_Taxes.md)). Lord Equipment and Building Relics may not be traded. |

---

## VP-Bearing Artifacts

Only these 4 artifacts award VP (**1 VP** each, checked at Cleanup & Checks):

1. **Crown of Aeonis** (Lord Equipment)
2. **Eternal Forge** (Building Relic)
3. **Shard of the Throne** (Utility)
4. **Imperial Seal** (Utility)

All other artifacts provide mechanical effects but no VP. See [Victory](Victory.md).

---

## Timing

- **Persistent** effects are always active while you control the artifact.
- Artifacts that specify **PRODUCTION** resolve during Production & Upkeep (see [Round Structure](Round_Structure.md), phase 6).
- Artifacts with timing windows (**ACTION**, **COMBAT**, **COUNCIL**, **WHEN [trigger]**) follow the same timing rules as Whisper Cards (see [Whispers](Whispers.md)).

---

## Artifact List

### Lord Equipment (7 artifacts)

**1. Blade of the Last Emperor**
- **Category:** Lord Equipment
- **Effect:** Your Lord rolls +1 die size for Attack (e.g., d6 → d8). **PURGE:** After winning a battle where your Lord was present, you may purge this artifact to capture the enemy Lord even if they would normally escape.
- **Type:** Persistent + Purge

**2. Crown of Aeonis**
- **Category:** Lord Equipment
- **Effect:** **1 VP** (checked at Cleanup & Checks). You gain +2 Influence during High Council voting. If your Lord is captured, the captor gains this artifact and the VP.
- **Type:** VP-Bearing

**3. Voidwalker's Cloak**
- **Category:** Lord Equipment
- **Effect:** Your Lord gains +1 Movement. **WHEN** your Lord would be captured: You may purge this artifact to escape instead. Your Lord retreats to your nearest controlled hex at 1 HP.
- **Type:** Persistent + Reactive

**4. Emberstone Gauntlet**
- **Category:** Lord Equipment
- **Effect:** Your Lord's Attack rolls gain: on a natural maximum result, deal 1 additional HP damage to the target.
- **Type:** Persistent

**5. Warden's Aegis**
- **Category:** Lord Equipment
- **Effect:** Your Lord gains +1 HP (maximum). Units in the same hex as your Lord gain +1 Defense die size.
- **Type:** Persistent

**6. Whisperer's Mask**
- **Category:** Lord Equipment
- **Effect:** Draw +1 Whisper Card at Round Start (see [Whispers](Whispers.md)). **COUNCIL:** Once per Council Phase, you may look at one player's secret objective.
- **Type:** Persistent + Reactive

**7. Scepter of Command**
- **Category:** Lord Equipment
- **Effect:** **ACTION:** Once per round, you may issue an order to a unit group up to 3 hexes from your Lord — that group takes a free Move action (1 hex).
- **Type:** Persistent

### Building Relics (6 artifacts)

**8. Ley Line Conduit**
- **Category:** Building Relic
- **Eligible Buildings:** Academy or any Mana-producing building
- **Effect:** **PRODUCTION:** This building produces +2 Mana. You gain 1 Remnant each time you complete an Arcane Discovery (see [Arcane](Arcane.md)).
- **Type:** Persistent

**9. Titan's Cornerstone**
- **Category:** Building Relic
- **Eligible Buildings:** Fortress or Tower
- **Effect:** The attached building cannot be destroyed by non-siege combat. Units defending this hex roll +1 die size for Defense.
- **Type:** Persistent

**10. Eternal Forge**
- **Category:** Building Relic
- **Eligible Buildings:** Forge
- **Effect:** **1 VP** (checked at Cleanup & Checks). **PRODUCTION:** You may recruit 1 unit at this hex for −1 Gold cost (minimum 1).
- **Type:** VP-Bearing

**11. Verdant Hearthstone**
- **Category:** Building Relic
- **Eligible Buildings:** Farm or City
- **Effect:** **PRODUCTION:** +2 Population growth at this hex. Adjacent hexes you control produce +1 Gold.
- **Type:** Persistent

**12. Astral Beacon**
- **Category:** Building Relic
- **Eligible Buildings:** Any building on a Portal hex
- **Effect:** You may treat all Portals on the map as connected to this hex for Portal travel, even enemy-controlled Portals.
- **Type:** Persistent

**13. Archive of the Fallen**
- **Category:** Building Relic
- **Eligible Buildings:** Academy
- **Effect:** **PURGE:** Immediately gain 2 Arcane Discoveries of Tier I from any school. Ignore prerequisites for these discoveries.
- **Type:** One-Time Purge

### Utility Artifacts (11 artifacts)

**14. Shard of the Throne**
- **Category:** Utility
- **Effect:** **1 VP** (checked at Cleanup & Checks). **WHEN** you lose a battle where your Lord was present: The winner may take this artifact from you. This artifact may be freely traded between players during a Trade action.
- **Type:** VP-Bearing

**15. Cartographer's Glass**
- **Category:** Utility
- **Effect:** **PURGE:** Reveal all unexplored hexes on the map. You gain 1 Remnant for each Ruins hex revealed this way.
- **Type:** One-Time Purge

**16. Scroll of Dominion**
- **Category:** Utility
- **Effect:** **PURGE:** Immediately place 1 building (any type you can normally build) on any hex you control. Ignore AP cost. You must still pay resource costs.
- **Type:** One-Time Purge

**17. Tome of Forbidden Rites**
- **Category:** Utility
- **Effect:** **PURGE:** Take an extra full turn immediately after your current turn ends. You may not purge this artifact on consecutive rounds.
- **Type:** One-Time Purge

**18. Mask of Many Faces**
- **Category:** Utility
- **Effect:** **COUNCIL:** Once per Council Phase, you may cast a vote anonymously — your Influence is counted but your identity is hidden from other players.
- **Type:** Persistent

**19. Wellspring Chalice**
- **Category:** Utility
- **Effect:** **PRODUCTION:** Choose one — gain 2 Gold, 2 Mana, or 2 Influence.
- **Type:** Persistent

**20. Imperial Seal**
- **Category:** Utility
- **Effect:** **1 VP** (checked at Cleanup & Checks). **COUNCIL:** Your proposals cannot be vetoed. **WHEN** a Law or Decree you support would be repealed: You may purge this artifact to prevent the repeal.
- **Type:** VP-Bearing + Reactive

**21. Echo of the World Tree**
- **Category:** Utility
- **Effect:** **WHEN** you would lose your last unit on a hex: That unit survives with 1 HP instead. Once per round.
- **Type:** Reactive

**22. Mercenary Contract**
- **Category:** Utility
- **Effect:** **PURGE:** Immediately recruit 3 Infantry units to any hex you control, ignoring Population limits. These units desert (remove them) at the end of next round unless they are in combat.
- **Type:** One-Time Purge

**23. Windcaller's Horn**
- **Category:** Utility
- **Effect:** **ACTION:** Once per round, one of your unit groups may move +2 hexes this turn, ignoring terrain movement penalties.
- **Type:** Persistent

**24. Shroud of Nightfall**
- **Category:** Utility
- **Effect:** **WHEN** another player targets you with a Whisper Card: Cancel that card's effect. It is discarded with no effect. Once per round.
- **Type:** Reactive

---

## Setup

1. Shuffle all 24 Artifact Cards into a face-down **Artifact Deck**. Place near the play area.
2. Place **Remnant tokens** (30–40) in a shared supply.
3. Set aside **Artifact Site markers** (5–6 tokens) near the Event deck.
4. No player starts with artifacts or Remnants.
