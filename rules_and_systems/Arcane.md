# Aeonis: Arcane Discovery (Research)

Arcane Discovery is Aeonis’ “technology” system: persistent magical and intellectual advancements that players **research** during the Action Phase. It is designed to feel like TI4 tech in play: you choose a path, meet **prerequisites**, and stack long-term advantages.

---

## 1) Key terms and components

- **Discovery**: A permanent upgrade/ability you gain by taking the **Research** action.
- **School**: A discovery’s “color.” Each school supports a different strategy.
- **Sigil**: The prerequisite currency. Each discovery you own grants **1 sigil** of its school.
- **Tier**: How deep/powerful a discovery is. Higher tiers cost more AP/resources and usually require more sigils.
- **Ritual**: A repeatable activated ability unlocked by a discovery (often with a Mana/Influence cost).
- **Upgrade**: A discovery that changes how a unit/building works. (See §5.)

School abbreviations (used throughout this chapter):

- **EVO**: Evocation (war magic)
- **ENC**: Enchantment (wards / craft)
- **DIV**: Divination (information / politics)
- **TRN**: Transmutation (economy / movement / conversion)
- **GEO**: Geomancy (land-shaping / borders / infrastructure)

Optional “forbidden” content:

- **NEC**: Necromancy (risk/reward; Population sacrifice). Not required for a first implementation; add later as an expansion module.

---

## 2) Discovery “card” anatomy (rules template)

Each discovery entry should specify:

- **Name**
- **School** (EVO / ENC / DIV / TRN)
- **Tier** (I / II / III)
- **Prerequisites** (sigils required)
- **Research cost** (resources) and **Research AP** (AP cost)
- **Rules text** (passive and/or ritual)
- **Type**: Passive / Ritual / Upgrade (optional but recommended)

---

## 3) Prerequisites (sigils) — TI4-style progression

### 3.1 Gaining sigils

When you gain a discovery, you immediately gain **1 sigil** of its school for prerequisite purposes.

Example:

- If you have 2 Evocation discoveries, you have **EVO 2**.

### 3.2 Meeting prerequisites

To research a discovery, you must meet its prerequisite line.

- **Prerequisites are checked at the moment you research.**
- **Sigils are not spent.** They are an ongoing requirement, like TI4 tech colors.

### 3.3 Specialties (tech-skip equivalent; optional but recommended)

Some tiles, buildings, artifacts, or Lord abilities may grant a **School Specialty** (a “skip”) that counts as **+1 sigil of a specific school** when checking prerequisites.

- Specialties **do not** give you the discovery’s effect.
- Specialties **do not** increase your sigil totals for future prerequisites unless the effect explicitly says so (default: they only apply during checks).

Examples of where specialties can live:

- A **unique starting tile** (see `Tiles.md`) that says “counts as **DIV specialty**.”
- An **Academy** upgrade line (see `Buildings.md`) that says “you have an **ENC specialty**.”
- A **relic** that says “while equipped, you have **TRN specialty**.”

---

## 4) Researching a discovery (core action)

### 4.1 When you can research

During the **Action Phase**, on your turn, you may take the **Research** action (see `Round_Structure.md`).

### 4.2 The Research action

1. **Choose** one discovery you do not already own.
2. **Check prerequisites** (sigils + any specialties).
3. **Pay AP** for the discovery’s tier:
   - **Tier I**: 1 AP
   - **Tier II**: 2 AP
   - **Tier III**: 3 AP
4. **Pay resources** (the discovery’s listed cost).
5. **Gain the discovery**: its effect becomes active immediately unless it specifies a timing window.
6. **Gain Remnants**: Gain Remnants based on the discovery's tier:
   - **Tier I**: 1 Remnant.
   - **Tier II**: 2 Remnants.
   - **Tier III**: 3 Remnants.
   See `Artifacts.md` for Remnant rules.

Notes:

- **One discovery per Research action.**
- If an effect says you “research for free,” you still choose a legal discovery, but you **ignore** its AP and resource costs unless the effect says otherwise.

### 4.3 Default resource costs (if a discovery does not list one)

Use these defaults (tune later):

- **Tier I**: 2 Mana
- **Tier II**: 4 Mana
- **Tier III**: 6 Mana

---

## 5) Upgrades (units and buildings)

Some discoveries are **Upgrades**. They change how a unit/building works for you.

### 5.1 Upgrade application (simple, TI4-like)

- Once you own an Upgrade, **future** recruits/builds of the upgraded thing use the upgraded rules.
- Existing pieces already on the map are **not** automatically upgraded (unless the upgrade says they are).

---

## 6) Integration hooks (how other systems can reference research)

- **Renown** (`Renown.md`): thresholds may grant discounts or “free Tier I” research.
- **Exploration / Ruins** (`Events.md`, `Tiles.md`): ruins can grant a specialty token or a one-time research discount.
- **Buildings** (`Buildings.md`): Academy / Forge can add specialties, discounts, or unlock Upgrade-only discoveries.
- **Strategy Cards** (`Strategy.md`): effects that grant “free research” should reference Tier I/II/III discoveries defined here.
- **Artifacts** (`Artifacts.md`): Completing any research generates Remnants. Some artifacts grant School Specialties or research bonuses.

---

## 7) Core Discovery Set (v1 starter list)

This is a **small, testable** initial set. Expand it once pacing and power level feel right.

Unless a discovery says otherwise, modifiers apply as:

- **“+1 to a roll”** means add 1 to the rolled value after rolling (minimum 1 is implicit).

### 7.1 Evocation (EVO)

1. **Battle Runes** (EVO • Tier I • Prereq: none • Cost: 2 Mana • Type: Ritual)  
   Once per battle round, before one of your Battle Line units rolls its Attack Die, you may spend **1 Mana**. If you do, add **+1** to that unit’s Attack roll.

2. **Searing Salvo** (EVO • Tier I • Prereq: none • Cost: 2 Mana • Type: Ritual)  
   When you declare an Attack, you may spend **2 Mana** to deal **1 damage** to one enemy unit currently on the Battle Line (if no Battle Line is formed yet, the defender chooses which of their committed units would take this damage once lines are formed).

3. **Storm Discipline** (EVO • Tier II • Prereq: EVO 1 • Cost: 4 Mana • Type: Passive)  
   The first time each round you **Press the Attack** (see `Combat.md`), the +1 AP cost is reduced to **0 AP**.

4. **Pyric Momentum** (EVO • Tier III • Prereq: EVO 2 • Cost: 6 Mana, 1 Influence • Type: Passive)  
   The first time each round you win a battle as the attacker (capture the target hex), gain **+1 Renown**.

### 7.2 Enchantment (ENC)

1. **Sigiled Masonry** (ENC • Tier I • Prereq: none • Cost: 1 Mana, 1 Gold • Type: Passive)  
   Once per round, when you build a **basic production building** (Farm/Mine/Grove/Embassy), reduce its **build cost** by **1** (minimum 0).

2. **Warding Charm** (ENC • Tier I • Prereq: none • Cost: 2 Mana • Type: Ritual)  
   Once per battle round in which you are the defender, after a defending Battle Line unit rolls its Defense Die, you may spend **1 Mana** to add **+1** to that Defense roll.

3. **Fortified Hexes** (ENC • Tier II • Prereq: ENC 1 • Cost: 3 Mana, 1 Gold • Type: Passive)  
   The first battle round each time an enemy declares an Attack targeting a hex you control that contains one of your **buildings**, your defending Battle Line units get **+1** to their first Defense rolls that battle round (apply to at most **2** units per battle round).

4. **Binding Vows** (ENC • Tier III • Prereq: ENC 2 • Cost: 5 Mana, 2 Influence • Type: Ritual)  
   Once per round, after a player initiates a **Trade** with you (see `Trade_Taxes.md`) you may declare a **Vow**. Until end of round, that player cannot declare an Attack targeting one of your controlled hexes unless they pay **+1 AP** for that Attack action.

### 7.3 Divination (DIV)

1. **Scrying Pool** (DIV • Tier I • Prereq: none • Cost: 2 Influence • Type: Passive)  
   At the start of the **High Council Phase**, you may look at the top card of the agenda deck and put it back.

2. **Battle Augury** (DIV • Tier I • Prereq: none • Cost: 1 Mana, 1 Influence • Type: Ritual)  
   Once per battle round, before an enemy Battle Line unit rolls its Attack Die, you may spend **1 Influence**. If you do, that unit’s Attack roll gets **-1** this battle round (minimum 1).

3. **Omen of Shelter** (DIV • Tier II • Prereq: DIV 1 • Cost: 2 Mana, 2 Influence • Type: Ritual)  
   Once per round, when a **Global Event** is revealed (see `Events.md`), you may spend **2 Influence**. If you do, you ignore that event’s effect (only for you).

4. **Foreknowledge** (DIV • Tier III • Prereq: DIV 2 • Cost: 3 Mana, 3 Influence • Type: Passive)  
   During **Round Start**, you may look at the top **2** cards of the Global Event deck and put them back in any order.

### 7.4 Transmutation (TRN)

1. **Golden Alchemy** (TRN • Tier I • Prereq: none • Cost: 2 Mana • Type: Passive)  
   During **Production & Upkeep**, you may convert up to **2 Mana → 3 Gold** total (once per round).

2. **Waystones** (TRN • Tier I • Prereq: none • Cost: 1 Mana, 1 Gold • Type: Passive)  
   Once per round, when you take a **Move** action, reduce the total AP cost of that move by **1** (minimum 1).

3. **Translocation** (TRN • Tier II • Prereq: TRN 1 • Cost: 4 Mana • Type: Ritual)  
   On your turn, when you take a **Move** action, you may instead pay **1 AP** and spend **3 Mana**. If you do, choose one of your unit groups in a controlled **City** or controlled **Portal** and place it in any hex you control. (This replaces normal movement for that action.)

4. **Leyline Logistics** (TRN • Tier III • Prereq: TRN 2 • Cost: 4 Mana, 2 Gold • Type: Passive)  
   Once per round, after you resolve a **Build** action in a City you control, gain **+1 AP** immediately. (This AP can be spent later this round.)

### 7.5 Geomancy (GEO)

Geomancy is the “realmcraft” school: shaping borders, choke points, and the arcane infrastructure that makes regions defensible and connected.

1. **Boundary Stones** (GEO • Tier I • Prereq: none • Cost: 1 Mana, 1 Influence • Type: Passive)  
   Once per round, during **Cleanup & Checks**, you may choose 1 **neutral** hex adjacent to a **City** or **Tower** you control. If that hex contains **no enemy units**, you gain control of it.

2. **Stonewright** (GEO • Tier I • Prereq: none • Cost: 1 Mana, 1 Gold • Type: Passive)  
   Once per round, when you build a **Tower**, **Fortress**, or **Bridge**, reduce that building’s **build cost** by **1 Gold** (minimum 0).

3. **Ley Anchors** (GEO • Tier II • Prereq: GEO 1 • Cost: 3 Mana, 1 Influence • Type: Passive)  
   Choose 1 hex you control that contains a **City**, **Tower**, or **Fortress**. While you control it, that hex grants you a **GEO specialty** when checking discovery prerequisites (see §3.3).

4. **Seal the Gate** (GEO • Tier III • Prereq: GEO 2 • Cost: 5 Mana, 2 Influence • Type: Ritual)  
   Once per round, on your turn, choose 1 **Portal** hex you control. Until end of round, other players cannot use **Portal travel (Portal → Portal)** to enter that Portal hex. (They may still enter it normally by moving adjacent and paying enter costs.)

---

## 8) Lord-specific discoveries (design contract)

Each Lord may have 1–3 **Lord-specific** discoveries. These follow the same core rules:

- They have a school, tier, prerequisites, and costs.
- Only that Lord may research them.
- They should usually either (a) reinforce the Lord’s theme, or (b) grant a specialty/discount hook that helps the Lord reach a distinct tech profile.

If a Lord-specific discovery is missing a Tier/Prereq line, treat it as **Tier II** with prerequisite **1 sigil** of its listed school until it is updated.
