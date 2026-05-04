# Prompt Engineering

**The foundational skill for getting reliable output from any local LLM.**

Before reaching for a bigger model or a framework, improve your prompts. Most local model failures are prompt failures — vague instructions, no format guidance, wrong temperature, no examples. This skill teaches the full toolkit.

---

## System Prompt Design

The system prompt is the highest-leverage input. It sets the model's role, constraints, output format, and behavior for the entire session.

**Anatomy of a strong system prompt:**
```
[Role] You are a senior Python developer who writes clean, typed, tested code.
[Constraints] You do not use deprecated libraries. You always include error handling.
[Output format] Respond with code blocks first, then a brief explanation below.
[Tone] Be direct. No filler phrases.
```

**Rules:**
- Be specific, not aspirational. "Write clean code" is vague. "Use type hints on all function signatures" is actionable.
- Put constraints before output format — models weight earlier instructions more heavily.
- One role, not many. Don't ask it to be a developer AND a teacher AND a reviewer in one system prompt.

---

## Few-Shot Examples

Show the model exactly what you want with 2–5 input/output pairs before your real request.

```
User: Summarize this in one sentence: [long text about climate change]
Assistant: Rising greenhouse gas emissions are driving global temperature increases that threaten ecosystems and human infrastructure.

User: Summarize this in one sentence: [long text about quantum computing]
Assistant: Quantum computers use superposition and entanglement to solve specific problems exponentially faster than classical hardware.

User: Summarize this in one sentence: [your actual text here]
```

**When to use:** Any task where the desired format, length, or style is hard to describe in words. Show it instead.

**Few-shot placement:** Put examples in the system prompt for persistent behavior, or in the conversation history for one-off tasks.

---

## Chain-of-Thought (CoT)

Force the model to reason step by step before giving a final answer. Dramatically improves accuracy on math, logic, debugging, and planning tasks.

**Simple CoT trigger:**
```
Think through this step by step before giving your final answer.
```

**Structured CoT:**
```
Before answering, write:
REASONING: [your step-by-step thinking]
ANSWER: [your final answer]
```

**Zero-shot CoT** (no examples needed): Add "Let's think step by step." to the end of any question. Works surprisingly well even on small models.

**When to use:** Anything involving multi-step reasoning, math, logic puzzles, debugging, planning. Not needed for simple lookup or format tasks.

---

## Temperature & Sampling Settings

| Setting | Value | Use case |
|---|---|---|
| `temperature` | 0.0–0.2 | Code, SQL, factual answers, structured output |
| `temperature` | 0.5–0.7 | General chat, explanations, balanced tasks |
| `temperature` | 0.8–1.2 | Creative writing, brainstorming, fiction |
| `top_p` | 0.9 | Good default — reduce if output is too random |
| `top_k` | 40 | Good default — lower = more focused |
| `repeat_penalty` | 1.1–1.3 | Reduce repetition loops on small models |

**Rule:** Low temperature for precision, high temperature for creativity. Never use high temperature for code or JSON output.

---

## Format Control

Don't assume the model will format output correctly. Tell it explicitly.

**Explicit format instructions:**
```
Respond ONLY with valid JSON. No prose before or after. No markdown code fences.
The JSON must match this schema exactly:
{"name": string, "score": number, "reason": string}
```

**Markdown control:**
```
Do not use markdown. No headers, no bullets, no bold. Plain text only.
```

**Length control:**
```
Respond in exactly 3 bullet points. Each bullet is one sentence maximum.
```

---

## Common Failure Modes & Fixes

| Failure | Cause | Fix |
|---|---|---|
| Model ignores instructions | Instructions buried after long context | Move key constraints to the TOP of the system prompt |
| Rambling, no structure | No output format specified | Add explicit format with example |
| Wrong answer stated confidently | No CoT, jumps to conclusion | Add "think step by step" or require reasoning before answer |
| Output cuts off mid-sentence | `max_tokens` too low | Increase `max_tokens` or `num_predict` |
| Loops / repeats itself | No repeat penalty | Set `repeat_penalty: 1.1` |
| Ignores later instructions | Context too long, early instructions dominate | Checkpoint and start fresh (see `context-compaction`) |
| JSON is malformed | No schema given, temperature too high | Lower temperature to 0.1, inject schema, use retry loop |
| Refuses the task | Over-cautious system prompt or RLHF | Rephrase without triggering safety filters; use a less-tuned model |

---

## Pairs Well With

- `spec-first-development` — write the spec with good prompts before coding
- `small-model-reasoning-boost` — combine with CoT for small models
- `structured-output-local` — advanced format control for JSON/schema output
- `context-compaction` — manage long prompt sessions

---

## License

CC0-1.0 — public domain, free to use for any purpose.
