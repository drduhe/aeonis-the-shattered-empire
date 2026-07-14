#!/usr/bin/env python3
"""Generate the low-ink Aeonis First Playable print-and-play kit.

The generator reads canonical Markdown wherever practical. It intentionally
fails when the First Playable card counts change, forcing the PnP inventory to
be reviewed in the same pass as the rules change.
"""

from __future__ import annotations

import math
import random
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, black, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
PAGE_W, PAGE_H = letter
MARGIN = 25

LORDS = ["Cassian", "Seraphel", "Vharok", "Elyndra", "Rakhis", "Nyxara", "Auriel", "Thalrik"]

CATEGORY_COLORS = {
    "Strategy": HexColor("#E9E0C5"),
    "Public Objective": HexColor("#DDE7D5"),
    "Secret Objective": HexColor("#E2DDEC"),
    "Global Event": HexColor("#D7E5EC"),
    "Exploration Event": HexColor("#E8DFC9"),
    "Agenda": HexColor("#E7D7D2"),
    "Whisper": HexColor("#DFDCE8"),
    "Artifact": HexColor("#EEE4BE"),
    "Tier I Discovery": HexColor("#D5E7E1"),
}


@dataclass(frozen=True)
class Card:
    category: str
    title: str
    body: str
    source: str


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def ascii_text(value: str) -> str:
    replacements = {
        "→": "->", "–": "-", "—": "-", "−": "-", "±": "+/-",
        "×": "x", "≥": ">=", "≤": "<=", "’": "'", "“": '"', "”": '"',
        "•": " | ", "§": "Section ", "…": "...", "Aeonis™": "Aeonis",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")


def plain(markdown: str) -> str:
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", markdown)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"[*_]{1,3}", "", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^>\s?", "", text, flags=re.M)
    text = re.sub(r"^\s*[-+]\s+", "- ", text, flags=re.M)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return ascii_text(text.strip())


def between(text: str, start: str, end: str) -> str:
    a = text.index(start) + len(start)
    b = text.index(end, a)
    return text[a:b]


def bullet_cards(block: str, category: str, source: str) -> list[Card]:
    result = []
    pattern = re.compile(r"^- \*\*(.+?)\*\*(?: \([^\n]*?\))?:\s*(.+)$", re.M)
    for match in pattern.finditer(block):
        result.append(Card(category, plain(match.group(1)), plain(match.group(2)), source))
    return result


def strategy_cards() -> list[Card]:
    block = between(read("rules_and_systems/Strategy.md"), "## 3. The Eight Strategy Cards", "## 4. System Integration")
    matches = list(re.finditer(r"^### (\d+)\. (.+)$", block, flags=re.M))
    cards = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        cards.append(Card("Strategy", f"{match.group(1)}. {match.group(2)}", plain(block[match.end():end]), "Strategy.md Section 3"))
    return cards


def objective_and_event_cards() -> list[Card]:
    packet = read("playtest/First_Playable_Packet.md")
    objectives = between(packet, "**Public Objectives (2 VP each", "**Scoring:**")
    secrets = between(packet, "**Secret Objectives (2 VP each):**", "Setup:")
    global_events = between(packet, "**Global Events (resolve in Event Phase, before Strategy Selection):**", "**Exploration Events")
    exploration = between(packet, "**Exploration Events (resolve immediately on first entry):**", "### 4.6 Arcane Discoveries")
    return (
        bullet_cards(objectives, "Public Objective", "First_Playable_Packet.md Section 4.4")
        + bullet_cards(secrets, "Secret Objective", "First_Playable_Packet.md Section 4.4")
        + bullet_cards(global_events, "Global Event", "First_Playable_Packet.md Section 4.5")
        + bullet_cards(exploration, "Exploration Event", "First_Playable_Packet.md Section 4.5")
    )


def whisper_cards() -> list[Card]:
    block = between(read("rules_and_systems/Whispers.md"), "## First Playable Whisper Deck (26 cards)", "## Full-Game Whisper Deck")
    matches = list(re.finditer(r"^#### (.+)$", block, flags=re.M))
    cards = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        body = re.sub(r"^###.*$", "", block[match.end():end], flags=re.M)
        cards.append(Card("Whisper", match.group(1), plain(body), "Whispers.md First Playable deck"))
    return cards


def artifact_cards() -> list[Card]:
    block = between(read("rules_and_systems/Artifacts.md"), "## Artifact List", "## Setup")
    matches = list(re.finditer(r"^\*\*(\d+)\. (.+?)\*\*$", block, flags=re.M))
    cards = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        body = re.sub(r"^###.*$", "", block[match.end():end], flags=re.M)
        cards.append(Card("Artifact", match.group(2), plain(body), "Artifacts.md Artifact List"))
    return cards


def discovery_cards() -> list[Card]:
    lines = read("rules_and_systems/Arcane.md").splitlines()
    cards = []
    for i, line in enumerate(lines):
        match = re.match(r"^\d+\. \*\*(.+?)\*\* \((.+)\)\s*$", line)
        if not match or not re.search(r"\bTier I\b", match.group(2)):
            continue
        body = match.group(2)
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            body += "\n" + lines[j].strip()
        cards.append(Card("Tier I Discovery", match.group(1), plain(body), "Arcane.md Section 7"))
    return cards


def agenda_cards() -> list[Card]:
    # These are the eight First Playable cards named in the packet and owned by High_Council.md Section 6.
    source_text = read("rules_and_systems/High_Council.md")
    content = [
        ("Road Networks", "LAW. Movement across Plains costs 1 less AP (minimum 1). Duration: until repealed."),
        ("Demilitarized Zone", "DECREE. Choose a named region or 3 connected hexes. No player may initiate attacks into the zone until end of round."),
        ("Open Borders Treaty", "DECREE. Name two players. This round, they may move through each other's controlled hexes without paying the enemy-ZOC entry surcharge."),
        ("Imperial Annexation", "DECREE. Proposer pays 5 Influence. Claim one neutral hex adjacent to the proposer's controlled territory immediately; resolve exploration if it was unrevealed."),
        ("Border Arbitration", "DECREE. Name a contested border hex between two players. Both commit up to 4 Influence; high spender gains control. Ties: Speaker chooses. Discard spent Influence."),
        ("Realm Tax", "LAW. During Production & Upkeep, each player gains 1 Gold, then pays 1 Influence or loses 1 Renown. Duration: until repealed."),
        ("Hero of the Realm", "TITLE. Eligibility: 5+ Renown. Benefit: gain 1 Influence during Production & Upkeep while held. Score 2 VP when first claimed. Check eligibility at Cleanup & Checks."),
        ("Magister of Mana", "TITLE. Eligibility: control 3 Mana-producing Forest/Grove hexes at Cleanup & Checks. Once per round, reduce one Research action or Ritual Mana cost by 1. Score 2 VP when first claimed."),
    ]
    for title, _ in content:
        if title not in source_text:
            raise RuntimeError(f"First Playable agenda is missing from High_Council.md: {title}")
    return [Card("Agenda", title, body, "High_Council.md Section 6") for title, body in content]


def all_cards() -> list[Card]:
    cards = strategy_cards() + objective_and_event_cards() + agenda_cards() + whisper_cards() + artifact_cards() + discovery_cards()
    expected = {
        "Strategy": 8, "Public Objective": 6, "Secret Objective": 6,
        "Global Event": 12, "Exploration Event": 9, "Agenda": 8,
        "Whisper": 26, "Artifact": 24, "Tier I Discovery": 10,
    }
    actual = {category: sum(card.category == category for card in cards) for category in expected}
    if actual != expected:
        raise RuntimeError(f"PnP card inventory drift: expected {expected}, found {actual}")
    return cards


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if stringWidth(trial, font, size) <= width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def fit_lines(text: str, width: float, height: float, start: float = 8.0, minimum: float = 5.4) -> tuple[float, list[str]]:
    size = start
    while size >= minimum:
        lines = wrap(text, "Helvetica", size, width)
        if len(lines) * size * 1.22 <= height:
            return size, lines
        size -= 0.2
    return minimum, wrap(text, "Helvetica", minimum, width)


def page_footer(c: canvas.Canvas, text: str) -> None:
    c.setFont("Helvetica", 7)
    c.setFillColor(Color(0.35, 0.35, 0.35))
    c.drawCentredString(PAGE_W / 2, 12, ascii_text(text))


def draw_card(c: canvas.Canvas, card: Card, x: float, y: float, w: float, h: float) -> None:
    c.setFillColor(white)
    c.setStrokeColor(black)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    c.setFillColor(CATEGORY_COLORS[card.category])
    c.roundRect(x + 1, y + h - 33, w - 2, 32, 7, fill=1, stroke=0)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 7.2)
    c.drawString(x + 8, y + h - 13, card.category.upper())
    title_size = 10 if len(card.title) < 29 else 8.5
    c.setFont("Helvetica-Bold", title_size)
    for index, line in enumerate(wrap(ascii_text(card.title), "Helvetica-Bold", title_size, w - 16)[:2]):
        c.drawString(x + 8, y + h - 26 - index * (title_size + 1), line)
    body_top = y + h - 53
    size, lines = fit_lines(ascii_text(card.body), w - 18, h - 79)
    c.setFont("Helvetica", size)
    leading = size * 1.22
    cursor = body_top
    for line in lines:
        if cursor < y + 22:
            break
        c.drawString(x + 9, cursor, line)
        cursor -= leading
    c.setFont("Helvetica-Oblique", 5.4)
    c.setFillColor(Color(0.35, 0.35, 0.35))
    c.drawRightString(x + w - 7, y + 8, ascii_text(card.source))


def generate_cards_pdf(cards: list[Card]) -> Path:
    path = OUT / "aeonis-first-playable-cards.pdf"
    c = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle("Aeonis First Playable Cards")
    card_w, card_h = 180, 252  # 2.5 x 3.5 inches
    gap_x, gap_y = 8, 12
    origin_x = (PAGE_W - (3 * card_w + 2 * gap_x)) / 2
    origin_y = (PAGE_H - (2 * card_h + gap_y)) / 2
    for index, card in enumerate(cards):
        slot = index % 6
        if slot == 0:
            c.setFont("Helvetica", 6)
            c.setFillColor(Color(0.4, 0.4, 0.4))
            c.drawString(origin_x, PAGE_H - 18, "AEONIS FIRST PLAYABLE - cut on card borders - print at 100%")
        col, row = slot % 3, 1 - slot // 3
        draw_card(c, card, origin_x + col * (card_w + gap_x), origin_y + row * (card_h + gap_y), card_w, card_h)
        if slot == 5 or index == len(cards) - 1:
            page_footer(c, f"Cards {index - slot + 1}-{index + 1} of {len(cards)}")
            c.showPage()
    c.save()
    return path


def draw_heading(c: canvas.Canvas, title: str, subtitle: str = "") -> float:
    c.setFillColor(HexColor("#2F253A"))
    c.rect(0, PAGE_H - 60, PAGE_W, 60, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(MARGIN, PAGE_H - 34, ascii_text(title))
    if subtitle:
        c.setFont("Helvetica", 8)
        c.drawString(MARGIN, PAGE_H - 49, ascii_text(subtitle))
    c.setFillColor(black)
    return PAGE_H - 78


def draw_text_lines(c: canvas.Canvas, lines: list[str], x: float, y: float, width: float, size: float = 8, leading: float | None = None) -> float:
    leading = leading or size * 1.25
    c.setFont("Helvetica", size)
    for raw in lines:
        for line in wrap(ascii_text(raw), "Helvetica", size, width):
            c.drawString(x, y, line)
            y -= leading
    return y


def lord_section(text: str, start_heading: str, next_headings: list[str]) -> str:
    start = text.find(start_heading)
    if start < 0:
        return ""
    end_candidates = [text.find(heading, start + len(start_heading)) for heading in next_headings]
    end_candidates = [value for value in end_candidates if value >= 0]
    end = min(end_candidates) if end_candidates else len(text)
    return text[start:end]


def reference_lines(markdown: str, font_size: float, width: float) -> list[tuple[str, bool]]:
    """Convert simple Markdown to wrapped printable lines while retaining headings."""
    result: list[tuple[str, bool]] = []
    for raw in markdown.splitlines():
        stripped = raw.strip()
        if not stripped or stripped == "---":
            if result and result[-1][0]:
                result.append(("", False))
            continue
        if re.match(r"^\|?[\s:|-]+\|?$", stripped):
            continue
        is_heading = bool(re.match(r"^#{1,6}\s+", stripped))
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [plain(cell) for cell in stripped.strip("|").split("|")]
            cleaned = " | ".join(cell for cell in cells if cell)
        else:
            cleaned = plain(stripped)
        font = "Helvetica-Bold" if is_heading else "Helvetica"
        for line in wrap(cleaned, font, font_size, width):
            result.append((line.upper() if is_heading else line, is_heading))
    while result and not result[-1][0]:
        result.pop()
    return result


def draw_lord_page(c: canvas.Canvas, lord: str) -> None:
    text = read(f"lords/{lord}.md")
    title = re.search(r"^# (.+)$", text, flags=re.M).group(1)
    selected = "\n\n".join([
        lord_section(text, "## Starting Setup", ["## Abilities"]),
        lord_section(text, "## Abilities", ["## Faction Research"]),
        lord_section(text, "## Faction Research", ["## Legendary Building"]),
        lord_section(text, "## Legendary Building", ["## Special Units", "## Faction Objectives"]),
        lord_section(text, "## Faction Objectives", ["## Faction Strategy"]),
    ])
    y = draw_heading(c, title, "First Playable faction reference - full timing and limits from the Lord sheet")
    col_width = (PAGE_W - 3 * MARGIN) / 2
    font_size = 8.4
    while font_size >= 6.8:
        lines = reference_lines(selected, font_size, col_width)
        capacity = int((y - 34) / (font_size * 1.24))
        if len(lines) <= capacity * 2:
            break
        font_size -= 0.2
    midpoint = math.ceil(len(lines) / 2)
    for col, subset in enumerate((lines[:midpoint], lines[midpoint:])):
        x = MARGIN + col * ((PAGE_W - MARGIN) / 2)
        yy = y
        for line, is_heading in subset:
            c.setFont("Helvetica-Bold" if is_heading else "Helvetica", font_size + 0.3 if is_heading else font_size)
            c.drawString(x, yy, line)
            yy -= font_size * 1.24
    page_footer(c, f"Source: lords/{lord}.md - generated reference, not a new rules source")
    c.showPage()


def draw_hex(c: canvas.Canvas, x: float, y: float, radius: float, fill: Color, label: str, sublabel: str = "") -> None:
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        points.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
    path = c.beginPath()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    path.close()
    c.setFillColor(fill)
    c.setStrokeColor(black)
    c.drawPath(path, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", max(5, radius / 4.5))
    c.drawCentredString(x, y + 1, ascii_text(label))
    if sublabel:
        c.setFont("Helvetica", max(4, radius / 5.5))
        c.drawCentredString(x, y - radius / 3, ascii_text(sublabel))


def terrain_palette(name: str) -> Color:
    palette = {
        "city": "#E8D6B5", "plains": "#E9E5C7", "forest": "#D6E5D1",
        "mountain": "#D9D9D9", "desert": "#EAD3A4", "ruins": "#D7CBE0",
        "portal": "#C9DCEB", "lake": "#CDE4EA", "seat": "#E6C66A", "unique": "#E0D2E8",
    }
    return HexColor(palette.get(name.lower(), "#EEEEEE"))


def draw_map_pages(c: canvas.Canvas) -> None:
    sys.path.insert(0, str(ROOT / "sim"))
    from aeonis_sim.engine.hexmap import generate_map  # pylint: disable=import-outside-toplevel

    abbreviations = {"plains": "PL", "forest": "FO", "mountain": "MT", "desert": "DE", "ruins": "RU", "portal": "PO", "lake": "LA", "city": "CI"}
    for players in range(3, 9):
        tiles, homes = generate_map(players, random.Random(20260713 + players))
        radius = 3 if players <= 4 else 4 if players <= 6 else 5
        y_top = draw_heading(c, f"{players}-Player Preset Map", "Deterministic PnP layout generated by the simulator's canonical hexmap procedure")
        size = 29 if radius == 3 else 23 if radius == 4 else 18.5
        cx, cy = PAGE_W / 2, (y_top + 85) / 2
        for (q, r), tile in tiles.items():
            x = cx + size * 1.5 * q
            y = cy + size * math.sqrt(3) * (r + q / 2)
            terrain = tile.terrain.value
            label = "SEAT" if tile.imperial_seat else (f"H{homes.index((q, r)) + 1}" if (q, r) in homes else abbreviations[terrain])
            fill_name = "seat" if tile.imperial_seat else terrain
            draw_hex(c, x, y, size * 0.93, terrain_palette(fill_name), label)
        c.setFont("Helvetica", 7)
        c.drawString(MARGIN, 48, "Legend: PL Plains | FO Forest | MT Mountain | DE Desert | RU Ruins | PO Portal | LA Lake | H# Home City")
        c.drawString(MARGIN, 36, "Assign H1-H# in Speaker order. Apply each Lord's Unique Starting Tile substitution after laying out the map.")
        page_footer(c, "Map source: sim/aeonis_sim/engine/hexmap.py; seed = 20260713 + player count")
        c.showPage()


def draw_player_board(c: canvas.Canvas) -> None:
    draw_heading(c, "Player Board", "Print one per player; use cubes, pencil, or dry-erase markers")
    tracks = [("Gold", 0, 20), ("Mana", 0, 20), ("Influence", 0, 20), ("AP", 0, 15), ("VP", 0, 15), ("Renown", 0, 10), ("Population Pool", 0, 25), ("Population Cap", 0, 25), ("Lord HP", 0, 4)]
    y = PAGE_H - 92
    for name, low, high in tracks:
        c.setFont("Helvetica-Bold", 8)
        c.drawString(MARGIN, y + 7, name)
        x0 = MARGIN + 92
        cell = min(18, (PAGE_W - x0 - MARGIN) / (high - low + 1))
        for value in range(low, high + 1):
            c.rect(x0 + (value - low) * cell, y, cell, 18, fill=0, stroke=1)
            c.setFont("Helvetica", 5.5)
            c.drawCentredString(x0 + (value - low + 0.5) * cell, y + 6, str(value))
        y -= 37
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "Production & Upkeep")
    reminders = [
        "1. Collect printed terrain and building production.",
        "2. Grow Population where an effect allows; never exceed Population Cap.",
        "3. Pay advanced-unit and active-Law upkeep. Buildings have no recurring resource upkeep.",
        "4. Resolve marked recurring effects and gain any Remnants due.",
        "5. Mark once-per-round abilities as ready for the next round at Cleanup & Checks.",
    ]
    draw_text_lines(c, reminders, MARGIN, y - 18, PAGE_W - 2 * MARGIN, 8)
    page_footer(c, "Print 8 copies for a full First Playable set")
    c.showPage()


def draw_markdown_reference(c: canvas.Canvas, rel: str, title: str) -> None:
    font_size = 8.1
    lines = reference_lines(read(rel), font_size, PAGE_W - 2 * MARGIN)
    per_page = 68
    for page_start in range(0, len(lines), per_page):
        y = draw_heading(c, title, f"Printable extract of {rel}; page {page_start // per_page + 1}")
        for line, is_heading in lines[page_start:page_start + per_page]:
            c.setFont("Helvetica-Bold" if is_heading else "Helvetica", font_size + 0.3 if is_heading else font_size)
            c.drawString(MARGIN, y, line)
            y -= 9.6
        page_footer(c, f"Source: {rel}")
        c.showPage()


def generate_reference_pdf() -> Path:
    path = OUT / "aeonis-first-playable-reference-kit.pdf"
    c = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle("Aeonis First Playable Reference Kit")
    y = draw_heading(c, "Aeonis: First Playable", "Low-ink reference kit - synchronized 2026-07-13")
    intro = [
        "WHAT THIS PDF CONTAINS", "- Deterministic setup maps for 3-8 players", "- Eight launch-Lord reference sheets",
        "- A reusable player board", "- The current Player Aid",
        "", "PRINTING", "Print at 100% on US Letter paper. Print the player-board page once per player. Lord sheets and maps are table references, not replacements for the owning Markdown chapters.",
        "", "ALSO REQUIRED", "Cards PDF, tokens/map-proxies PDF, polyhedral dice (d4/d6/d8/d10), pencils or cubes, and sleeves/cardstock as desired.",
        "", "CANON", "Round_Structure.md owns timing. System chapters own their rules. First_Playable_Packet.md owns explicit First Playable overrides. Generated PDFs are derived artifacts.",
    ]
    draw_text_lines(c, intro, MARGIN, y, PAGE_W - 2 * MARGIN, 10, 14)
    page_footer(c, "Generated from repository canon; see pnp/README.md")
    c.showPage()
    draw_map_pages(c)
    for lord in LORDS:
        draw_lord_page(c, lord)
    draw_player_board(c)
    draw_markdown_reference(c, "rulebook/Player_Aid.md", "Player Aid")
    c.save()
    return path


def token_grid(c: canvas.Canvas, labels: list[str], title: str, subtitle: str, cols: int = 7, size: float = 68) -> None:
    draw_heading(c, title, subtitle)
    gap = 4
    start_x = (PAGE_W - (cols * size + (cols - 1) * gap)) / 2
    rows = math.ceil(len(labels) / cols)
    total_h = rows * size + (rows - 1) * gap
    start_y = PAGE_H - 82 - size
    if total_h > PAGE_H - 112:
        size = (PAGE_H - 112 - (rows - 1) * gap) / rows
        start_x = (PAGE_W - (cols * size + (cols - 1) * gap)) / 2
        start_y = PAGE_H - 82 - size
    for index, label in enumerate(labels):
        col, row = index % cols, index // cols
        x, y = start_x + col * (size + gap), start_y - row * (size + gap)
        c.setFillColor(HexColor("#F2F0F5") if index % 2 else white)
        c.setStrokeColor(black)
        c.rect(x, y, size, size, fill=1, stroke=1)
        words = wrap(ascii_text(label), "Helvetica-Bold", 7, size - 6)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 7)
        yy = y + size / 2 + (len(words) - 1) * 4
        for word in words[:3]:
            c.drawCentredString(x + size / 2, yy, word)
            yy -= 8
    page_footer(c, "Cut on solid borders; mount to chipboard or place in coin capsules if desired")
    c.showPage()


def map_proxy_pages(c: canvas.Canvas) -> None:
    counts = [
        ("Plains", 21), ("Forest", 16), ("Mountain", 19), ("Desert", 8),
        ("Ruins", 4), ("Portal", 3), ("Lake", 3), ("Home City", 8), ("Imperial Seat", 1),
        ("Arcane Nexus", 1), ("Ironworks Ridge", 1), ("Caravan Bazaar", 1), ("Sacred Grove", 1),
        ("Oasis Wellspring", 1), ("Obsidian Spire", 1), ("Hallowed Grove", 1), ("Rift Anchor", 1),
    ]
    tiles = [(label, i + 1, count) for label, count in counts for i in range(count)]
    per_page = 54
    for page_index in range(math.ceil(len(tiles) / per_page)):
        draw_heading(c, f"Map Proxy Hexes {page_index + 1}/2", "Maximum 8-player inventory; small-footprint prototype scale")
        subset = tiles[page_index * per_page:(page_index + 1) * per_page]
        radius = 34
        cols = 8
        for index, (label, number, count) in enumerate(subset):
            col, row = index % cols, index // cols
            x = 50 + col * 73
            y = PAGE_H - 113 - row * 88
            key = "unique" if label in {"Arcane Nexus", "Ironworks Ridge", "Caravan Bazaar", "Sacred Grove", "Oasis Wellspring", "Obsidian Spire", "Hallowed Grove", "Rift Anchor"} else label.split()[-1].lower()
            short = {"Home City": "HOME", "Imperial Seat": "SEAT"}.get(label, label[:8].upper())
            draw_hex(c, x, y, radius, terrain_palette(key), short, f"{number}/{count}")
        page_footer(c, "Use only the tile counts required by the selected player-count map")
        c.showPage()


def generate_tokens_pdf() -> Path:
    path = OUT / "aeonis-first-playable-tokens-and-map-proxies.pdf"
    c = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle("Aeonis First Playable Tokens and Map Proxies")
    map_proxy_pages(c)
    player_labels = ["LORD"] + ["INFANTRY"] * 10 + ["CAVALRY"] * 4 + ["ARCHER"] * 4 + ["CONTROL"] * 20
    token_grid(c, player_labels, "One Player's Pieces", "Print this page 8 times on different colored paper/cardstock", cols=7, size=68)
    buildings = [
        *( ["FARM"] * 8), *( ["GROVE"] * 8), *( ["MINE"] * 8), *( ["EMBASSY"] * 8),
        *( ["TOWER"] * 6), *( ["FORTRESS"] * 4), *( ["GUILD HALL"] * 4), *( ["MARKET"] * 4),
        *( ["FORGE"] * 4), *( ["ACADEMY"] * 4), *( ["BANK"] * 4), *( ["CASTLE"] * 4), *( ["BRIDGE"] * 2),
    ]
    for index in range(0, len(buildings), 42):
        token_grid(c, buildings[index:index + 42], f"Shared Buildings {index // 42 + 1}/2", "Shared First Playable building supply", cols=7, size=68)
    legendary = ["GRAND EXCHANGE", "ARCANE SANCTUM", "IRON CITADEL", "HEARTWOOD SANCTUM", "WINDSWORN WARCAMP", "HALL OF WHISPERS", "CATHEDRAL OF RADIANCE", "DIMENSIONAL NEXUS"]
    markers = ["REMNANT"] * 40 + ["ARTIFACT SITE"] * 6 + ["SIEGE"] * 4 + ["SPEAKER"] + ["ROUND"] + legendary
    for index in range(0, len(markers), 42):
        token_grid(c, markers[index:index + 42], f"Shared Markers {index // 42 + 1}/2", "Remnants, sites, siege, table markers, and launch Legendary Buildings", cols=7, size=68)
    c.save()
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cards = all_cards()
    paths = [generate_cards_pdf(cards), generate_reference_pdf(), generate_tokens_pdf()]
    for path in paths:
        print(path.relative_to(ROOT))
    print(f"cards={len(cards)}")


if __name__ == "__main__":
    main()
