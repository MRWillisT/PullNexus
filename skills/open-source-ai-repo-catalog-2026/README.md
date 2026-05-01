# open-source-ai-repo-catalog-2026

Based on self.dll's "69 Best Open-Source AI Repositories in April 2026" post, adapted into a PullNexus skill plus a machine-readable catalog for direct tool lookup.

## What This Adds

This companion skill is different from the strategy-oriented toolbox skill.

- `open-source-ai-toolbox-2026` helps choose the right stack.
- `open-source-ai-repo-catalog-2026` helps look up exact tool names by category.

It includes a structured catalog file with extracted repository names, categories, links, and short notes so assistants can answer questions like:

- "What are the RAG tools in that list?"
- "Which repos were in the deployment section?"
- "Show me the Claude-specific tools"
- "What exact repo link should I use for vLLM or Chroma?"

## Data Integrity Note

The source post advertises 69 repos. The public fetch available here yielded 62 concrete repo entries. This PullNexus skill preserves attribution and marks the catalog as a partial extraction rather than inventing missing items.

## Files

- `catalog.json` — machine-readable category and repo data
- `examples.jsonl` — training examples for exact-name lookup
- `eval.jsonl` — evaluation prompts for category and repo retrieval

## Credit

Inspired by: https://x.com/seelffff/status/2049214021430325677

This PullNexus adaptation restructures the source into queryable registry data with explicit provenance.
