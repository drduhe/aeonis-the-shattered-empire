# Aeonis — Smart Agent Framework (Design/Build/Maintain)

This project already has a strong “source-of-truth” set of docs in `new/`. The purpose of this framework is to make an AI assistant reliable at:

- Designing new rules/content **without drifting** from canon.
- Maintaining consistency across chapters, playtest packets, and the Codex app.
- Producing repeatable outputs (new Lord sheets, event cards, objective sets, balance notes, playtest reports).

---

## Non-negotiables (read first)

**Canon hierarchy** — the most specific owning doc wins:

1. `rules_and_systems/Round_Structure.md` owns timing (phase names, windows, ordering).
2. Each system chapter owns its system (`Combat.md` owns combat, `Tiles.md` owns control/ZOC, ...).
3. `playtest/First_Playable_Packet.md` may override only via an explicit "First Playable rule".
4. `rules_and_systems/INDEX.md` is the decision log — resolved decisions get registered there.

**Terminology tripwires** (full canon: `lore/Naming_Bible.md`):

- "Imperial Seat" never "Throne of Power" • "Influence" never "IP" • "Speaking Stones" never "Palantír" • "Discovery/Ritual" never "spell" as a rules term • "Renown" not "Fame"/"Prestige".
- Magi Guild, Iron Vanguard, Sacred Order are retired placeholders — never use them.

**Propagation is mandatory.** A definition changes in exactly one owning doc, then every dependent doc updates in the same pass: affected chapters, `First_Playable_Packet.md`, `rulebook/Learn_to_Play.md` + `rulebook/Player_Aid.md`, and `content-manifest.json` for new/renamed files. Use `agents/checklists/Canon_Change_Checklist.md`.

**Plans are not canon.** Anything in `docs/plans/` marked PROPOSED changes nothing until playtested and recorded under "Design decisions (resolved)" in `INDEX.md`.

**Timing windows are explicit.** Every effect names its window ("During the High Council Phase", "On your turn in the Action Phase", "At Cleanup & Checks"). Never write an effect without one.

**No new currencies or keywords** without a definition section in an owning chapter, a Naming Bible entry, and cross-references.

**No human playtesters for a while (2026-07-03).** Balance and PROPOSED-plan promotion are **sim-led**: persona tournaments, hypothesis reports, and explicit regression gates — not "wait for table time." Sim conclusions stay labeled sim-only until the owner schedules humans. See `.cursor/rules/aeonis-playtest-constraints.mdc`.

---

## Repo map

- `rules_and_systems/` — the rule chapters; `INDEX.md` is TOC + decision log + red flags.
- `lords/` — 12 faction sheets (8 launch + 4 expansion roster).
- `lore/` — `Lore.md` (worldbook) + `Naming_Bible.md` (terminology canon).
- `playtest/` — `First_Playable_Packet.md` (current test scope), `Full_Game_Scope.md`, `Balance_Dashboard.md`, `session_log.csv`.
- `rulebook/` — `Learn_to_Play.md` + `Player_Aid.md` (derived docs; always update after rules changes).
- `components/` — `Components.md` (prototype kit) + `Production_Manifest.md` (manufacturing BOM).
- `marketing/` — `Positioning.md` (locked product decisions), pitch, comps, campaign math.
- `docs/plans/` — dated design plans; PROPOSED ≠ canon.
- `agents/` — roles, templates, checklists. `mcp/aeonis-tools/` — validation MCP server.
- `content-manifest.json` + `app.js`/`index.html` — the Codex browsing app.

---

## Validate before you finish

From the repo root (this folder):

- **Manifest parses:** `python3 -c "import json; json.load(open('content-manifest.json'))" && echo OK` — after adding/renaming any doc the Codex app should surface.
- **Terminology sweep:** `grep -rnE "Palantír|Throne of Power|Magi Guild|Iron Vanguard|Sacred Order" --include='*.md' . ; grep -rnw "IP" --include='*.md' .` — expect hits only in this file, `Naming_Bible.md`'s forbidden-terms table, `INDEX.md`'s decision log, `docs/plans/` history, and the MCP README's example config.
- **Deeper checks:** the MCP server in `mcp/aeonis-tools/` provides `validate_manifest` (files exist), `broken_links_report`, `impact_report` (term blast radius before a rename), `check_defined_terms`, and `timing_window_lint`. See its README.

---

## Canon (source of truth)

When working on Aeonis, treat these as canonical:

- `rules_and_systems/INDEX.md` (table of contents + “red flags”)
- `rules_and_systems/Round_Structure.md` (timing spine)
- `playtest/First_Playable_Packet.md` (what is “on” for current playtests)
- `components/Components.md` (what needs to exist physically)
- `content-manifest.json` + `app.js` (what the Codex app can browse)

If you change a definition that other docs rely on (AP, Influence, ZOC, “Control”, “Imperial Seat”, etc.), you must **propagate the change** to every impacted doc (see checklists in `agents/checklists/`).

---

## “Smart agent” roles (how to delegate work)

You can use these roles as mental models, or paste them into a Cursor prompt when starting a task.

### 1) System Architect (rules designer)

- **Goal**: make rules changes that are mechanically sound and cross-chapter consistent.
- **Inputs**: desired design outcome + which chapter(s) are in scope.
- **Outputs**: a concrete patch to the relevant `rules_and_systems/*.md` plus an integration note for `First_Playable_Packet.md` if needed.
- **Guardrails**:
  - Respect `Round_Structure.md` timing windows.
  - Avoid introducing new resources/keywords unless defined once and referenced everywhere.

### 2) Balance Analyst (economy + pacing)

- **Goal**: tune numbers and incentives to hit target pace (90–180 minutes for First Playable).
- **Inputs**: current costs, VP sources, starting state, and playtest observations.
- **Outputs**:
  - a “balance memo” (what to change + why),
  - a short list of testable hypotheses (what would improve),
  - optional: a suggested playtest scenario (“try 3 rounds with X”).

### 3) Content Designer (Lords/cards/events/objectives)

- **Goal**: create new content that plugs into existing systems cleanly.
- **Inputs**: desired faction fantasy + playstyle + constraints (First Playable vs full game).
- **Outputs**: a new doc in `lords/` or `rules_and_systems/` using the templates in `agents/templates/`.
- **Guardrails**: every new mechanic must map to an existing system hook (AP, Population, Influence, Renown, Council, etc.), or be explicitly defined.

### 4) Rulebook Editor (clarity + consistency)

- **Goal**: remove ambiguity, align terminology, add cross-references.
- **Outputs**: tight wording edits + a list of “defined terms” changes if any.

### 5) Codex Maintainer (manifest + browsing)

- **Goal**: keep `content-manifest.json` aligned with docs so the Codex app remains navigable.
- **Outputs**: manifest edits (and any small UI changes only when needed).

---

## Default workflows (repeatable playbook)

### A) Propose a rules change (safe, low drift)

Use `agents/checklists/Canon_Change_Checklist.md`.

1. Identify the **one canonical definition** you’re changing (term + location).
2. Update the owning doc (often the system chapter).
3. Update `First_Playable_Packet.md` if the change affects First Playable.
4. Update cross-references (other chapters + Index).
5. If it’s a doc you want surfaced in the Codex UI, update `content-manifest.json`.

### B) Add a new Lord (repeatable)

Use `agents/templates/Lord_Sheet_Template.md` and `agents/checklists/Content_Integration_Checklist.md`.

1. Write the Lord sheet (starting setup, passive/active, unique tile/building/discovery, objective).
2. Ensure terminology matches canon and references existing systems.
3. Add to `content-manifest.json` under the `lords` category (if you want it browseable).
4. If First Playable: add explicit First Playable constraints in `playtest/First_Playable_Packet.md`.

### C) Add cards (events/objectives/strategy)

Use the relevant template in `agents/templates/`.

- Always specify **timing window** (Round Start / Council / Action turn / Production & Upkeep / Event / Cleanup).
- Always specify **scope** (self / target player / region / hex / global).
- Always specify **resolution order** if it interacts with combat, movement, or council.

### D) Run playtests and iterate

Use `agents/templates/Playtest_Report_Template.md`.

1. Keep the test packet minimal (First Playable).
2. Log the handful of metrics that matter (round count, VP pace, “AP feels”, conflict frequency, council impact).
3. Convert findings into 3–5 hypotheses and patch the docs accordingly.

---

## Folder: `agents/`

- `agents/roles/`: reusable role prompts and “how to think” guides.
- `agents/templates/`: copy/paste templates for new content.
- `agents/checklists/`: integration and consistency checklists.
