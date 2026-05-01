# PullNexus — Vision

**Tagline:** Your local AI shouldn't have to be dumb. Pull skills, tools, and knowledge on demand — free, open, community-built.

---

## 1. The Problem

Local LLMs are powerful but isolated. They:

- Forget niche expertise outside their training data
- Hallucinate on specialized domains (trading, radar, async debugging)
- Keep reinventing the wheel — every user teaches their model the same things separately
- Have no way to acquire new capabilities on demand without a full retrain

When a local model hits a wall, today's only options are:
1. Prompt engineer around the limitation (often fails)
2. Switch to a cloud API (costs money, kills privacy, breaks local-first philosophy)
3. Fine-tune with more data (requires weeks of work)

There's a missing infrastructure layer: **a pull-on-demand registry for local AI capabilities.**

---

## 2. The Solution: PullNexus

PullNexus is a living, open commons where anyone contributes high-quality skills, tools, curated conversations, JSONL training data, or prompt packs. Your local model (Ollama, LM Studio, llama.cpp) hits a wall → queries PullNexus → instantly pulls the exact skill it needs → levels up on the fly.

**No subscriptions. No corporate gatekeeping. Just Wikipedia + Hugging Face + npm, built for local AI brains.**

### The Core Loop

```
1. Local model encounters a limitation
2. Developer runs: pullnexus search <topic>
3. CLI finds the right skill
4. Developer runs: pullnexus pull <skill-name>
5. Model loads skill into context or uses it for fine-tuning
6. Model is now smarter on that topic
7. Developer improves the skill → submits it back
8. Everyone benefits from the improvement
```

---

## 3. Why Now

The timing is perfect:

- **Ollama** crossed massive mainstream adoption — local AI is no longer niche
- **Affordable hardware is here:** RTX 5060 Ti and equivalents make strong VRAM setups realistic for regular users
- **Growing backlash** against API pricing and paywalls is pushing more people toward fully local setups
- **The "AI skills" ecosystem is exploding**, but there's still no general-purpose, community-owned, pull-on-demand registry
- **n8n shipped native MCP support** — major tools are becoming LLM-editable. PullNexus is where the community shares how to use them
- **Agents can now pay for their own data** via Coinbase's x402 protocol — the autonomous agent economy is starting. PullNexus is where you find the skills to build with it
- **HuggingFace is a great data warehouse. OpenSkills is closed. Agent toolkits are provider-specific.** None of them are local-first, pull-on-demand, and community-owned

---

## 4. What a Skill Is

A PullNexus skill is a folder containing:

```
skills/python-advanced-debugging/
├── skill.json          ← Metadata: name, description, tags, version, license
├── examples.jsonl      ← JSONL conversation pairs (the real training data)
├── README.md           ← Human-readable explanation + usage instructions
└── eval.jsonl          ← Test cases to verify the skill works
```

Skills can be used three ways:
1. **RAG / context injection** — drop the folder into your model's context window
2. **Fine-tuning data** — use `examples.jsonl` to teach behavior patterns
3. **MCP tool** — skills with `mcp_compatible: true` integrate with tool-calling frameworks

---

## 5. The Contributor Loop (Unfair Advantage)

Real conversations with local models → JSONL pipeline → high-quality training data → submit back to the commons. Real usage becomes new skills. This closes the loop beautifully and makes contribution nearly effortless.

No other project in this space has this. The founding dataset was built from 1.5 years of real AI-assisted project work — not synthetic textbook examples.

```
Use local AI on real projects
         ↓
Export conversations → run JSONL pipeline
         ↓
High-quality training examples (verified by real usage)
         ↓
Submit to PullNexus as a skill
         ↓
Community benefits → model gets smarter → more real usage
         ↓
[loop]
```

---

## 6. Differentiation

| Platform | What It Is | What's Missing |
|---|---|---|
| HuggingFace | Data warehouse | Not pull-on-demand, not local-first |
| OpenSkills | Skills ecosystem | Closed, provider-specific |
| Agent toolkits | Tool calling frameworks | Not community-owned, not general-purpose |
| **PullNexus** | Living skill commons | **Nothing — this is it** |

---

## 7. Core Features

### MVP (Ship First)
- Standardized skill format (JSONL + Markdown as the core spec)
- GitHub-backed registry + simple web UI (GitHub Pages to start)
- CLI tool: `pullnexus pull`, `pullnexus search`, `pullnexus submit`, `pullnexus list`, `pullnexus info`
- 10 seed skills live on day one
- Ollama / LM Studio / MCP integration examples

### Later
- Web search API for local models
- Automated quality scoring + evals
- Federated nodes (run your own mirror)
- Bounty board for missing skills
- Reputation system
- Monetized premium skills via x402 micro-payments (optional tier, free tier stays free)
- MCP Tool Registry — curated list of MCP-compatible tools with community reviews

---

## 8. Challenges & Mitigations

| Challenge | Mitigation |
|---|---|
| Quality | Stars, reviews, test cases, curation queue |
| Spam | GitHub workflow + signing |
| Incentives | Leaderboards, badges, PullNexus Hall of Fame |
| Legal | Clear CC0/MIT contribution license + provenance tracking |

---

## 9. Governance

PullNexus will start with a simple steering committee of founding contributors. Major decisions — core registry policies, format changes — go through public discussion with voting weighted by contribution history. As it grows, it can evolve into a proper open source foundation structure.

---

## 10. Seed Skills (Day One Inventory)

All built from real conversations and battle-tested JSONL pipelines — not theoretical:

| Skill | Source |
|---|---|
| `python-advanced-debugging` | synthetic_multiturn_debugging |
| `pytest-and-testing` | synthetic_pytest_testing |
| `vibe-coder-workflow` | autonomous_agent_sharegpt_vibecoder |
| `reasoning-and-problem-solving` | synthetic_reasoning_and_problem_solving |
| `autonomous-agent-patterns` | autonomous_agent_sharegpt |
| `code-refactoring` | converted-chats code refactoring sessions |
| `crypto-trading-bot` | synthetic_crypto_trading_knowledge |
| `n8n-mcp-workflows` | community + MCP workflow patterns |
| `autonomous-agent-payments` | community + x402 payment flow patterns |
| `kronos-trading-integration` | KronosA forecast integration patterns |

---

*PullNexus — Pull from the Nexus. Give back to the Nexus. Keep local AI smart.*
