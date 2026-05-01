# reasoning-and-problem-solving

Systematic problem decomposition for complex technical questions. This skill teaches a local LLM to reason through ambiguous, open-ended problems rather than jumping to the first plausible answer.

## What This Skill Covers

- **Diagnosing vague failures** — "crashes after 4–6 hours, no exception" style problems
- **Architecture tradeoffs** — REST polling vs WebSockets, RAG vs fine-tuning, sync vs async
- **Breaking down complex problems** — turning a fuzzy goal into an ordered list of concrete steps
- **Reasoning under uncertainty** — stating confidence levels, asking for evidence, avoiding fabrication
- **Decision frameworks** — comparing options on dimensions that actually matter
- **Root cause analysis** — working backwards from symptoms to causes

## Reasoning Patterns Taught

The model learns to:
1. Restate the problem before solving it
2. Identify what information is missing before guessing
3. Generate multiple hypotheses and rank them by probability
4. Describe tradeoffs honestly — not just "it depends"
5. Provide a recommended choice with clear justification
6. Know when to stop reasoning and ask a clarifying question

## Who Should Use This Skill

Any local LLM that needs to handle open-ended, multi-factor technical questions. Especially useful for architectural decisions, debugging sessions that start with vague descriptions, and tradeoff analysis.

## Example Prompts

- "My trading bot crashes unpredictably after 4–6 hours — not throwing exceptions, just stops"
- "Should I use REST polling or WebSockets for real-time data? What are the actual tradeoffs?"
- "How do you decide between RAG and fine-tuning for a local model?"
- "My system works in dev but behaves differently in production — where do I start?"

## Usage

```bash
pullnexus pull reasoning-and-problem-solving
```

## License

CC0-1.0 — public domain.
