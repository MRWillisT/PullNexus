import json, pathlib

path = pathlib.Path("skills/index.json")
idx = json.loads(path.read_text())
existing = {s["name"] for s in idx["skills"]}

new_entries = [
    {
        "name": "autonomous-agent-training-pack",
        "resource_type": "dataset",
        "version": "1.0.0",
        "description": "160+ synthetic JSONL training examples for local autonomous agent behavior. 16 themed files covering planning, coding, tool use, multi-agent coordination, safety, memory, reliability, evaluation, vibe-coding, and general assistant patterns. Includes train/val/test splits, validation script, split generator, manifest, and sampling guide.",
        "tags": ["dataset", "training", "autonomous-agent", "local-ai", "sharegpt", "chatml", "synthetic", "multi-agent", "tool-use", "safety", "memory", "use:dataset"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "category": "training",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "installable": True,
        "formats": ["sharegpt", "chatml"],
        "total_examples": 160,
        "compatible_with": ["axolotl", "unsloth", "llama-factory", "torchtune", "trl"]
    },
    {
        "name": "synthetic-general-training-pack",
        "resource_type": "dataset",
        "version": "1.0.0",
        "description": "110+ synthetic JSONL training examples for general coding assistant behavior. 11 themed files covering backtesting, execution, general assistant, web languages, README writing, reasoning, risk, trading psychology, uncertainty, refusals, and vibe coding. Useful for reducing domain skew in any local model.",
        "tags": ["dataset", "training", "synthetic", "local-ai", "sharegpt", "general-assistant", "coding", "web", "use:dataset"],
        "license": "MIT",
        "author": "PullNexus Contributors",
        "source": "https://github.com/MRWillisT/PullNexus",
        "category": "training",
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
        "installable": True,
        "formats": ["sharegpt"],
        "total_examples": 110,
        "compatible_with": ["axolotl", "unsloth", "llama-factory", "torchtune", "trl"]
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
