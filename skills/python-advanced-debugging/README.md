# python-advanced-debugging

Expert multi-turn debugging techniques for Python applications. This skill teaches a local LLM to diagnose and resolve non-obvious production bugs — the kind that don't throw exceptions, just silently fail.

## What This Skill Covers

- **Silent failures** — processes that run but stop doing work (no errors, no crash)
- **Async event loop blockages** — `asyncio` hangs caused by blocking calls (`time.sleep`, `requests`, heavy CPU)
- **Rate limit handling** — diagnosing bots that resume after 429s but stop trading
- **P&L calculation errors** — finding off-by-one fee bugs in financial calculations
- **Systematic debugging workflow** — how to narrow down root cause before writing any code

## Debugging Patterns Taught

The model learns to:
1. Ask the right clarifying questions before jumping to solutions
2. Provide targeted diagnostic commands (`grep`, log inspection, watchdog tasks)
3. Interpret intermediate results and reason about what they indicate
4. Self-correct when initial hypothesis doesn't match evidence
5. Deliver concrete, testable fixes with validation steps

## Who Should Use This Skill

Python developers working on production bots, async services, or any long-running application that silently stops working. Especially useful for crypto trading bots, data pipelines, and event-driven systems.

## Example Prompts

- "My bot stops placing orders after 2 hours with no error message"
- "My async app hangs — CPU goes to 0%, no logs, no exceptions"
- "My P&L calculation is $6 off from what the exchange shows"
- "Bot hits rate limits, waits, resumes scanning but never trades again"

## Usage

```bash
pullnexus pull python-advanced-debugging
```

Use `examples.jsonl` for fine-tuning or drop the folder into your model's context for RAG-style retrieval.

## License

CC0-1.0 — public domain.
