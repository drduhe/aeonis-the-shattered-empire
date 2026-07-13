# Aeonis: Map Construction

> **Status:** DRAFT / PROPOSED (Plan 4). Not canon until playtested and registered in `INDEX.md`. First Playable setup in `../playtest/First_Playable_Packet.md` §3 remains authoritative for current tables. See `../docs/plans/2026-07-02-plan-high-player-count.md`.

---

## 1. Purpose

Define reproducible map setup for **3–8 players**: home slices, shared core, geometry constraints, and setup modes. This chapter feeds tile inventory for `../components/Components.md` and `../components/Production_Manifest.md`.

---

## 2. Slice system

Each player receives a **home slice**:

| Slot | Contents |
|---|---|
| Home | 1× **City** (Home City) |
| Resource-strong | 1× printed high-yield terrain (Mountain, Forest, or Desert — balanced across slices) |
| Special-adjacent | 1× **Ruins** or **Portal** (or a tile that guarantees Ruins/Portal within 2 hexes of home) |
| Standard | 2× standard terrain (Plains / Forest / Mountain mix) |
| Open | 1× flexible filler (Plains preferred) |

**Unique starting tiles:** If the Lord sheet specifies a Unique Starting Tile, it replaces the matching home-slice terrain slot (still counts as that terrain for movement). See `Tiles.md` and Lord sheets.

---

## 3. Shared core

All slices attach around a **shared core**:

1. **Imperial Seat** hex (treat as a City) at the center.
2. A **contested ring** of neutral high-value tiles (Deserts, Ruins, Portals, Lakes as choke points).

---

## 4. Per-count geometry (draft targets)

Constraints at every count:

- Every Home City is **≥ 4 hexes** from any other Home City.
- Every Home City is **≤ 4 hexes** from the Imperial Seat's contested ring.
- Each slice's total printed primary production is within **±1** of every other slice.
- Every slice touches at least one Ruins or Portal within **2 hexes** of home.

| Players | Map radius (approx.) | Home slices | Contested-ring tiles (target) | Notes |
|---|---|---|---|---|
| 3 | 3 | 3 | 8–10 | Compact; 1 Desert between each adjacent pair |
| 4 | 3–4 | 4 | 10–12 | First Playable default geometry |
| 5 | 4 | 5 | 12–14 | +~3 neutrals vs 4p |
| 6 | 4 | 6 | 14–16 | Stress-test Docket + Whisper draw |
| 7 | 4–5 | 7 | 16–18 | Possible second Whisper deck fallback |
| 8 | 5 | 8 | 18–20 | Manufacturing gate for 7–8 SKU |

Exact tile IDs and diagrams land when physical counts are frozen; First Playable keeps the verbal presets in the packet until then.

---

## 5. Setup modes

1. **Preset layouts (default for First Playable / teaching):** Follow `First_Playable_Packet.md` §3 (3–4p fully specified; 5–8p scaled from the same rules). Prefer this chapter's geometry table when diagrams exist.
2. **Slice draft (experienced groups):** Deal **2** candidate slices per player; each picks **1**. Place chosen slices around the core in Speaker order (or random seats).

---

## 6. Cross-references

- Control, ZOC, and terrain: `Tiles.md`
- First Playable setup: `../playtest/First_Playable_Packet.md` §3
- Component counts: `../components/Components.md`, `../components/Production_Manifest.md`
- High-count council / Whisper scaling: `High_Council.md` §3.2b, `Whispers.md` §2
