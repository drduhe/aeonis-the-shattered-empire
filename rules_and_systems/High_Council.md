# Aeonis: High Council

The **High Council** is the game’s political arena: players propose motions, negotiate, vote, and enact realm-wide rules and rewards. Many other systems (movement restrictions, borders, titles, AP boosts, taxes) reference “High Council decrees”; this chapter defines the procedure and timing for those effects.

This phase occurs during **Step 3: High Council Phase** of `Round_Structure.md`.

---

## Components and Terms

- **Speaker**: the player who runs the agenda, breaks certain ties, and sets proposal order when needed.
- **Motion**: a proposal placed before the council to be voted on.
- **Decree**: a one-time effect that resolves immediately when passed.
- **Law**: a persistent rule that stays in effect until repealed.
- **Title**: a named distinction that grants VP and/or bonuses while held.
- **Influence**: a resource used to propose, lobby, annex, and pay certain political costs. (Some older text may call this “IP”; treat them as the same resource.)

---

## 1. Speaker (who has it and how it moves)

Default rule:

- **First round**: randomly determine the Speaker.
- **Each new round**: the Speaker passes clockwise (or to the next player in initiative order—pick one method and keep it consistent).

Optional rule (TI4-like):

- A specific Strategy Card (e.g., “Diplomatic Decree”) grants or transfers the Speaker token as part of its primary.

The Speaker’s responsibilities:

- Maintain the agenda order.
- Ensure motions are legal and clearly stated.
- Break ties when a rule says “Speaker breaks ties.”

---

## 2. Council Votes (how voting power works)

Each player has **Council Votes** during the High Council Phase.

### 2.1 Base votes

- **Base**: 1 vote per player.

### 2.2 Renown bonus votes

Renown represents legitimacy and sway.

- **+1 vote** if you have **5+ Renown**
- **+1 additional vote** if you have **10+ Renown**

(If you later add more Renown tiers, extend this pattern as desired.)

### 2.3 Lobbying (spending Influence to add votes on one motion)

When a motion is called to a vote, players may lobby:

- In **initiative order**, each player may spend Influence to gain temporary votes **for this motion only**.
- **Rate**: 2 Influence = +1 vote (round down; minimum spend 2).
- Lobby votes are added to your Council Votes for this motion, then discarded.

Note: This creates a sink for Influence without making every vote purely “wallet wins.”

---

## 3. High Council Phase Procedure

### 3.1 Agenda opens

1. Reveal any **Council-only** events or agenda items (if used).
2. Identify the **proposal order** (default: initiative order; Speaker breaks ties).

### 3.2 Proposal window (placing motions on the agenda)

In proposal order, each player may do **one** of the following:

- **Propose** one motion, or
- **Pass** (you do not propose this round)

Proposal cost (default):

- To propose a motion, pay **1 Influence**.

Hard limit:

- Maximum **one motion proposed per player per round**.
- The agenda may contain at most **(#players)** motions (because of the limit above).

### 3.3 Negotiation window

Before voting on each motion, allow table negotiation.

Scope:

- **Promises** (future support, non-aggression, “I’ll vote yes if…”) are always allowed.
- **Resource transfers** follow the trade rules:
  - If you want trading to remain an AP-costed action, then treat resource transfers here as *promises* to trade later.
  - If you want the council to allow “instant deals,” add a house rule: “During the High Council, players may exchange resources without spending AP.”

### 3.4 Voting

Resolve motions one at a time, in the order proposed.

1. Restate the motion clearly (including duration and scope).
2. Each player declares how many votes they are committing:
   - Their **Council Votes** (base + Renown), plus any **Lobbying** votes purchased with Influence.
3. Tally votes:
   - **Passes** on a strict majority of votes cast (ties fail).
   - **Tie-break** (optional): if tied, the **Speaker breaks ties**.

### 3.5 Enactment

Apply the results immediately:

- **Decrees** resolve now and are then discarded.
- **Laws** enter play and persist until repealed.
- **Titles** are awarded immediately (and can be stolen/removed only by rules that say so).

---

## 4. Motion Legality Rules

A motion is legal if:

- It is **clearly stated** (what changes, where, for how long).
- It does not contradict a **hard rule** (unless your table allows constitutional override motions).
- It names an enforcement condition when needed (e.g., “until end of round,” “for 2 rounds,” “until repealed”).

Recommended motion categories:

- **Border / Movement**
- **Economy / Taxes**
- **Military / Security**
- **Titles / Prestige**
- **Emergency / Crisis** (reactive)

---

## 5. Enforcement and Duration

### 5.1 Duration defaults

If a motion does not specify duration, use these defaults:

- **Decree**: resolves immediately and ends.
- **Law**: persists until repealed.
- **Title**: persists while its conditions are maintained (see below).

### 5.2 Title maintenance

Titles should specify:

- **Eligibility**: what you must control/achieve.
- **Check timing**: when eligibility is checked (recommended: **Cleanup & Checks** each round).
- **Loss condition**: if you are not eligible at check time, you lose the title.

### 5.3 Repealing laws

Any player may propose **Repeal [Law Name]** as their motion. If it passes, remove the law immediately.

---

## 6. Example Motions (ready-to-play)

Use these as templates; tune numbers during playtests.

### 6.1 Border / Movement

- **Road Networks (Law)**:
  - Effect: Movement across **Plains** costs 1 less AP (minimum 1).
  - Duration: until repealed.

- **Demilitarized Zone (Decree)**:
  - Choose a named region or 3 connected hexes.
  - Effect: No player may initiate attacks into the zone until end of round.

- **Open Borders Treaty (Decree)**:
  - Name two players.
  - Effect: Those players may move through each other’s controlled hexes this round without paying the “enter enemy ZOC” surcharge (if used).

### 6.2 Economy / Taxes

- **Realm Tax (Law)**:
  - Effect: Each round, each player gains +1 Gold but must pay 1 Influence (or lose 1 Renown).
  - Duration: until repealed.

- **War Levy (Decree)**:
  - Effect: The player with the most controlled Cities must pay 2 Gold; that Gold is split among all other players (rounding down).

### 6.3 Titles / Prestige

- **Hero of the Realm (Title)**:
  - Eligibility: 5+ Renown.
  - Benefit: +1 Influence per round while held.
  - VP: 2 VP when first claimed (or 1 VP per round held—pick one scoring model).

- **Magister of Mana (Title)**:
  - Eligibility: Control 3 Mana-producing hexes (Forests/Groves) at Cleanup.
  - Benefit: Once per round, reduce the Mana cost of a spell or discovery by 1.
  - VP: 2 VP when first claimed.

### 6.4 Annexation / Disputes

- **Imperial Annexation (Decree)**:
  - Cost: proposer pays 5 Influence.
  - Target: one neutral hex adjacent to the proposer’s controlled territory.
  - Effect: proposer claims control of that hex immediately (subject to any exploration rules if it was unrevealed).

- **Border Arbitration (Decree)**:
  - Name a contested border hex between two players.
  - Effect: both players commit up to 4 Influence; high spender wins control (ties: Speaker chooses). Spent Influence is discarded.

---

## 7. Design Notes (why these defaults exist)

- The council is meant to be **frequent but bounded**: one proposal per player keeps it impactful without turning every round into a pure negotiation game.
- Renown grants legitimacy (votes), while Influence remains a flexible currency (lobbying + annexation), creating two distinct “political powers.”

