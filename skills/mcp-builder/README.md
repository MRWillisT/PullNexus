# mcp-builder

An architecture skill for designing Model Context Protocol (MCP) servers and tool interfaces that integrate reliably into agent workflows.

## What it teaches

- Structure MCP tool definitions with clear input/output contracts
- Design tool interfaces that are safe to call autonomously (idempotent, bounded side effects)
- Handle tool errors gracefully so the agent can recover
- Choose between resources vs. tools vs. prompts in the MCP primitive model
- Wire MCP servers into common clients (Claude Code, Continue.dev, Cursor)

## When to use

- Building a new MCP server from scratch
- Wrapping an existing API or CLI as an MCP tool
- Designing multi-tool agents that need reliable context injection
- Debugging MCP tool registration or invocation failures

## Example invocations

```
I want to expose my company's internal API as an MCP tool for Claude.
Help me design a file-management MCP server that's safe to use autonomously.
My MCP tool keeps timing out — how should I handle that?
```

## Format

ShareGPT JSONL — 6 conversation pairs covering MCP server design, tool interface decisions, and integration patterns.

## Tags

`mcp`, `tools`, `integration`, `protocol`, `automation`

## License

See `skill.json` for license details.
