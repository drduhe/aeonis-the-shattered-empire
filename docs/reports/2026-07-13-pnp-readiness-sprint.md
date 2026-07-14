# Synchronization + PnP Readiness Sprint — 2026-07-13

## Outcome

The First Playable is now runnable from a repeatable, low-ink US Letter print-and-play kit. The generator treats the Markdown chapters and simulator map builder as sources; generated PDFs remain derived artifacts.

## Synchronization completed

- Corrected derived objective, Coronation Rite, artifact, and Legendary Building scoring language in the teaching documents.
- Corrected the First Playable event inventory to **12 global + 9 exploration** and the Strategy inventory to **8 cards at every player count**.
- Replaced the ambiguous Borderbreaker condition with an explicit **Cleanup & Checks** window and three pairwise distances of 3 or more.
- Synchronized Legendary Building scoring on all 12 Lord sheets to **2 VP once on construction**.
- Synchronized setup Population: Lord units occupy 0; available Pool equals Cap minus the listed starting army. Most launch Lords start at **10 / 7** Cap / Pool; Rakhis starts at **10 / 6**.
- Added explicit Production & Upkeep windows to Realm Tax and Hero of the Realm.
- Refreshed the balance-dashboard watch values, ambiguity-ledger statuses, test-count reference, and obsolete Codex filenames.

## Generated kit

| PDF | Pages | Contents |
| --- | ---: | --- |
| `aeonis-first-playable-cards.pdf` | 19 | 109 cuttable poker-size cards |
| `aeonis-first-playable-reference-kit.pdf` | 19 | Cover, six setup maps, eight launch-Lord sheets, player board, three-page Player Aid |
| `aeonis-first-playable-tokens-and-map-proxies.pdf` | 7 | 91 proxy map hexes, per-player pieces, shared buildings, Remnants, sites, siege markers, and Legendaries |

Card inventory gate: 8 Strategy + 6 public + 6 secret + 12 global events + 9 exploration events + 8 agendas + 26 Whispers + 24 artifacts + 10 Tier I Discoveries = **109**.

## Verification

- Generator inventory assertions: passed.
- Manifest JSON parse and file existence validation: passed.
- Final PDFs: **45 pages total**, all rendered to PNG and visually inspected by layout family and dense-page samples.
- PDF text extraction, page-count, Letter-size, and nonblank-page checks: passed.
- Simulator regression suite: passed (**350 tests**).
- Terminology and timing-window sweeps: passed subject to the repository's documented historical exceptions.

## What this does not claim

- This is prototype usability, not final graphic design, accessibility certification, prepress, or manufacturer dieline approval.
- Card backs are intentionally omitted; sleeves or opaque cardstock are recommended.
- The proxy hexes use a compact table footprint and are not the final manufactured tile scale.
- No human sessions have been logged yet. Balance conclusions remain sim-only until the owner schedules human play.
- The kit covers First Playable content, not the incomplete full-game decks or expansion Lord balance pass.

## Regenerate

From the repository root, with ReportLab installed:

```powershell
python pnp/generate_pnp.py
```

See `../../pnp/README.md` for print and assembly instructions.
