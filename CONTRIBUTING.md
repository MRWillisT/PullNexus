# Contributing to PullNexus

This guide covers how to contribute resources to the PullNexus registry and how submissions are reviewed.

---

## What Can I Contribute?

| Type | What it is | Example |
|---|---|---|
| **skill** | JSONL conversation examples that teach a capability | `python-advanced-debugging` |
| **template** | Launch config, command flags, or config file | `qwen3-35b-12gb-llama-server` |
| **policy** | Best-practice rule set or operational guideline | `kv-cache-vram-best-practices` |
| **playbook** | Step-by-step runbook for setup or deployment | `ollama-open-webui-setup` |
| **tool** | CLI tool, script, or MCP-compatible tool | `ollama`, `llama.cpp` |
| **dataset** | Curated JSONL or HuggingFace dataset | HF training sets |
| **environment** | Hardware/software stack profile | `env-8gb-vram-local-chat` |
| **eval** | Benchmark or evaluation harness | evaluation suites |
| **repository** | External repository worth indexing as a reference | `ggml-org/llama.cpp` |

You can also contribute:
- **Improvements** — better examples, eval cases, or README clarity for existing resources
- **Bug reports** — issues with the CLI, registry, or skill format
- **Requests** — open an issue describing a resource you'd find useful

---

## Fastest Way to Contribute (No Setup Required)

[Open a Submit Issue](https://github.com/MRWillisT/PullNexus/issues/new/choose) if you want to suggest a resource without setting up the CLI or preparing files yourself.

---

## CLI Wizard (Recommended for Developers)

If you have `pullnexus` installed, the interactive wizard builds your submission folder automatically:

```bash
pip install pullnexus
pullnexus submit --interactive --type template   # or policy, playbook, skill, tool...
```

It prompts for the required fields, parses llama-server flags into structured `config_params` where relevant, and writes a submission folder into `submissions/<name>/`. From there, open a pull request with the generated files.

---

## Skill Format

PullNexus supports multiple resource types. The layout below is specific to `skill` submissions, which are the most structured resource type in the registry.

Every skill lives in `skills/<your-skill-name>/` and contains these files:

```
skills/your-skill-name/
├── skill.json          ← Required: metadata (name, description, tags, version, license)
├── examples.jsonl      ← Required: JSONL conversation pairs or examples
├── README.md           ← Required: human-readable description and usage
└── eval.jsonl          ← Recommended: test cases to verify the skill works
```

Copy `skills/_template/` to get started:
```bash
cp -r skills/_template skills/your-skill-name
```

### `skill.json` fields

| Field | Required | Description |
|---|---|---|
| `name` | ✓ | Kebab-case identifier matching the folder name |
| `version` | ✓ | Semantic version string (start with `1.0.0`) |
| `description` | ✓ | One clear sentence describing what the skill teaches |
| `tags` | ✓ | Array of lowercase tag strings for discoverability |
| `license` | ✓ | Must be `CC0-1.0` for community skills |
| `examples` | ✓ | Number of examples in `examples.jsonl` |
| `mcp_compatible` | — | `true` if the skill includes or describes MCP tool usage |
| `author` | — | Your GitHub username |

### `examples.jsonl` format

Each line must be valid JSON with a `conversations` key (ShareGPT format):

```json
{"conversations": [
  {"from": "human", "value": "The user's question or request."},
  {"from": "gpt", "value": "The ideal assistant response."}
]}
```

Multi-turn conversations are supported:
```json
{"conversations": [
  {"from": "human", "value": "First question."},
  {"from": "gpt", "value": "First response."},
  {"from": "human", "value": "Follow-up."},
  {"from": "gpt", "value": "Follow-up response."}
]}
```

Quality guidelines:
- Minimum 5 examples; aim for 10+
- Use real problems, not textbook examples
- Show the reasoning process, not just the answer
- Include edge cases and failure modes
- Avoid PII, secrets, credentials, and copyrighted content

### `eval.jsonl` format

Each line is a test case:
```json
{
  "id": "eval_001",
  "input": "The prompt to test the model with.",
  "expected_behavior": "Description of what the ideal response does (and avoids).",
  "tags": ["tag1", "tag2"]
}
```

---

## Submitting via Pull Request

### Step 1: Build or validate your submission

**Option A: Use the wizard**
```bash
pullnexus submit --interactive --type template
# Output lands in submissions/<name>/
```

**Option B: Build manually, then validate**
```bash
pullnexus submit path/to/your-resource-name --dry-run
```

Fix any errors before continuing.

### Step 2: Fork and branch

```bash
# Fork MRWillisT/PullNexus on GitHub, then:
git clone https://github.com/YOUR_USERNAME/PullNexus
cd PullNexus
git checkout -b resource/your-resource-name
```

### Step 3: Copy your resource folder

```bash
cp -r path/to/your-resource-name skills/your-resource-name
```

For non-skill resources, keep the generated metadata and README together in the folder you submit.

### Step 4: Update the index

Add your resource metadata to `skills/index.json` and follow the existing format exactly.

### Step 5: Open a Pull Request

Push your branch and open a PR against `main`. Use this title format:
```
resource: add your-resource-name
```

In the PR description, briefly explain:
- What the resource is for
- Where the examples or source material came from
- Any caveats or known gaps

---

## Review Process

Maintainers will check:
- [ ] All required files present
- [ ] `skill.json` fields complete and valid
- [ ] Any included JSONL files are valid and match the expected schema
- [ ] No PII, secrets, or copyrighted material
- [ ] `skills/index.json` updated
- [ ] `README.md` is clear and accurate

Most PRs are reviewed within a few days. If a submission is rejected or needs changes, the review should explain what to fix.

---

## Improving Existing Skills

Open a PR that:
- Adds more examples to `examples.jsonl`
- Adds or improves `eval.jsonl` cases
- Fixes errors in `README.md`
- Bumps the `version` in `skill.json` (patch version for small fixes, minor for new content)

---

## Code of Conduct

- Be respectful and constructive in reviews
- Don't submit resources that contain harmful, deceptive, or unsafe content
- Don't submit resources that teach models to bypass safety measures
- Resources that contain PII, credentials, or proprietary data will be rejected

---

## Questions?

Open an issue with the label `question`.

*Search the registry. Pull what fits. Submit what helped.*
