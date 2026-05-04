# agent-role-orchestrator

System prompt for the **Orchestrator** — the primary autonomous agent role in a local multi-agent system. Plans, delegates to specialist roles, maintains memory across sessions, and verifies every outcome.

## Usage

Paste `system_prompt.txt` as the system prompt for your main/primary agent.

Works well paired with:
- `agent-role-coder` — implementation specialist
- `agent-role-reviewer` — quality and safety checker
- `local-agent-loop-setup` — full multi-agent setup playbook
- `local-agent-system-blueprint` — beginner guide to wiring it together

## What it does

- Enforces plan-first behavior before any action
- Delegates to specialized roles (Coder, Reviewer, Toolsmith, Memory Keeper)
- Requires verification before declaring tasks complete
- Has a built-in safety gate: pauses on destructive/irreversible operations

## Install

```bash
pullnexus install agent-role-orchestrator
```

*License: MIT | Author: PullNexus Contributors*
