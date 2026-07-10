#!/usr/bin/env python3
"""
Aeonis Tools MCP server (stdlib only).

Implements a minimal subset of MCP over stdio:
- initialize
- tools/list
- tools/call

Transport framing: LSP-style Content-Length headers.
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


MCP_PROTOCOL_VERSION = "2024-11-05"


def _eprint(*args: Any) -> None:
    # Never write non-framed output to stdout; stderr is safe for logs.
    print(*args, file=sys.stderr, flush=True)


def _read_exact(stream, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = stream.read(n - len(buf))
        if not chunk:
            break
        buf += chunk
    return buf


def _read_framed_message(stream) -> Optional[Dict[str, Any]]:
    """
    Read a single LSP-framed JSON message:
      Content-Length: <n>\r\n
      ...headers...\r\n
      \r\n
      <json bytes>
    """
    header_bytes = b""
    while b"\r\n\r\n" not in header_bytes:
        b1 = stream.read(1)
        if not b1:
            return None
        header_bytes += b1
        # Guard against runaway headers
        if len(header_bytes) > 64 * 1024:
            raise RuntimeError("Header too large")

    header_blob, _sep, rest = header_bytes.partition(b"\r\n\r\n")
    headers: Dict[str, str] = {}
    for line in header_blob.split(b"\r\n"):
        if not line.strip():
            continue
        if b":" not in line:
            continue
        k, v = line.split(b":", 1)
        headers[k.decode("utf-8", "replace").strip().lower()] = v.decode("utf-8", "replace").strip()

    if "content-length" not in headers:
        raise RuntimeError("Missing Content-Length")
    try:
        length = int(headers["content-length"])
    except ValueError as e:
        raise RuntimeError("Invalid Content-Length") from e

    body = rest + _read_exact(stream, max(0, length - len(rest)))
    if len(body) != length:
        raise EOFError("Unexpected EOF while reading body")
    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON body: {e}") from e


def _write_framed_message(stream, payload: Dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8")
    stream.write(header)
    stream.write(body)
    stream.flush()


def _jsonrpc_error(_id: Any, code: int, message: str, data: Any = None) -> Dict[str, Any]:
    err: Dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": _id, "error": err}


def _jsonrpc_result(_id: Any, result: Any) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": _id, "result": result}


def _tool_text_result(text: str) -> Dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


def _norm_rel_path(p: str) -> str:
    return str(Path(p).as_posix())


def _repo_root() -> Path:
    # Default to current working directory (Cursor should set cwd to repo root).
    return Path(os.getcwd()).resolve()


def _safe_join(root: Path, user_path: str) -> Path:
    # Resolve a user-provided relative path under root (no escape).
    p = (root / user_path).resolve()
    if root not in p.parents and p != root:
        raise ValueError(f"Path escapes root: {user_path}")
    return p


def _iter_files(root: Path, patterns: Tuple[str, ...]) -> Iterable[Path]:
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            path = Path(dirpath) / fn
            for pat in patterns:
                if path.match(pat):
                    yield path
                    break


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _load_json(path: Path) -> Any:
    return json.loads(_read_text(path))


def _format_findings(findings: List[Dict[str, Any]]) -> str:
    return json.dumps(findings, ensure_ascii=False, indent=2)


def tool_validate_manifest(args: Dict[str, Any]) -> str:
    root = _repo_root()
    manifest_rel = args.get("manifestPath", "content-manifest.json")
    manifest_path = _safe_join(root, manifest_rel)

    errors: List[str] = []
    warnings: List[str] = []
    findings: List[Dict[str, Any]] = []

    if not manifest_path.exists():
        errors.append(f"Missing manifest file: {manifest_rel}")
        return _format_findings([{"level": "error", "message": m} for m in errors])

    try:
        manifest = _load_json(manifest_path)
    except Exception as e:
        errors.append(f"Manifest JSON parse failed: {e}")
        return _format_findings([{"level": "error", "message": m} for m in errors])

    categories = manifest.get("categories")
    if not isinstance(categories, list):
        errors.append("manifest.categories must be an array")
        return _format_findings([{"level": "error", "message": m} for m in errors])

    allowed_status = {"core", "playtest", "draft", "internal", "notes", ""}
    seen_paths: Dict[str, List[str]] = {}

    for ci, cat in enumerate(categories):
        if not isinstance(cat, dict):
            errors.append(f"categories[{ci}] must be an object")
            continue
        cid = cat.get("id")
        label = cat.get("label")
        docs = cat.get("docs")
        if not isinstance(cid, str) or not cid.strip():
            errors.append(f"categories[{ci}].id must be a non-empty string")
        if not isinstance(label, str) or not label.strip():
            errors.append(f"categories[{ci}].label must be a non-empty string")
        if not isinstance(docs, list):
            errors.append(f"categories[{ci}].docs must be an array")
            continue

        for di, doc in enumerate(docs):
            loc = f"categories[{ci}].docs[{di}]"
            if not isinstance(doc, dict):
                errors.append(f"{loc} must be an object")
                continue

            title = doc.get("title")
            path = doc.get("path")
            desc = doc.get("description", "")
            status = doc.get("status", "")
            minutes = doc.get("minutes", None)

            if not isinstance(title, str) or not title.strip():
                errors.append(f"{loc}.title must be a non-empty string")
            if not isinstance(path, str) or not path.strip():
                errors.append(f"{loc}.path must be a non-empty string")
                continue
            if desc is not None and not isinstance(desc, str):
                errors.append(f"{loc}.description must be a string")
            if status is not None and not isinstance(status, str):
                errors.append(f"{loc}.status must be a string")
            if isinstance(status, str) and status and status.lower() not in allowed_status:
                warnings.append(f"{loc}.status is not a known status: {status!r}")
            if minutes is not None and not (isinstance(minutes, int) and minutes >= 0):
                warnings.append(f"{loc}.minutes should be a non-negative integer")

            seen_paths.setdefault(path, []).append(loc)

            # Manifest document paths are relative to the repository root.
            expected = _safe_join(root, path)
            if not expected.exists():
                errors.append(f"{loc}.path missing on disk: {path}")

    for p, locs in seen_paths.items():
        if len(locs) > 1:
            warnings.append(f"Duplicate manifest path {p!r} referenced at: {', '.join(locs)}")

    for m in errors:
        findings.append({"level": "error", "message": m})
    for m in warnings:
        findings.append({"level": "warning", "message": m})

    if not findings:
        findings.append({"level": "ok", "message": "Manifest validated successfully."})

    return _format_findings(findings)


_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _extract_md_links(md: str) -> List[str]:
    links: List[str] = []
    for _text, href in _MD_LINK_RE.findall(md):
        href = href.strip()
        if not href:
            continue
        # strip optional title: (path "title")
        if " " in href and (href.endswith('"') or href.endswith("'")):
            # naive but good enough for our docs
            href = href.split(" ", 1)[0]
        links.append(href)
    return links


def _is_external_href(href: str) -> bool:
    return bool(re.match(r"^(https?:\/\/|mailto:|#)", href, flags=re.I))


def tool_broken_links_report(args: Dict[str, Any]) -> str:
    root = _repo_root()
    root_dir = args.get("rootDir", ".")
    manifest_rel = args.get("manifestPath", "content-manifest.json")
    manifest_only = bool(args.get("manifestOnly", True))

    base = _safe_join(root, root_dir)
    if not base.exists():
        return _format_findings([{"level": "error", "message": f"rootDir not found: {root_dir}"}])

    targets: List[Path] = []
    if manifest_only:
        manifest_path = _safe_join(root, manifest_rel)
        try:
            manifest = _load_json(manifest_path)
        except Exception as e:
            return _format_findings([{"level": "error", "message": f"Failed to read manifest: {e}"}])
        for cat in (manifest.get("categories") or []):
            for doc in (cat.get("docs") or []):
                p = doc.get("path")
                if isinstance(p, str) and p.endswith(".md"):
                    targets.append(_safe_join(root, p))
    else:
        targets = list(_iter_files(base, ("**/*.md",)))

    findings: List[Dict[str, Any]] = []

    for fp in targets:
        try:
            md = _read_text(fp)
        except Exception as e:
            findings.append({"level": "error", "file": _norm_rel_path(fp.relative_to(root)), "message": f"Failed to read: {e}"})
            continue

        for href in _extract_md_links(md):
            if _is_external_href(href):
                continue
            # Only check relative links that point to local files (including .md)
            href_clean = href.split("#", 1)[0].strip()
            if not href_clean:
                continue
            if re.match(r"^[A-Za-z]:[\\/]", href_clean) or href_clean.startswith("/"):
                # absolute path: treat as external to repo rules
                continue

            resolved = (fp.parent / href_clean).resolve()
            if not resolved.exists():
                findings.append(
                    {
                        "level": "warning",
                        "file": _norm_rel_path(fp.relative_to(root)),
                        "link": href,
                        "message": "Broken relative link (target missing)"
                    }
                )

    if not findings:
        findings.append({"level": "ok", "message": "No broken relative markdown links found (for selected scope)."})
    return _format_findings(findings)


def tool_impact_report(args: Dict[str, Any]) -> str:
    root = _repo_root()
    root_dir = args.get("rootDir", ".")
    query = args.get("query")
    if not isinstance(query, str) or not query.strip():
        return _format_findings([{"level": "error", "message": "query must be a non-empty string"}])
    ci = bool(args.get("caseInsensitive", True))
    max_per_file = int(args.get("maxMatchesPerFile", 20))
    max_per_file = max(1, min(max_per_file, 500))

    base = _safe_join(root, root_dir)
    if not base.exists():
        return _format_findings([{"level": "error", "message": f"rootDir not found: {root_dir}"}])

    flags = re.I if ci else 0
    pattern = re.compile(re.escape(query), flags=flags)

    findings: List[Dict[str, Any]] = []
    for fp in _iter_files(base, ("**/*.md", "**/*.json")):
        try:
            text = _read_text(fp)
        except Exception:
            continue
        matches = list(pattern.finditer(text))
        if not matches:
            continue

        # line-index
        lines = text.splitlines()
        # Build cumulative offsets for line mapping
        offsets: List[int] = []
        cur = 0
        for ln in lines:
            offsets.append(cur)
            cur += len(ln) + 1

        def offset_to_line_col(off: int) -> Tuple[int, int]:
            # linear scan is fine for our doc sizes
            line = 0
            for i in range(len(offsets)):
                if offsets[i] <= off:
                    line = i
                else:
                    break
            col = off - offsets[line]
            return (line + 1, col + 1)

        file_hits: List[Dict[str, Any]] = []
        for m in matches[:max_per_file]:
            line, col = offset_to_line_col(m.start())
            snippet = lines[line - 1].strip() if 0 <= line - 1 < len(lines) else ""
            file_hits.append({"line": line, "col": col, "snippet": snippet})

        findings.append(
            {
                "file": _norm_rel_path(fp.relative_to(root)),
                "count": len(matches),
                "hits": file_hits
            }
        )

    findings.sort(key=lambda x: x.get("count", 0), reverse=True)
    if not findings:
        return _format_findings([{"level": "ok", "message": f"No matches for {query!r} under {root_dir}."}])
    return _format_findings(findings)


@dataclass(frozen=True)
class TermRule:
    id: str
    preferred: str
    forbidden: Tuple[str, ...]


def tool_check_defined_terms(args: Dict[str, Any]) -> str:
    root = _repo_root()
    root_dir = args.get("rootDir", ".")
    rules_raw = args.get("rules")
    if rules_raw is None:
        # Default project rules (can be extended via args)
        rules: List[TermRule] = [
            TermRule(id="influence-vs-ip", preferred="Influence", forbidden=("IP", "Influence Points")),
        ]
    else:
        if not isinstance(rules_raw, list):
            return _format_findings([{"level": "error", "message": "rules must be an array"}])
        rules = []
        for r in rules_raw:
            if not isinstance(r, dict):
                continue
            rid = r.get("id", "")
            pref = r.get("preferred", "")
            forb = r.get("forbidden", [])
            if not isinstance(rid, str) or not rid:
                continue
            if not isinstance(pref, str) or not pref:
                continue
            if not isinstance(forb, list) or not all(isinstance(x, str) and x for x in forb):
                continue
            rules.append(TermRule(id=rid, preferred=pref, forbidden=tuple(forb)))

    base = _safe_join(root, root_dir)
    if not base.exists():
        return _format_findings([{"level": "error", "message": f"rootDir not found: {root_dir}"}])

    findings: List[Dict[str, Any]] = []
    for fp in _iter_files(base, ("**/*.md",)):
        try:
            text = _read_text(fp)
        except Exception:
            continue
        lines = text.splitlines()

        for rule in rules:
            for forb in rule.forbidden:
                # word-ish boundary for short tokens, but allow punctuation
                pat = re.compile(rf"(?i)(?<![A-Za-z0-9]){re.escape(forb)}(?![A-Za-z0-9])")
                for i, ln in enumerate(lines, start=1):
                    if pat.search(ln):
                        findings.append(
                            {
                                "level": "warning",
                                "rule": rule.id,
                                "preferred": rule.preferred,
                                "forbidden": forb,
                                "file": _norm_rel_path(fp.relative_to(root)),
                                "line": i,
                                "snippet": ln.strip()
                            }
                        )

    if not findings:
        findings.append({"level": "ok", "message": "No terminology drift findings for configured rules."})
    return _format_findings(findings)


_DEFAULT_WINDOW_PHRASES = (
    "during",
    "before",
    "after",
    "when",
    "whenever",
    "until end of round",
    "at the start",
    "at cleanup",
    "at the end",
    "round start",
    "cleanup & checks",
    "on your turn",
    "action phase",
    "high council phase",
    "production & upkeep",
    "in the action phase",
    "in the high council phase",
    "in the production",
    "in the event phase",
)


def tool_timing_window_lint(args: Dict[str, Any]) -> str:
    root = _repo_root()
    root_dir = args.get("rootDir", ".")
    window_phrases = args.get("windowPhrases", list(_DEFAULT_WINDOW_PHRASES))
    max_findings = int(args.get("maxFindings", 200))
    max_findings = max(1, min(max_findings, 5000))

    if not isinstance(window_phrases, list) or not all(isinstance(x, str) and x for x in window_phrases):
        return _format_findings([{"level": "error", "message": "windowPhrases must be an array of non-empty strings"}])

    base = _safe_join(root, root_dir)
    if not base.exists():
        return _format_findings([{"level": "error", "message": f"rootDir not found: {root_dir}"}])

    # Very simple heuristic: paragraphs/bullets that look like effects but lack timing words.
    effect_words = re.compile(r"(?i)\b(gain|lose|may|must|cannot|instead|resolve|draw|discard|build|recruit|research|attack|move)\b")
    timing_words = re.compile("|".join(re.escape(p) for p in window_phrases), flags=re.I)

    findings: List[Dict[str, Any]] = []
    for fp in _iter_files(base, ("**/*.md",)):
        try:
            text = _read_text(fp)
        except Exception:
            continue
        lines = text.splitlines()
        for i, ln in enumerate(lines, start=1):
            s = ln.strip()
            if not s:
                continue
            # Skip headings, code fences, tables, and obvious references/stat lines.
            if s.startswith(("#", "```", ">", "|")):
                continue
            if re.match(
                r"^- \*\*(attack|defense|health|movement range|cost|build cost|"
                r"population|upkeep|vp|prerequisite|type|stats|notes?)\*\*\s*:",
                s,
                flags=re.I,
            ):
                continue
            # Lint explicit effect/rule-text fields, not stat blocks, action
            # menus, examples, or component lists that merely contain verbs.
            if not re.search(r"(?i)\*\*(effect|rule text)\*\*\s*:", s):
                continue
            if not effect_words.search(s):
                continue
            # A standard ability block may put `Timing:` on a nearby line.
            context = " ".join(lines[max(0, i - 4):i])
            if timing_words.search(s) or re.search(r"(?i)\*\*timing\*\*\s*:", context):
                continue
            findings.append(
                {
                    "level": "warning",
                    "file": _norm_rel_path(fp.relative_to(root)),
                    "line": i,
                    "snippet": s,
                    "message": "Rule-like line lacks an explicit timing window (heuristic)."
                }
            )
            if len(findings) >= max_findings:
                break
        if len(findings) >= max_findings:
            break

    if not findings:
        findings.append({"level": "ok", "message": "No timing-window lint findings (heuristic) for selected scope."})
    return _format_findings(findings)


def _extract_bullets(md: str) -> List[str]:
    items: List[str] = []
    for ln in md.splitlines():
        s = ln.strip()
        if s.startswith("- "):
            items.append(s[2:].strip())
    return items


def _normalize_component_item(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    # normalize common bullet prefixes like "4×", "4x"
    s = re.sub(r"^\d+\s*[×x]\s*", "", s)
    return s


def tool_components_diff(args: Dict[str, Any]) -> str:
    root = _repo_root()
    base_rel = args.get("basePath")
    comp_rel = args.get("comparePath")
    if not isinstance(base_rel, str) or not isinstance(comp_rel, str) or not base_rel or not comp_rel:
        return _format_findings([{"level": "error", "message": "basePath and comparePath must be non-empty strings"}])

    base_path = _safe_join(root, base_rel)
    comp_path = _safe_join(root, comp_rel)
    if not base_path.exists():
        return _format_findings([{"level": "error", "message": f"basePath missing: {base_rel}"}])
    if not comp_path.exists():
        return _format_findings([{"level": "error", "message": f"comparePath missing: {comp_rel}"}])

    base_items = [_normalize_component_item(x) for x in _extract_bullets(_read_text(base_path))]
    comp_items = [_normalize_component_item(x) for x in _extract_bullets(_read_text(comp_path))]

    base_set = set(x for x in base_items if x)
    comp_set = set(x for x in comp_items if x)

    added = sorted(comp_set - base_set)
    removed = sorted(base_set - comp_set)

    return _format_findings(
        [
            {"level": "info", "basePath": base_rel, "comparePath": comp_rel},
            {"added": added},
            {"removed": removed},
        ]
    )


TOOLS = {
    "validate_manifest": {
        "description": "Validate content-manifest.json and ensure referenced docs exist.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "manifestPath": {"type": "string", "default": "content-manifest.json"},
            },
            "required": [],
            "additionalProperties": False,
        },
        "handler": tool_validate_manifest,
    },
    "broken_links_report": {
        "description": "Find broken relative markdown links (optionally only manifest docs).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rootDir": {"type": "string", "default": "new"},
                "manifestPath": {"type": "string", "default": "content-manifest.json"},
                "manifestOnly": {"type": "boolean", "default": True},
            },
            "required": [],
            "additionalProperties": False,
        },
        "handler": tool_broken_links_report,
    },
    "impact_report": {
        "description": "Search docs for a term and return occurrences + snippets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rootDir": {"type": "string", "default": "new"},
                "query": {"type": "string"},
                "caseInsensitive": {"type": "boolean", "default": True},
                "maxMatchesPerFile": {"type": "integer", "default": 20, "minimum": 1, "maximum": 500},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "handler": tool_impact_report,
    },
    "check_defined_terms": {
        "description": "Detect terminology drift (e.g., IP vs Influence) with configurable rules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rootDir": {"type": "string", "default": "new"},
                "rules": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "preferred": {"type": "string"},
                            "forbidden": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["id", "preferred", "forbidden"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": [],
            "additionalProperties": False,
        },
        "handler": tool_check_defined_terms,
    },
    "timing_window_lint": {
        "description": "Heuristic lint: find rule-like lines missing explicit timing windows.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rootDir": {"type": "string", "default": "new"},
                "windowPhrases": {"type": "array", "items": {"type": "string"}},
                "maxFindings": {"type": "integer", "default": 200, "minimum": 1, "maximum": 5000},
            },
            "required": [],
            "additionalProperties": False,
        },
        "handler": tool_timing_window_lint,
    },
    "components_diff": {
        "description": "Diff two markdown component lists and report added/removed items (normalized).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "basePath": {"type": "string"},
                "comparePath": {"type": "string"},
            },
            "required": ["basePath", "comparePath"],
            "additionalProperties": False,
        },
        "handler": tool_components_diff,
    },
}


def _handle_initialize(params: Dict[str, Any]) -> Dict[str, Any]:
    client_protocol = params.get("protocolVersion") if isinstance(params, dict) else None
    # We reply with our protocol version; Cursor typically tolerates this if compatible.
    return {
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "capabilities": {
            "tools": {},
        },
        "serverInfo": {"name": "aeonis-tools", "version": "0.1.0"},
        "clientProtocolVersion": client_protocol,
    }


def _handle_tools_list() -> Dict[str, Any]:
    tools = []
    for name, meta in TOOLS.items():
        tools.append(
            {
                "name": name,
                "description": meta["description"],
                "inputSchema": meta["inputSchema"],
            }
        )
    tools.sort(key=lambda t: t["name"])
    return {"tools": tools}


def _handle_tools_call(params: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(params, dict):
        raise ValueError("params must be an object")
    name = params.get("name")
    arguments = params.get("arguments", {})
    if not isinstance(name, str) or name not in TOOLS:
        raise ValueError(f"Unknown tool: {name!r}")
    if arguments is None:
        arguments = {}
    if not isinstance(arguments, dict):
        raise ValueError("arguments must be an object")
    handler = TOOLS[name]["handler"]
    out_text = handler(arguments)
    return _tool_text_result(out_text)


def main() -> int:
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer

    while True:
        try:
            msg = _read_framed_message(stdin)
        except EOFError:
            return 0
        except Exception as e:
            _eprint("read error:", e)
            return 1

        if msg is None:
            return 0

        if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
            # Non-JSONRPC payload; ignore
            continue

        _id = msg.get("id", None)
        method = msg.get("method")
        params = msg.get("params", {})

        # Notifications have no id; do not respond
        if _id is None:
            continue

        try:
            if method == "initialize":
                result = _handle_initialize(params if isinstance(params, dict) else {})
                _write_framed_message(stdout, _jsonrpc_result(_id, result))
            elif method == "tools/list":
                _write_framed_message(stdout, _jsonrpc_result(_id, _handle_tools_list()))
            elif method == "tools/call":
                _write_framed_message(stdout, _jsonrpc_result(_id, _handle_tools_call(params)))
            else:
                _write_framed_message(stdout, _jsonrpc_error(_id, -32601, f"Method not found: {method}"))
        except Exception as e:
            _write_framed_message(stdout, _jsonrpc_error(_id, -32603, "Internal error", data=str(e)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

