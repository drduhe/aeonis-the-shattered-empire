# Aeonis: Advanced Units

Advanced Units are the faction-specific elite forces listed on each Lord sheet under "Special Units." They are the military depth layer of the **full game** — the fantasy counterpart to late-game unit unlocks in games like TI4.

- **First Playable:** Advanced Units are **off** (see `../playtest/First_Playable_Packet.md`).
- **Full game:** on, using this chapter.

This chapter owns the system rules (unlock gates, recruiting, limits, upkeep). The individual unit stats and abilities live on the Lord sheets in `../lords/`.

---

## 1. Definitions

- **Elite Unit**: a faction unit of the first rank. Each Lord has 1 Elite Unit design.
- **Advanced Unit**: a faction unit of the second rank, usually with upkeep. Each Lord has 1 Advanced Unit design (some are typed, e.g., "Advanced Unit (Siege)" or "Advanced Unit (Cavalry)").
- **Mythic Unit**: a faction capstone unit (currently Seraphel's Aether Seer; future Lords may have more). Treated as Advanced for all rules except where stated.
- **Rank**: Elite, Advanced, or Mythic.

Faction units are **military units** for all purposes (ZOC, control, battle line, capture of hexes) unless their sheet says otherwise. A typed faction unit (e.g., "(Cavalry)") also counts as that basic unit type for effects that reference it, but uses its own stats.

---

## 2. Unlock gates

You cannot recruit a faction unit until its rank is unlocked:

| Rank | Unlock requirement |
| --- | --- |
| **Elite** | You control a **Forge** (see `Buildings.md`). |
| **Advanced** | You own at least one **Tier II Arcane Discovery** (see `Arcane.md`). |
| **Mythic** | You have built your **Legendary Building** (see `Buildings.md`). |

- Unlocks are checked **at the moment you recruit**. If you later lose the prerequisite (Forge destroyed, Legendary captured), units already on the map remain, but you cannot recruit more until you requalify.
- Lord sheets may add a **faction prerequisite** on top of these (the sheet says so explicitly).

---

## 3. Recruiting faction units

Faction units are recruited with the normal **Recruit** action (see `Actions.md`), with these defaults:

| Rank | Gold | Mana | Population | Where |
| --- | --- | --- | --- | --- |
| **Elite** | 2 | 1 | 2 | Any City you control |
| **Advanced** | 3 | 1 | 2 | Any City you control |
| **Mythic** | 3 | 3 | 3 | The City containing your Legendary Building |

- A Lord sheet may override these costs; the sheet wins.
- A faction unit counts as **both** units of a Recruit action's 2-unit allowance (it is the only unit you may place with that Recruit action).
- All normal Recruit limits apply (once per City per round, Population availability).

### 3.1 On-map limits

- **Elite:** at most **2** on the map at once.
- **Advanced:** at most **1** on the map at once.
- **Mythic:** at most **1** on the map at once.

These limits are also the component counts (see `../components/Components.md`). If a faction unit is destroyed, it may be recruited again later.

---

## 4. Upkeep

- If a unit's sheet lists an upkeep cost, pay it during **Production & Upkeep** each round (see `Round_Structure.md`, step 6, and `Trade_Taxes.md`).
- **Missed upkeep:** if you cannot or choose not to pay, the unit is **disbanded** immediately — remove it from the map and refund its Population to your pool.
- Elite Units have **no upkeep** unless their sheet says otherwise. Advanced/Mythic Units usually do.

---

## 5. Combat and movement defaults

- **Movement Range:** 1 hex per Move action unless the sheet says otherwise (Cavalry-typed units: 2, per `Movement.md`).
- Faction units occupy Battle Line slots normally and count toward the Battle Line Cap (see `Combat.md`).
- Faction unit abilities that modify combat resolve at the timing their sheet specifies; if the sheet is silent, treat the ability as resolving at the same step as the roll or effect it modifies.
- Faction units are **not** Lords: they cannot be captured, they are destroyed at 0 HP like other units.

---

## 6. Design contract (for new faction units)

Every new faction unit must specify:

- **Rank** (Elite / Advanced / Mythic) and any basic-unit typing.
- **Stats**: Attack die, Defense die, HP (and Movement Range if not 1).
- **Recruit cost** only if it deviates from the §3 defaults.
- **Upkeep** (or "none").
- **One special ability** with an explicit timing window.
- A theme line.

Keep abilities narrow and situational; faction units should feel like sharpened tools, not bigger numbers. Rules reference: this chapter.

---

## 7. Playtest watch-items

- Are Elite units worth 2 Gold + 1 Mana + 2 Population vs 2 basic units for less?
- Does the Forge gate make the Forge an auto-build? (If so, consider moving Elite gates to faction prerequisites.)
- Does missed-upkeep disbanding feel too punishing, or does it create good tension?
- Nyxara's Shade Assassin (ambush placement) and Morvane-style recursion effects are the highest-risk abilities — watch for feel-bad moments.
