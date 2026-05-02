# uncertainty-behavior-policy

Governs how an AI assistant should behave when it lacks information or confidence.

Core rule: **don't pretend to know what you don't know.**

## Install

```bash
pullnexus install uncertainty-behavior-policy
```

## What It Covers

- When to state unknowns vs make assumptions
- How to ask for the minimum missing detail
- Which domains require extra caution (installs, file ops, financial logic)
- How to self-correct without excessive hedging
- Ready-to-paste system prompt snippet

## Use Case

Add `policy.md` as a constraint block in any system prompt where the agent makes
tool calls, file changes, or installation decisions. Works especially well as a
companion to the agent role prompts:

```
pullnexus install agent-role-orchestrator
pullnexus install uncertainty-behavior-policy
```

## Pairs With

- [agent-role-orchestrator](../agent-role-orchestrator/) — primary agent brain
- [agent-role-reviewer](../agent-role-reviewer/) — reviewer checks for overconfidence
- [local-agent-system-blueprint](../local-agent-system-blueprint/) — system design guide
