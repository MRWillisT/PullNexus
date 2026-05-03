# lean-agent

Agent behavior prompt that enforces **narrow, low-context fixes**. Restricts exploration to the minimum needed to solve the issue and enforces smallest-safe-change discipline throughout.

## Usage

Use as a system prompt or agent mode in any local LLM setup, VS Code Copilot agent mode, Continue.dev, or Cursor.

In VS Code, save as a `.agent.md` file in `.github/` or your prompts folder and select it from the agent mode picker.

## What it does

- Starts from the file the user mentioned — no broad repo scanning
- Reads only files directly needed to solve the issue
- Makes the smallest possible safe change
- Keeps status updates brief and only reports new information
- Asks one clarifying question only when genuinely blocked

## When to use it

- Bug fixes in a known file
- Single-function edits
- Token-constrained sessions with small models
- Any time you want focused output without background exploration

## Pairs well with

- `code-only-mode` — stack on top for zero-prose output
- `uncertainty-behavior-policy` — adds safe fallback behavior when the agent is unsure

## Install

```bash
pullnexus install lean-agent
```

Copy `agent.md` into your agent configuration or `.github/` prompts folder.

*License: MIT | Author: MRWillisT*
