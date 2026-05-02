# n8n MCP Tool

Connect local LLMs to 400+ n8n integrations via the [n8n MCP server](https://github.com/czlonkowski/n8n-mcp).

## What it does

Exposes n8n's workflow engine as an MCP tool — your LLM can create, read, update, and trigger n8n workflows without any copy-paste JSON. Full TypeScript SDK with type safety, built-in validation, and direct deployment support.

## Setup

```bash
# Install n8n locally or use cloud
npm install -g n8n

# Clone and run the MCP server
git clone https://github.com/czlonkowski/n8n-mcp
cd n8n-mcp
npm install && npm run build

# Add to your MCP client config (Claude Code, Continue.dev, etc.)
# See repo README for client-specific setup steps
```

## Example use cases

- Build a Slack → Google Sheets automation without leaving your editor
- Let an agent create a webhook workflow and test it end-to-end
- Orchestrate multi-step data pipelines with 400+ available integrations

## Compatibility

- Tested with Claude Code and Continue.dev
- Requires n8n v1.x+ and Node.js 18+
- Unverified with Ollama direct MCP bridge

## Links

- GitHub: https://github.com/czlonkowski/n8n-mcp
- n8n docs: https://docs.n8n.io
