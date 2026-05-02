# Contributing to PullNexus

Thank you for contributing to the open commons of local AI knowledge. Every resource you add makes local models smarter for everyone — for free, forever.

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

You can also contribute:
- **Improvements** — better examples, eval cases, or README clarity for existing resources
- **Bug reports** — issues with the CLI, registry, or skill format
- **Requests** — open an issue describing a resource you'd find useful

---

## Fastest Way to Contribute (No Setup Required)

[Open a Submit Issue](https://github.com/MRWillisT/PullNexus/issues/new/choose) — fill in the form and a maintainer handles the rest. No install, no fork, no JSON.

---

## CLI Wizard (Recommended for Developers)

If you have `pullnexus` installed, the interactive wizard builds your submission folder automatically:

```bash
pip install pullnexus
pullnexus submit --interactive --type template   # or policy, playbook, skill, tool...
```

It prompts for all required fields, auto-parses llama-server flags into structured `config_params`, and writes a ready-to-submit `skill.json` + `README.md` into `submissions/<name>/`. Then open a PR with that folder.

---

## Skill Format

Every skill lives in `skills/<your-skill-name>/` and contains these files:

```
skills/your-skill-name/
├── skill.json          ← Required: metadata (name, description, tags, version, license)
├── examples.jsonl      ← Required: JSONL conversation pairs (the training data)
├── README.md           ← Required: human-readable description and usage
└── eval.jsonl          ← Recommended: test cases to verify the skill works
```

Copy `skills/_template/` to get started:
```bash
cp -r skills/_template skills/your-skill-name
```

### skill.json fields

| Field | Required | Description |
|---|---|---|
| `name` | ✓ | Kebab-case identifier matching the folder name |
| `version` | ✓ | Semantic version string (start with `1.0.0`) |
| `description` | ✓ | One clear sentence — what does this skill teach? |
| `tags` | ✓ | Array of lowercase tag strings for discoverability |
| `license` | ✓ | Must be `CC0-1.0` for community skills |
| `examples` | ✓ | Number of examples in `examples.jsonl` |
| `mcp_compatible` | — | `true` if the skill includes or describes MCP tool usage |
| `author` | — | Your GitHub username |

### examples.jsonl format

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

**Quality guidelines:**
- Minimum 5 examples; aim for 10+
- Use real problems, not textbook examples
- Show the reasoning process, not just the answer
- Include edge cases and failure modes
- Avoid PII, secrets, credentials, and copyrighted content

### eval.jsonl format

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

**Option A — Use the wizard (generates everything):**
```bash
pullnexus submit --interactive --type template
# Output lands in submissions/<name>/
```

**Option B — Build manually, then validate:**
```bash
pullnexus submit path/to/your-skill-name --dry-run
```

Fix any errors before continuing.

### Step 2: Fork and branch

```bash
# Fork MRWillisT/PullNexus on GitHub, then:
git clone https://github.com/YOUR_USERNAME/PullNexus
cd PullNexus
git checkout -b skill/your-skill-name
```

### Step 3: Copy your skill folder

```bash
cp -r path/to/your-skill-name skills/your-skill-name
```

### Step 4: Update the index

Add your skill's metadata to `skills/index.json` — follow the existing format exactly.

### Step 5: Open a Pull Request

Push your branch and open a PR against `main`. Use this title format:
```
skill: add your-skill-name
```

In the PR description, briefly explain:
- What the skill teaches
- Where the examples came from (synthetic, real conversations, etc.)
- Any caveats or known gaps

---

## Review Process

Maintainers will check:
- [ ] All required files present
- [ ] `skill.json` fields complete and valid
- [ ] `examples.jsonl` is valid JSONL with correct schema
- [ ] No PII, secrets, or copyrighted material
- [ ] `skills/index.json` updated
- [ ] `README.md` is clear and accurate

Most skill PRs are reviewed within a few days. If your skill is rejected, the feedback will explain what to fix.

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
- Don't submit skills that contain harmful, deceptive, or unsafe content
- Don't submit skills that teach models to bypass safety measures
- Skills that contain PII, credentials, or proprietary data will be rejected

---

## Questions?

Open an issue with the label `question`. We're happy to help you get your first skill submitted.

*Pull from the Nexus. Give back to the Nexus. Keep local AI smart.*
