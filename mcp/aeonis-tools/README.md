# Aeonis Tools (MCP Server)

This folder contains a local MCP server that provides **deterministic** tools for maintaining the Aeonis design docs.

It has **no third‑party dependencies** (Python stdlib only).

## Tools provided

All paths are relative to the repo root unless otherwise stated.

### `validate_manifest`

Validates `new/content-manifest.json` and ensures all referenced docs exist.

**Input**

```json
{
  "manifestPath": "new/content-manifest.json"
}
```

### `broken_links_report`

Finds broken relative markdown links (optionally only in docs referenced by the manifest).

**Input**

```json
{
  "rootDir": "new",
  "manifestPath": "new/content-manifest.json",
  "manifestOnly": true
}
```

### `impact_report`

Searches the Aeonis docs for a term and returns occurrences + file list.

**Input**

```json
{
  "rootDir": "new",
  "query": "ZOC",
  "caseInsensitive": true,
  "maxMatchesPerFile": 20
}
```

### `check_defined_terms`

Flags terminology drift (e.g., “IP” vs “Influence”) and reports occurrences with context.

**Input**

```json
{
  "rootDir": "new",
  "rules": [
    { "id": "influence-vs-ip", "preferred": "Influence", "forbidden": ["IP", "Influence Points"] }
  ]
}
```

### `timing_window_lint`

Heuristic lint: flags rule paragraphs that look like effects but don’t mention a timing window.

**Input**

```json
{
  "rootDir": "new",
  "windowPhrases": ["during", "at the start", "at cleanup", "on your turn", "in the action phase", "in the high council phase"],
  "maxFindings": 200
}
```

### `components_diff`

Diffs two component lists (markdown) and reports added/removed items (normalized).

**Input**

```json
{
  "basePath": "new/components/Components.md",
  "comparePath": "new/components/Components.md"
}
```

## Running locally

The server speaks MCP over stdio (LSP-style `Content-Length` framing).

```bash
python3 mcp/aeonis-tools/server.py
```

## Adding to Cursor (MCP)

In Cursor Settings → MCP, add a new server with:

- **Command**: `python3`
- **Args**: `mcp/aeonis-tools/server.py`
- **Working directory**: your repo root (this folder’s parent)

If your Cursor UI asks for JSON config, use this shape (adjust `cwd` as needed):

```json
{
  "mcpServers": {
    "aeonis-tools": {
      "command": "python3",
      "args": ["mcp/aeonis-tools/server.py"],
      "cwd": "/Users/drduhe/Desktop/Desktop/Aeonis"
    }
  }
}
```

