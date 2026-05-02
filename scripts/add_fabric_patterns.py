"""Add top 20 Fabric patterns from danielmiessler/Fabric as skill entries."""
import json, pathlib

TOP_PATTERNS = [
    ("extract_wisdom",      "Extract the most insightful ideas, quotes, and actionable advice from any text or transcript. Fabric's most famous pattern — outputs structured wisdom blocks.", ["summarize", "insights", "learning", "content", "use:writing"]),
    ("summarize",           "Produce a clean, structured summary of any input text: one-sentence TL;DR, key points, and action items. General-purpose and reliable.", ["summarize", "writing", "productivity", "use:writing"]),
    ("analyze_paper",       "Deep analysis of an academic or technical paper: core claims, methodology, evidence quality, and practical takeaways for practitioners.", ["research", "academic", "analysis", "reading", "use:research"]),
    ("improve_writing",     "Rewrite and improve any prose for clarity, concision, and impact. Preserves voice while eliminating filler and fixing structure.", ["writing", "editing", "content", "use:writing"]),
    ("explain_code",        "Explain any code snippet in plain language: what it does, how it works, potential issues, and suggested improvements.", ["code", "debugging", "learning", "developer", "use:code"]),
    ("review_code",         "Code review with actionable feedback: bugs, security issues, style violations, and concrete suggestions for improvement.", ["code", "review", "security", "developer", "use:code"]),
    ("create_summary",      "Create a comprehensive summary with sections: one-line summary, key points, quotes, and references. More structured than summarize.", ["summarize", "writing", "productivity", "use:writing"]),
    ("find_logical_fallacies", "Identify logical fallacies in any argument or text. Returns fallacy name, example from text, and explanation. Useful for research and debate prep.", ["reasoning", "analysis", "critical-thinking", "debate", "use:research"]),
    ("analyze_claims",      "Evaluate factual claims in text for accuracy and evidence quality. Separates well-supported claims from speculation and misinformation.", ["analysis", "fact-checking", "research", "reasoning", "use:research"]),
    ("improve_prompt",      "Take a rough LLM prompt and rewrite it to be more precise, structured, and likely to get the intended output. Meta-skill for prompt engineering.", ["prompting", "llm", "developer", "prompt-engineering", "use:developer"]),
    ("create_user_story",   "Convert a feature description or requirement into a properly formatted Agile user story with acceptance criteria.", ["agile", "product", "planning", "developer", "use:developer"]),
    ("write_essay",         "Write a well-structured essay on any topic: thesis, supporting arguments, counterarguments, and conclusion. Paul Graham style by default.", ["writing", "content", "essays", "use:writing"]),
    ("create_mermaid_visualization", "Convert any structured information (process, system, relationships) into a Mermaid diagram definition ready to render.", ["visualization", "diagrams", "mermaid", "developer", "use:developer"]),
    ("summarize_git_diff",  "Summarize a git diff into a clear, human-readable explanation of what changed and why. Perfect for PR descriptions and changelogs.", ["git", "code", "developer", "changelog", "use:code"]),
    ("create_git_diff_commit", "Generate a well-formatted git commit message from a diff. Follows conventional commits format with scope and description.", ["git", "code", "developer", "commits", "use:code"]),
    ("analyze_threat_report", "Extract key threat intelligence from a security report: threat actors, TTPs, IOCs, and recommended mitigations. CISA/MITRE-aware.", ["security", "threat-intel", "analysis", "cybersecurity", "use:security"]),
    ("create_stride_threat_model", "Generate a STRIDE threat model from a system description: Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege.", ["security", "threat-modeling", "stride", "developer", "use:security"]),
    ("extract_ideas",       "Pull the most interesting and novel ideas from any content. Returns a clean bulleted list, no filler. Great for rapid research synthesis.", ["ideas", "research", "brainstorm", "learning", "use:research"]),
    ("create_prd",          "Create a Product Requirements Document from a feature description or problem statement. Includes goals, non-goals, requirements, and open questions.", ["product", "planning", "prd", "developer", "use:developer"]),
    ("label_and_rate",      "Label content by category and quality, then rate it on multiple dimensions. Useful for batch triage of large content collections.", ["content", "rating", "classification", "productivity", "use:writing"]),
]

p = pathlib.Path("skills/index.json")
idx = json.loads(p.read_text())
existing = {s["name"] for s in idx["skills"]}

added = 0
for slug, desc, tags in TOP_PATTERNS:
    name = f"fabric-{slug.replace('_', '-')}"
    if name in existing:
        continue
    cat = next((t.split(":")[1] for t in tags if t.startswith("use:")), "other")
    idx["skills"].append({
        "name": name,
        "resource_type": "skill",
        "version": "1.0.0",
        "description": desc,
        "tags": tags,
        "license": "MIT",
        "author": "danielmiessler",
        "source": f"https://github.com/danielmiessler/fabric/tree/main/data/patterns/{slug}",
        "repo": "danielmiessler/Fabric",
        "fabric_pattern": slug,
        "installable": False,
        "category": cat,
        "maturity": "stable",
        "maintained": "yes",
        "last_verified": "2026-05-02",
    })
    added += 1

idx["total"] = len(idx["skills"])
idx["updated"] = "2026-05-02"
p.write_text(json.dumps(idx, indent=2))
print(f"Added {added} Fabric patterns. New total: {idx['total']}")
