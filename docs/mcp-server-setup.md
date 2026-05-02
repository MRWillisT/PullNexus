# MCP Server Setup

PullNexus ships a built-in MCP server. Any MCP-compatible client can use it to search, recommend, and install resources from the registry without any CLI wrappers.

## Install

```bash
pip install pullnexus[mcp]
```

---

## Transport Options

| Mode | Command | Best for |
|------|---------|---------|
| stdio | `pullnexus serve` | Local clients (Claude Code, Continue.dev, Cursor) |
| HTTP | `pullnexus serve --transport http` | Team setups, hosted instances |

---

## Claude Code

Add to `~/.claude/claude_mcp_config.json` (or your project-local `.mcp.json`):

```json
{
  "mcpServers": {
    "pullnexus": {
      "command": "pullnexus",
      "args": ["serve"],
      "env": {}
    }
  }
}
```

Restart Claude Code. You can now say:
- *"Search PullNexus for RAG debugging skills"*
- *"Recommend resources for fine-tuning a small model"*
- *"Install python-advanced-debugging from PullNexus"*

---

## Continue.dev

Add to `~/.continue/config.json` under `mcpServers`:

```json
{
  "mcpServers": [
    {
      "name": "pullnexus",
      "command": "pullnexus",
      "args": ["serve"]
    }
  ]
}
```

---

## Cursor

In Cursor settings → MCP → Add server:

```json
{
  "pullnexus": {
    "command": "pullnexus",
    "args": ["serve"],
    "transport": "stdio"
  }
}
```

---

## HTTP Mode (team / cloud)

Start the server on your machine or a shared server:

```bash
pullnexus serve --transport http --host 0.0.0.0 --port 7337
```

Then configure clients with:

```json
{
  "mcpServers": {
    "pullnexus": {
      "url": "http://your-server:7337/mcp"
    }
  }
}
```

---

## Available Tools

| Tool | Description |
|------|-------------|
| `pullnexus_search` | Search by keyword, type, or tag |
| `pullnexus_recommend` | Recommend resources for a problem statement |
| `pullnexus_info` | Full metadata + README + compatibility summary |
| `pullnexus_install` | Download resource files to local directory |
| `pullnexus_types` | List all resource types with counts |
| `pullnexus_feedback` | Submit a compatibility report |

---

## Notes

- The server reads from the live GitHub registry over HTTPS — no local cache required.
- Feedback reports are appended to `feedback/<resource-id>.jsonl`. Open a PR to contribute yours to the shared index.
- Compatibility data appears in `pullnexus_info` once a resource has **3+ reports**.
