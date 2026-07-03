# Aeonis: Strategy Cards

## Overview

The Strategy Card system drives initiative order and gives each round its strategic identity. Each round, players draft cards from a shared pool of **8 Strategy Cards**. Each card grants a **primary ability** (used by the card's owner on their turn) and a **secondary ability** (an opt-in follow that other players may pay for when the primary resolves). Lower card numbers act earlier in the Action Phase but carry more modest abilities; higher numbers act later but hit harder.

This chapter is the owning doc for the Strategy Card system. Timing rules live in `Round_Structure.md` (Strategy Selection is step 3).

---

## 1. The Draft

### 1.1 Draft order (canon)

Players choose Strategy Cards in **ascending VP order** (lowest VP picks first). This gives trailing players first access to the strongest cards, serving as a built-in catch-up mechanism.

- **Ties:** broken by lowest Renown, then clockwise from the Speaker.
- This order is fixed for the full game and applies to all player counts (3-8).

### 1.2 Cards per player (by player count)

All **8 cards** are revealed every round, at every player count.

- **3-4 players:** each player drafts **2 cards**. Complete one full pass in draft order (1 card each), then a second pass in the same order.
- **5-8 players:** each player drafts **1 card**.

### 1.3 Unchosen cards (bounty)

At the end of Strategy Selection, place **1 Gold** from the supply on each card that was not drafted. Gold accumulates across rounds. When a player drafts a card carrying Gold, they take all Gold on it immediately.

### 1.4 Initiative order

- Every Strategy Card has a **number** (1-8). Lower numbers act first in the Action Phase.
- If you hold 2 cards, your initiative is your **lowest** card number.

---

## 2. Primaries and Secondaries

### 2.1 Primary ability

- Activating a Strategy Card primary is an **action** taken on your turn during the Action Phase (see `Actions.md`). Pay the AP cost listed on the card.
- Each card's primary may be used **once per round**.
- You are never required to use your primary.

### 2.2 Secondary ability (opt-in follow)

- Immediately after a primary fully resolves, **each other player**, in initiative order, may use that card's secondary by paying its listed cost.
- Secondaries do **not** consume the follower's turn and do not use an action.
- Each player may use a given card's secondary **at most once per round**.
- The card's owner may never use their own card's secondary.

---

## 3. The Eight Strategy Cards (canon deck)

### 1. Arcane Ascendancy

- **Primary (1 AP):** Gain 2 Mana, then research one **Tier I** discovery for free (ignore its AP and resource costs).
- **Secondary:** You may immediately research one discovery you qualify for by paying its resource cost **+1 Mana** (no AP; does not consume your turn).
- **Initiative:** 1

### 2. Resource Surge

- **Primary (0 AP):** Gain 2 Gold, 2 Mana, and 1 Influence.
- **Secondary:** Spend 1 AP to gain 1 Gold and 1 Mana.
- **Initiative:** 2

### 3. Military Maneuvers

- **Primary (1 AP):** Resolve one **Move** action for one group at **0 AP path cost** (ZOC surcharges still apply). You may then immediately declare one **Attack** this turn for **1 AP** instead of 2.
- **Secondary:** Spend 1 AP to move one of your unit groups **1 hex** (pay terrain and ZOC costs normally).
- **Initiative:** 3

### 4. Diplomatic Decree

- **Primary (1 AP):** Gain 2 Influence and take the **Speaker token**. Then convene an **emergency council session**: propose one motion and resolve it immediately using the normal voting rules (`High_Council.md`). Lobbying is allowed; no other proposals are heard.
- **Secondary:** Spend 1 AP to gain 2 Influence.
- **Initiative:** 4

### 5. Expansion Strategy

- **Primary (1 AP):** Claim one **neutral** hex adjacent to territory you control that contains no other player's units. Gain +1 Population Pool (up to cap).
- **Secondary:** Spend 2 Influence to claim one **neutral** hex adjacent to territory you control that contains no other player's units.
- **Initiative:** 5

### 6. Tactical Reinforcements

- **Primary (1 AP):** Recruit up to 2 units for **free** (no Gold/Mana cost; Population costs still apply) in one City you control. This ignores the once-per-City-per-round Recruit limit.
- **Secondary:** Spend 1 AP to take a **Recruit** action (paying normal costs) at one City you control, even if that City has already recruited this round.
- **Initiative:** 6

### 7. Economic Boom

- **Primary (0 AP):** Gain 5 Gold.
- **Secondary:** Spend 1 AP to gain 2 Gold.
- **Initiative:** 7

### 8. Imperial Mandate

- **Primary (1 AP):** If you control the **Imperial Seat**, gain **1 VP**. Otherwise, draw **1 secret objective**. In either case, gain 1 Influence.
- **Secondary:** Spend 2 Influence to draw 1 Whisper Card.
- **Initiative:** 8

---

## 4. System Integration

- **Catch-up:** The VP-ascending draft means trailing players choose first — grabbing Imperial Mandate or Arcane Ascendancy before leaders can.
- **Politics:** Diplomatic Decree is the only way to move the Speaker token and force a mid-round vote; it makes initiative 4 a political weapon.
- **Economy:** Resource Surge and Economic Boom bracket the economy; the bounty rule (§1.3) makes habitually-skipped cards worth revisiting.
- **Whispers:** Imperial Mandate's secondary is a reliable Whisper source; see `Whispers.md`.
- **Objectives:** Imperial Mandate respects the secret objective hand cap (see `Objectives.md`).

---

## 5. Optional Variations

### 5.1 Faction Strategy Cards

Introduce faction-specific Strategy Cards tailored to each Lord's playstyle, drafted into the pool as replacements by table agreement. Design contract: same anatomy (number, primary with AP cost, opt-in secondary).

### 5.2 Event-Driven Cards

Certain Global Events may add a temporary ninth Strategy Card to the pool for one round with a unique effect. Remove it at Cleanup.
