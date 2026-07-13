# Aeonis: Objectives

This chapter is the **owning rules reference** for the objective system: how objective cards are drawn, held, verified, and scored, plus the full card lists for the Public deck (Stage I and Stage II) and the Secret deck.

- **VP context**: objectives are one VP source among several — see `Victory.md`.
- **Timing spine**: scoring happens at **Cleanup & Checks** unless a card says otherwise — see `Round_Structure.md`, phase 7.
- **First Playable**: the playtest packet prints a reduced 6 public + 6 secret set (see `../playtest/First_Playable_Packet.md`, section 4.4). Those cards appear in the full decks below unchanged in effect.

---

## 1. Overview & Definitions

### 1.1 How objectives work

- Each objective card is worth **2 VP** (public and secret alike; see `Victory.md`).
- **Public Objectives** form one **shared revealed row**. Every player may score each revealed card once; place one of your control markers on the card when you score it.
- **Secret Objectives** are drawn from the secret deck and kept **hidden** from other players until scored.
- An objective is **scored** when its condition is **verified at Cleanup & Checks**, unless the card says otherwise (see 1.3).
- A scored public objective stays in the shared row so other players may score it; your marker proves you cannot score it again. A scored secret objective stays face-up near your VP track as a score record. **Each objective scores once per player** and grants no ongoing effect.
- Whenever you score an objective, you score VP — this triggers the standard "draw 1 Whisper Card when you score VP" rule (see `Whispers.md`).

### 1.2 Definitions

- **Public deck**: a 24-card deck of public objectives, split into **Stage I** (12 cards) and **Stage II** (12 cards). Revealed cards form the shared public row. See section 2.
- **Secret deck**: a 20-card deck of secret objectives. See section 2.
- **Unscored objective**: a revealed public card without your control marker, or a secret objective you hold that you have not scored.
- **Progress marker**: one of your control markers placed beside a cumulative objective to track your progress (e.g., "win 2 battles"). Public-objective progress begins when that card is revealed; earlier events never count. Secret-objective progress begins when you draw the card. For secrets, markers sit on the face-down card — opponents may see the count, but not the condition.
- **Hex distance**: the smallest number of hex-to-hex steps between two hexes, counted across adjacent hexes on the map (including Lakes and hexes any player controls). Terrain costs, ZOC, and passability are ignored — hex distance measures the map, not movement (see `Movement.md` for movement costs, which are unrelated).
- **Winning a battle**: you win a battle when its Aftermath resolves in your favor (see `Combat.md`, section 5):
  - As **attacker**: the defender's committed units are eliminated and you gain control of the target hex (`Combat.md` §5.1).
  - As **defender**: the attacker retreats or is eliminated (`Combat.md` §5.2).
  - **Sieges**: the attacker wins by Siege victory (`Combat.md` §6.5); the defender wins when the siege ends with the defender still controlling the hex (the attacker lifts the siege, loses adjacency, or is eliminated).
  - A battle that merely **pauses** (both sides still have committed units and the Attack action ends) has no winner yet.
- **Control**, **own**, **in play**: control of hexes follows `Tiles.md`. A building is "in play" if it is on the map and on a hex you control. A unit is "in play" if it is on the map. You "own" a card, artifact, or discovery if it is currently in your play area or attached to your pieces per its own rules.

### 1.3 Scoring windows and resolution order

- **Default window**: objectives are verified during **Cleanup & Checks**, as part of the **Victory checks** step (`Round_Structure.md`, phase 7, step 5), **before** the VP-threshold check.
  - In **initiative order**, each player may score **at most 1 public objective**, then any number of eligible secret objectives (reveal secrets as you score them).
- **Immediate window**: a card marked **"Scoring window: Immediate"** may instead be scored at the **moment its condition is verified**, during any phase (reveal it, score 2 VP, discard it). If you do not score it immediately, you may still score it at any later moment the condition is verified again.
- **Cumulative conditions**: cards that count events over time (marked with a **Tracking** line) are verified by player-colored progress markers. Public cards count only events after reveal; secret cards count only events after draw. The markers are the tracking method — no memory-dependent claims are allowed.
- **Conditions must hold when checked**: for state-based conditions ("control 7 hexes"), the condition must be true at the moment of verification. There is no credit for having met it earlier in the round.

---

## 2. Deck Structure

### 2.1 Public deck (24 cards: Stage I + Stage II)

- **Stage I (12 cards)**: objectives tuned to be achievable by rounds 1–4.
- **Stage II (12 cards)**: harder objectives tuned for the mid and late game.

**Shared-row setup and staging (default rule):**

1. During setup, shuffle the Stage I cards and the Stage II cards into **two separate face-down decks**.
2. Reveal **2 Stage I cards** to form the opening shared public row.
3. At each **Round Start from Round 2**, reveal 1 public objective. Draw from Stage I through the end of Round 3.
4. At **Round Start of Round 4**, shuffle the Stage II deck together with the remaining Stage I deck to form a **single public deck**, then reveal that round's card. All later reveals come from this combined deck.
5. **Exception**: if the Stage I deck is empty before Round 4, shuffle the Stage II deck in immediately.

*Why Round 4:* Stage I is tuned to be achievable by rounds 1–4; folding Stage II in at Round 4 means mid/late-game draws scale with board development instead of handing a fresh player an unreachable goal.

**Variant — Early Escalation:** shuffle Stage I and Stage II together at setup. Higher variance; recommended only for experienced groups.

### 2.2 Secret deck (20 cards)

- Shuffle all 20 secret objectives into a single face-down deck during setup.
- Discarded secret objectives go to a **face-down discard pile**. If the secret deck empties, shuffle the discard pile to form a new deck.
- Public objectives are not discarded after scoring; revealed cards remain in the shared row for the rest of the game.

---

## 3. Draw and Hand Rules

### 3.1 Starting draws

- During setup, each player draws **1 secret objective** and keeps it hidden. The opening 2 public objectives are revealed to the shared row per section 2.1.

### 3.2 Round 3 secret draw

- At **Round Start of Round 3**, each player draws **1 additional secret objective** (per the First Playable packet, section 4.4).

### 3.3 Secret objective cap

- A player may hold **at most 3 unscored secret objectives**.
- **Drawing at the cap**: if an effect lets you draw a secret objective while you already hold 3 unscored secrets, instead **draw 2 cards** from the secret deck, **choose up to 1 to keep, and discard the rest** face-down. If you keep one, you **must** immediately discard one of your other unscored secret objectives face-down (your choice), so that you never hold more than 3.

*Why 3:* the cap limits outstanding hidden VP to 6 (of the 10 VP threshold), preventing hidden blowouts — consistent with the "secret objectives are 2 VP" design decision in `INDEX.md`. The draw-2-keep-1 rule keeps draw effects (e.g., the **Winds of Fortune** event) valuable at the cap by offering selection instead of raw cards.

### 3.4 Additional public reveals

- Whenever an effect lets you draw a public objective (e.g., **Winds of Fortune**, see `First_Playable_Packet.md` section 4.5), reveal the next card from the current public deck into the shared row. It is available to every player immediately but can be scored only at its stated window.
- There is no row-size cap; public objectives remain open information.

---

## 4. Objective Cards

Every card below is worth **2 VP** and uses the **default scoring window (Cleanup & Checks)** unless a **Scoring window** line says otherwise. Cards with a **Tracking** line have cumulative conditions — track them with progress markers as defined in 1.2.

### 4.1 Stage I Public Objectives (12)

#### Frontier Lord

- **Category:** Territory
- **Condition:** Control 7 hexes.
- **Clarifications:** Every hex you control counts (see `Tiles.md` for control rules), including your starting home cluster and bridged Lake hexes.

#### Builder

- **Category:** Economy
- **Condition:** Have 3 buildings in play.
- **Clarifications:** Buildings of any type count (production, military/defensive, advanced, Legendary, Bridge), whether built or captured, as long as they are on hexes you control.

#### Council Power

- **Category:** Politics
- **Condition:** Spend 4 total Influence lobbying on motions that pass.
- **Clarifications:** Count only Influence you spend during the High Council Phase on a **For** vote whose motion passes (see `High_Council.md` §2.3 and §3.4–3.5). The 4 Influence may be split across multiple motions.
- **Tracking:** After this card is revealed, place that many of your control markers beside it whenever your qualifying motion passes.

#### Portal Mastery

- **Category:** Exploration
- **Condition:** Control a Portal and use Portal travel at least once.
- **Clarifications:** Portal control follows `Tiles.md` (occupy it at the start of your turn, or have your Tower on it). Portal travel is the Portal-to-Portal move defined in `Movement.md` §4. Both parts must be satisfied when checked: a travel marker earned after this card was revealed, plus current Portal control.
- **Tracking:** After this card is revealed, place your control marker beside it the first time you use Portal travel.

#### Warlord

- **Category:** Military
- **Condition:** Win 2 battles (attacker or defender).
- **Clarifications:** Uses the "Winning a battle" definition in section 1.2.
- **Tracking:** After this card is revealed, place your control marker beside it each time you win a battle.

#### Seat of Empire

- **Category:** Territory
- **Condition:** Control the Imperial Seat at Cleanup & Checks.
- **Clarifications:** This is separate from, and in addition to, the Imperial Seat's **Coronation Rite** (see `Victory.md` and `First_Playable_Packet.md` §3.2).

#### Twin Cities

- **Category:** Military / Territory
- **Condition:** Control 2 Cities.
- **Clarifications:** The Imperial Seat counts as a City. Your Home City counts. Captured enemy Home Cities count.

#### Adept of the Schools

- **Category:** Arcane
- **Condition:** Own 2 Arcane Discoveries.
- **Clarifications:** Any schools and tiers count (see `Arcane.md`). School Specialties are not Discoveries and do not count.

#### Voice of the Realm

- **Category:** Politics
- **Condition:** Have 5 or more Renown.
- **Clarifications:** Read directly from the Renown track (see `Renown.md`). If the optional Renown Decay rule is used, you must hold 5+ when checked.

#### Relic Seeker

- **Category:** Exploration
- **Condition:** Own an Artifact.
- **Clarifications:** Any category counts (Lord Equipment, Building Relic, or Utility; see `Artifacts.md`) as long as you control it when checked. Remnants are not Artifacts.

#### Merchant Lord

- **Category:** Economy
- **Condition:** Have 8 or more Gold.
- **Clarifications:** Read directly from your Gold stock at Cleanup & Checks. This is separate from, and may be scored in addition to, the secret objective **Golden Hoard** (10 Gold, Immediate window).

#### Standing Army

- **Category:** Military
- **Condition:** Have 8 military units in play.
- **Clarifications:** Infantry, Cavalry, and Archers on the map count. Your Lord does not count.

### 4.2 Stage II Public Objectives (12)

#### Dominion

- **Category:** Territory
- **Condition:** Control 12 hexes.
- **Clarifications:** As **Frontier Lord**, at a mid/late-game scale.

#### Prosperous Realm

- **Category:** Economy / Growth
- **Condition:** Have 5 buildings in play and a Population Cap of 12 or more.
- **Clarifications:** Buildings of any type count while they are on hexes you control. Read Population Cap from your player board (see `Population.md`). This replaces **Master of Cities**, which required capturing an enemy Home City at most player counts and recorded no scores at 4p/6p in the first two audit ladders.

#### Living Legend

- **Category:** Economy
- **Condition:** Have your Legendary Building in play, in a City you control.
- **Clarifications:** "Your" Legendary Building is the faction capstone on your Lord Sheet (see `Buildings.md`). If the City containing it has been captured, you do not meet this condition (the captor may have scored **1 VP once** for the capture, but cannot score this card — it is not their Legendary Building).

#### Crossroads of Empire

- **Category:** Exploration / Territory
- **Condition:** Control 4 special tiles.
- **Clarifications:** Cities, Ruins, Portals, and the Imperial Seat are special tiles. The Imperial Seat counts once, not once as the Seat and again as a City. This replaces **Heir of Aeonis** so the objective deck does not stack another scoring reward onto the Coronation Rite.

#### Archmage

- **Category:** Arcane
- **Condition:** Own 4 Arcane Discoveries, including at least 1 of Tier II or higher.
- **Clarifications:** See `Arcane.md`. School Specialties do not count. **Not usable** with the First Playable arcane module (Tier I only) — see section 5.3.

#### Breaker of Walls

- **Category:** Military
- **Condition:** Win a Siege as the attacker.
- **Clarifications:** You must capture a hex that was under a Siege marker (a Fortress hex, or a City whose defender declared Hold the Walls; see `Combat.md` §6.5).
- **Tracking:** After this card is revealed, place your control marker beside it when you win a Siege.

#### Conqueror

- **Category:** Military
- **Condition:** Win 5 battles (attacker or defender).
- **Clarifications:** Uses the "Winning a battle" definition in section 1.2.
- **Tracking:** After this card is revealed, place your control marker beside it each time you win a battle.

#### Hold the Line

- **Category:** Military
- **Condition:** Win 2 battles as the defender.
- **Clarifications:** Uses the defender victory definition in section 1.2. The wins may occur in the same or different hexes.
- **Tracking:** After this card is revealed, place your control marker beside it each time you win as the defender. This replaces **Kingslayer** so Lord capture does not bundle objective VP with its existing VP, Renown, equipment-transfer, and ability-lockout rewards.

#### Lawgiver

- **Category:** Politics
- **Condition:** Support 2 Laws that pass.
- **Clarifications:** Laws only (not Decrees or Titles; see `High_Council.md`). You must cast a **For** vote on each qualifying Law during the High Council Phase.
- **Tracking:** After this card is revealed, place your control marker beside it whenever a Law you supported passes. This remains achievable when the proposed Plan 4 Docket limits who may propose.

#### Beacon of Renown

- **Category:** Politics
- **Condition:** Have 10 or more Renown.
- **Clarifications:** Read directly from the Renown track (see `Renown.md`).

#### Imperial Treasury

- **Category:** Economy
- **Condition:** Have 20 or more total resources (Gold + Mana + Influence combined) at Cleanup & Checks.
- **Clarifications:** Counted at the same moment as the Renown surplus check in `Renown.md` (which grants +1 Renown per 10 total resources held at Cleanup & Checks); both apply.

#### Reliquary

- **Category:** Exploration
- **Condition:** Own 3 Artifacts.
- **Clarifications:** Any mix of categories (see `Artifacts.md`); all three must be under your control when checked.

### 4.3 Secret Objectives (20)

#### Hidden Arsenal

- **Category:** Military
- **Condition:** Build a Fortress and win a battle involving that hex.
- **Clarifications:** You must have built the Fortress yourself. The battle's target hex must be the Fortress hex; winning as attacker or defender both count (uses the "Winning a battle" definition in section 1.2).
- **Tracking:** Place a progress marker on this card when you win a qualifying battle.

#### Golden Hoard

- **Category:** Economy
- **Condition:** Have 10 Gold at once.
- **Scoring window:** Immediate — you may reveal and score this card at the moment you have 10 or more Gold, during any phase.

#### Mana Flood

- **Category:** Economy
- **Condition:** Have 10 Mana at once.
- **Scoring window:** Immediate — you may reveal and score this card at the moment you have 10 or more Mana, during any phase.

#### The Quiet Knife

- **Category:** Politics
- **Condition:** Take control of a hex via Influence (annexation, arbitration, or Influence takeover).
- **Clarifications:** Qualifying methods: **Imperial Annexation** you proposed, winning a **Border Arbitration**, winning a contested neutral-claim **Influence bid**, or an **Influence takeover** (see `Tiles.md` and `High_Council.md`). The Adjacency Claim does **not** count (no Influence is spent).
- **Tracking:** Place a progress marker on this card when you gain a hex by a qualifying method.

#### Borderbreaker

- **Category:** Territory
- **Condition:** At Cleanup & Checks, have units in 3 hexes that are each at least 3 hexes apart from one another.
- **Clarifications:** All three pairwise hex distances must be 3 or more (see the hex distance definition in section 1.2). Military units and your Lord both count as "units."

#### Architect of Control

- **Category:** Exploration / Territory
- **Condition:** Control 2 special tiles (any combination of City / Ruins / Portal / Imperial Seat).
- **Clarifications:** Your Home City is a City and counts. The Imperial Seat is one special tile (it does not also count separately as a City for this card).

#### Bloodied Blade

- **Category:** Military
- **Condition:** Win a battle in which your Lord was on your Battle Line.
- **Clarifications:** Your Lord must have been on the Battle Line during at least one battle round of the battle you won (see `Combat.md` §2.1.2).
- **Tracking:** Place a progress marker on this card when you win a qualifying battle.

#### Breaker of Lines

- **Category:** Military
- **Condition:** Destroy 3 or more enemy units in a single battle round.
- **Clarifications:** Count enemy units removed by your side's rolls during one battle round, including Archer Pre-Strike. A Lord captured in that battle round counts as one unit for this count.
- **Tracking:** Place a progress marker on this card at the end of a qualifying battle round.

#### Horselord

- **Category:** Military
- **Condition:** Have 3 Cavalry in play.

#### Pathfinder

- **Category:** Exploration
- **Condition:** Resolve 3 Exploration Events triggered by your units entering unexplored hexes.
- **Clarifications:** You must be the entering player (see `Events.md` triggers referenced in `Round_Structure.md` §5.3).
- **Tracking:** Place a progress marker on this card each time you resolve a qualifying Exploration Event.

#### Far Dominion

- **Category:** Territory
- **Condition:** Control a hex at least 5 hexes away from your Home City.
- **Clarifications:** Uses the hex distance definition in section 1.2.

#### Bridgewright

- **Category:** Territory
- **Condition:** Control a Lake hex containing a Bridge you built.
- **Clarifications:** Bridge pieces are your color (see `Buildings.md`); the Bridge on the map is the evidence. If the hex was captured from you, you do not meet this condition until you retake it.

#### Desert Crown

- **Category:** Territory / Politics
- **Condition:** Control 2 Desert hexes.
- **Clarifications:** Unique tiles that count as Desert terrain count (see `Tiles.md`).

#### Master of Trade

- **Category:** Economy
- **Condition:** Complete 3 Trade actions you initiated.
- **Clarifications:** A Trade is complete when both sides have exchanged per the agreed terms (see `Trade_Taxes.md`). Trades initiated at 0 AP (e.g., via a Market) count.
- **Tracking:** Place a progress marker on this card each time a Trade you initiated completes.

#### Remnant Collector

- **Category:** Economy / Exploration
- **Condition:** Have 5 Remnants at once.
- **Clarifications:** You may always decline to purge Remnants (purging is optional; see `Artifacts.md`).
- **Scoring window:** Immediate — you may reveal and score this card at the moment you have 5 or more Remnants, during any phase.

#### Silver Tongue

- **Category:** Politics
- **Condition:** A motion you proposed passes in a vote in which you spent Influence to lobby.
- **Clarifications:** Lobbying per `High_Council.md` §2.3 (minimum spend 2 Influence). The lobbying must be on the vote for your own motion.
- **Tracking:** Place a progress marker on this card when a qualifying motion passes.

#### Titleholder

- **Category:** Politics
- **Condition:** Hold a Title at Cleanup & Checks.
- **Clarifications:** Any Title counts (e.g., Hero of the Realm, Magister of Mana). You must still be eligible per the Title's maintenance check (see `High_Council.md` §5.2).

#### Archivist

- **Category:** Arcane
- **Condition:** Own 3 Arcane Discoveries.
- **Clarifications:** Any schools and tiers count (see `Arcane.md`). School Specialties do not count.

#### Ear to the Stones

- **Category:** Subterfuge
- **Condition:** Play 4 Whisper Cards (cumulative across the game).
- **Clarifications:** A Whisper cancelled by Sabotage still counts as played; Sabotage itself counts as played (see `Whispers.md`).
- **Tracking:** Place a progress marker on this card each time you play a Whisper Card.

#### Teeming Realm

- **Category:** Growth
- **Condition:** Have a Population Cap of 15 or more.
- **Clarifications:** Read directly from your Population Cap track (see `Population.md`).

### 4.4 Retired objective-row experiment

This section preserves a killed sim configuration for reproducibility. It is not a current playtest rule.

#### Staged economy opening (E3)

- **Retired rule:** At setup, the shared row's opening **2** revealed cards were **Builder** and **Merchant Lord** instead of a random pair.
- **Intent:** Make economy paths **visible from round 1** without changing thresholds or pacing knobs (contrast E1/E2/E5, killed in sim).
- **Status:** **KILLED 2026-07-03** — sim toggle `objectives.staged_economy_opening` remains only to reproduce the E3 ladder; see `../docs/plans/2026-07-03-plan-early-economy-impact.md`.

---

## 5. Design Notes

### 5.1 Playstyle spread

Every deck spreads its conditions across the game's major playstyles so that any strategy can find objectives that reward it:

| Playstyle | Stage I Public | Stage II Public | Secret |
| --- | --- | --- | --- |
| **Military** | Warlord, Standing Army, Twin Cities | Conqueror, Breaker of Walls, Hold the Line | Hidden Arsenal, Bloodied Blade, Breaker of Lines, Horselord |
| **Economy** | Builder, Merchant Lord | Prosperous Realm, Imperial Treasury, Living Legend | Golden Hoard, Mana Flood, Master of Trade, Remnant Collector |
| **Politics** | Council Power, Voice of the Realm | Lawgiver, Beacon of Renown | The Quiet Knife, Silver Tongue, Titleholder |
| **Arcane** | Adept of the Schools | Archmage | Archivist |
| **Exploration** | Portal Mastery, Relic Seeker | Crossroads of Empire, Reliquary | Architect of Control, Pathfinder |
| **Territory** | Frontier Lord, Seat of Empire | Dominion, Crossroads of Empire | Borderbreaker, Far Dominion, Bridgewright, Desert Crown |
| **Subterfuge / Growth** | — | — | Ear to the Stones, Teeming Realm |

### 5.2 Verifiability rules (design contract)

Every objective condition **must** be objectively verifiable with components on the table:

- **State-based conditions** (control X hexes, own Y artifacts, have Z resources) are read directly from the board, tracks, and player areas at the moment of verification.
- **Event-based conditions** (win battles, pass motions, play Whispers) **must** carry a **Tracking** line: place a progress marker on the card at the moment each qualifying event occurs. No condition may rely on table memory.
- Public cards that currently require player-colored tracking after reveal: Council Power, Portal Mastery, Warlord, Breaker of Walls, Conqueror, Hold the Line, and Lawgiver. Secret cards track only after draw: Hidden Arsenal, The Quiet Knife, Bloodied Blade, Breaker of Lines, Pathfinder, Master of Trade, Silver Tongue, and Ear to the Stones.
- New objectives added later must follow the same contract, use only mechanics defined in an owning chapter, and reference that chapter in a clarification line.

### 5.3 First Playable compatibility

- The First Playable packet continues to print only its 6 public + 6 secret set (section 4.4 of the packet); those 12 cards appear here unchanged in effect. **Borderbreaker** replaces the packet's "define regions by table agreement" note with the concrete 3-hexes-apart rule (section 4.3) — use the concrete rule whenever this chapter is in play.
- If you use the **full decks** together with the First Playable arcane module (Tier I only, packet section 4.6), **remove Archmage** from the Stage II deck (Tier II research is disabled there). All other cards are fully playable under First Playable restrictions.

### 5.4 Balance intent

- **Stage I** conditions are sized to be achievable by rounds 1–4 with focused play (e.g., 7 hexes from a 4-hex start, 2 Tier I Discoveries, 8 units under a 10-Population start).
- **Stage II** conditions require mid/late-game development (12 hexes, 3 Cities, sieges, Tier II research, 10 Renown) and enter the deck at Round 4 (section 2.1) so they are never a new player's only path.
- **Secrets** are deliberately more specific than publics: they reward committing to a plan opponents cannot see, and the 3-card cap (section 3.3) bounds the hidden VP swing.
- **Counterplay**: most conditions are contestable on the board — hexes and Cities can be retaken, Artifacts and the Imperial Seat change hands, Laws can be repealed, and Titles have maintenance checks. Immediate-window cards (Golden Hoard, Mana Flood, Remnant Collector) are stockpile targets that reward striking a hoarder before they cash in.

### 5.5 Public-deck audit decisions (2026-07-13)

The 24-card audit keeps the 12/12 stage split and 2 VP value while removing three legibility and incentive traps:

1. Public cumulative progress starts only after reveal, so the shared row shows every player's real progress and never requires reconstructing earlier rounds.
2. **Crossroads of Empire** replaces **Heir of Aeonis**, avoiding a third overlapping reward for holding the Imperial Seat.
3. **Hold the Line** replaces **Kingslayer**, avoiding another reward on the already-loaded Lord-capture moment and adding a visible defensive victory path.
4. **Council Power** and **Lawgiver** reward participation rather than proposal ownership, so they remain attainable if the Plan 4 Docket is later promoted.
5. **Merchant Lord** replaces **Realm of Plenty**. The first audit ladder found Realm of Plenty effectively automatic (340 scores across 60 revealed games), while the full deck without Merchant Lord pushed the economist persona to 0–3.3% at 6p/8p.
6. **Prosperous Realm** replaces **Master of Cities**. The first two ladders recorded no Master of Cities scores at 4p/6p and confirmed that the deck over-weighted military/territory conditions.

**Sim hypotheses:** audited objectives should provide at least 60% of winner VP, preserve the accepted 6–8-round mean, and avoid any objective with zero scores across the 4p/6p/8p mixed-persona audit except **Archmage**, which is removed whenever the Tier II module is disabled.
