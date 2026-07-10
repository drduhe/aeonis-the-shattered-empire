# Aeonis: The Shattered Empire — Learn to Play

> **Draft for First Playable — matches the rules chapters as of this writing. The chapter docs remain authoritative.**

This book teaches the **First Playable** version of Aeonis for 3–8 players: baseline units only (Infantry, Cavalry, Archers), **Tier I** Arcane Discoveries only, the 26-card Whisper deck, the full artifact system, the 8-card agenda deck, and all 8 Lords. Advanced units, Accords/Diplomacy, and Tier II/III Discoveries are not used. Exact scope: `../playtest/First_Playable_Packet.md`.

---

## 1. What is Aeonis?

The Eternal Empire is gone. Its last emperor died without an heir, its provinces tore themselves apart, and the **Imperial Seat** — the throne-city at the heart of the realm — sits coveted by everyone. You are one of eight banished Lords: exiles, schemers, warlords, and mystics returned to claim what remains. The ancient Speaking Stones still whisper across the shattered land, carrying secrets, sealed orders, and political bargains to those who know how to listen.

In Aeonis you do a little of everything a ruler does: march armies across a hex map and fight for territory, vote (and horse-trade) in the High Council, research arcane Discoveries, dig up artifacts of the fallen empire, and grow the population that feeds your war machine. Every round mixes war, politics, economy, and magic — and the first Lord to reach **10 Victory Points (VP)** triggers the final round.

---

## 2. Object of the game

The first player to reach **10 VP** triggers the final round: finish the current round through Cleanup & Checks, and the player with the most VP at the end of that round wins. Ties are broken by most Renown, then most Influence. (For learning games, you can play to **8 VP** instead.)

Your main VP sources:

- **Objectives** — each public or secret objective you score is worth **2 VP**.
- **The Imperial Seat** — control it at Cleanup & Checks for **+1 VP** each round.
- **Capturing an enemy Lord** in battle — **+1 VP**.
- **Your Legendary Building** — worth **2 VP** while in play.
- **VP-bearing artifacts** — 4 of the 24 artifacts are worth **1 VP** each.
- **Council Titles** — Hero of the Realm and Magister of Mana each grant **2 VP** when first claimed.
- **Imperial Mandate** (Strategy Card) — its primary grants **1 VP** if you control the Imperial Seat.

Full details in section 10 and in `../rules_and_systems/Victory.md`.

---

## 3. Components overview

From `../components/Components.md`:

- **Hex tiles** — Cities, the Imperial Seat, Plains, Forests, Mountains, Deserts, Ruins, Portals, Lakes, plus 8 unique starting tiles (one per Lord).
- **Lord sheets** — stats, starting resources and units, abilities, Legendary Building.
- **Unit standees (per player)** — 1 Lord, 10 Infantry, 4 Cavalry, 4 Archers.
- **Control tokens (per player)** — mark controlled hexes.
- **Building tokens (shared)** — Farm, Mine, Grove, Embassy, Tower, Fortress, Bridge, Guild Hall, Forge, Academy, Bank, Castle, Market.
- **Legendary Building tokens** — 1 unique token per Lord.
- **Resource tokens** — Gold, Mana, Influence.
- **Trackers** — AP, Renown, VP, Population (Pool + Cap), Lord HP; plus the Speaker token.
- **Strategy Cards (8)** — drafted every round; set initiative.
- **Objective cards** — 6 public + 6 secret (2 VP each).
- **Event cards** — Global Events and Exploration Events.
- **Agenda cards (8)** — pre-written council motions.
- **Whisper Cards (26)** — one-shot tactical effects, private hand.
- **Artifact Cards (24)**, **Remnant tokens (30–40)**, **Artifact Site markers (5–6)**.
- **Dice** — d4, d6, d8, d10.
- **Siege markers and Title tokens.**

---

## 4. Setup, step by step

1. **Build the map.** Place the **Imperial Seat** tile in the center (a City with a bonus: its controller gains **+1 VP** at Cleanup & Checks). **3–4 players:** each player gets a **home cluster** of 4 tiles touching the central ring — 1 City (your Home City), 1 Plains, 1 Forest, 1 Mountain. In the neutral ring, place 1 Desert between each pair of home clusters, 2 Ruins, 2 Portals (not adjacent to each other), and 2 Lakes forming at least one choke point. **5–8 players:** add roughly +3 neutral tiles per player beyond 4; scale Deserts to 1 per pair of adjacent clusters, Ruins to 1 per 2 players (round up), Portals and Lakes to 1 per 3 players each (round up, minimum 2).
2. **Pick Lords.** Each player takes a different Lord sheet, standees, and control tokens. If your sheet lists a **Unique Starting Tile**, swap it in for the specified home-cluster tile (it still counts as its listed terrain type).
3. **Place starting units.** Put the units listed on your Lord sheet in your Home City, with your Lord standee. (Default: 3 Infantry + 1 Archer. Lords differ — Rakhis starts with 2 Infantry + 1 Cavalry.)
4. **Mark starting control.** You control your 4-tile home cluster; everything else starts neutral.
5. **Set your trackers.** **5 AP**, **0 Renown**, **0 VP**, **Population Cap 10**, **Population Pool 10** (full). Take the starting Gold/Mana/Influence on your Lord sheet (default: 2 Gold, 2 Mana, 1 Influence).
6. **Prepare the decks.** Lay out the 8 **Strategy Cards**. Shuffle the **agenda deck** (8), **Whisper deck** (26), **Artifact Deck** (24, face down), and the **Global** and **Exploration Event** decks. Set out the Remnant supply and Artifact Site markers. No one starts with artifacts or Remnants.
7. **Draw objectives.** Each player draws **1 public objective** (reveal it) and **1 secret objective** (keep hidden). Each is worth 2 VP when scored.
8. **Draw Whispers.** Each player draws **2 Whisper Cards** into a private hand.
9. **Choose the first Speaker at random**; give them the Speaker token.
10. **Begin Round 1.** Reminder: at the start of **Round 3**, each player draws 1 additional secret objective.

---

## 5. The round

Every round follows the same 7 phases, in this order (`../rules_and_systems/Round_Structure.md`):

1. Round Start
2. Event Phase
3. Strategy Selection
4. High Council Phase
5. Action Phase (rotating turns)
6. Production & Upkeep
7. Cleanup & Checks

To see how they fit together, follow one example round at a four-player table. Our leads: **Rakhis, the Sandlord** (fast cavalry raider; 2 VP, 1 Renown) and **Vharok, Lord of Steel** (fortress tank; 3 VP, 5 Renown). Rakhis's **Sandstride** ignores enemy ZOC surcharges; Vharok's **Bastion Doctrine** lets any controlled built hex Hold the Walls with +1 defending Battle Line capacity. Cassian and Elyndra fill the other seats. It is Round 3; Cassian holds the Speaker token.

### Phase 1: Round Start

Refresh all "once per round" abilities, reset every player's AP pool, return any banked AP, and have each player draw **2 Whisper Cards**. Lords heal to full HP.

Your AP pool is the base on your Lord sheet (default **5**) plus bonuses: **+1 AP per controlled City** (max +2 from Cities), **+1** from a Guild Hall, **+1 permanently at 5 Renown**.

> **Example:** Rakhis resets to 5 base + 1 (Home City) = **6 AP**. Vharok banked 2 AP when he passed last round and has 5 Renown: 5 + 1 (City) + 1 (Renown) + 2 (banked) = **9 AP**. Everyone draws 2 Whispers.

### Phase 2: Event Phase

Draw and resolve one **Global Event**. Events land *before* strategy picks on purpose — they set the tone everyone must adapt to.

> **Example:** The event is **Mana Surge**: each player gains +2 Mana. Elyndra grins; Rakhis starts eyeing a cheap Research action.

### Phase 3: Strategy Selection

All 8 Strategy Cards are available every round. Players draft in **ascending VP order** (lowest VP picks first — ties broken by lowest Renown, then clockwise from the Speaker). At **3–4 players**, each player drafts **2 cards** (two full passes); at **5–8 players**, each drafts 1. Your **initiative** for the round is your lowest card number. After the draft, place **1 Gold** from the supply on each undrafted card — whoever drafts that card in a later round takes all the Gold on it.

> **Example:** Rakhis and Cassian are tied at 2 VP; Rakhis has less Renown, so he picks first, then Cassian, Vharok, Elyndra. First pass: Rakhis takes **Military Maneuvers** (3), Cassian **Economic Boom** (7), Vharok **Tactical Reinforcements** (6), Elyndra **Arcane Ascendancy** (1). Second pass, same order: **Resource Surge** (2), **Diplomatic Decree** (4), **Imperial Mandate** (8), **Expansion Strategy** (5). All 8 cards drafted — no bounty Gold this round. Initiative: Elyndra (1), Rakhis (2), Cassian (4), Vharok (6).

### Phase 4: High Council Phase

The political phase: proposals, the agenda card reveal, negotiation, voting, enactment. Section 8 walks the full procedure with vote math.

> **Example:** In proposal order, only Vharok proposes: he pays 1 Influence to put **Realm Tax** on the agenda. Speaker Cassian reveals the top agenda card — **Border Arbitration** — which anyone may propose for free this round; nobody bites, so it will be discarded. The Realm Tax vote plays out in section 8 (it passes, and Vharok gains +1 Renown for passing his own motion).

### Phase 5: Action Phase (rotating turns)

Players take turns in **initiative order**. On your turn you take **exactly one action**, pay its AP cost, and play passes on. This rotation continues until everyone has passed or run out of AP. Section 6 covers every action.

> **Example:** Elyndra acts first (initiative 1), then Rakhis, Cassian, Vharok, and back around. Rakhis opens with his **Military Maneuvers** primary (1 AP): a free Move slides his cavalry next to a Desert hex Vharok controls. The battle comes on his next turn (worked in section 6). After the primary resolves, each other player, in initiative order, may pay for the card's *secondary* (1 AP to move a group 1 hex) without using a turn. Later, Vharok fires **Tactical Reinforcements** (1 AP) to recruit 2 units for free in his Home City.

### Phase 6: Production & Upkeep

All players resolve, in initiative order (or simultaneously if the table prefers):

1. **Production:** gain resources from every hex and building you control — Plains give Population, Forests Mana, Mountains Gold, Deserts Influence (buildings boost these; see the Player Aid).
2. **Population growth:** replenish your Population Pool by **+1 base, +1 per controlled Plains, +2 per controlled City**, up to your Population Cap.
3. **Upkeep:** pay maintenance for advanced buildings (e.g., Forge: 1 Mana per round). Basic units have **no** Gold upkeep — Population is their limit.
4. **"Each round" effects** (laws, artifacts, Discoveries) resolve now unless they say otherwise.
5. **Remnants:** each **Ruins** hex you control generates **1 Remnant**.

> **Example:** Rakhis controls his home cluster plus the conquered Desert: 1 Mana (Forest), 1 Gold (Mountain), 1 Influence (Desert), and Population growth of 1 + 1 (Plains) + 2 (City) = +4. Vharok collects his production and pays 1 Mana to keep his Forge running.

### Phase 7: Cleanup & Checks

1. Discard round-limited effects and reset "once per round" markers.
2. **Release captured Lords** — they return to their owner's Home City at full HP.
3. **Whisper hand limit:** anyone holding more than **7** Whisper Cards discards down to 7.
4. **Victory checks:** score objectives whose conditions hold right now (in initiative order), check Imperial Seat VP, Titles, Legendary Buildings, and VP artifacts — then check whether anyone has reached 10 VP.
5. Advance the round marker and **pass the Speaker token clockwise**.

> **Example:** Rakhis scores his public objective **Warlord** (win 2 battles) for 2 VP — and draws 1 Whisper, because scoring VP always draws a Whisper. Cassian controls the Imperial Seat: +1 VP. Nobody is at 10 VP, so the Speaker token passes clockwise and Round 4 begins.

---

## 6. Your turn in the Action Phase

On your turn, choose **one** action from this menu (`../rules_and_systems/Actions.md`):

| Action | AP cost | Notes |
| --- | --- | --- |
| **Move** | Path cost | 1 AP/hex on most terrain, 2 on Mountains/Deserts; +1 per enemy ZOC hex |
| **Attack** | 2 AP | One battle round; +1 AP to Press the Attack |
| **Build** | 3 AP | Legendary Buildings: 4 AP; plus the building's resource cost |
| **Recruit** | 1 AP | Up to 2 units in one controlled City; once per City per round |
| **Research** | 1 AP (Tier I) | Plus the Discovery's resource cost (default Tier I: 2 Mana) |
| **Trade** | 1 AP | Initiate a trade; once per round |
| **Strategy Card primary** | Varies | Printed on the card; once per round |
| **Play an ACTION Whisper** | 0 AP | Uses your turn anyway |
| **Claim Artifact** | 1 AP | Requires your unit on an Artifact Site hex |
| **Pass** | — | You take no further turns; bank up to 2 unused AP |

You can also **purge 3 Remnants at any time on your turn** to draw an Artifact Card — that is a free action and does not use your turn.

### Move

Pick **one group** (any number of your units stacked in one hex) and pay the total cost of its path. **Movement Range** caps hexes entered per Move action: Infantry 1, Archers 1, Cavalry 2, Lords per their sheet; a group moves at its *slowest* member's range.

**Terrain costs:** Plains, Forests, Cities 1 AP per hex; Mountains, Deserts 2. Lakes are impassable unless bridged. **Portals** cost 1 AP to enter or exit, but Portal-to-Portal travel is **0 AP** — allowed only if the destination Portal is neutral or yours.

**Zone of Control (ZOC):** every hex adjacent to enemy military units is in that enemy's ZOC. Entering a ZOC hex costs **+1 AP** on top of terrain. **Cavalry flanking:** Cavalry ignore the surcharge on the *first* ZOC hex entered each Move action. You cannot enter an enemy-**controlled** hex unless you pay the ZOC surcharge (if in ZOC), a treaty or motion allows it, or you are attacking it — but enemy hexes with *no units nearby* aren't in ZOC and can simply be walked into.

> **Example:** Rakhis moves a Cavalry group 2 hexes toward Vharok's line. Both Plains hexes are adjacent to Vharok's Infantry, but **Sandstride** ignores both ZOC surcharges. Total: **2 AP**. Another Lord's Cavalry would ignore only the first surcharge and pay 3 AP total.

### Attack

Attacks are **declared**, not moved into: pay **2 AP**, name a target hex, and fight with units from adjacent hexes. Each Attack action resolves **exactly one battle round**; you may pay **+1 AP** once to **Press the Attack** for a second. Here is one full battle, with dice.

> **Example:** Rakhis attacks the Desert hex Vharok controls. Rakhis commits 2 Cavalry and 1 Infantry from adjacent hexes; Vharok commits the 2 Infantry in the hex plus an adjacent Archer. A standard hex has a **Battle Line Cap of 3**, so every committed unit is on the line; no Reserves.
>
> 1. **Reinforce Battle Lines** — both lines already full.
> 2. **Archer Pre-Strike** — Rakhis has no Archers. Vharok's Archer targets Cavalry A: attack d6 rolls **5** vs. the Cavalry's defense d6 of **3**. Attack beats defense: 1 damage; Cavalry A drops from 2 HP to 1.
> 3. **Attacker Strike** — Cavalry A targets the Archer: d8 rolls **6** vs. d4 defense of **2** — the Archer (1 HP) is destroyed. Cavalry B targets Infantry 1: d8 rolls **4** vs. d6 of **4** — a tie deals no damage. Rakhis's Infantry targets Infantry 2: d6 rolls **5** vs. **2** — destroyed.
> 4. **Defender Counterstrike** — only Infantry 1 remains. It targets wounded Cavalry A: d6 rolls **6** vs. defense **1** — Cavalry A is destroyed.
> 5. **Retreat Check** — attacker first: Rakhis stays. Vharok could pull his last Infantry to an adjacent hex he controls, but holds.
> 6. **Victory Check** — both sides still have committed units, so the battle would pause here…
>
> …but Rakhis pays **+1 AP to Press the Attack**. Second battle round: Cavalry B rolls d8 **7** vs. Infantry 1's **3** — destroyed. The defender is eliminated: Rakhis **immediately takes control** of the hex, occupies it with up to 3 survivors, and gains **+1 Renown** (first hex captured this round). Total cost: 3 AP.

### Build

Pay **3 AP** plus the building's resource cost to construct on a hex you control (**4 AP** for your Legendary Building). Production buildings must match their terrain (Farm/Plains, Mine/Mountains, Grove/Forests, Embassy/Deserts); advanced buildings go in Cities. Basic terrain holds 1 building; Cities hold 2 (3 with research). Most buildings occupy Population while they exist.

> **Example:** Vharok spends 3 AP, 5 Gold, and 2 Mana to raise a **Fortress** on his Mountain (occupies 2 Population). Defenders there now get +2 Defense, and any attack against it is automatically a Siege.

### Recruit

Pay **1 AP**, choose **one controlled City**, and place **up to 2 units** there, paying each unit's cost: **Infantry** 1 Gold + 1 Population, **Cavalry** 2 Gold + 2 Population, **Archer** 1 Gold + 1 Mana + 1 Population. Each City can host recruitment **only once per round** — you may Recruit again on a later turn, but at a *different* City.

> **Example:** Rakhis pays 1 AP, 3 Gold, and 3 Population for 1 Cavalry + 1 Infantry in his Home City, which is now done recruiting this round.

### Research

Pay **1 AP** plus the Discovery's resource cost to learn one **Tier I** Arcane Discovery you don't already own (First Playable uses Tier I only — ten Discoveries across five schools). Its effect is active immediately, and completing it earns you **1 Remnant**. See section 9.

> **Example:** Rakhis spends 1 AP, 1 Mana, and 1 Gold on **Waystones** (Transmutation): once per round his Move actions cost 1 less AP (minimum 1). He also pockets 1 Remnant.

### Trade

Pay **1 AP** to initiate a trade with another player — resources, Remnants, Utility Artifacts, promises, even hexes or units. You may initiate only **once per round** (a Market allows one trade at 0 AP).

### Strategy Card primary

Using your card's primary is an action; pay the AP printed on it. Each primary works **once per round**. After it fully resolves, every *other* player, in initiative order, may pay for the card's **secondary** — secondaries don't consume anyone's turn, and each player may use a given secondary at most once per round.

### Play an ACTION Whisper

Play a Whisper with **ACTION** timing instead of a normal action. It costs **0 AP**, but it *is* your turn — play passes afterward. (COMBAT, COUNCIL, and WHEN Whispers are played inline at their trigger and don't use your turn at all.)

> **Example:** Cassian plays **Hidden Cache** as his action and takes 3 Gold.

### Pass (and banking AP)

When you pass, you're out for the rest of the round — and you may **bank up to 2 unused AP** for next round. Everything above 2 is lost.

---

## 7. Combat in detail

Full rules in `../rules_and_systems/Combat.md`. The system keeps fights fast and punishes doomstacks.

**Committing and the Battle Line.** When an attack is declared, the attacker commits any units from hexes adjacent to the target; the defender commits units in the target hex plus any from adjacent hexes. Committed units stay where they are — they're "in the fight." Each side puts up to the **Battle Line Cap** on the line: **3 units** on a standard hex, **5** on a City or Fortress. The rest are **Reserves**. Only line units roll dice; Reserves replace casualties.

**One battle round per Attack action:**

1. **Reinforce Battle Lines** — promote Reserves to fill gaps up to the cap.
2. **Archer Pre-Strike** — Archers on the line strike early: all attacking Archers roll first, then all defending Archers. Each picks a target on the enemy line.
3. **Attacker Strike** — each attacking line unit picks a target and rolls its Attack die; the target rolls its Defense die. **Attack > Defense: 1 damage.** Ties deal nothing. Units at 0 HP are removed at once.
4. **Defender Counterstrike** — surviving defenders do the same.
5. **Retreat Check** — attacker decides first. An attacker retreat ends the battle with all survivors in their origin hexes. A defender may retreat only from **standard hexes**, to an adjacent hex they control — **never from Cities or Fortresses** unless a card or motion allows it.
6. **Victory Check** — if one side has no committed units left, the battle is decided. Otherwise it **pauses**; continuing costs another Attack action on a later turn.

**Press the Attack.** After the battle round, the attacker may pay **+1 AP** to resolve one more round immediately — at most once per Attack action (so 2 battle rounds maximum per action).

**Aftermath.** If the defender is wiped out, the attacker takes control of the hex immediately and may occupy it with survivors up to the Battle Line Cap. If the attacker retreats or is wiped out, the defender holds.

**Sieges.** Attacking a **Fortress** hex is always a Siege; when attacking a **City**, the defender may declare **Hold the Walls** to make it one. Place a Siege marker: it persists across turns and rounds. Each Attack action against the hex resolves one siege battle round; at the start of each, either side may add up to **3 units** from adjacent hexes as Reserves. The attacker may lift the siege at the end of any siege round; it ends automatically if the attacker has no committed units adjacent. Sieges are the *only* multi-turn combat state.

**Lords in battle.** Your Lord is a unit: it moves, commits, and can stand on the Battle Line (counting toward the cap), rolling the dice on its Lord sheet. When a Lord hits 0 HP it is **captured**, not destroyed: the captor gains **+2 Renown and +1 VP** and takes all the Lord's equipped artifacts. While captured, the owner **cannot use any Lord abilities** — but still plays and scores normally. At Cleanup & Checks, captured Lords return home at full HP.

**Whispers in combat.** COMBAT Whispers are played at the battle step named on the card — at most 1 Whisper per timing window per occurrence.

---

## 8. The High Council

The council convenes every round in Phase 4 (`../rules_and_systems/High_Council.md`).

**Your votes.** Everyone has a base of **1 Council Vote**, **+1 at 5+ Renown**, and **+1 more at 10+ Renown**.

**The procedure:**

1. **Agenda opens** — determine proposal order (default: initiative order).
2. **Proposal window** — in order, each player may propose **one motion** by paying **1 Influence** (or pass). Maximum one motion per player per round.
3. **Agenda card reveal** — the Speaker flips the top card of the **agenda deck**. Any player may propose *that* motion **for free** this round; it doesn't count against the one-motion limit. If nobody proposes it, discard it at end of phase.
4. **Negotiation** — promises are always fair game; actual resource transfers follow the trade rules.
5. **Voting** — resolve motions one at a time, in the order proposed. When a motion is called, players may **lobby** in initiative order: **2 Influence buys +1 vote** for this motion only (minimum spend 2). Everyone commits votes for or against. A motion **passes on a strict majority of votes cast — ties fail** (optionally, the Speaker breaks ties). Passing your own motion earns **+1 Renown**.
6. **Enactment** — Decrees resolve immediately, Laws persist until repealed, Titles are awarded on the spot.

> **Worked vote:** Vharok has proposed **Realm Tax** (a Law: each round, every player gains +1 Gold but must pay 1 Influence or lose 1 Renown). Lobbying, in initiative order: Elyndra spends 2 Influence for +1 vote; the others decline. **For:** Vharok 2 votes (base 1, +1 for 5 Renown) + Elyndra 2 (base 1, +1 lobbied) = **4**. **Against:** Rakhis 1 + Cassian 1 = **2**. Six votes cast, 4 is a strict majority: the Law passes, and Vharok gains +1 Renown. Had Cassian played **Backroom Deal** (+2 votes against), it would have died in a 4–4 tie.

COUNCIL Whispers (Veto, Backroom Deal, Political Leverage, Leaked Intelligence) play at the council moments named on the cards.

---

## 9. Magic, artifacts, and Whispers

### Arcane Discoveries (Tier I)

Research is your tech tree (`../rules_and_systems/Arcane.md`). First Playable allows the **ten Tier I Discoveries** — two per school: Evocation (Battle Runes, Searing Salvo), Enchantment (Sigiled Masonry, Warding Charm), Divination (Scrying Pool, Battle Augury), Transmutation (Golden Alchemy, Waystones), Geomancy (Boundary Stones, Stonewright). None has prerequisites. A Research action costs **1 AP plus the listed resource cost** (default 2 Mana), grants the Discovery immediately, and pays out **1 Remnant**. Some are passives; others unlock **Rituals** — repeatable abilities with their own costs. "Research a Tier I discovery for free" means ignore both AP and resource costs.

### Artifacts and Remnants

Artifacts are 24 unique relics of the fallen empire (`../rules_and_systems/Artifacts.md`). Two ways to get one:

- **Purge 3 Remnants** at any time on your turn to draw the top Artifact Card — free action, 0 AP. Remnants come from exploration, controlled Ruins (1 each per round), completing Discoveries, Whispers, and Events.
- **Artifact Sites** — certain Events place a Site marker with a face-up artifact on a hex. Any player with a unit there may spend **1 AP** to claim it.

Artifacts come in three categories: **Lord Equipment** attaches to your Lord (max **2**; a captor takes them all), **Building Relics** attach to an eligible building (1 per building; they change hands with the hex), and **Utility** artifacts sit in your play area. Only 4 artifacts award VP — **Crown of Aeonis, Eternal Forge, Shard of the Throne, Imperial Seal** — 1 VP each at Cleanup & Checks, each stealable in its own way.

### Whispers

Whisper Cards are one-shot tricks in a private hand (`../rules_and_systems/Whispers.md`). Draw **2 at every Round Start**, plus **1 whenever you score VP**. Hand limit **7**, enforced at Cleanup. Every card names a timing window:

| Timing | When it plays |
| --- | --- |
| **ACTION** | On your turn, instead of your normal action (0 AP, but it uses the turn) |
| **COMBAT** | During the named step of a battle you're in |
| **COUNCIL** | At the named moment of the High Council Phase |
| **WHEN [X]** | Immediately after the described trigger occurs |

You may play at most **1 Whisper per timing window per occurrence**. Only ACTION Whispers consume your turn. And beware **Sabotage**: it cancels any Whisper as it's played, and cannot itself be Sabotaged.

---

## 10. Scoring and winning

Almost everything scores at **Cleanup & Checks**:

- **Objectives** are verified there, in initiative order, before the victory-threshold check. If the condition holds at that moment, reveal (if secret) and score **2 VP** — meeting a condition mid-round and losing it by Cleanup scores nothing. Exception: objectives marked **Immediate** (like Golden Hoard) score the moment the condition is true. Each card scores once, then is discarded. And **every time you score VP, draw 1 Whisper Card.**
- **Imperial Seat:** control it at Cleanup for **+1 VP** that round.
- **Titles** are checked at Cleanup: keep the eligibility or lose the Title (the 2 VP from first claiming it are yours forever).
- **Legendary Buildings** (2 VP) and **VP-bearing artifacts** (1 VP each) count while you control them — lose the City or the artifact and the VP go with it.
- **Lord captures** (+1 VP) score immediately when they happen.

You start with 1 public + 1 secret objective; a second secret arrives at Round 3, and effects like Imperial Mandate can draw more (max **3 unscored secrets**).

**Ending the game:** the first time any player reaches **10 VP** (checked at Cleanup), that round is the final round — the game ends at the end of its Cleanup & Checks, and the highest VP total wins. Tiebreakers: most Renown, then most Influence.

---

## 11. Quick reference: 10 common mistakes

1. **Forgetting the ZOC surcharge.** Hexes adjacent to enemy units cost +1 AP to enter — Cavalry skip it only on their *first* ZOC hex per Move action.
2. **Scoring objectives mid-round.** Most objectives are verified at Cleanup & Checks; the condition must hold *then*. Only "Immediate" cards (Golden Hoard, Mana Flood) score on the spot.
3. **Recruiting twice at one City.** Each City hosts recruitment once per round — a second Recruit action must target a different City.
4. **Blowing past the Whisper hand limit.** You can hold 8+ during the round, but you discard to **7** at Cleanup.
5. **Moving into a fight.** Attacks are declared from adjacent hexes; committed units stay in their origin hexes and only *occupy* the target after winning.
6. **Playing combat to the death.** Each Attack action is **one** battle round (two with Press the Attack). Unfinished battles pause; only sieges persist.
7. **Banking too much AP.** Passing banks at most **2 AP** — the rest evaporates.
8. **Forgetting bounty Gold.** Undrafted Strategy Cards get 1 Gold at the end of Strategy Selection; drafting one later collects the pile.
9. **Confusing control with ZOC.** Buildings and control markers hold territory but generate **no ZOC** — only units do. Undefended hexes can be walked into and flipped.
10. **Skipping the VP Whisper draw.** Every VP score — objective, capture, Seat, Title — draws you 1 Whisper Card.

*Good luck, Lord. The Stones are listening.*
