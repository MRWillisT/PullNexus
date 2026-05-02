import json, pathlib

path = pathlib.Path("skills/index.json")
idx = json.loads(path.read_text())
existing = {s["name"] for s in idx["skills"]}

new_entries = [
    {
        "name": "uncertainty-behavior-policy",
        "resource_type": "policy",
        "version": "1.0.0",
        "description": "Governs how an AI assistant should behave when it lacks information or confidence. Prefer reversible actions, state what is unknown, inspect before claiming, and correct plainly. Essential for any local agent that makes tool calls or file changes.",
        "tags": ["policy", "uncertainty", "agent", "safety", "local-ai", "behavior", "reliability", "use:policy"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "category": "safety",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "policy_file": "policy.md",
        "compatible_with": ["ollama", "lm-studio", "claude", "openai", "any"]
    },
    {
        "name": "windows-local-ai-tips",
        "resource_type": "policy",
        "version": "1.0.0",
        "description": "Essential commands and safety habits for running local AI on Windows. Covers py -3, ollama, nvidia-smi, rg, and PowerShell-native practices. Reduces common mistakes when managing models, files, and training runs on Windows.",
        "tags": ["policy", "windows", "local-ai", "ollama", "setup", "safety", "powershell", "nvidia", "use:policy"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "category": "setup",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "policy_file": "policy.md",
        "compatible_with": ["ollama", "lm-studio", "any"]
    },
    {
        "name": "multi-agent-roles-template",
        "resource_type": "template",
        "version": "1.0.0",
        "description": "JSON template for defining a multi-agent system: Orchestrator + Planner, Coder, Toolsmith, Reviewer, Memory Keeper roles with personality, handoff outputs, delegation rules, and memory schema. Drop-in starting point for any local agent runtime.",
        "tags": ["template", "multi-agent", "orchestrator", "agent", "local-ai", "planning", "roles", "json", "use:template"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "category": "agent",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "template_file": "template.json",
        "compatible_with": ["ollama", "lm-studio", "claude", "openai", "any"]
    },
    {
        "name": "agent-memory-state-template",
        "resource_type": "template",
        "version": "1.0.0",
        "description": "JSON template for tracking an autonomous agent persistent memory: user preferences, project constraints, active objectives with milestones, rejected approaches, and next actions. Drop into any local agent runtime to enable cross-session continuity.",
        "tags": ["template", "memory", "agent", "local-ai", "multi-agent", "persistence", "json", "use:template"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "category": "agent",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "template_file": "template.json",
        "compatible_with": ["ollama", "lm-studio", "claude", "openai", "any"]
    },
]

added = 0
for e in new_entries:
    if e["name"] not in existing:
        idx["skills"].append(e)
        added += 1

idx["total"] = len(idx["skills"])
idx["updated"] = "2026-05-02"
path.write_text(json.dumps(idx, indent=2))

by_type = {}
for s in idx["skills"]:
    t = s.get("resource_type", "unknown")
    by_type[t] = by_type.get(t, 0) + 1

total = idx["total"]
print(f"Added {added} entries. Total: {total}")
for k, v in sorted(by_type.items()):
    print(f"  {k}: {v}")
