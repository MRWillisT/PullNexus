# PullNexus Skill Format Specification

Version: 1.0  
Status: Stable

---

## Overview

A PullNexus skill is a folder containing structured conversation data, metadata, and documentation that teaches a local LLM a specific capability. Skills are designed to be:

- **Usable immediately** — drop a skill folder into your model's context window
- **Fine-tunable** — use `examples.jsonl` as training data for QLoRA or full fine-tuning
- **MCP-compatible** — some skills describe or include MCP tool definitions
- **Community-reviewable** — `eval.jsonl` makes it possible to test skill quality automatically

---

## Folder Structure

```
skills/<skill-name>/
├── skill.json          ← Required: machine-readable metadata
├── examples.jsonl      ← Required: conversation training pairs
├── README.md           ← Required: human-readable description and usage
├── eval.jsonl          ← Recommended: evaluation test cases
└── tools/              ← Optional: MCP tool definitions
    └── tool.json
```

### Naming Convention

Skill folder names must be:
- Lowercase kebab-case: `python-advanced-debugging`, not `Python_Advanced_Debugging`
- Descriptive but concise (2–4 words)
- Unique within the registry

---

## skill.json

The canonical metadata file for a skill.

### Schema

```json
{
  "name": "string",           // Required — kebab-case, matches folder name
  "version": "string",        // Required — semver: "1.0.0"
  "description": "string",    // Required — one sentence describing the skill
  "tags": ["string"],         // Required — array of lowercase tag strings
  "license": "string",        // Required — must be "CC0-1.0" for community skills
  "examples": 0,              // Required — count of examples in examples.jsonl
  "mcp_compatible": false,    // Optional — true if skill includes MCP tool usage
  "author": "string",         // Optional — GitHub username
  "source": "string"          // Optional — "synthetic", "real-conversations", etc.
}
```

### Example

```json
{
  "name": "python-advanced-debugging",
  "version": "1.0.0",
  "description": "Expert multi-turn debugging techniques for Python — async hangs, silent failures, rate limits, and systematic diagnosis workflows.",
  "tags": ["python", "debugging", "async", "development"],
  "license": "CC0-1.0",
  "examples": 6,
  "mcp_compatible": false,
  "author": "MRWillisT",
  "source": "synthetic"
}
```

### Versioning

Follow semantic versioning:
- `patch` (1.0.0 → 1.0.1): Fixed a typo, improved wording in an example
- `minor` (1.0.0 → 1.1.0): Added new examples or eval cases
- `major` (1.0.0 → 2.0.0): Breaking change to skill scope or format

---

## examples.jsonl

The core training data. Each line is a valid JSON object representing one conversation.

### Format: ShareGPT (required)

```jsonl
{"conversations": [{"from": "human", "value": "..."}, {"from": "gpt", "value": "..."}]}
```

**Multi-turn conversations** are fully supported:
```jsonl
{"conversations": [
  {"from": "human", "value": "First question."},
  {"from": "gpt", "value": "First response."},
  {"from": "human", "value": "Follow-up."},
  {"from": "gpt", "value": "Follow-up response."}
]}
```

### Optional: include an id field

```jsonl
{"id": "debug_001", "conversations": [...]}
```

IDs must be unique within the file if provided.

### Quality Standards

| Criteria | Guideline |
|---|---|
| Minimum examples | 5 (aim for 10+) |
| Conversation style | Natural, realistic — not textbook exercises |
| Response quality | Show the reasoning process, not just the answer |
| Edge cases | Include at least one example where the answer is "I need more information" |
| No PII | Remove names, emails, account details, API keys |
| No credentials | No API keys, passwords, or auth tokens — even fake-looking ones |
| No copyrighted text | Don't reproduce full books, articles, or proprietary code |

### Alternative Format: ChatML

Skills may also include a ChatML-format equivalent:
```jsonl
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

If you include both formats, name the ChatML file `examples_chatml.jsonl`.

---

## eval.jsonl

Optional but strongly recommended. Evaluation cases let maintainers and contributors verify that a skill actually works after it's been loaded into a model.

### Schema

```json
{
  "id": "eval_001",
  "input": "The prompt to send to the model.",
  "expected_behavior": "Description of what the ideal response does and does NOT do.",
  "tags": ["tag1", "tag2"]
}
```

### Example

```jsonl
{"id": "eval_debug_001", "input": "My Python bot stops placing orders after 2 hours with no error message.", "expected_behavior": "The model should ask for log output, not immediately suggest a code fix. It should provide a specific grep command and ask about guard conditions.", "tags": ["silent-failure", "diagnosis"]}
```

### How eval.jsonl is Used

- Manual testing by maintainers during PR review
- Future: automated eval runner in CI
- Skill quality badge system (planned)

---

## README.md

A human-readable description of the skill for developers browsing the registry.

### Required Sections

```markdown
# skill-name

One paragraph describing what the skill teaches and when to use it.

## What This Skill Covers

Bullet list of specific capabilities.

## Who Should Use This Skill

Target user or situation description.

## Example Prompts

3–5 example questions this skill helps answer.

## Usage

pullnexus pull skill-name

## License

CC0-1.0 — public domain.
```

---

## tools/ (Optional)

For skills with `mcp_compatible: true`, you may include a `tools/` subfolder with MCP tool definitions.

```
tools/
└── tool.json    ← MCP tool definition (JSON Schema format)
```

MCP tool definition format follows the [MCP specification](https://modelcontextprotocol.io/).

---

## skills/index.json

The machine-readable registry index. Maintained by PullNexus maintainers (updated on each skill PR merge).

```json
{
  "version": "1.0",
  "updated": "YYYY-MM-DD",
  "total": 5,
  "skills": [
    {
      "name": "skill-name",
      "version": "1.0.0",
      "description": "...",
      "tags": ["tag1", "tag2"],
      "license": "CC0-1.0",
      "examples": 10,
      "mcp_compatible": false,
      "author": "github-username"
    }
  ]
}
```

The CLI uses `skills/index.json` as its primary data source for `search`, `list`, and `info` commands.

---

## Validation

Use the CLI to validate your skill before submitting:

```bash
pullnexus submit path/to/your-skill --dry-run
```

Checks performed:
- Required files present (`skill.json`, `examples.jsonl`, `README.md`)
- `skill.json` valid JSON with all required fields
- `examples.jsonl` valid JSONL with correct `conversations` schema
- `eval.jsonl` valid JSONL with recommended fields (warnings only)
- Minimum example count (warning if fewer than 3)

---

*This spec is version 1.0. Changes will be announced in GitHub Discussions before taking effect.*
