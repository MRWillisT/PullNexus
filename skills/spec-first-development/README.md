# Spec-First Development

**Teaches any local LLM to think before it codes.**

Most local agents jump straight into code and produce messy, incomplete, or hallucinated output. This skill enforces a clean **Spec → Validate → Implement → Verify** workflow that dramatically improves reliability on 7B–70B models.

> First AI-submitted skill to PullNexus — contributed by Grok (xAI).

## When to Pull This Skill

- Any coding task > 15 lines
- Building tools, agents, APIs, scripts
- Fine-tuning / RAG datasets where consistency matters
- Pairs well with: `lean-agent`, `reasoning-and-problem-solving`, `autonomous-agent-patterns`, `systematic-debugging`

## Core Process (4 Steps)

1. **Clarify & Spec** — Requirements, edge cases, success metrics, constraints
2. **Validate** — Self-review the spec and surface open questions
3. **Implement** — Only after spec is confirmed
4. **Test & Document** — Built-in verification and usage notes

## The Spec Template

A minimal spec should cover:

```
Goals:           What does this do and why?
Constraints:     Language, libraries, size, performance limits
Success Metrics: How will we know it works?
Edge Cases:      What can go wrong, and how should it be handled?
```

## Example Usage

```bash
pullnexus pull spec-first-development
```

Tell your agent:

> "Using spec-first-development, build me a FastAPI user registration endpoint with email verification."

The model will output a full spec first, ask for confirmation, then implement.

## Validate Your Spec (Optional Tool)

A helper script is included at `tools/validate_spec.py`:

```bash
echo "Goals: ... Constraints: ... Success Metrics: ... Edge cases: ..." | python tools/validate_spec.py
```

## Compatibility

Works with any model via Ollama, LM Studio, llama.cpp, or any local agent framework. MCP-compatible — can be injected as a system prompt tool.

## License

CC0-1.0 — public domain, free to use for any purpose.
