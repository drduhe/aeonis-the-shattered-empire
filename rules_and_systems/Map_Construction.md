# Aeonis: Map Construction

> **Status:** Geometry **SIM-VALIDATED 2026-07-13** and promoted for First Playable presets; slice drafting, Docket, and high-count Whisper changes remain PROPOSED pending humans. See `../docs/reports/2026-07-13-plan4-geometry-spacing.md`.

---

## 1. Purpose

Define reproducible map setup for **3–8 players**: home slices, shared core, geometry constraints, and setup modes. This chapter feeds tile inventory for `../components/Components.md` and `../components/Production_Manifest.md`.

---

## 2. Slice system

Each player receives a **home cluster** in the validated preset and a six-slot **home slice** in the experienced slice-draft variant:

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

Validated constraints:

- Home Cities are placed in angular order around the outer ring, never by coordinate-row order.
- Every Home City is **≥ 4 hexes** from any other Home City at 3–7 players. At 8 players, the radius-5 perimeter supports a validated minimum of **3**; requiring 4 would require a larger/sparse radius-6 design and substantially more tiles.
- Every Home City is **≤ 4 hexes** from the Imperial Seat's contested ring.
- Each slice's total printed primary production is within **±1** of every other slice.
- Every slice touches at least one Ruins or Portal within **2 hexes** of home.

| Players | Radius | Total hexes | Min home distance | Contested tiles | Hexes/player |
|---:|---:|---:|---:|---:|---:|
| 3 | 3 | 37 | 5 | 9 | 12.33 |
| 4 | 3 | 37 | 4 | 10 | 9.25 |
| 5 | 4 | 61 | 4 | 12 | 12.20 |
| 6 | 4 | 61 | 4 | 13 | 10.17 |
| 7 | 5 | 91 | 4 | 17 | 13.00 |
| 8 | 5 | 91 | 3 | 18 | 11.38 |

**Contested tiles** are Deserts, Ruins, Portals, and Lakes. Across 200 generated presets per count, every home met Ruins/Portal access, every starting-production spread stayed within ±1, and every Seat-ring distance stayed within 4.

### 4.1 Reproducible preset procedure

1. Tile a complete axial hex disk at the radius in the table; place the Imperial Seat at `(0, 0)`.
2. Sort outer-ring coordinates by geometric angle and place Home Cities at evenly spaced indices. This angular sort is mandatory; sorting by row clusters homes at high counts.
3. In Speaker order, place each three-tile starting cluster inward from its Home City: 1 Plains, 1 Forest, and 1 Mountain. Apply Unique Starting Tile substitutions afterward.
4. Place Portals non-adjacent, then Ruins, prioritizing uncovered homes until every home has one of those special tiles within distance 2.
5. Place one Desert in the neutral gap between each adjacent home pair; add Lakes per the count table; fill remaining hexes evenly with Plains, Forest, and Mountain.

The simulator's `hexmap.py` is the executable reference for this preset algorithm. Axial anchor coordinates are deterministic by player count; neutral placement may vary by seed while preserving all gates.

---

## 5. Setup modes

1. **Preset layouts (default for First Playable / teaching):** Follow the validated geometry table and procedure above, summarized in `First_Playable_Packet.md` §3.
2. **Slice draft (experienced groups):** Deal **2** candidate slices per player; each picks **1**. Place chosen slices around the core in Speaker order (or random seats).

---

## 6. Cross-references

- Control, ZOC, and terrain: `Tiles.md`
- First Playable setup: `../playtest/First_Playable_Packet.md` §3
- Component counts: `../components/Components.md`, `../components/Production_Manifest.md`
- High-count council / Whisper scaling: `High_Council.md` §3.2b, `Whispers.md` §2
