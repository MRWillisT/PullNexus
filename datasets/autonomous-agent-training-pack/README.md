# autonomous-agent-training-pack

160+ synthetic JSONL examples for training a local autonomous agent. Covers the full behavioral spectrum: planning, tool use, coding, multi-agent coordination, safety, memory, reliability, research, desktop automation, and more.

## Install

```bash
pullnexus install autonomous-agent-training-pack
```

## What's Included

| File | Focus | Examples |
|---|---|---|
| `autonomous_agent_sharegpt_10.jsonl` | Core agent capabilities | 10 |
| `autonomous_agent_chatml_10.jsonl` | ChatML-format equivalent | 10 |
| `autonomous_agent_sharegpt_coding_10.jsonl` | Coding agent workflows | 10 |
| `autonomous_agent_sharegpt_tooling_10.jsonl` | Tool orchestration | 10 |
| `autonomous_agent_sharegpt_reliability_10.jsonl` | Reliability + error recovery | 10 |
| `autonomous_agent_sharegpt_memory_10.jsonl` | Cross-session memory | 10 |
| `autonomous_agent_sharegpt_hardmode_10.jsonl` | Adversarial + safety boundaries | 10 |
| `autonomous_agent_sharegpt_multiagent_10.jsonl` | Multi-agent coordination | 10 |
| `autonomous_agent_sharegpt_eval_10.jsonl` | Output quality evaluation | 10 |
| `autonomous_agent_sharegpt_research_10.jsonl` | Research + tradeoff reasoning | 10 |
| `autonomous_agent_sharegpt_desktop_10.jsonl` | Desktop + local file workflows | 10 |
| `autonomous_agent_sharegpt_vibecoder_10.jsonl` | Vibe coder + safe local AI workflows | 10 |
| `autonomous_agent_sharegpt_general_assistant_10.jsonl` | General helper behavior | 10 |
| `autonomous_agent_sharegpt_writing_explanation_10.jsonl` | README, docs, plan summaries | 10 |
| `autonomous_agent_sharegpt_uncertainty_correction_10.jsonl` | Saying "I don't know", accepting corrections | 10 |
| `autonomous_agent_sharegpt_nonpython_web_shell_10.jsonl` | HTML, JS, TS, PS, bash, React, SQL | 10 |

**Ready-to-use splits:**
- `autonomous_agent_train.jsonl` (88 examples)
- `autonomous_agent_val.jsonl` (40 examples)
- `autonomous_agent_test.jsonl` (32 examples)

**Tooling:**
- `validate_autonomous_agent_jsonl.py` — validates schema + checks for duplicates
- `create_autonomous_agent_splits.py` — regenerates splits deterministically
- `autonomous_agent_sampling_guide.md` — recommended training weights per file
- `autonomous_agent_dataset_manifest.json` — structured index + ingest order

## Recommended Training Stack

Compatible with any fine-tuning framework that accepts ShareGPT or ChatML format:
- **Axolotl** — use ShareGPT or ChatML config
- **Unsloth** — use ShareGPT format
- **LlamaFactory** — use `alpaca_gpt4` style with the ShareGPT files

## Quick Start

```bash
# Validate all files
python validate_autonomous_agent_jsonl.py

# Regenerate train/val/test splits
python create_autonomous_agent_splits.py
```

## What This Trains

A model fine-tuned on this dataset will:
- Plan before acting, not just react
- Use tools methodically with verification
- Coordinate across multiple agents
- Maintain memory state across sessions
- Handle adversarial or ambiguous requests safely
- Know when to say "I don't know"
- Self-correct when wrong

## Pairs With

- [agent-role-orchestrator](../agent-role-orchestrator/) — system prompt to pair with training
- [agent-role-coder](../agent-role-coder/) — coder specialist prompt
- [multi-agent-roles-template](../multi-agent-roles-template/) — role assignment template
- [uncertainty-behavior-policy](../uncertainty-behavior-policy/) — runtime behavior policy
