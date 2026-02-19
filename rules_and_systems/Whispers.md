# Aeonis: Whisper Cards

Whisper Cards are a shared deck of one-time tactical effects that players draw into a private hand and play at specific timing windows. They represent the intelligence gathered by Speaking Stones, secret preparations of hidden agents, sealed orders, and political schemes that a Lord can deploy at the critical moment.

> *"The Stones do not shout. They whisper -- and those who listen rule."*

---

## Core Rules

### 1. The Deck

- All Whisper Cards are shuffled into a single shared deck at game start.
- Played and discarded Whispers go to a face-up **discard pile**.
- When the draw deck is exhausted, shuffle the discard pile to form a new draw deck.

### 2. Drawing Whispers

- At **Round Start**, each player draws **2 Whisper Cards** from the deck.
- Additional draws may be granted by:
  - **Scoring VP**: whenever you score VP from any source, draw 1 Whisper.
  - **Strategy Card effects**: some Strategy Card secondaries may grant draws.
  - **Lord abilities**: if a Lord sheet grants Whisper draws, it will say so.
  - **Events**: certain events may grant draws.

### 3. Hand Limit

- Each player may hold at most **7 Whisper Cards** in hand.
- At **Cleanup & Checks**, any player with more than 7 must discard down to 7 (their choice which to discard).

### 4. Playing Whispers

Each Whisper specifies a **timing window** that determines when it can be played:

| Timing         | When you can play it                                                                 |
| -------------- | ------------------------------------------------------------------------------------ |
| **ACTION**     | On your turn during the Action Phase, instead of your normal action. Costs 0 AP.     |
| **COMBAT**     | During the specified step of a battle you are involved in.                            |
| **COUNCIL**    | During the High Council Phase, at the specified moment.                               |
| **WHEN [X]**   | Immediately after the described trigger occurs. Any player whose trigger matches may play. |

Rules for playing:

- Each player may play **at most 1 Whisper per timing window** per occurrence. (Example: in a single battle round, you may play 1 combat Whisper during Strike and 1 during Pre-Strike, but not 2 during Strike.)
- **ACTION** Whispers use your turn for the round. You do not pay AP, but play passes to the next player afterward (just like any other action).
- **Other timing** Whispers do not consume your turn. You play them "inline" when the trigger occurs.
- If multiple players want to play a Whisper in response to the same trigger, resolve in **initiative order** (active player first, then clockwise).
- Whispers are played face-up, resolved immediately, then placed in the discard pile.

### 5. Sabotage (the counter-card)

The Whisper "**Sabotage**" can cancel another Whisper as it is played. When Sabotage is played:

- The targeted Whisper's effect is completely negated.
- Both Sabotage and the negated Whisper are discarded.
- Sabotage cannot be Sabotaged (it resolves instantly).

---

## Whisper Timing and the Round

For reference, here is where Whisper play windows map to the round structure (see `Round_Structure.md`):

1. **Round Start**: Draw 2 Whispers. WHEN triggers that say "at Round Start" can be played.
2. **Event Phase**: WHEN triggers related to events.
3. **Strategy Selection**: No standard Whisper windows.
4. **High Council Phase**: COUNCIL Whispers can be played.
5. **Action Phase**: ACTION Whispers on your turn. COMBAT Whispers during battles. WHEN triggers throughout.
6. **Production & Upkeep**: WHEN triggers related to production.
7. **Cleanup & Checks**: Discard down to hand limit of 7.

---

## First Playable Whisper Deck (26 cards)

### Combat Whispers (8)

#### Shield Wall

- **Timing:** COMBAT (during Counterstrike step)
- **Requirement:** You are the defender.
- **Effect:** Choose one of your Battle Line units. It gains **+2 Defense** for this battle round.

#### Flanking Charge

- **Timing:** COMBAT (during Strike step)
- **Requirement:** You have at least one Cavalry on your Battle Line.
- **Effect:** Choose one of your Cavalry on the Battle Line. It rolls **d12** instead of d8 for its Attack this battle round.

#### Deadly Volley

- **Timing:** COMBAT (during Archer Pre-Strike)
- **Requirement:** You have Archers on your Battle Line.
- **Effect:** Each of your Archers on the Battle Line deals **+1 damage** on successful hits this Pre-Strike (a hit that would deal 1 damage now deals 2).

#### Tactical Withdrawal

- **Timing:** COMBAT (during Retreat Check)
- **Requirement:** You are retreating.
- **Effect:** Your retreating units may move to any hex you control within **2 hexes** of the battle hex (not just adjacent hexes).

#### Rallying Cry

- **Timing:** WHEN you suffer more casualties than the opponent in a battle round.
- **Effect:** Gain **+1 AP** immediately. This AP must be spent this round.

#### Fortify Position

- **Timing:** WHEN you win a battle as defender.
- **Effect:** Place **1 Infantry** for free in the defended hex. (You must have available Population; the Infantry still occupies 1 Population.)

#### Overwhelming Numbers

- **Timing:** COMBAT (during Reinforce Battle Lines step)
- **Effect:** Increase your Battle Line Cap by **+1** for this battle round only. (You may immediately promote 1 additional Reserve to the Battle Line.)

#### Iron Resolve

- **Timing:** COMBAT (before dice are rolled for Strike or Counterstrike)
- **Effect:** Choose one of your Battle Line units. It **cannot be destroyed** this battle round. If its HP would reach 0, it survives at 1 HP instead.

---

### Political Whispers (5)

#### Sabotage

- **Timing:** WHEN another player plays a Whisper Card.
- **Effect:** Cancel that Whisper's effect completely. Both Sabotage and the targeted Whisper are discarded. Sabotage cannot itself be Sabotaged.

#### Backroom Deal

- **Timing:** COUNCIL (during Voting, before votes are tallied for a motion)
- **Effect:** Add **+2 votes** to either the "for" or "against" side of the current motion (your choice). These votes are in addition to your normal Council Votes and any Lobbying.

#### Veto

- **Timing:** COUNCIL (immediately after a motion passes)
- **Effect:** The motion **fails instead**. All effects of the motion are negated; Influence spent on Lobbying is still lost. (Cannot target Title motions.)

#### Political Leverage

- **Timing:** COUNCIL (during the Proposal Window)
- **Effect:** Gain **2 Influence**. You may **propose one additional motion** this round (in addition to your normal one-per-round limit). The additional proposal still costs 1 Influence as normal.

#### Leaked Intelligence

- **Timing:** COUNCIL (when the Speaker reveals the agenda card for the round)
- **Effect:** Look through the agenda deck. Replace the revealed card with any card from the deck. Shuffle the remaining deck. The new card becomes the free-proposal option this round.

---

### Economic Whispers (6)

#### Hidden Cache

- **Timing:** ACTION
- **Effect:** Gain **3 Gold** or **3 Mana** (choose one).

#### War Profiteer

- **Timing:** WHEN another player initiates an Attack action (not your attack).
- **Effect:** Gain **2 Gold**.

#### Emergency Conscription

- **Timing:** WHEN you complete a Recruit action.
- **Effect:** Place **1 additional Infantry** for free in the same City. (You must have available Population; the Infantry occupies 1 Population as normal. This does not count against the 2-unit Recruit limit.)

#### Prospector's Find

- **Timing:** ACTION
- **Effect:** Choose one tile you control. During the next Production & Upkeep Phase, that tile produces **double its normal resources**.

#### Contraband

- **Timing:** ACTION
- **Effect:** Gain **1 Gold, 1 Mana, and 1 Influence**.

#### Relic Hunter

- **Timing:** ACTION / WHEN you enter an unexplored hex.
- **Effect:** Gain 1 Remnant immediately, in addition to any Exploration Event rewards (see `Artifacts.md`).

---

### Movement & Arcane Whispers (4)

#### Forced March

- **Timing:** WHEN you take a Move action (before resolving movement).
- **Effect:** Your moving group's **Movement Range** is increased by **+1 hex** for this Move action. (AP costs are still paid normally for the extra hex.)

#### Blink

- **Timing:** WHEN you take a Move action (before resolving movement).
- **Effect:** Choose **one unit** in your moving group. Instead of moving with the group, that unit is immediately placed in any **controlled City** you own. The rest of the group moves normally.

#### Ley Line Surge

- **Timing:** ACTION
- **Effect:** Gain **2 Mana**. The next Research action you take this round costs **0 AP** (you still pay the discovery's resource cost).

#### Waystone Activation

- **Timing:** WHEN you use Portal travel.
- **Effect:** You may travel to a Portal **controlled by another player** this one time, ignoring the normal permission restriction. (You still pay normal Portal entry/exit AP costs.)

---

### Subterfuge Whispers (3)

#### Saboteur

- **Timing:** ACTION
- **Effect:** Choose an enemy **building** on a hex **adjacent to one you control**. That building is **disabled** until end of next round. (It produces no resources, grants no bonuses, and does not count as existing for objectives. It is not destroyed and returns to normal when the effect expires.)

#### Mercenary Company

- **Timing:** ACTION
- **Effect:** Place **2 Infantry** in any **neutral hex adjacent to territory you control**. You gain control of that hex. (Each Infantry placed requires 1 available Population.)

#### Relic Thief

- **Timing:** WHEN another player claims an artifact from an Artifact Site.
- **Effect:** Cancel their claim. You claim the artifact instead. You must have a unit in an adjacent hex (see `Artifacts.md`).

---

## Design Notes

### Why "Whispers"?

The Speaking Stones are one of Aeonis's defining lore elements -- ancient artifacts that let lords spy, communicate, and scheme across vast distances. Whisper Cards represent what those Stones make possible: advance intelligence, secret orders delivered through stone networks, agents positioned before anyone knew to look, and political machinations arranged in murmured conference. When you play a Whisper, you're acting on something your Stones heard before the rest of the realm caught on.

### Balance Principles

- **Combat Whispers** are powerful but narrow: they require you to be in a battle and often require specific units (Cavalry, Archers). They reward players who build diverse armies.
- **Political Whispers** are high-impact but costly in opportunity: Sabotage, Veto, and Backroom Deal are all cards you want to hold "just in case," creating hand-management tension.
- **Economic Whispers** are reliable but modest: they smooth out resource droughts and reward opportunistic play.
- **Movement/Arcane Whispers** enable surprise plays: Blink and Forced March let you reposition in ways opponents didn't expect.
- **Subterfuge Whispers** are the "mean" cards: Saboteur hurts an opponent's engine, Mercenary Company steals territory. They are deliberately few in number so they don't dominate the feel of the game.

### Scaling for Full Game

The First Playable deck is 26 cards. For the full game (and higher player counts), expand to **40-60 cards** by:

- Adding duplicates of core cards (2x Sabotage, 2x Shield Wall, 2x Hidden Cache).
- Introducing Lord-specific Whispers (1-2 per faction that synergize with their abilities).
- Adding higher-tier combat Whispers that reference advanced units or Arcane Discoveries.
- Adding more Subterfuge options for deeper political play.

### Interaction with Other Systems

- **Renown**: consider granting +1 Whisper draw at 5 Renown and 10 Renown thresholds (in addition to the AP bonuses).
- **Strategy Cards**: the secondary ability of certain Strategy Cards could grant Whisper draws (e.g., "whenever another player plays a Whisper this round, draw 1 Whisper").
- **Arcane Discoveries**: Tier II/III discoveries could grant Whisper-like effects that are permanent or repeatable, replacing the one-shot nature of cards.
