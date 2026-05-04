# agent-memory-state-template

JSON schema for persistent agent memory — user preferences, project constraints, active objectives with milestones, rejected approaches, and next actions.

## Install

```bash
pullnexus install agent-memory-state-template
```

## What's In It

| Field | Purpose |
|---|---|
| `user_preferences` | Response style, risk tolerance, confirmation thresholds |
| `project_constraints` | Fixed rules (offline-only, max RAM, etc.) |
| `active_objectives` | Goals with sub-milestones and status tracking |
| `rejected_approaches` | Record of what was tried and why it failed |
| `next_actions` | Carry-forward tasks between sessions |

## Usage

The Memory Keeper role (or the Orchestrator at end of each session) should:
1. Read the current state file
2. Update `active_objectives` milestones
3. Append to `rejected_approaches` if something failed
4. Write `next_actions` for the next session resume

## Pairs With

- [multi-agent-roles-template](../multi-agent-roles-template/) — role definitions including Memory Keeper
- [agent-role-orchestrator](../agent-role-orchestrator/) — primary agent that reads/writes memory
- [local-agent-system-blueprint](../local-agent-system-blueprint/) — Memory layer explained
