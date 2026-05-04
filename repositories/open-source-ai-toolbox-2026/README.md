# open-source-ai-toolbox-2026

Based on self.dll's "69 Best Open-Source AI Repositories in April 2026" post, extended into a PullNexus-ready skill with JSONL training examples and eval cases.

## What This Skill Does

This skill helps an assistant turn a giant open-source AI tools list into practical recommendations. Instead of dumping 69 links, it maps user goals to a sensible stack:

- LLM inference (local and hosted)
- RAG and knowledge systems
- Agent frameworks
- Prompt testing and evals
- Fine-tuning workflows
- Tool/context pipelines and MCP ecosystem pieces
- Deployment and scale paths
- Vision/multimodal components
- Data prep utilities

## How To Use

Use this skill when users ask questions like:

- "What open-source stack should I use for local AI?"
- "What should I use for RAG and evals?"
- "I only have one GPU, what tools fit my setup?"
- "Give me a practical production path from prototype to deployment"

The assistant should:

1. Ask for constraints (budget, hardware, latency, team size, coding level).
2. Recommend a minimal stack first, then optional upgrades.
3. Explain tradeoffs (simplicity vs scale, local vs hosted, flexibility vs ops burden).
4. Provide migration paths, not just one-off picks.

## Credit

Inspired by: https://x.com/seelffff/status/2049214021430325677

This PullNexus version adapts the source into reusable guidance patterns for local assistants.
