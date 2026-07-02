# Artifact System Design

**Date:** 2026-02-19
**Status:** Approved — ready for implementation
**Scope:** Full system in First Playable

---

## 1. Concept

Artifacts are rare, named, unique relics of the fallen Eternal Empire. Each is a physical card drawn from a shared **Artifact Deck** (20–24 cards). No two are alike. They represent the most powerful objects in Aeonis — enchanted weapons, ancient regalia, forbidden tomes, and embedded warding stones.

Design reference: TI4 Relics — rare, powerful uniques with a mix of persistent and one-time effects, adapted with fantasy flavor and deeper integration into Aeonis's Lord, building, and council systems.

---

## 2. Artifact Categories

| Category | What it is | Attached to | Contestable via |
|---|---|---|---|
| **Lord Equipment** | Gear your Lord wields or wears | Your Lord token (max 2) | Lord capture in combat |
| **Building Relics** | Ancient power sources embedded in infrastructure | A specific building you control | Hex control change or building destruction |
| **Utility Artifacts** | Standalone effects — scrolls, maps, tomes | Your player area (no location) | Specific steal conditions on the card, or not at all |

---

## 3. Acquisition — Hybrid Model

### 3.1 Artifact Sites (event-driven)

Artifact Sites are **not** a special tile type. They are created dynamically during play when specific Events resolve.

- Certain **Global Events** (e.g., "Ruins Unearthed," "Echo of the Old Empire") or **Exploration Events** (e.g., "Ancient Vault Discovered") place an **Artifact Site marker** on an existing hex and reveal the top Artifact Card face-up on it.
- Any player with a unit on that hex may spend **1 AP** during the Action Phase to claim the artifact.
- The marker remains until the artifact is claimed, then is removed. The hex returns to its normal function.
- Multiple Artifact Sites can exist simultaneously.

### 3.2 Remnants

Generic tokens earned from multiple sources. Purge (return to supply) **3 Remnants** at any time during your turn to draw the top card of the Artifact Deck. This is a **free action** (no AP cost).

**Fragment sources:**

| Source | Fragments Gained | Timing |
|---|---|---|
| Exploration Event (entering unexplored hex) | 0–2 (per event card) | Immediately on trigger |
| Controlling a Ruins hex | 1 per Ruins hex | Production & Upkeep |
| Completing an Arcane Discovery | 1 (Tier I) or 2 (Tier II) | Immediately on completion |
| Specific Whisper Cards | 1–2 (per card text) | Per card timing window |
| Specific Global Events | 0–2 (per event card) | Event Phase |
| Council motion reward | 1 (if a motion grants it) | Council Phase resolution |

---

## 4. Effect Design

### 4.1 Effect type distribution (across 20–24 artifacts)

| Effect Type | Count | Description |
|---|---|---|
| **Persistent Passive** | ~8 | Ongoing advantage while you control it |
| **One-Time Purge** | ~7 | Powerful single use — discard the artifact to trigger |
| **VP-Bearing** | 3–4 | Worth 1 VP while you control it (also has a mechanical effect) |
| **Reactive** | ~4 | Triggered by a specific condition (combat, council vote, event) |

### 4.2 Timing windows

Artifacts follow existing Aeonis timing conventions:

- **Persistent**: Always active while controlled.
- **ACTION**: Play during your turn in the Action Phase.
- **COMBAT**: Play during combat resolution.
- **COUNCIL**: Play during High Council Phase.
- **WHEN [trigger]**: Reactive — activates when the condition is met.
- **PRODUCTION**: Resolves during Production & Upkeep.

---

## 5. Artifact List

### 5.1 Lord Equipment (7 artifacts)

| # | Name | Effect | Type |
|---|---|---|---|
| 1 | **Blade of the Last Emperor** | Your Lord rolls +1 die size for Attack (e.g., d6 → d8). PURGE: After winning combat, capture the enemy Lord even if they would normally escape. | Persistent + Purge |
| 2 | **Crown of Aeonis** | **1 VP.** You gain +2 Influence during High Council voting. If your Lord is captured, the captor gains this artifact and the VP. | VP-Bearing |
| 3 | **Voidwalker's Cloak** | Your Lord gains +1 Movement. WHEN your Lord would be captured: You may purge this artifact to escape instead (Lord retreats to nearest controlled hex). | Persistent + Reactive |
| 4 | **Emberstone Gauntlet** | Your Lord's combat rolls gain: On a natural max result, deal 1 additional HP damage. | Persistent |
| 5 | **Warden's Aegis** | Your Lord gains +1 HP. Units in the same hex as your Lord gain +1 Defense die size. | Persistent |
| 6 | **Whisperer's Mask** | Draw +1 Whisper Card at Round Start. COUNCIL: You may look at one player's secret objective. | Persistent + Reactive |
| 7 | **Scepter of Command** | ACTION: Once per round, you may issue an order to a unit group up to 3 hexes away — they take a free Move action (1 hex). | Persistent |

### 5.2 Building Relics (6 artifacts)

| # | Name | Attaches To | Effect | Type |
|---|---|---|---|---|
| 8 | **Ley Line Conduit** | Academy or Mana-producing building | PRODUCTION: This building produces +2 Mana. You gain 1 Remnant each time you complete an Arcane Discovery. | Persistent |
| 9 | **Titan's Cornerstone** | Any Fortress or Tower | The attached building cannot be destroyed by non-siege combat. Units defending this hex roll +1 die size. | Persistent |
| 10 | **Eternal Forge** | Forge | **1 VP.** PRODUCTION: You may recruit 1 unit at this hex for −1 Gold cost (minimum 1). | VP-Bearing |
| 11 | **Verdant Hearthstone** | Farm or City | PRODUCTION: +2 Population growth at this hex. Adjacent hexes you control produce +1 Gold. | Persistent |
| 12 | **Astral Beacon** | Any building on a Portal hex | You may treat all Portals on the map as connected to this hex, even enemy-controlled ones. | Persistent |
| 13 | **Archive of the Fallen** | Academy or Library | PURGE: Immediately gain 2 Arcane Discoveries of Tier I from any school (ignore prerequisites). | One-Time Purge |

### 5.3 Utility Artifacts (10–11 artifacts)

| # | Name | Effect | Type |
|---|---|---|---|
| 14 | **Shard of the Throne** | **1 VP.** WHEN you lose a combat where your Lord was present: The winner may take this artifact. Can also be traded freely between players. | VP-Bearing |
| 15 | **Cartographer's Glass** | PURGE: Reveal all unexplored hexes on the map. You gain 1 Remnant for each Ruins hex revealed this way. | One-Time Purge |
| 16 | **Scroll of Dominion** | PURGE: Immediately place 1 free building (any type you can normally build) on any hex you control, ignoring AP cost. You still pay resource costs. | One-Time Purge |
| 17 | **Tome of Forbidden Rites** | PURGE: Take an extra full turn immediately after your current turn ends. (Cannot be used on consecutive rounds.) | One-Time Purge |
| 18 | **Mask of Many Faces** | COUNCIL: Once per Council Phase, you may cast a vote anonymously — your Influence is counted but your identity is hidden from other players. | Persistent |
| 19 | **Wellspring Chalice** | PRODUCTION: Choose one — gain 2 Gold, 2 Mana, or 2 Influence. | Persistent |
| 20 | **Imperial Seal** | **1 VP.** COUNCIL: Your proposals cannot be vetoed. WHEN a Law or Decree would be repealed: You may purge this to prevent it. | VP-Bearing + Reactive |
| 21 | **Echo of the World Tree** | WHEN you would lose your last unit on a hex: That unit survives with 1 HP instead. (Once per round.) | Reactive |
| 22 | **Mercenary Contract** | PURGE: Immediately recruit 3 Infantry units to any hex you control, ignoring Population limits. These units desert (are removed) at the end of next round if not in combat. | One-Time Purge |
| 23 | **Windcaller's Horn** | ACTION: Once per round, one of your unit groups may move +2 hexes this turn (ignoring terrain movement penalties). | Persistent |
| 24 | **Shroud of Nightfall** | WHEN another player targets you with a Whisper Card: Cancel that card's effect. It is discarded with no effect. (Once per round.) | Reactive |

---

## 6. Attachment & Limits

- **Lord Equipment**: Immediately attaches to your Lord. A Lord may carry up to **2 Equipment artifacts**. If you gain a third, you must discard one (return to bottom of the Artifact Deck).
- **Building Relics**: Must be assigned to an eligible building you control when gained. If you have no eligible building, hold it in your player area until you do (no effect until attached).
- **Utility Artifacts**: Go to your player area. No limit.

---

## 7. Losing & Transferring Artifacts

| Trigger | What happens |
|---|---|
| **Lord captured** | Captor takes all Lord Equipment from the captured Lord. Other artifact types unaffected. |
| **Building destroyed or hex lost** | If a Building Relic's hex changes control, the new controller claims the relic (stays attached). If the building is destroyed with no occupier, the relic returns to the bottom of the Artifact Deck. |
| **Specific card text** | Some artifacts (e.g., Shard of the Throne) have explicit transfer conditions. Follow the card. |
| **Voluntary trade** | Players may trade Utility Artifacts and Remnants as part of normal trade actions (per `Trade_Taxes.md`). Lord Equipment and Building Relics cannot be traded. |

---

## 8. VP Model

Only **4 specific artifacts** are VP-bearing (1 VP each while controlled):

1. **Crown of Aeonis** (Lord Equipment) — transfers on Lord capture
2. **Eternal Forge** (Building Relic) — transfers on hex control
3. **Shard of the Throne** (Utility) — transfers on combat loss, freely tradeable
4. **Imperial Seal** (Utility) — can be purged to block council repeal

This replaces the current blanket "1 VP per Artifact" rule in `Victory.md`.

---

## 9. Setup

1. **Shuffle the Artifact Deck** (all 20–24 cards). Place face-down near the play area.
2. **Place Remnant supply** (30–40 tokens) in a shared pool.
3. **Set aside Artifact Site markers** (5–6 tokens) near the Event deck.
4. No player starts with artifacts or fragments. Artifact Sites appear during play via Events.

---

## 10. Physical Components

| Component | Quantity | Description |
|---|---|---|
| **Artifact Cards** | 20–24 | Standard card size. Name, category icon (Lord/Building/Utility), effect text, timing window, VP badge if applicable. |
| **Remnant Tokens** | 30–40 | Small tokens (coin or shard-shaped). Generic — no types. Shared supply. |
| **Artifact Site Markers** | 5–6 | Small tokens placed on hexes when Events create Artifact Sites. Removed when artifact is claimed. |

---

## 11. Integration — Files Requiring Updates

| File | Change |
|---|---|
| **New: `rules_and_systems/Artifacts.md`** | Full system chapter (this design, formatted as rules text) |
| `Victory.md` | Replace "1 VP per artifact" with named VP-bearing artifacts |
| `Components.md` | Add Artifact Cards, Remnant Tokens, Artifact Site Markers |
| `Actions.md` | Add "Claim Artifact (1 AP)" action; update AP boost reference |
| `Events.md` | Add Artifact Site events (2–3 Global, 1–2 Exploration); add fragment rewards to existing events |
| `Arcane.md` | Add fragment generation on Discovery completion |
| `Round_Structure.md` | Confirm "each round" artifact effects resolve in Production & Upkeep (already compatible) |
| `Buildings.md` | Add Building Relic attachment rules; update Advanced Forge reference |
| `Trade_Taxes.md` | Add artifacts and fragments as tradeable goods |
| `Tiles.md` | Add note that hexes can be temporarily designated as Artifact Sites via events |
| `First_Playable_Packet.md` | Add full artifact system to playtest scope |
| `content-manifest.json` | Add `Artifacts.md` chapter entry |
| `INDEX.md` | Remove "Artifacts" from remaining-work list; add to chapter listing |
| `Whispers.md` | Add 1–2 Whisper Cards that interact with fragments or artifacts |
