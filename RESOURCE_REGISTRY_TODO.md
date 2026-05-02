# PullNexus Typed Resource Registry TODO

Last updated: 2026-05-02

## Goal
Build PullNexus beyond a skill-only registry into a typed, gap-filling resource network for local LLMs.

## P0 - Foundation
- [x] Expand catalog repo entries into first-class discoverable resources.
- [x] Add resource type defaults (`resource_type`) in registry loading.
- [x] Add `--type` filtering to `pullnexus list`, `pullnexus search`, and `pullnexus recommend`.
- [x] Add schema version field to JSON outputs (`schema_version`) for stable agent parsing.
- [x] Add `pullnexus types --json` command to enumerate available resource types and counts.

## P1 - New First-Class Resource Types
- [x] `tool` resources: MCP servers, SDK wrappers, integration adapters. (`n8n-mcp-tool`)
- [x] `dataset` resources: training corpora, eval datasets, synthetic packs, licensing metadata. (`synthetic-training-datasets`)
- [x] `eval` resources: benchmark suites, score rubrics, pass/fail gates. (`rag-eval-baseline`)
- [x] `playbook` resources: deploy/runbook procedures. (`local-rag-starter-pack`)
- [x] `policy` resources: guardrails, refusal rules, safety/compliance templates. (`safe-output-guardrails`, `pii-redaction-policy`)
- [x] `template` resources: starter project layouts and config bundles. (`local-rag-starter-template`, `mcp-server-starter-template`, `fine-tune-pipeline-template`)
- [x] `environment` resources: known-good stacks (GPU tier, runtime, vector DB, embedding model). (`env-8gb-vram-local-chat`, `env-24gb-vram-agent-stack`, `env-apple-silicon-local-ai`)

## P1 - RAG-Specific Expansion
- [x] Add a `local-rag-starter-pack` playbook (ingestion, chunking, retrieval, eval, deployment).
- [x] Add a `rag-eval-baseline` resource with retrieval and answer-quality checks.
- [x] Add compatibility notes for common local stacks (Ollama + Chroma/Weaviate + reranker).
- [ ] Promote `HKUDS/RAG-Anything` and similar entries into curated `tool` + `playbook` resources.

## P2 - Feedback & Compatibility
- [x] Define minimal feedback schema per resource: `model`, `hardware`, `use_case`, `outcome`, `notes`.
- [x] Add `pullnexus feedback <resource-id>` CLI command (saves locally; GitHub-backed submission coming).
- [x] Surface compatibility data in `pullnexus info` output (works_on, known_issues, unverified_on).
- [x] Include quality/provenance fields in `pullnexus info` (maturity, maintained, last_verified).
- [x] Include `compatibility` field in `pullnexus info --json` for agent-native consumption.
- [x] Add `--context model=<name>,hardware=<vram>` flag to `pullnexus recommend` to filter by compatibility.

### Out of scope until 200+ resources
- Web UI feedback form (PullNexus is LLM-first CLI)
- Anti-gaming / identity staking (add friction only when gaming is observed)
- Global star ratings (contextual display only — never fake certainty)
- ML-based pattern recognition (build from real data after 100+ feedback entries exist)

## P2 - UX and API Consistency
- [x] Add `resource_type` column to all human-readable discovery surfaces where helpful.
- [x] Add `installable` semantics to command UX (`pull` rejects non-installable resource types).
- [x] Add `pullnexus recommend`, `pullnexus categories`, `pullnexus types` commands to CLI.
- [x] Add `--json` to `pullnexus info` for agent-native consumption.
- [ ] Add `pullnexus info` sections by type (skill/tool/dataset/playbook/policy).
- [ ] Add optional `--json` to any remaining discovery commands.

## P2 - Quality and Trust
- [x] Add provenance requirements per resource (`source`, `author`) — validated in submit flow.
- [x] Add validation rules by type in submit flow (type-specific field warnings).
- [x] Add quality scoring metadata (`maturity`, `maintained`, `last_verified`) to schema constants.
- [ ] Add signed checksum support for downloadable artifacts.
- [ ] Add `supersedes` field to skill schema — allows a newer entry to declare it replaces an older one. Superseded entries are hidden in search by default but still accessible via `pullnexus info`. Prevents duplicate/conflicting skills accumulating as the registry grows.

## Open Questions — Resolved

- [x] **`repository` type:** Fold it. "Repository" describes where something lives, not what it is. A repo is a tool, dataset, or playbook — contributors must pick the right one. `repository` stays as a legacy/catalog type but new submissions must use a real type.
- [x] **`recommend` default:** All types. Default to the most useful behavior — let users narrow with `--type skill` if needed. Defaulting to skills-only undermines the whole multi-type vision.
- [x] **Mandatory fields per type:** `name`, `version`, `description`, `tags`, `license`, `resource_type` — that's it for every type. Everything else is optional. Simple = more contributors.
- [x] **Feedback volume threshold:** 3 reports before showing compatibility data. Below 3 shows "unverified". Count always displayed so users can judge confidence.
- [x] **Feedback storage:** Separate `feedback/` index, one JSONL file per resource (`feedback/python-advanced-debugging.jsonl`). Avoids merge conflicts when multiple contributors submit simultaneously.

## P3 - PullNexus MCP Server

> Goal: any MCP-compatible client (Claude Code, Continue.dev, Cursor, LM Studio) gets
> skill search, install, and recommend built in — no CLI wrapper, no extra code.

### Core server
- [ ] Build first-party MCP server (`pullnexus/mcp_server.py`) using `fastmcp` or `mcp` SDK
- [ ] Expose as `pullnexus serve` CLI command — starts a local stdio/HTTP MCP server
- [ ] Package as optional extra: `pip install pullnexus[mcp]`
- [ ] Publish a Docker image for self-hosted / team deployments

### MCP tools to expose
- [ ] `pullnexus_search(query, type?, tag?)` — returns ranked skill list as JSON
- [ ] `pullnexus_recommend(problem, type?, limit?)` — returns scored recommendations
- [ ] `pullnexus_info(skill_name)` — returns full metadata + README as structured JSON
- [ ] `pullnexus_install(skill_name, output_path?)` — pulls skill files to local path
- [ ] `pullnexus_types()` — returns all resource types and counts
- [ ] `pullnexus_feedback(resource_id, model, hardware, use_case, outcome, notes?)` — submit report

### Client config examples
- [ ] Claude Code (`claude_mcp_config.json`) setup snippet in docs
- [ ] Continue.dev (`config.json` mcpServers block) setup snippet in docs
- [ ] Cursor / generic stdio MCP client config example
- [ ] Add `docs/mcp-server-setup.md` with copy-paste config for all three

### Discoverability
- [ ] Register on [mcp.so](https://mcp.so) and [glama.ai/mcp](https://glama.ai/mcp/servers) directories
- [ ] Add `mcp_compatible: true` to PullNexus's own `skill.json` / index entry
- [ ] Add MCP badge to README

### Open questions (P3)
- [ ] stdio vs HTTP transport — stdio for local-first, HTTP for team/cloud deployments?
- [ ] Should the MCP server read the local `skills/` folder first (offline mode) then fall back to remote?
- [ ] Rate limiting strategy for the public HTTP endpoint (if hosted)

## Why This Matters
When a local LLM hits a gap, it should retrieve not only a skill, but also the right tool, dataset, eval, playbook, and policy to close that gap reliably.
