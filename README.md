# Aeonis: The Shattered Empire

Working design repository for a Kickstarter-bound epic fantasy grand-strategy board game — TI4-scale sessions (4–10 hours, 3–8 players) in a world of banished Lords, Arcane Discoveries, and player-authored politics.

This is **not** a playable digital game. It is the canonical rules corpus, playtest tooling, marketing site, and AI-assisted design workflow for the physical product.

---

## Start here

| If you want to… | Open |
| --- | --- |
| Learn the game | [`rulebook/Learn_to_Play.md`](rulebook/Learn_to_Play.md) → [`playtest/First_Playable_Packet.md`](playtest/First_Playable_Packet.md) |
| Browse all docs in a UI | [`codex.html`](codex.html) (local) or [GitHub Pages site](https://drduhe.github.io/aeonis-the-shattered-empire/) |
| See what's canon vs proposed | [`rules_and_systems/INDEX.md`](rules_and_systems/INDEX.md) |
| Run balance experiments | [`sim/README.md`](sim/README.md) |
| Contribute with an AI assistant | [`AGENTS.md`](AGENTS.md) |
| Check locked product decisions | [`marketing/Positioning.md`](marketing/Positioning.md) |

**Canon hierarchy (short version):** `Round_Structure.md` owns timing → each system chapter owns its mechanic → `First_Playable_Packet.md` may override via explicit "First Playable rule" → `INDEX.md` is the decision log. Anything in `docs/plans/` marked PROPOSED is **not** canon until playtested and registered in `INDEX.md`.

---

## Core loop

**Event → Strategy pick → High Council → rotating actions (AP) → production/upkeep → cleanup → VP race** (10 VP standard; 8 VP short game).

Major systems (each has an owning chapter in `rules_and_systems/`):

- **AP economy** — rotating turns, variable costs, passing, limited banking (`Actions.md`)
- **Map** — hex tiles, terrain production, control/borders, unit-based ZOC (`Tiles.md`, `Movement.md`)
- **Conflict** — battle line + reserves, sieges, Lord capture (+1 VP, ability lockout) (`Combat.md`)
- **Progression** — Arcane Discoveries, Buildings (incl. Legendary capstones), Artifacts, Whispers (`Arcane.md`, `Buildings.md`, `Artifacts.md`, `Whispers.md`)
- **Politics** — High Council motions, Renown, Influence (`High_Council.md`, `Renown.md`)
- **Victory** — public/secret objectives, council titles, Coronation Rite, combat, events (`Victory.md`, `Objectives.md`)
- **Turn order** — 8-card Strategy deck with primaries and opt-in secondaries (`Strategy.md`)
- **Growth & trade** — Population cap, upkeep, player-initiated trade (`Population.md`, `Trade_Taxes.md`)
- **Setting** — Speaking Stones, rediscovered magic, banished Lords (`lore/Lore.md`, `lore/Naming_Bible.md`)

Eight launch Lords + four expansion roster sheets live in [`lords/`](lords/).

---

## Repository map

```
rules_and_systems/   Mechanic chapters + INDEX.md (TOC + decision log)
playtest/            First Playable packet, balance dashboard, session log, ambiguity ledger
lords/               12 faction sheets (8 launch + 4 expansion)
rulebook/            Learn to Play + Player Aid (derived teaching docs)
lore/                Worldbook + Naming Bible (terminology canon)
components/          Prototype kit + production BOM
marketing/           Positioning, pitch, campaign plan, comps
sim/                 Python engine-authoritative playtest simulator
docs/plans/          Dated design plans (PROPOSED ≠ canon)
docs/reports/        Sim tournament and playtest HTML/MD reports
agents/              AI roles, templates, canon-change checklists
mcp/aeonis-tools/    Doc validation MCP server (manifest, links, lint)
codex.html           Codex browsing app (driven by content-manifest.json)
index.html           Public marketing / Kickstarter waitlist landing page
AGENTS.md            Single source of truth for AI assistant workflows
```

---

## Current status

**Written and canonical:** round structure, combat, buildings, artifacts, Whispers, objectives, diplomacy, and the First Playable packet (3–8 players). Recent sim-validated slice: **Plan 3 MVP** — shared public objective row, Coronation Rite, objective scoring at Cleanup & Checks (see `INDEX.md`; labeled sim-only until human table confirmation).

**Validation mode:** balance iteration is **sim-led** (persona tournaments, bracket configs, regression gates in `sim/configs/`). Human sessions log to `playtest/session_log.csv` via `agents/templates/Playtest_Report_Template.md` when table time is available.

**Open work** tracked in:

- `rules_and_systems/INDEX.md` — remaining design items
- `docs/plans/INDEX.md` — plan statuses, sim milestone track, open design questions
- `docs/reports/INDEX.md` — current sim baselines and hypothesis scoreboard
- `docs/plans/2026-07-02-aeonis-design-roadmap.md` — phased roadmap

---

## Local development

### Codex & marketing site

Open `codex.html` or `index.html` in a browser (static files; no build step).

### Simulator

Requires **Python 3.11+**. From `sim/`:

```bash
python3.11 -m venv .venv
# Windows:  .venv\Scripts\Activate.ps1
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest          # 346 tests
```

Bot games and tournament brackets: see [`sim/README.md`](sim/README.md).

### Doc hygiene

```bash
python3 -c "import json; json.load(open('content-manifest.json'))" && echo OK
```

Deeper checks: MCP tools in [`mcp/aeonis-tools/`](mcp/aeonis-tools/README.md) (`validate_manifest`, `broken_links_report`, `timing_window_lint`, etc.).

---

## Kickstarter intent

Building toward a first print run to:

- **Manufacture** the initial production copy.
- **Refine** rules clarity, balance, and onboarding.
- **Expand** the Lord roster and content variety across sessions.

Locked product decisions: [`marketing/Positioning.md`](marketing/Positioning.md).
