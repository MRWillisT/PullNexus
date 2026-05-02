# Synthetic Training Datasets

Curated synthetic multi-turn JSONL datasets for fine-tuning local LLMs. CC0 licensed — use for anything.

## Included datasets

| Dataset | Format | Examples | Focus |
|---|---|---|---|
| `python-advanced-debugging` | ShareGPT / ChatML | 6 | Async hangs, silent failures, rate limits |
| `pytest-and-testing` | ShareGPT | 6 | Test design, fixtures, coverage |
| `reasoning-and-problem-solving` | ShareGPT | 6 | Systematic decomposition, decision trees |
| `crypto-trading-bot` | ShareGPT | 6 | Strategy logic, risk management |
| `code-refactoring` | ShareGPT | 6 | Extract, rename, simplify, SOLID |
| `vibe-coder-workflow` | ShareGPT | 6 | Rapid prototyping, LLM-first dev |
| `autonomous-agent` | ShareGPT / ChatML | 10 | Tool use, memory, multi-agent |

## Formats

Both **ShareGPT** (conversations array) and **ChatML** (messages array) formats provided. Compatible with:

- [Axolotl](https://github.com/axolotl-ai-cloud/axolotl)
- [Unsloth](https://github.com/unslothai/unsloth)
- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
- [torchtune](https://github.com/pytorch/torchtune)

## Usage

```bash
pullnexus pull synthetic-training-datasets
cd pullnexus-skills/synthetic-training-datasets

# All examples combined
cat */examples.jsonl > combined_train.jsonl

# Use with Axolotl
axolotl train config.yml --dataset combined_train.jsonl
```

## License

CC0-1.0 — public domain. No attribution required. Use commercially. Fine-tune anything.
