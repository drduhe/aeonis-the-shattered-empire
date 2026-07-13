# Aeonis: High Council

The **High Council** is the game’s political arena: players propose motions, negotiate, vote, and enact realm-wide rules and rewards. Many other systems (movement restrictions, borders, titles, AP boosts, taxes) reference “High Council decrees”; this chapter defines the procedure and timing for those effects.

This phase occurs during **Step 4: High Council Phase** of `Round_Structure.md`.

---

## Components and Terms

- **Speaker**: the player who runs the agenda, breaks certain ties, and sets proposal order when needed.
- **Motion**: a proposal placed before the council to be voted on.
- **Decree**: a one-time effect that resolves immediately when passed.
- **Law**: a persistent rule that stays in effect until repealed.
- **Title**: a named distinction that grants VP and/or bonuses while held.
- **Influence**: a resource used to propose, lobby, annex, and pay certain political costs.
- **Agenda deck**: a deck of pre-written motions revealed by the Speaker each round (see §3.2a).

---

## 1. Speaker (who has it and how it moves)

Default rule:

- **First round**: randomly determine the Speaker.
- **Each new round**: the Speaker token passes **clockwise** during Cleanup & Checks (see `Round_Structure.md`, step 7).

Exception (canon):

- The **Diplomatic Decree** Strategy Card transfers the Speaker token to its owner as part of its primary (see `Strategy.md`).

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

### 2.4 Auriel — The Tree's Assent

Once per round during the High Council Phase, when Auriel casts her vote and before votes are tallied, she may sanctify that motion. Her Council Votes and Lobbying votes count double on that motion. Whenever a motion Auriel supported passes, she gains +1 Renown; if it was sanctified, she gains +2 Renown instead. Sanctify changes only Auriel's votes and does not multiply table-wide modifiers or votes supplied by another player.

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

### 3.2b The Docket (PROPOSED — Plan 4; not canon)

> **Status:** PROPOSED. Current §3.2 / §3.2a remain in force until this is playtested and registered under Design decisions in `INDEX.md`. See `../docs/plans/2026-07-02-plan-high-player-count.md`.

Replace open proposal with a fixed-size **docket** so council length stays roughly constant from 3–8 players:

1. **Agenda-deck reveal (always on the docket).** The Speaker reveals the top agenda card; it is **always voted on** this phase (no longer optional to propose). Free-propose effects become **docket-jump** effects: “add your motion to the docket without bidding.”
2. **Player motion slot(s).** During the proposal window, each player may **bid Influence** (secret simultaneous bid, or open ascending — both allowed pending playtest) to place a motion on the docket. Highest bid pays and proposes; ties broken by the Speaker. Losing bids are returned.
   - **3–5 players:** docket may hold **two** player motions (bid winner and runner-up, each paying their own bid).
   - **6–8 players:** docket holds **one** player motion (bid winner only).
3. **Deleted:** the flat **1 Influence** proposal cost (the bid replaces it).

Phase target: High Council ≤ **15 minutes** at 8 players.

### 3.2a Agenda deck (canonical rules)

The **agenda deck** gives the council drawn content in addition to player-authored motions.

- After all proposals are placed (§3.2), the **Speaker reveals the top card** of the agenda deck.
- Any player may propose **that** motion **for free** this round (no proposal Influence cost). This does **not** count against the one-motion-per-player limit.
- If no player proposes it, the revealed card is discarded at end of phase.
- Effects that interact with the agenda deck (e.g., **Scrying Pool** in `Arcane.md`, **Leaked Intelligence** in `Whispers.md`) refer to this deck.
- The First Playable agenda deck list lives in `../playtest/First_Playable_Packet.md` (section 5).

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
  - VP: 2 VP when first claimed.

- **Magister of Mana (Title)**:
  - Eligibility: Control 3 Mana-producing hexes (Forests/Groves) at Cleanup.
  - Benefit: Once per round, reduce the Mana cost of a Research action or Ritual by 1.
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

## 6a. Full Agenda Deck (20 cards)

This section defines the complete **agenda deck** for full games: 20 pre-written motions revealed by the Speaker per §3.2a. The First Playable subset (8 cards) is listed in `../playtest/First_Playable_Packet.md` (section 5); those 8 cards appear here unchanged.

Definitions:

- **Election**: a motion subtype in which the council votes **for a player** instead of yes/no; the elected player receives the card's effect. Defined in §6a.1. Elections exist only as agenda cards in this section; no other chapter needs to change.

### 6a.1 Election motions (new subtype)

An **Election** is a motion subtype: the card names an effect, and the council votes **for a player** instead of yes/no. Resolve an Election using the §3.4 procedure with one change to step 2: in **initiative order** (the same order used for Lobbying, §2.3), each player must either declare one **candidate** (any player, including themselves) and commit votes to that candidate, or abstain. A player's Council Votes (base + Renown, see §2) and any Lobbying votes (§2.3, purchased at the normal rate of 2 Influence = +1 vote, for this motion only) must all support the same single candidate; votes may not be split between candidates. At Enactment (§3.5), the candidate with the most committed votes is **elected** and receives the card's effect; the Speaker must break ties by choosing one of the tied candidates. An Election does not "pass" or "fail": if at least 1 vote is committed, a player is elected; if no votes are committed, the card is discarded with no effect.

### 6a.2 Deck handling and resolution notes

- **Setup**: shuffle all 20 cards into one face-down agenda deck. Reveal per §3.2a each round.
- **Free proposal scope**: proposing a revealed agenda card for free (§3.2a) waives only the 1 Influence **proposal** cost. Costs written on the motion itself (e.g., Imperial Annexation's 5 Influence) must still be paid by the proposer.
- **Title recipients**: when proposing a Title card, the proposer must name the intended recipient (any player, including themselves). If the motion passes, the Title is awarded only if the named player meets the Title's Eligibility at Enactment; otherwise the motion has no effect and the card is discarded.
- **Discards**: Decrees and Elections are discarded after resolving. A passed Law card stays on the table until repealed (§5.3), then is discarded. A Title card stays with its holder; if the holder fails the Cleanup check (§5.2), discard the card.
- **Empty deck**: if the agenda deck is empty at the reveal step, shuffle the agenda discard pile to form a new deck; if both are empty, skip the reveal this round.
- **Illegal cards**: some cards below state a condition under which they "may not be proposed." If a revealed card may not be proposed, it is discarded at end of phase per §3.2a.

### 6a.3 The 20 cards

Cards 1-8 are the First Playable core; cards 9-20 are full-game additions.

#### First Playable core (8 cards)

- **1. Road Networks (Law)** — as defined in §6.1.

- **2. Demilitarized Zone (Decree)** — as defined in §6.1.

- **3. Open Borders Treaty (Decree)** — as defined in §6.1.

- **4. Imperial Annexation (Decree)** — as defined in §6.4.

- **5. Border Arbitration (Decree)** — as defined in §6.4.

- **6. Realm Tax (Law)** — as defined in §6.2.

- **7. Hero of the Realm (Title)**:
  - Eligibility: **5 or more Renown** (see `Renown.md`).
  - Effect: The holder gains **2 VP** the first time they claim this Title (the VP are kept even if the Title is later lost; see `Victory.md`). While holding this Title, the holder gains **1 Influence** during each Production & Upkeep Phase.
  - Check timing: **Cleanup & Checks** each round.
  - Loss condition: if the holder has fewer than 5 Renown at the check, they must discard the Title.
  - Note: the agenda deck commits to the "2 VP when first claimed" scoring model from §6.3.

- **8. Magister of Mana (Title)**:
  - Eligibility: control **3 or more Mana-producing hexes** (Forests and/or Groves; see `Tiles.md`).
  - Effect: The holder gains **2 VP** the first time they claim this Title (kept if the Title is later lost). While holding this Title, once per round, when the holder takes a Research action or activates a Ritual, they may reduce its Mana cost by **1** (minimum 0; see `Arcane.md`).
  - Check timing: **Cleanup & Checks** each round.
  - Loss condition: if the holder controls fewer than 3 Mana-producing hexes at the check, they must discard the Title.

#### New Laws (4 cards)

- **9. Muster Rolls (Law)**:
  - Effect: When a player takes a **Recruit** action (see `Actions.md`), they may place up to **3 units** in the chosen City instead of 2. All other Recruit rules (costs, Population, once-per-City-per-round) are unchanged.
  - Duration: until repealed.

- **10. Silence of the Stones (Law)**:
  - Effect: During **Cleanup & Checks**, the Whisper hand limit is **5** instead of 7; players with more than 5 Whisper Cards must discard down to 5 (their choice; see `Whispers.md` and `Round_Structure.md`, step 7).
  - Duration: until repealed.

- **11. Arcane Endowment (Law)**:
  - Effect: The **first Research action** each player takes each round costs **1 less Mana** (minimum 0). AP costs are unchanged (see `Arcane.md`).
  - Duration: until repealed.

- **12. Standing Army Tithe (Law)**:
  - Effect: During each **Production & Upkeep Phase** (upkeep step), each player with **8 or more military units** (Infantry/Cavalry/Archers; Lords do not count) on the map must pay **1 Gold**. A player who cannot pay must instead remove 1 of their military units (their choice).
  - Duration: until repealed.

#### New Decrees (4 cards)

- **13. War Reparations (Decree)**:
  - Target: the proposer must name one player who won a battle **as the attacker during the previous round**, and the player who defended in that battle. If no player qualifies, this card may not be proposed.
  - Effect: On enactment, the named attacker must pay **2 Gold** to the named defender. If they have fewer than 2 Gold, they must pay all the Gold they have and lose **1 Renown**.
  - Duration: resolves immediately.

- **14. Imperial Excavation (Decree)**:
  - Effect: On enactment, the proposer must place an **Artifact Site marker** on a **neutral Ruins hex** of their choice (if there is none, on any neutral hex of their choice). Draw the top card of the Artifact Deck and place it face-up on the marker (see `Artifacts.md`). The site is claimable by **any** player per the normal Artifact Site rules (1 AP, unit on the hex).
  - Duration: resolves immediately (the site persists until claimed).
  - Resolution note: if the Artifact Deck is empty, this card may not be proposed.

- **15. General Amnesty (Decree)**:
  - Effect: This round, captured Lords are released **early**: at the **end of the Action Phase** (before the Production & Upkeep Phase), every captured Lord returns to its owner's Home City at full HP and its abilities are restored (instead of waiting for Cleanup & Checks; see `Combat.md` and `Round_Structure.md`, step 7). VP and Renown already gained from captures are unaffected.
  - Duration: until end of round.

- **16. Imperial Census (Decree)**:
  - Effect: On enactment, count each player's Influence **simultaneously** (snapshot before any payments). Each player counted at **5 or more Influence** must pay **2 Influence** to the supply. Then each player counted at **1 or fewer Influence** gains **1 Influence** from the supply.
  - Duration: resolves immediately.

#### New Titles (2 cards)

- **17. Grand Marshal (Title)**:
  - Eligibility: have **8 or more military units** (Infantry/Cavalry/Archers; Lords do not count) on the map.
  - Effect: The holder gains **2 VP** the first time they claim this Title (kept if the Title is later lost). While holding this Title, once per round, when the holder takes an **Attack** action, they may reduce its AP cost by **1** (from 2 AP to 1 AP; the optional Press the Attack surcharge is unchanged; see `Combat.md` and `Actions.md`).
  - Check timing: **Cleanup & Checks** each round.
  - Loss condition: if the holder has fewer than 8 military units on the map at the check, they must discard the Title.

- **18. Keeper of Relics (Title)**:
  - Eligibility: own **2 or more Artifact Cards** (any category; see `Artifacts.md`).
  - Effect: The holder gains **2 VP** the first time they claim this Title (kept if the Title is later lost). While holding this Title, the holder gains **1 Remnant** during each Production & Upkeep Phase (in addition to Remnants from Ruins hexes).
  - Check timing: **Cleanup & Checks** each round.
  - Loss condition: if the holder owns fewer than 2 Artifact Cards at the check, they must discard the Title.

#### Elections (2 cards)

- **19. Warden of the Seat (Election)**:
  - Effect: Until the **end of the next round**, players other than the elected player must not declare an **Attack** action targeting the **Imperial Seat** hex while the elected player controls it or has units in it (see `Combat.md`, `Tiles.md`).
  - Duration: until end of next round.
  - Resolution notes: this does not restrict attacks on any other hex, and does not itself grant or change control of the Imperial Seat. An ongoing siege of the Imperial Seat against the elected player may not be continued (no Attack actions may be spent on it) while the protection lasts.

- **20. Realm Treasurer (Election)**:
  - Effect: On enactment, the elected player immediately collects **1 Gold from each other player**. A player with 0 Gold pays nothing (no substitute cost).
  - Duration: resolves immediately.

### 6a.4 Balance intent (why these numbers)

- **Muster Rolls** adds one unit per Recruit action because Gold, Population, and the once-per-City limit still cap totals; it favors wide, multi-City play.
- **Silence of the Stones** (limit 5) trims Whisper hoarding for combo turns without touching the 2-per-round draw rate.
- **Arcane Endowment** (−1 Mana, first Research only) roughly halves the Tier I default cost (2 Mana) once per round without discounting deep Tier II/III chains.
- **Standing Army Tithe** and **Grand Marshal** share the **8-unit** threshold deliberately: the tax and the title tug at the same militarized players (default starting armies are 4 units, so 8 is a real commitment against a 10 Population cap).
- **Imperial Census** thresholds (pay at 5+, gain at ≤1) compress Influence extremes without zeroing anyone out; **War Reparations**' 2 Gold mirrors War Levy (§6.2).
- **Keeper of Relics** requires 2 artifacts — roughly 6 Remnants of effort or two contested Artifact Site claims — so it rewards sustained exploration, not one lucky draw.

---

## 7. Design Notes (why these defaults exist)

- The council is meant to be **frequent but bounded**: one proposal per player keeps it impactful without turning every round into a pure negotiation game.
- Renown grants legitimacy (votes), while Influence remains a flexible currency (lobbying + annexation), creating two distinct “political powers.”

