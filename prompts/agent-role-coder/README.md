# agent-role-coder

System prompt for a **Coder** specialist agent. Focused on accurate implementation, test-backed changes, and self-correcting error handling. Works with any local LLM or multi-agent orchestration setup.

## Usage

Paste `system_prompt.txt` as the system prompt for your coding agent role.

Works well paired with:
- `agent-role-orchestrator` — the planner/delegator that calls this role
- `agent-role-reviewer` — runs after Coder to catch regressions
- `local-agent-loop-setup` — playbook for wiring multi-agent setups

## What it does

- Requires the agent to restate the target before touching code
- Enforces smallest-change discipline
- Mandates test/lint/build verification after every edit
- Requires self-reflection on failure before retrying

## Install

```bash
pullnexus install agent-role-coder
```

Then copy `system_prompt.txt` into your agent configuration.

*License: MIT | Author: PullNexus Contributors*
