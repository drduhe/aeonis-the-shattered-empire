# Aeonis: First Playable Packet (2–4 players)

This packet is a **small, concrete, testable** version of Aeonis meant to be played in ~90–180 minutes while exercising the core loop:

**Strategy pick → High Council → rotating actions (AP) → battles → production/upkeep → events → VP race.**

It deliberately restricts content so playtests focus on **pacing, map flow, and interaction**.

---

## 1) What rules are “on”

Use these chapters as written:

- `Round_Structure.md`
- `High_Council.md`
- `Actions.md`
- `Movement.md`
- `Combat.md`
- `Tiles.md`
- `Population.md`
- `Trade_Taxes.md`
- `Buildings.md`

First Playable restrictions are listed below where needed.

---

## 2) Player count and victory

- **Players**: 2–4
- **Victory threshold**: **8 VP** triggers the final round; highest VP at end of that round wins (ties: most Renown, then most Influence).

---

## 3) Setup (map + starting state)

### 3.1 Map layout

Build a small map with:

- 1 central tile: **Imperial Seat** (treat as a City).
- One “home cluster” per player placed around it (each cluster touches the central ring).

**Home cluster per player (4 tiles):**

- 1× City (your home city)
- 1× Plains
- 1× Forest
- 1× Mountain

**Unique starting tiles (First Playable rule):**

- If your Lord sheet includes a **Unique Starting Tile**, replace the specified home-cluster tile with that unique tile (it still counts as the listed terrain type for movement and most rules; see `Tiles.md`).

**Neutral ring:**

- Place 1× Desert between each pair of home clusters (so deserts become political flashpoints).
- Place 2× Ruins anywhere in the neutral ring.
- Place 2× Portals anywhere in the neutral ring (not adjacent to each other).
- Place 2× Lakes anywhere that creates at least one meaningful choke point (bridges exist in this packet).

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

### 3.4 Starting units (per player)

Place in your Home City:

- 3× Infantry
- 1× Archer

### 3.5 Starting control

You begin controlling your home cluster:

- Your City + your Plains + your Forest + your Mountain

Neutral tiles start neutral.

---

## 4) Allowed content (tight scope)

### 4.1 Units (allowed)

Use only the baseline units from `Combat.md`:

- Infantry, Cavalry, Archers

(No advanced units in First Playable.)

### 4.2 Buildings (allowed)

Allowed:

- Farm, Mine, Grove, Embassy
- Tower
- Fortress
- Guild Hall
- Market
- Bridge

Not used in First Playable:

- Academy, Forge/Arcane Forge, Bank, Castle, Legendary Buildings (save for later balance passes)

### 4.3 Strategy cards (use 6)

Use these six from `Strategy.md` (print as cards):

1. **Arcane Ascendancy**
2. **Resource Surge**
3. **Military Maneuvers**
4. **Diplomatic Decree**
6. **Tactical Reinforcements**
7. **Economic Boom**

### 4.4 Objectives (print 6 public + 6 secret)

**Public Objectives (2 VP each):**

- **Frontier Lord**: Control 7 hexes.
- **Builder**: Have 3 buildings in play.
- **Council Power**: Win 2 High Council votes you proposed.
- **Portal Mastery**: Control a Portal and use Portal travel at least once.
- **Warlord**: Win 2 battles (attacker or defender).
- **Seat of Empire**: Control the Imperial Seat at Cleanup & Checks.

**Secret Objectives (3 VP each):**

- **Hidden Arsenal**: Build a Fortress and win a battle involving that hex.
- **Golden Hoard**: Have 10 Gold at once.
- **Mana Flood**: Have 10 Mana at once.
- **The Quiet Knife**: Take control of a hex via Influence (annexation/arbitration/Influence takeover).
- **Borderbreaker**: End the round with units in 3 different regions of the map (define regions by table agreement).
- **Architect of Control**: Control 2 special tiles (any combination of City/Ruins/Portal/Imperial Seat).

Setup:

- Each player draws 1 public + 1 secret at start.
- At the start of Round 3, each player draws 1 additional secret.

### 4.5 Events (print 8 global + 8 exploration)

**Global Events (resolve in Event Phase):**

- **Harsh Winter**: Each player loses 2 Gold unless they control at least 1 Farm.
- **Festival**: All players gain +1 AP next round.
- **Migration Wave**: Each player with at least 2 Plains gains +2 Population Pool (up to cap).
- **Council Crisis**: The Speaker must put a motion on the agenda; if it fails, Speaker loses 1 Renown.
- **Mana Surge**: Each player gains +2 Mana.
- **Border Skirmishes**: The player with the most controlled hexes gains +1 Renown; ties: all tied gain +1 Renown.
- **Supply Disruption**: Each player must discard 2 total resources (any mix of Gold/Mana/Influence).
- **Open Roads**: Until end of round, movement across Plains costs 1 less AP (min 1).

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

## 5) High Council “agenda deck” (8 cards)

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

## 6) Playtest goals (what to watch)

1. **Pacing**: Do rounds stay snappy with “one battle round per Attack” and Move path-cost AP?
2. **Map flow**: Do Lakes + Bridges create fun chokepoints without stalling play?
3. **Politics**: Does the High Council matter every round without taking over the session?
4. **War feel**: Do front lines emerge naturally with Battle Line/Reserves and sieges?
5. **Economy feel**: Does Population-as-cap create meaningful tradeoffs vs buildings and army size?

---

## 7) Lords

Use the Lord sheets in `lords/`:

- `lords/Lord_of_the_Arcane.md`
- `lords/Lord_of_Steel.md`
- `lords/Merchant_Prince.md`
- `lords/Warden_of_Groves.md`

