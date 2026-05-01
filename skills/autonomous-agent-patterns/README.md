# autonomous-agent-patterns

Core patterns for building and running autonomous AI agents. This skill teaches a local LLM to operate as a genuine agent — planning, using tools, recovering from errors, and persisting memory across sessions — not just generating text.

## What This Skill Covers

- **Task planning** — breaking a user goal into ordered, verifiable steps
- **Tool orchestration** — using search, file, shell, and code tools in the right order
- **Multi-step execution** — running workflows end-to-end with checkpoints
- **Error recovery** — detecting failures and self-correcting without user intervention
- **Memory persistence** — storing and loading state across sessions
- **Verification discipline** — checking outputs before declaring done
- **Constraint awareness** — respecting user-defined limits (offline-only, RAM cap, etc.)

## Agent Behavior Patterns

The model learns:
1. Plan before acting on non-trivial tasks
2. Use tools instead of guessing at facts
3. Verify results (tests, diffs, file existence, counts)
4. Recover from failures: reflect → patch → retry
5. Store updated memory and report completion concisely
6. Respect explicit and implicit constraints

## MCP Compatibility

This skill is marked `mcp_compatible: true`. The patterns work directly with MCP tool-calling interfaces — the agent behaviors translate to real tool invocations.

## Who Should Use This Skill

Developers building agent systems with local LLMs, or any model being asked to operate autonomously. Especially useful with Ollama + Continue.dev + MCP integrations.

## Example Prompts

- "Scan my logs folder and summarize top error types from the last 24 hours"
- "Refactor my Python utility into a package and set up tests — report back when done"
- "Over the next few messages, remember: no cloud APIs, must run on 8GB RAM"
- "Investigate why my build got slower this month and propose fixes"

## Usage

```bash
pullnexus pull autonomous-agent-patterns
```

## License

CC0-1.0 — public domain.
