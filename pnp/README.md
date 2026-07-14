# Aeonis First Playable — Print-and-Play Kit

This folder owns the repeatable generator for the low-ink **First Playable** prototype. The generated PDFs are derived artifacts; they do not override the canonical Markdown rules.

## Ready-to-print files

- [`aeonis-first-playable-cards.pdf`](../output/pdf/aeonis-first-playable-cards.pdf) — 109 poker-size cards: 8 Strategy, 6 public objectives, 6 secret objectives, 12 global events, 9 exploration events, 8 agendas, 26 Whispers, 24 artifacts, and 10 Tier I Discoveries.
- [`aeonis-first-playable-reference-kit.pdf`](../output/pdf/aeonis-first-playable-reference-kit.pdf) — setup maps for 3–8 players, eight launch-Lord references, player board, and Player Aid.
- [`aeonis-first-playable-tokens-and-map-proxies.pdf`](../output/pdf/aeonis-first-playable-tokens-and-map-proxies.pdf) — small-footprint map hexes plus player, building, artifact, and status tokens.

## Print and assemble

1. Print on US Letter paper at **100% / actual size**. Do not use “fit to page.”
2. Cut cards on their solid borders. Sleeve with spare cards or mount to cardstock; no card backs are required for prototype testing.
3. Print the “One Player’s Pieces” token page once per player, preferably on a distinct paper color. Print the player-board page once per player.
4. Cut only the map proxy hexes required by the chosen player-count layout. The two proxy pages contain the maximum eight-player inventory.
5. Supply at least 4× d4, 6× d6, 4× d8, and 4× d10. Pencils, cubes, coins, or glass beads can replace any trackers or resource tokens.

For faster assembly, use generic hex tiles or draw the selected map diagram on a dry-erase hex mat; use cubes for units and control markers. The PDFs are intended to make the game runnable, not to lock final graphic design or manufactured component scale.

## Regenerate

Install ReportLab, then run from the repository root:

```powershell
python pnp/generate_pnp.py
```

The generator reads the Strategy, objective, event, Whisper, artifact, Discovery, Lord, Player Aid, and simulator map sources. It fails if any First Playable card category no longer matches its reviewed count, making component drift visible during canon changes.

After generation, render every PDF page to PNG and inspect the result as described by the repository’s PDF workflow. The generated outputs belong in `output/pdf/`; temporary renders belong in `temp/`.

## Canon and propagation

- Timing: `rules_and_systems/Round_Structure.md`
- System rules: the owning `rules_and_systems/*.md` chapter
- First Playable restrictions: `playtest/First_Playable_Packet.md`
- Component inventory: `components/Components.md`
- Printable derivation: this generator

When behavior or inventory changes, update the owning document and all dependent documents, simulator behavior, and this kit in the same pass. Follow `agents/checklists/Canon_Change_Checklist.md`.
