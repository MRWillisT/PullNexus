# synthetic-general-training-pack

110+ synthetic JSONL examples for training a general coding assistant. 11 themed files covering broad programming, debugging, writing, reasoning, and everyday help patterns.

Designed to reduce domain skew — pair with domain-specific datasets to build a balanced local model.

## Install

```bash
pullnexus install synthetic-general-training-pack
```

## What's Included

| File | Focus | Examples |
|---|---|---|
| `synthetic_advanced_backtesting_2026-04-28.jsonl` | Monte Carlo, vectorized backtest, quant methods | 10 |
| `synthetic_brainstorming_2026-04-29.jsonl` | Idea generation, option analysis | 10 |
| `synthetic_execution_and_ops_2026-04-28.jsonl` | Task execution, operational workflows | 10 |
| `synthetic_general_assistant_2026-04-29.jsonl` | Everyday questions, decisions, explanations | 10 |
| `synthetic_modern_languages_2026-04-28.jsonl` | TypeScript, React, SQL, modern JS patterns | 10 |
| `synthetic_readme_and_docs_2026-04-29.jsonl` | README writing, changelogs, plain-English docs | 10 |
| `synthetic_reasoning_and_problem_solving_2026-04-28.jsonl` | Tradeoffs, debugging logic, decision trees | 10 |
| `synthetic_risk_management_2026-04-28.jsonl` | Risk framing, mitigation, systematic decision-making | 10 |
| `synthetic_trading_psychology_2026-04-28.jsonl` | Emotional discipline, bias awareness, planning under pressure | 10 |
| `synthetic_uncertainty_and_refusals_2026-04-29.jsonl` | Saying "I don't know", graceful refusals, asking for context | 10 |
| `synthetic_vibe_coder_fullcycle_2026-04-29.jsonl` | Full project flow: plan, implement, debug, ship | 10 |

## Who This Is For

- Builders fine-tuning a local model that's skewed toward one domain (trading, Python, etc.)
- Anyone who wants their assistant to be a better general thinker, writer, and debugger
- Use alongside `autonomous-agent-training-pack` for a more complete behavioral profile

## Compatible Formats

ShareGPT (`conversations` with `human`/`gpt` keys). Works directly with Axolotl, Unsloth, LlamaFactory, and any other framework that accepts ShareGPT JSONL.

## Pairs With

- [autonomous-agent-training-pack](../autonomous-agent-training-pack/) — agent behavior complement
- [uncertainty-behavior-policy](../uncertainty-behavior-policy/) — runtime uncertainty policy
- [vibe-coder-workflow](../vibe-coder-workflow/) — workflow guidance to complement the training data
