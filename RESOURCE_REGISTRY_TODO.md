# PullNexus Typed Resource Registry TODO

Last updated: 2026-05-01

## Goal
Build PullNexus beyond a skill-only registry into a typed, gap-filling resource network for local LLMs.

## P0 - Foundation (Next)
- [x] Expand catalog repo entries into first-class discoverable resources.
- [x] Add resource type defaults (`resource_type`) in registry loading.
- [x] Add `--type` filtering to `pullnexus list`, `pullnexus search`, and `pullnexus recommend`.
- [x] Add schema version field to JSON outputs (`schema_version`) for stable agent parsing.
- [x] Add `pullnexus types --json` command to enumerate available resource types and counts.

## P1 - New First-Class Resource Types
- [ ] `tool` resources: MCP servers, SDK wrappers, integration adapters.
- [ ] `dataset` resources: training corpora, eval datasets, synthetic packs, licensing metadata.
- [ ] `eval` resources: benchmark suites, score rubrics, pass/fail gates.
- [ ] `playbook` resources: deploy/runbook procedures (for example, local RAG deployment).
- [ ] `policy` resources: guardrails, refusal rules, safety/compliance templates.
- [ ] `template` resources: starter project layouts and config bundles.
- [ ] `environment` resources: known-good stacks (GPU tier, runtime, vector DB, embedding model).

## P1 - RAG-Specific Expansion
- [ ] Promote `HKUDS/RAG-Anything` and similar entries into curated `tool` + `playbook` resources.
- [ ] Add a `local-rag-starter-pack` playbook (ingestion, chunking, retrieval, eval, deployment).
- [ ] Add a `rag-eval-baseline` resource with retrieval and answer-quality checks.
- [ ] Add compatibility notes for common local stacks (Ollama + Chroma/Weaviate + reranker).

## P2 - Feedback & Compatibility
> An LLM reaching out when it hits a gap needs to know "will this work on my setup?" before pulling anything.
> Contextual compatibility reports are more useful than a global score.

- [ ] Define minimal feedback schema per resource: `model`, `hardware`, `use_case`, `outcome` (success/fail), `notes`.
- [ ] Add `pullnexus feedback <resource-id>` CLI command to submit a compatibility report (GitHub-backed storage).
- [ ] Surface compatibility data in `pullnexus info` output:
	- `✓ Works on:` Llama2-7b (N reports), Mistral-7b (N reports)
	- `✗ Known issues:` GPU <8GB (N reports)
	- `⚠ Unverified on:` GPT4All, Phi-2
- [ ] Include `compatibility` field in `pullnexus info --json` for agent-native consumption.
- [ ] Add `--context model=<name>,hardware=<vram>` flag to `pullnexus recommend` to filter by known-good compatibility.

### Out of scope until 200+ resources
- Web UI feedback form (PullNexus is LLM-first CLI)
- Anti-gaming / identity staking (add friction only when gaming is observed)
- Global star ratings (contextual display only — never fake certainty)
- ML-based pattern recognition (build from real data after 100+ feedback entries exist)

## P2 - UX and API Consistency
- [ ] Add `resource_type` column to all human-readable discovery surfaces where helpful.
- [ ] Add `installable` semantics to command UX (`pull` should reject non-installable resource types).
- [ ] Add `pullnexus info` sections by type (skill/tool/dataset/playbook/policy).
- [ ] Add optional `--json` to any remaining discovery commands for agent-native workflows.

## P2 - Quality and Trust
- [ ] Add provenance requirements per resource (`source`, `license`, `inspired_by`, maintainer).
- [ ] Add validation rules by type in submit flow.
- [ ] Add quality scoring metadata (`maturity`, `maintained`, `last_verified`).
- [ ] Add signed checksum support for downloadable artifacts.

## Open Questions
- [ ] Should `repository` remain a type or be folded into `tool`/`dataset`/`playbook` after curation?
- [ ] Should `recommend` default to `--type skill` or include all types by default?
- [ ] Which minimum fields are mandatory for each type in `skill.json`/resource metadata?
- [ ] What is the minimum feedback volume (N reports) before compatibility data is shown rather than "unverified"?
- [ ] Should feedback be stored as flat JSONL per resource in the repo, or as a separate `feedback/` index?

## Why This Matters
When a local LLM hits a gap, it should retrieve not only a skill, but also the right tool, dataset, eval, playbook, and policy to close that gap reliably.
