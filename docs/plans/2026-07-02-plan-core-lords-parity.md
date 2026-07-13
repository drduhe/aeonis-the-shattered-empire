# Plan 5: Core Lords Parity Pass

- **Status:** **PROMOTED 2026-07-09** — signature redesigns are canonical and registered in `rules_and_systems/INDEX.md`. Sim-led validation; human confirmation remains pending.
- **Date:** 2026-07-02
- **Owning docs:** the 8 core Lord sheets (`lords/Cassian.md` … `lords/Thalrik.md`)
- **Related plans:** Plan 1 (Engaged state — Rakhis synergy), Plan 4 (Docket — Ozren/Auriel council effects), Plan 6 (Diplomacy binding deals — Cassian)

---

## 1. Problem

Faction asymmetry is the marketing pitch ("the fantasy setting unlocks unique mechanical experiences" — `marketing/Positioning.md`), but the **expansion roster now out-designs the launch roster**. The four newest Lords each bend a core system: Serathis *lives on Lakes*, Morvane *raises the dead* with an exclusive magic school, Tsuvara *moves her home City*, Ozren *flips votes and hexes without combat*. Most core-8 abilities are numeric modifiers: +1 Defense here, −1 AP there, +1 Gold on a trigger.

**Concrete duplication found during audit:** Seraphel's *Arcane Efficiency*, Vharok's *Siegecraft*, and the EVO Tier II discovery *Storm Discipline* are all the same effect (free Press the Attack once per round/condition). The "Lord of the Arcane" has **no research-related ability at all** — his identity is expressed only by his tile and faction discoveries.

## 2. The Signature Bar

Every Lord must pass all four tests:

1. **Bends one core system** — breaks a rule everyone else follows (not just a discount on it).
2. **Visible most rounds** — a spectator can tell who you're playing by watching one round.
3. **Creates a distinct victory lean** — the bend implies a strategy no other Lord executes the same way.
4. **One sentence to teach** — "she lives on lakes," "he raises the dead," "her city moves."

## 3. Audit of the core 8

| Lord | Current signature | Bar? | Gap |
|---|---|---|---|
| Cassian | Trade AP discount; +1 Gold after lobbying | ✗ | Pure numeric income; no bend |
| Seraphel | Free Press (duplicate!); agenda peek (duplicates DIV *Scrying Pool*) | ✗ | Off-theme; both abilities duplicated elsewhere |
| Vharok | +1 Def w/ building; free Press vs sieges | ✗ | Thematic but numeric |
| Elyndra | +1 Population; Forest defense reroll | ✗ | Numeric |
| Rakhis | Desert cost 1 (others 2); post-win free 1-hex move | ~ | Half a bend; sharpen |
| Nyxara | Draws 3 Whispers, hand 8; peek on others' plays | ✓ | Passes (info-economy bend) |
| Auriel | +1 Renown per passed motion she backed; Lord-aura Defense | ~ | Income, not a bend |
| Thal'rik | Uses **any** Portal, ignoring treaties | ✓ | Passes (map-topology bend) |

Five of eight need work; two need sharpening; one passes clean. Priority order: **Seraphel, Cassian, Elyndra, Vharok, Auriel**, then Rakhis sharpening.

## 4. Per-Lord signature briefs (direction, to be designed individually)

Each brief replaces or upgrades the *weakest existing ability* — sheets keep three abilities total; no ability inflation.

- **Seraphel — "Polymath."** The research system bends for him: Seraphel counts **+1 sigil of every school** when checking prerequisites, and once per round may take a **second Research action** in the same turn (paying all costs). Delete *Arcane Efficiency* (the duplicate). Victory lean: first to Tier III, Ritual-stacked late game. *One sentence: "He researches like the empire never fell."*
- **Cassian — "The Consortium's Ledger."** The deal system bends for him: Cassian may make one deal per round **binding** (per `Diplomacy.md` §1, which normally only binds immediate exchanges), and may initiate one Trade per round at **0 AP even when it is not his turn**. Victory lean: the table's bank; everyone's plans route through him. *"He is the market."*
- **Elyndra — "The Deep Roots."** Map connectivity bends for her: once per round, one of her unit groups may move between **any two Forest hexes she controls** as if adjacent (1 AP). Her forests become a private road network — a green mirror of Thal'rik's portals. *"Her forests are one forest."*
- **Vharok — "Bastion Doctrine."** The siege system bends for him: Vharok may declare **Hold the Walls in any hex containing one of his buildings** (not just Cities), and his Battle Line cap is **+1 when defending** such a hex. Every Tower and Mine becomes a keep. *"Every wall is his wall."*
- **Auriel — "The Tree's Assent."** The council bends for her: once per round she may **sanctify one motion** — her Council Votes count **double** on it, and if it passes she scores the existing Divine Mandate Renown twice. (If Plan 4's Docket lands: sanctifying also lets her place a motion on the docket without bidding, once per game.) *"The Tree votes through her."*
- **Rakhis — "Sandstride" (sharpen).** His groups treat Deserts as 1 AP, ignore enemy ZOC surcharges, may retreat once per battle before the first Pre-Strike, and keep the existing post-win free move. This uses existing ZOC and retreat rules rather than Plan 1's unpromoted Engaged term. *"You cannot pin the wind."* **Update 2026-07-12:** Dial 3 removed ZOC-ignore; Dial 3b tried dropping retreat and was **reverted** — current Sandstride is Desert 1 AP + pre-Pre-Strike retreat (see `lords/Rakhis.md`).
- **Nyxara, Thal'rik** — no redesign; re-cost only if playtests show drift.

## 5. Process

1. **Write the design contract** (§2 bar + guardrails below) into a short "Lord design contract" section in `rules_and_systems/INDEX.md` so future Lords are held to it.
2. **Batches of two** (pair each redesign with a near-passing Lord for contrast): Seraphel+Cassian → Elyndra+Vharok → Auriel+Rakhis.
3. Per batch: draft sheet edits → cross-reference audit (each bend touches an owning chapter; see §7) → 2 head-to-head playtests vs. unchanged Lords → lock or iterate.

**Guardrails**

- **Parity of interest, not power.** Target win rates stay within the Balance Dashboard band (each Lord 35–65% in its matchups); the goal is that every Lord *feels* like a different game.
- **The teaching pair stays simple.** Rakhis and Vharok anchor the First Playable teaching game (`playtest/First_Playable_Packet.md`); their redesigns must not add setup complexity or new tokens. (Rakhis's Sandstride is a removal of a rule for him — acceptable. Vharok's Bastion is one sentence — acceptable.)
- **No new components** beyond what `Components.md` already lists, except at most one marker type per Lord.

## 6. Playtest validation

**Execution record (2026-07-09):** The six redesigned sheets and all owning/derived chapters were propagated in one pass. Nine deterministic M4 tests cover setup and signature hooks; the rotating 40-game foundation bracket completed 40/40 without crash, timeout, or degeneracy. Because human playtesters are unavailable, the blind-identification test and matchup win-rate band remain human-confirmation gates rather than blockers to sim-led promotion. The small partial-M4 balance read is preserved in `../reports/2026-07-09-plan5-m4-foundation.md`; it must not be used for tuning until full M4 fidelity lands.

- **Blind identification test:** an observer watching rounds 2–4 should name the Lord from play pattern alone — target 6/8 correct.
- **Win-rate band:** 35–65% per Lord across the pairing matrix (`Balance_Dashboard.md` Lord tracker).
- **Strategy-spread check:** VP-source distribution per Lord should differ measurably (Seraphel research-heavy, Cassian trade/politics, Vharok defense/military).
- **Kill criteria per brief:** e.g., if Cassian's off-turn trade slows the Action Phase (constant interrupts), restrict to once per other player's turn; if Elyndra's root network makes her uncatchable, limit to groups of ≤ 3 units.

## 7. Rule-text changes and propagation checklist

| Doc | Change |
|---|---|
| `lords/Seraphel.md`, `Cassian.md`, `Elyndra.md`, `Vharok.md`, `Auriel.md`, `Rakhis.md` | Ability rewrites per §4 |
| `rules_and_systems/Arcane.md` | Note Seraphel's Polymath in §3.3 (specialty interactions) |
| `rules_and_systems/Diplomacy.md` | Cassian's binding-deal exception |
| `rules_and_systems/Movement.md` / `Tiles.md` | Elyndra's Forest adjacency; Rakhis disengage cross-ref |
| `rules_and_systems/Combat.md` | Vharok Hold-the-Walls exception; Rakhis Engaged exemption |
| `rules_and_systems/High_Council.md` | Auriel sanctify timing (and Docket interaction if Plan 4 lands) |
| `rules_and_systems/INDEX.md` | Lord design contract section |
| `playtest/First_Playable_Packet.md` §8 | Rakhis/Vharok stat blocks & ability text |
| `rulebook/Learn_to_Play.md`, `rulebook/Player_Aid.md` | Teaching-pair ability text |
| `playtest/Balance_Dashboard.md` | Lord tracker rows note redesign dates (before/after comparability) |

## 8. Sequencing

Executed independently of Plan 1 by expressing Rakhis through existing ZOC and retreat windows. M4 Lord-asymmetry implementation may now proceed without a sheet-redesign blocker.
