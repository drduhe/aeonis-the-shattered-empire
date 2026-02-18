# Aeonis: First Playable Packet (3-8 players)

This packet is a **small, concrete, testable** version of Aeonis meant to be played in TI4-scale sessions while exercising the core loop:

**Event -> Strategy pick -> High Council -> rotating actions (AP) -> battles -> production/upkeep -> VP race.**

It deliberately restricts content so playtests focus on **pacing, map flow, and interaction**.

---

## 1) What rules are "on"

Use these chapters as written:

- `Round_Structure.md` (includes the new Event Phase timing: events resolve before Strategy Selection)
- `High_Council.md`
- `Actions.md` (includes canonical Recruit rules and Build at 3 AP)
- `Movement.md` (includes ZOC clarification and Cavalry flanking)
- `Combat.md` (includes softened Lord capture: +1 VP, ability lockout instead of score lockout)
- `Tiles.md` (includes unit-based ZOC rules)
- `Population.md`
- `Trade_Taxes.md`
- `Buildings.md`
- `Whispers.md` (tactical one-shot Whisper Cards drawn into a private hand; 24-card First Playable deck)

First Playable restrictions are listed below where needed.

---

## 2) Player count and victory

- **Players**: 3-8 (scale map per section 3 below)
- **Victory threshold**: **10 VP** triggers the final round; highest VP at end of that round wins (ties: most Renown, then most Influence).
- **Short game variant**: Use **8 VP** threshold for learning games or shorter sessions.

---

## 3) Setup (map + starting state)

### 3.1 Map layout

Build a map scaled to player count:

**For 3-4 players:**

- 1 central tile: **Imperial Seat** (treat as a City).
- One "home cluster" per player placed around it (each cluster touches the central ring).

**For 5-8 players:**

- 1 central tile: **Imperial Seat** (treat as a City).
- Add additional neutral tiles to the ring proportional to player count (roughly +3 neutral tiles per additional player beyond 4).
- Ensure each player's home cluster touches the neutral ring.

**Home cluster per player (4 tiles):**

- 1x City (your home city)
- 1x Plains
- 1x Forest
- 1x Mountain

**Unique starting tiles (First Playable rule):**

- If your Lord sheet includes a **Unique Starting Tile**, replace the specified home-cluster tile with that unique tile (it still counts as the listed terrain type for movement and most rules; see `Tiles.md`).

**Neutral ring (3-4 players):**

- Place 1x Desert between each pair of home clusters (so deserts become political flashpoints).
- Place 2x Ruins anywhere in the neutral ring.
- Place 2x Portals anywhere in the neutral ring (not adjacent to each other).
- Place 2x Lakes anywhere that creates at least one meaningful choke point (bridges exist in this packet).

**Neutral ring (5-8 players):**

- Scale Deserts to 1 per pair of adjacent home clusters.
- Scale Ruins to 1 per 2 players (round up).
- Scale Portals to 1 per 3 players (round up, minimum 2).
- Scale Lakes to 1 per 3 players (round up, minimum 2).
- Add additional Plains/Forests/Mountains as needed to fill gaps.

### 3.2 Imperial Seat (First Playable rule)

The Imperial Seat is a City with this additional rule:

- If you control the Imperial Seat at **Cleanup & Checks**, gain **+1 VP**.

### 3.3 Starting resources & tracks (per player)

- **AP**: 5
- **Renown**: 0
- **VP**: 0
- **Population Cap**: 10
- **Population Pool**: 10 (full at start)
- **Resources**: 2 Gold, 2 Mana, 1 Influence
- **Whisper Cards**: 2 (draw from the shared deck during setup, before Round 1 begins)

### 3.4 Starting units (per player)

Place in your Home City:

- 3x Infantry
- 1x Archer

### 3.5 Starting control

You begin controlling your home cluster:

- Your City + your Plains + your Forest + your Mountain

Neutral tiles start neutral.

---

## 4) Allowed content (tight scope)

### 4.1 Units (allowed)

Use only the baseline units from `Combat.md`:

- Infantry, Cavalry, Archers

Recruitment costs (see `Actions.md`):

| Unit     | Gold | Mana | Population |
| -------- | ---- | ---- | ---------- |
| Infantry | 1    | -    | 1          |
| Cavalry  | 2    | -    | 2          |
| Archer   | 1    | 1    | 1          |

(No advanced units in First Playable.)

### 4.2 Buildings (allowed)

Allowed:

- Farm, Mine, Grove, Embassy
- Tower
- Fortress
- Guild Hall
- Market
- Bridge

**Build action cost: 3 AP** (see `Actions.md`).

Not used in First Playable:

- Academy, Forge/Arcane Forge, Bank, Castle, Legendary Buildings (save for later balance passes)

### 4.3 Strategy cards (use 6 for 3-4 players, all 8 for 5-8)

**For 3-4 players**, use these six from `Strategy.md` (print as cards):

1. **Arcane Ascendancy**
2. **Resource Surge**
3. **Military Maneuvers**
4. **Diplomatic Decree**
6. **Tactical Reinforcements**
7. **Economic Boom**

**For 5-8 players**, add:

5. **Expansion Strategy**
8. **Arcane Convergence**

**Draft order (canon):** Lowest VP picks first. Ties broken by lowest Renown, then clockwise from Speaker.

### 4.4 Objectives (print 6 public + 6 secret)

**Public Objectives (2 VP each):**

- **Frontier Lord**: Control 7 hexes.
- **Builder**: Have 3 buildings in play.
- **Council Power**: Win 2 High Council votes you proposed.
- **Portal Mastery**: Control a Portal and use Portal travel at least once.
- **Warlord**: Win 2 battles (attacker or defender).
- **Seat of Empire**: Control the Imperial Seat at Cleanup & Checks.

**Secret Objectives (2 VP each):**

- **Hidden Arsenal**: Build a Fortress and win a battle involving that hex.
- **Golden Hoard**: Have 10 Gold at once.
- **Mana Flood**: Have 10 Mana at once.
- **The Quiet Knife**: Take control of a hex via Influence (annexation/arbitration/Influence takeover).
- **Borderbreaker**: End the round with units in 3 different regions of the map (define regions by table agreement).
- **Architect of Control**: Control 2 special tiles (any combination of City/Ruins/Portal/Imperial Seat).

Setup:

- Each player draws 1 public + 1 secret at start.
- At the start of Round 3, each player draws 1 additional secret.

### 4.5 Events (print 10 global + 8 exploration)

**Global Events (resolve in Event Phase, before Strategy Selection):**

- **Harsh Winter**: Each player loses 2 Gold unless they control at least 1 Farm.
- **Festival**: All players gain +1 AP next round.
- **Migration Wave**: Each player with at least 2 Plains gains +2 Population Pool (up to cap).
- **Council Crisis**: The Speaker must put a motion on the agenda; if it fails, Speaker loses 1 Renown.
- **Mana Surge**: Each player gains +2 Mana.
- **Border Skirmishes**: The player with the most controlled hexes gains +1 Renown; ties: all tied gain +1 Renown.
- **Supply Disruption**: Each player must discard 2 total resources (any mix of Gold/Mana/Influence).
- **Open Roads**: Until end of round, movement across Plains costs 1 less AP (min 1).
- **Populist Uprising** (catch-up): The player(s) with the fewest controlled hexes gain +2 Population Pool (up to cap) and +1 Influence.
- **Winds of Fortune** (catch-up): The player(s) with the fewest VP gain +2 AP next round and may draw one additional objective card (public or secret, their choice).

**Exploration Events (resolve immediately on first entry):**

- **Ancient Ruins**: Gain 2 Gold or 2 Mana (choose one).
- **Trapped Vault**: Lose 1 unit from the entering group OR pay 2 Gold to avoid.
- **Speaking Stone Echo**: Gain +1 Influence and +1 Renown.
- **Lost Cartographer**: Reveal any one unrevealed tile (if using fog) and gain +1 AP this round.
- **Wandering Mercenaries**: Gain 1 Infantry for free (place in the entering hex if legal; otherwise your nearest controlled City).
- **Cursed Ground**: The hex produces no resources until you spend 2 Influence to cleanse it.
- **Relic Fragment**: Gain 1 VP immediately.
- **Portal Instability**: If the hex is a Portal, you may immediately Portal travel once at 0 AP (destination must be neutral or yours).

---

### 4.6 Arcane Discoveries (optional, recommended)

The First Playable already includes Strategy Cards that reference research (e.g., **Arcane Ascendancy**). To keep the packet self-contained, enable this small Arcane module:

- Use `rules_and_systems/Arcane.md`.
- **Allowed tier**: **Tier I only** (ignore Tier II/III and specialties).
- **Available discoveries**: the Tier I entries in section 7 (10 total).

Rules reminder (Tier I only):

- **Research** is an action you may take on your turn (see `Arcane.md`).
- **Cost**: 1 AP + the discovery's listed resource cost.
- If a card effect says "research a Tier I discovery for free," you ignore both AP and resource costs (you still choose a Tier I discovery you don't already own).

Printing note:

- Print the Tier I discoveries as reference cards, or list them on a single player-aid sheet.

### 4.7 Whisper Cards (print 24-card deck)

Use the full First Playable deck from `Whispers.md`. Shuffle all 24 cards into a single shared deck.

**Setup:** Each player draws 2 Whisper Cards before Round 1.

**Each round:** Draw 2 more at Round Start. Hand limit is 7 (discard excess at Cleanup & Checks).

**Card summary by category:**

**Combat (8 cards):** Shield Wall, Flanking Charge, Deadly Volley, Tactical Withdrawal, Rallying Cry, Fortify Position, Overwhelming Numbers, Iron Resolve

**Political (5 cards):** Sabotage, Backroom Deal, Veto, Political Leverage, Leaked Intelligence

**Economic (5 cards):** Hidden Cache, War Profiteer, Emergency Conscription, Prospector's Find, Contraband

**Movement/Arcane (4 cards):** Forced March, Blink, Ley Line Surge, Waystone Activation

**Subterfuge (2 cards):** Saboteur, Mercenary Company

See `Whispers.md` for full card text and timing rules.

---

## 5) High Council "agenda deck" (8 cards)

For First Playable, use a simple agenda deck:

- Road Networks (Law)
- Demilitarized Zone (Decree)
- Open Borders Treaty (Decree)
- Imperial Annexation (Decree)
- Border Arbitration (Decree)
- Realm Tax (Law)
- Hero of the Realm (Title)
- Magister of Mana (Title)

Rule: each round, after proposals are placed, the Speaker reveals the top **one** agenda card. Any player may propose **that** motion for free (no proposal Influence cost) this round if they wish.

---

## 6) Round structure reminder

The round order for First Playable follows `Round_Structure.md`:

1. **Round Start** (refresh abilities, reset AP, **draw 2 Whispers**)
2. **Event Phase** (draw and resolve one global event)
3. **Strategy Selection** (lowest VP picks first)
4. **High Council Phase** (proposals, negotiation, voting; COUNCIL Whispers may be played)
5. **Action Phase** (rotating turns in initiative order; ACTION/COMBAT/WHEN Whispers may be played)
6. **Production & Upkeep** (gain resources, grow population, pay upkeep)
7. **Cleanup & Checks** (release captured Lords, **discard Whispers to hand limit 7**, check VP threshold, advance round marker)

---

## 7) Playtest goals (what to watch)

1. **Pacing**: Do rounds stay snappy with 3 AP Build and the new Recruit action? Does the Event-first order create interesting setup tension?
2. **Map flow**: Do Lakes + Bridges create fun chokepoints without stalling play?
3. **Politics**: Does the High Council matter every round without taking over the session?
4. **War feel**: Do front lines emerge naturally with Battle Line/Reserves and sieges? Does the unit-based ZOC create meaningful defensive play?
5. **Economy feel**: Does Population-as-cap create meaningful tradeoffs vs buildings and army size?
6. **Catch-up**: Does the VP-based draft order + catch-up events prevent runaway leaders?
7. **Cavalry role**: Do Cavalry feel distinct from Infantry thanks to flanking + movement range?
8. **Lord asymmetry**: Do the differentiated Lord combat stats create meaningful choices about when to commit your Lord to battle?
9. **Whispers**: Do Whisper Cards create exciting moments without overwhelming decision space? Is Sabotage too powerful or too rare? Does the draw rate (2/round) feel right?

---

## 8) Lords

Use the Lord sheets in `lords/`:

- `lords/Seraphel.md` (Lord of the Arcane)
- `lords/Vharok.md` (Lord of Steel)
- `lords/Cassian.md` (Merchant Prince)
- `lords/Elyndra.md` (Warden of Groves)
