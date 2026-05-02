# PullNexus
**GitHub-backed registry and CLI for local AI resources.** Search, pull, and submit reusable skills, tools, templates, datasets, and workflow artifacts.

[![PyPI](https://img.shields.io/pypi/v/pullnexus)](https://pypi.org/project/pullnexus/) [![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE) [![Registry](https://img.shields.io/badge/registry-155%20resources-brightgreen)](skills/index.json)

---

## Quickstart

```bash
pip install pullnexus
```

**Search the registry:**
```bash
pullnexus search "fine-tune 35B on consumer GPU"
pullnexus search "local agent loop" --type skill
```

**Browse what's available:**
```bash
pullnexus list-skills --type dataset
pullnexus pull local-rag-starter-pack
```

**Start a submission:**
```bash
pullnexus submit --interactive --type skill
# or open an issue: github.com/MRWillisT/PullNexus/issues/new/choose
```

> Current registry: 155 resources across 10 resource types: skills, tools, templates, playbooks, policies, prompts, datasets, environments, evals, and repositories.

---

## 1. Vision 

Local models are improving quickly, but the surrounding workflow is still fragmented. Useful prompts, JSONL examples, tool definitions, templates, hardware notes, and evaluation sets are scattered across repositories, gists, and chat logs.

PullNexus packages those artifacts into a consistent registry format that can be searched from a CLI today and extended by other clients over time. The practical goal is simple: find a relevant resource, inspect its metadata, pull it if it is installable, or use it as reference material for your own local setup.

It is a small, open distribution layer for local AI workflows rather than a model host, hosted agent platform, or prompt gallery.

---

## 2. Why Now

Several pieces have matured at the same time:

- Local inference tools such as Ollama, llama.cpp, LM Studio, and vLLM are now normal parts of developer workflows.
- More people are keeping inference local because pricing, privacy, and latency matter in day-to-day use.
- The reusable material around those workflows still lacks a standard home. Models and datasets have hubs; operational artifacts usually do not.
- Most adjacent tools solve runtime orchestration or model hosting, not discovery and reuse of smaller building blocks like skills, playbooks, templates, or evals.

That makes a typed, pull-oriented registry useful even at a modest scale.

---

## 3. How It Works

1. Resources are indexed in `skills/index.json` with typed metadata.
2. The CLI can search the registry, filter by type/category/tag, and pull installable resources.
3. Contributors can submit through GitHub or generate a draft folder with the interactive wizard.
4. Resources stay versioned, tagged, and reviewable in the repository.
5. The same schema can support richer clients and integrations later.

### Contribution Workflow

Resources do not need to start as "skills." A useful JSONL conversation set, deployment playbook, model template, policy document, tool reference, or environment profile can all go through the same registry format.

In practice, many entries come from real project work: something becomes reusable, gets documented, and is added to the registry with metadata and optional supporting files.

### CLI Surface

Current public commands:

```
pullnexus search rust debugger --type skill
pullnexus list-skills --category automation
pullnexus pull local-rag-starter-pack
pullnexus submit --interactive --type playbook
```

Some resource types are installable file packages; others are reference entries that point to external repositories, datasets, or documentation.

---

## 4. What a Skill Actually Looks Like

Here's the folder structure for a skill — this is what people submit:

```
skills/python-advanced-debugging/
├── skill.json          → Metadata (name, description, tags, version, license)
├── examples.jsonl      → JSONL conversation pairs or training examples
├── README.md           → Human-readable explanation and usage notes
├── eval.jsonl          → Test cases to verify the skill behaves as expected
└── tools/              → Optional MCP tool definitions
```

**Example skill.json:**
```json
{
  "name": "python-advanced-debugging",
  "version": "1.2.0",
  "description": "Expert techniques for memory leaks, pdb, and tracing in Python",
  "tags": ["python", "debugging", "development"],
  "license": "CC0-1.0",
  "evaluation_cases": 12,
  "mcp_compatible": true
}
```

The structure is intentionally plain so that review, reuse, and validation stay straightforward.

---

## 5. Current Surface

### Available today
- GitHub-backed registry with 155 indexed resources across 10 resource types
- Public CLI commands for search, pull/install, listing, and submission scaffolding
- Interactive submission wizard that generates resource folders and validates metadata
- Schema support for skills, tools, templates, policies, playbooks, prompts, datasets, environments, evals, and repositories
- Local/remote registry fetching so the CLI can degrade gracefully when GitHub is unavailable
- Skill folders built around plain files: metadata, JSONL examples, README, and optional eval/tool definitions

### Near-term work
- Expose the additional packaged command surfaces more cleanly in the main CLI
- Improve MCP/client integration documentation
- Tighten validation, review, and compatibility reporting around submitted resources
- Improve registry browsing and filtering UX
- Add more automation around publishing and quality checks

---

## 6. Positioning

PullNexus sits between raw repositories and full platform products. It is not trying to host models or replace agent runtimes. Its job is narrower: keep reusable local-AI resources in one searchable format with enough metadata to make them easy to discover and reuse.

| Platform | Primary focus | Gap PullNexus addresses |
|---|---|---|
| HuggingFace | Models and datasets | Not organized around smaller local-AI workflow artifacts |
| OpenSkills | Hosted skills ecosystem | Not open, repo-native, or local-first |
| Agent toolkits | Runtime and tool frameworks | Do not solve registry/discovery for reusable resources |
| **PullNexus** | Registry for local-AI resources | Early-stage project focused on schema, search, and contribution flow |

---

## 7. Challenges & Mitigations

| Challenge | Mitigation |
|---|---|
| Quality | Stars, reviews, test cases, curation queue |
| Spam | GitHub workflow + signing |
| Incentives | Attribution, contributor history, and reusable outputs |
| Legal | Clear CC0/MIT contribution license + provenance tracking |

---

## 8. Governance

PullNexus is currently maintained by one person. Decisions about the registry format, contribution rules, and moderation are made openly in the repository through issues and pull requests. That keeps the project straightforward: fast decisions, public rationale, and a clear paper trail.

If the project grows into a true multi-maintainer effort, governance can expand into a lightweight maintainer model with documented roles and decision rules. For now, the priority is simple: keep the standards clear, keep the process public, and keep the project useful.

---

## 9. Registry Highlights

A few entry points worth knowing about:

- `autonomous-agent-training-pack` — 160+ synthetic JSONL examples, 16 themes, ready-to-use train/val/test splits
- `synthetic-general-training-pack` — 110+ general-purpose training examples for coding, reasoning, docs, and web
- `agent-role-orchestrator` / `agent-role-coder` / `agent-role-reviewer` — system prompts for a full multi-agent local setup
- `local-agent-system-blueprint` — beginner guide to building a local autonomous agent system
- `multi-agent-roles-template` — JSON role config for a 5-agent local system out of the box
- `vibe-coder-workflow` — the full self-taught builder loop, from vague idea to working code
- `qwen3-35b-12gb-llama-server` — community-contributed llama-server config for Qwen3 on 12GB VRAM
- `kv-cache-vram-best-practices` — VRAM optimization policy for KV cache tuning
- `n8n-mcp-workflows` / `autonomous-agent-payments` — MCP ecosystem entries

Search the registry to browse all 155 entries: `pullnexus list-skills`

---

## 10. Near-Term Roadmap

| Area | Next step |
|---|---|
| CLI | Expose additional packaged commands more consistently and align help text with the public surface |
| Registry | Keep expanding coverage across the 9 supported resource types while tightening metadata quality |
| Docs | Add clearer integration guidance for CLI, MCP/server usage, and contribution paths |
| Review | Improve validation, compatibility reporting, and contributor feedback loops |
| Discovery | Add better browsing, filtering, and categorization around the live index |



---

## 11. About the Maintainer

PullNexus is maintained by a developer who has spent roughly a year and a half working on real AI-assisted projects. The project grew out of repeated reuse problems: useful prompts, JSONL examples, deployment notes, and tool references kept showing up in ad hoc formats with no clear place to standardize them.

That is why the repository is biased toward practical artifacts and plain files. The goal is not to present a grand platform vision first; it is to make reusable local-AI material easier to package, review, find, and use.



---

*Search the registry. Pull what fits. Submit what helped.*
