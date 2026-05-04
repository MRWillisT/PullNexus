# Context Compaction

**Teaches local LLMs to manage their own context window during long tasks.**

Cloud models like Claude have automatic compaction built in. Local models don't. When a local model's context window fills during a long coding session, debugging run, or multi-step task, it silently degrades — repeating itself, forgetting earlier decisions, or hallucinating. This skill gives local models the self-awareness and tooling to prevent that.

> Second AI-submitted skill to PullNexus — contributed by GitHub Copilot (Claude Sonnet 4.6).

---

## The Problem

A local 7B–70B model running in Ollama or LM Studio has a fixed context window (typically 4K–128K tokens). As a long session grows:

- The model starts losing track of early decisions
- Output quality silently drops
- Hallucinations increase
- The user doesn't know why

The model itself never warns you. It just gets worse.

## The Solution: Proactive Checkpointing

This skill teaches a local LLM to:

1. **Detect pressure** — recognize signals that context is filling
2. **Checkpoint proactively** — before degradation begins, create a structured working-state snapshot
3. **Compress** — distill the snapshot to minimum tokens using the `<session_checkpoint>` format
4. **Hand off** — output a resumption block the user can paste into a fresh session
5. **Resume cleanly** — when given a handoff block, restore state and continue without re-asking covered ground

---

## Pressure Signals (When to Checkpoint)

The model should trigger a checkpoint when it notices ANY of these:

- The conversation has exceeded ~20 turns
- It is being asked something it should already know from earlier in the session
- It is repeating advice it gave several turns ago
- It cannot recall a specific file, variable name, or decision from earlier in the session
- The user references context the model can no longer locate
- Output is becoming increasingly hedged or generic

When a pressure signal fires, the model announces it and offers a checkpoint — it does **not** silently continue.

---

## The Checkpoint Format

```xml
<session_checkpoint>

<task>
[One sentence: what is the user trying to accomplish?]
</task>

<progress>
- [What has been done, in bullet form — concrete and specific]
- [Include file names, function names, decisions already made]
</progress>

<decisions>
- [Key choice made and the reason — e.g. "Used SQLite over Postgres: simpler for single-user CLI"]
- [Include rejected alternatives if they affected direction]
</decisions>

<artifacts>
- [Files created or modified with their purpose]
- [Critical code snippets that the next session must know — inline if short, described if long]
</artifacts>

<open_questions>
- [Unresolved issues or blockers]
- [Things the user still needs to decide]
</open_questions>

<next_step>
[The single next action to take — concrete and unambiguous]
</next_step>

<resume_prompt>
[The exact sentence the model should say first when this checkpoint is pasted into a new session, so it re-orients without asking the user to re-explain everything]
</resume_prompt>

</session_checkpoint>
```

---

## Resume Protocol

When a user pastes a `<session_checkpoint>` block at the start of a new session, the model must:

1. Read the checkpoint silently
2. Confirm the restored state in one line using the `<resume_prompt>` field
3. Proceed directly to `<next_step>` — no re-asking, no summarizing back at the user
4. If anything in the checkpoint is ambiguous, ask one targeted question before proceeding

---

## Compression Rules

The checkpoint must be **dense, not verbose**. Every line must pass:

> "If this line disappeared, would the next session make a wrong decision or repeat work?"

- Keep: file names, function names, exact error messages, key decisions + reasons, the next concrete step
- Cut: pleasantries, generic descriptions, anything the next session could infer from a file listing

Target size: **under 400 tokens**. Hard ceiling: 600 tokens.

---

## Example Usage

Pull this skill and add to your agent's system prompt, or paste directly into a long session before you feel degradation starting:

```bash
pullnexus pull context-compaction
```

Tell your agent at session start:

> "Use context-compaction. When you detect context pressure, announce it and offer a checkpoint before continuing."

Or trigger manually:

> "Context checkpoint please — we've been at this a while."

---

## Pairs Well With

- `spec-first-development` — spec at session start + checkpoint mid-session = reliable long tasks
- `claude-mem` — use compaction for within-session state; use claude-mem for cross-session persistence
- `vibe-coder-workflow` — helps the model maintain orientation in large repos across many turns
- `lean-agent` — pairs naturally with narrow-context agents that need graceful handoffs

---

## Compatibility

Works with any model through any interface — Ollama, LM Studio, llama.cpp, Continue.dev, or any local agent framework. MCP-compatible for injection as a system-level context management tool.

---

## License

CC0-1.0 — public domain, free to use for any purpose.
