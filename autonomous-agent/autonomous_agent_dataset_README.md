# Autonomous Agent Training Set

This pack contains high-quality JSONL examples for local AI training on autonomous agent behavior.

## Files

- `autonomous_agent_sharegpt_10.jsonl`
  - 10 ShareGPT-format examples (`conversations` with `human`/`gpt`)
  - Broad autonomous agent capabilities
- `autonomous_agent_chatml_10.jsonl`
  - ChatML-style equivalent (`messages` with `user`/`assistant`)
  - Useful if your training pipeline expects role-based chat format
- `autonomous_agent_sharegpt_coding_10.jsonl`
  - 10 additional ShareGPT examples focused on coding-agent workflows
  - Includes retries, refactors, CI safety, static analysis, and release automation
- `autonomous_agent_sharegpt_research_10.jsonl`
  - 10 ShareGPT examples focused on research, evaluation frameworks, and tradeoff reasoning
- `autonomous_agent_sharegpt_desktop_10.jsonl`
  - 10 ShareGPT examples focused on desktop automation and safe local file workflows
- `autonomous_agent_sharegpt_reliability_10.jsonl`
  - 10 ShareGPT examples focused on reliability engineering, resiliency, and error recovery
- `autonomous_agent_sharegpt_memory_10.jsonl`
  - 10 ShareGPT examples focused on memory persistence and cross-session continuation
- `autonomous_agent_sharegpt_hardmode_10.jsonl`
  - 10 ShareGPT examples focused on adversarial requests, safety boundaries, and recovery under pressure
- `autonomous_agent_sharegpt_tooling_10.jsonl`
  - 10 ShareGPT examples focused on explicit tool orchestration and verification workflows
- `autonomous_agent_sharegpt_eval_10.jsonl`
  - 10 ShareGPT examples focused on judging agent output quality and selecting stronger responses
- `autonomous_agent_sharegpt_multiagent_10.jsonl`
  - 10 ShareGPT examples focused on multi-agent coordination and result synthesis
- `autonomous_agent_sharegpt_vibecoder_10.jsonl`
  - 10 ShareGPT examples focused on self-taught builder workflows, local AI setup, safe command habits, dataset hygiene, and practical repo triage
- `autonomous_agent_sharegpt_general_assistant_10.jsonl`
  - 10 ShareGPT examples focused on everyday general-helper behavior, simple explanations, decisions, planning, and non-code support
- `autonomous_agent_sharegpt_writing_explanation_10.jsonl`
  - 10 ShareGPT examples focused on README writing, documentation, plan docs, changelogs, and plain-English explanations
- `autonomous_agent_sharegpt_uncertainty_correction_10.jsonl`
  - 10 ShareGPT examples focused on saying "not enough context", asking for evidence, accepting corrections, and recovering gracefully
- `autonomous_agent_sharegpt_nonpython_web_shell_10.jsonl`
  - 10 ShareGPT examples focused on HTML, CSS, JavaScript, TypeScript, PowerShell, bash, React, Express, npm, and SQL
- `autonomous_agent_dataset_manifest.json`
  - Structured index with ingest order, focus areas, and totals
- `validate_autonomous_agent_jsonl.py`
  - Local validation script for JSON syntax, schema checks, and duplicate ID detection
- `create_autonomous_agent_splits.py`
  - Deterministic split generator for `train/val/test` JSONL files
- `autonomous_agent_train.jsonl`
  - Training split (88 examples)
- `autonomous_agent_val.jsonl`
  - Validation split (11 examples)
- `autonomous_agent_test.jsonl`
  - Held-out test split (11 examples)
- `autonomous_agent_sampling_guide.md`
  - Weighted sampling recommendations and training defaults

## Coverage Focus

- Task planning and goal decomposition
- Tool usage patterns (search/edit/execute/validate)
- Multi-step execution and workflow management
- Self-reflection, error detection, and correction loops
- Memory persistence and cross-session continuation

## Notes

- All files are line-delimited JSON (one object per line).
- IDs are unique within each file.
- You can concatenate files if your trainer supports merged corpora.
- Current total: 160 examples (150 ShareGPT + 10 ChatML).
- Split sizes: train 128 / val 16 / test 16 (deterministic seed: `20260428`).
