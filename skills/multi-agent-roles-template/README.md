# multi-agent-roles-template

JSON starting point for a multi-agent system with an Orchestrator + 5 specialist roles.

## Install

```bash
pullnexus install multi-agent-roles-template
```

## Roles Included

| Role | Responsibility |
|---|---|
| Orchestrator (Navigator) | Plans, delegates, verifies, merges |
| Planner | Task decomposition + milestones |
| Coder | Implementation and refactoring |
| Toolsmith | File ops, search, command orchestration |
| Reviewer | Bug/regression detection, risk review |
| Memory Keeper | Long-horizon context persistence |

## Delegation Rules Built In

- Single-file change → orchestrator + coder only
- Multi-step debug → planner + toolsmith + coder + reviewer
- Long-running objective → add memory_keeper at each milestone
- High-risk ops → mandatory reviewer approval before apply

## Customize It

1. Rename `Navigator` to match your orchestrator model or persona
2. Add or remove specialist agents to fit your system
3. Extend `memory_schema` with your project's specific constraints

## Pairs With

- [agent-role-orchestrator](../agent-role-orchestrator/) — system prompt for the Orchestrator role
- [agent-role-coder](../agent-role-coder/) — system prompt for the Coder role
- [agent-role-reviewer](../agent-role-reviewer/) — system prompt for the Reviewer role
- [agent-memory-state-template](../agent-memory-state-template/) — runtime memory schema
- [local-agent-system-blueprint](../local-agent-system-blueprint/) — big-picture design guide
