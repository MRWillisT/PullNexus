# Autonomous Agent Sampling Guide

This guide provides practical weighted sampling defaults for your current local training set.

## Recommended Training Mix

Use weighted sampling across source domains during training:

- `autonomous_agent_sharegpt_coding_10.jsonl`: 1.2x
- `autonomous_agent_sharegpt_tooling_10.jsonl`: 1.2x
- `autonomous_agent_sharegpt_reliability_10.jsonl`: 1.1x
- `autonomous_agent_sharegpt_memory_10.jsonl`: 1.1x
- `autonomous_agent_sharegpt_hardmode_10.jsonl`: 1.0x
- `autonomous_agent_sharegpt_multiagent_10.jsonl`: 0.9x
- `autonomous_agent_sharegpt_vibecoder_10.jsonl`: 1.2x
- `autonomous_agent_sharegpt_general_assistant_10.jsonl`: 1.4x
- `autonomous_agent_sharegpt_writing_explanation_10.jsonl`: 1.3x
- `autonomous_agent_sharegpt_uncertainty_correction_10.jsonl`: 1.3x
- `autonomous_agent_sharegpt_nonpython_web_shell_10.jsonl`: 1.2x
- `autonomous_agent_sharegpt_research_10.jsonl`: 0.9x
- `autonomous_agent_sharegpt_desktop_10.jsonl`: 0.9x
- `autonomous_agent_sharegpt_eval_10.jsonl`: 0.8x
- `autonomous_agent_sharegpt_10.jsonl`: 1.0x
- `autonomous_agent_chatml_10.jsonl`: 0.7x

## Why These Weights

- Slightly upweight coding/tooling/reliability to improve real task completion.
- Upweight vibe-coder examples if you want the model to be better at turning vague local project work into safe, concrete steps.
- Upweight general, writing, uncertainty, and non-Python examples to counterbalance the current trading/weather/Python skew.
- Keep hardmode at parity to strengthen safety and error recovery.
- Include eval/judge data at a moderate rate to avoid making the model overly “grader-like.”
- Keep ChatML present but lower if your main runtime format is ShareGPT.

## Split Files

- `autonomous_agent_train.jsonl` (128 examples)
- `autonomous_agent_val.jsonl` (16 examples)
- `autonomous_agent_test.jsonl` (16 examples)

These were generated deterministically with seed `20260428`.

## Practical Training Notes

- Start with 2-4 epochs max for this dataset size.
- Track validation loss and stop early on overfitting signals.
- Run a small post-train eval focused on:
  - task decomposition quality
  - correct tool sequencing
  - self-correction behavior
  - memory consistency across turns
