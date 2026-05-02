import json
import pathlib

path = pathlib.Path("skills/index.json")
idx = json.loads(path.read_text())

new_entries = [
    {
        "name": "agent-role-coder",
        "resource_type": "prompt",
        "version": "1.0.0",
        "description": "System prompt for a Coder specialist agent. Focused on accurate implementation, test-backed changes, and self-correcting error handling. Drop into any local LLM or multi-agent setup.",
        "tags": ["prompt", "system-prompt", "agent", "coder", "multi-agent", "local-ai", "use:prompt"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "installable": True,
        "category": "agent",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "prompt_file": "system_prompt.txt",
        "compatible_with": ["ollama", "lm-studio", "claude", "openai"]
    },
    {
        "name": "agent-role-orchestrator",
        "resource_type": "prompt",
        "version": "1.0.0",
        "description": "System prompt for the Orchestrator -- the primary autonomous agent role. Plans, delegates to specialist roles, maintains memory, and verifies outcomes. The top-level brain of a multi-agent local AI system.",
        "tags": ["prompt", "system-prompt", "agent", "orchestrator", "multi-agent", "local-ai", "planning", "use:prompt"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "installable": True,
        "category": "agent",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "prompt_file": "system_prompt.txt",
        "compatible_with": ["ollama", "lm-studio", "claude", "openai"]
    },
    {
        "name": "agent-role-reviewer",
        "resource_type": "prompt",
        "version": "1.0.0",
        "description": "System prompt for a Reviewer specialist agent. Critically evaluates changes, identifies bugs and regressions, requires evidence for correctness claims. Outputs structured findings with severity ordering and a final verdict.",
        "tags": ["prompt", "system-prompt", "agent", "reviewer", "code-review", "multi-agent", "local-ai", "use:prompt"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "installable": True,
        "category": "agent",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "prompt_file": "system_prompt.txt",
        "compatible_with": ["ollama", "lm-studio", "claude", "openai"]
    },
    {
        "name": "local-agent-system-blueprint",
        "resource_type": "prompt",
        "version": "1.0.0",
        "description": "Beginner-friendly guide for building a local autonomous agent system: Brain/Hands/Manager/Memory layers, personality vs role separation, runtime loop, minimum memory, and tool stack. Pairs with the Orchestrator/Coder/Reviewer prompts.",
        "tags": ["prompt", "blueprint", "agent", "local-ai", "multi-agent", "orchestrator", "beginner", "planning", "use:prompt"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "installable": True,
        "category": "agent",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "prompt_file": "blueprint.md",
        "compatible_with": ["ollama", "lm-studio", "any"]
    },
]

# Check if vibe-coder-workflow already in index, update its tags if so
existing_names = {s["name"] for s in idx["skills"]}
for entry in new_entries:
    if entry["name"] not in existing_names:
        idx["skills"].append(entry)

# Update vibe-coder-workflow in place to add prompt tag + workflow_file
for s in idx["skills"]:
    if s["name"] == "vibe-coder-workflow":
        if "prompt" not in s.get("tags", []):
            s["tags"].append("prompt")
        if "vibe-coder" not in s.get("tags", []):
            s["tags"].append("vibe-coder")
        s["prompt_file"] = "workflow.md"
        s["last_verified"] = "2026-05-02"
        break

idx["total"] = len(idx["skills"])
idx["updated"] = "2026-05-02"

path.write_text(json.dumps(idx, indent=2))

by_type = {}
for s in idx["skills"]:
    t = s.get("resource_type", "unknown")
    by_type[t] = by_type.get(t, 0) + 1

print(f"Total: {idx['total']}")
for k, v in sorted(by_type.items()):
    print(f"  {k}: {v}")
