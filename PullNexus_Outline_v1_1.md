# PullNexus — Project To-Do List
*Last updated: 2026-04-30*

---

## 🔴 URGENT — Do This Week

### 1. Create Core Repo Files
Create the following structure in `MRWillisT/PullNexus` on GitHub:

```
README.md              ✅ Done (outline in place)
CONTRIBUTING.md        ← stub, even one paragraph is fine
LICENSE                ← use MIT or CC0-1.0
docs/
  vision.md            ← paste the full PullNexus_Outline_v1.md here
  skill-format.md      ← the skill schema spec (the folder example + skill.json)
skills/
  _template/
    skill.json         ← blank template contributors copy
    examples.jsonl     ← 2-3 placeholder examples showing format
    README.md          ← "fill this out to describe your skill"
    eval.jsonl         ← placeholder eval format
```

### 2. Lock Down the Name Everywhere
- [ ] GitHub org: `PullNexus` ✅ Done
- [ ] GitHub repo: `MRWillisT/PullNexus` ✅ Done
- [ ] PyPI — register `pullnexus` as a package (even a placeholder)
- [ ] Domain — grab `pullnexus.dev` or `pullnexus.io`

### 3. Transfer Plan
- Keep repo private under personal account while building
- Transfer to PullNexus org when ready to go public
- Settings → Transfer Repository → type org name → done

---

## 🟡 This Month

### 4. Convert Seed Skills From Existing JSONL Dataset
Pull directly from `W:\Copilot-Training-Data\ready-for-training\synthetic\` — these are basically ready:

- [ ] `python-advanced-debugging` ← from `synthetic_multiturn_debugging_2026-04-28.jsonl`
- [ ] `pytest-and-testing` ← from `synthetic_pytest_testing_2026-04-28.jsonl`
- [ ] `vibe-coder-workflow` ← from `autonomous_agent_sharegpt_vibecoder_10.jsonl`
- [ ] `reasoning-and-problem-solving` ← from `synthetic_reasoning_and_problem_solving_2026-04-28.jsonl`
- [ ] `code-refactoring` ← from converted-chats Code Refactoring files
- [ ] `crypto-trading-bot` ← from `synthetic_crypto_trading_knowledge_2026-04-28.jsonl`
- [ ] `n8n-mcp-workflows` ← NEW (see feature note below ⬇️)
- [ ] `autonomous-agent-payments` ← NEW (see x402 feature note below ⬇️)

### 5. Build the CLI (Python)
Basic commands to start:
```
pullnexus search <query>
pullnexus install <skill-name>
pullnexus submit <path-to-skill>
pullnexus list
```

### 6. GitHub Pages Landing Page
Simple one-pager for now. Name, tagline, what it is, how to contribute, link to repo.

---

## 🟢 Launch (Day 30 Target)

### 7. Write Launch Post
Post on:
- [ ] r/LocalLLaMA
- [ ] r/MachineLearning
- [ ] HuggingFace community
- [ ] X/Twitter
- [ ] Continue.dev Discord

### 8. Reach Out To
- [ ] Ollama team
- [ ] LM Studio team
- [ ] Continue.dev maintainers
- [ ] n8n community (see n8n feature note below)
- [ ] Apify community (MCPC CLI + MCP server — see x402 feature note below)
- [ ] Coinbase developer community (x402 protocol)

---

## 💡 FEATURE NOTE — n8n MCP Integration (Add As Seed Skill + Future Feature)

**What happened:** n8n (open-source Zapier alternative) just shipped an official MCP connector.
LLMs can now create and edit full n8n workflows natively via a new TypeScript SDK.
Type safety, built-in validation, fluent builder API, direct deployment — no copy-paste JSON hell.

**Why it matters for PullNexus:**
- NOT a competitor — completely different scope
- PROOF the local AI + MCP ecosystem is exploding exactly like the "Why Now" section predicts
- n8n has 1000+ app integrations — automation is a massive use case for local models

**What to do with this:**

1. **Seed skill on day one:** `n8n-mcp-workflows` — teach local models how to use the n8n MCP
   connector to build automation workflows. Would be one of the most useful skills in the
   registry immediately.

2. **"Why Now" update:** Add a bullet point to the vision doc:
   > "n8n just shipped native MCP support — major tools are becoming LLM-editable.
   > PullNexus is where the community shares how to use them."

3. **Future feature — MCP Tool Registry:** Beyond JSONL skills, PullNexus could host
   a curated list of MCP-compatible tools (n8n, browser control, file systems, APIs)
   with community reviews and integration examples. This is a natural expansion of
   the registry concept.

4. **Launch post angle:** Use n8n as an example of the momentum:
   > "The ecosystem is moving fast. n8n just became LLM-native via MCP.
   > Where do you find the best skills for using it with your local model?
   > That's what PullNexus is for."

**Bottom line:** This is bullish. The timing window just got wider.
People are actively building MCP-native tools and they need somewhere to share and
discover skills for using them. That's PullNexus.

---

## 💡 FEATURE NOTE — x402 Autonomous Agent Payments (Seed Skill + Future Feature)

**What happened:** @svpino demonstrated an autonomous agent that pays for its own data
using Coinbase's experimental x402 open protocol — on-chain USDC micro-payments over HTTP
on the Base blockchain. No API keys, no credit card, no user intervention.

The agent has its own wallet, detects when it needs paid data (Instagram scraping via Apify),
and handles the payment itself. Built using Apify's MCPC CLI, their MCP server, and Claude Code.

Essentially: **agents that can spend their own money** — a major step toward truly autonomous AI.

**Why it matters for PullNexus:**
- NOT a competitor — it's a capability, not a registry
- PROOF the MCP ecosystem is maturing fast — first n8n, now autonomous payments
- Apify + x402 + MCPC is exactly the kind of tool combo local model users will want skills for
- Positions PullNexus as the nexus that connects all these emerging MCP capabilities

**What to do with this:**

1. **Seed skill on day one:** `autonomous-agent-payments` — teach local models how to set up
   x402 wallets, configure MCPC, and call paid Apify tools autonomously. Cutting edge, high
   value, nobody else has this documented as a pullable skill yet.

2. **"Why Now" update:** Add to the vision doc:
   > "Agents can now pay for their own data via Coinbase's x402 protocol — the autonomous
   > agent economy is starting. PullNexus is where you find the skills to build with it."

3. **Future feature — Monetized Skills:** x402 opens an interesting long-term door —
   premium skill contributors could eventually charge micro-payments for specialized,
   high-quality skills via the same protocol. Free tier stays free (CC0), but expert
   skills could be monetized by their creators. Community-owned but sustainably funded.

4. **Launch post angle:** Stack n8n + x402 together as momentum proof:
   > "n8n just became LLM-native. Agents just got their own wallets.
   > The MCP ecosystem is moving fast. PullNexus is where the community
   > shares how to actually use all of it."

5. **Reach out:** Post in Apify's community and tag @svpino on X — this is exactly the
   kind of project that gets signal boosts from people building in this space.

**Source:** https://x.com/svpino/status/2049564790604075515

**Bottom line:** Two massive ecosystem validations in one day (n8n + x402).
The "Why Now" section of your vision doc is writing itself in real time.

---

## 📋 Backlog (Later)

- [ ] Automated quality scoring + evals
- [ ] Federated nodes (self-hosted mirrors)
- [ ] Bounty board for missing skills
- [ ] Reputation + leaderboard system
- [ ] Web search API for local models
- [ ] Formal governance / foundation structure
- [ ] Monetized premium skills via x402 micro-payments (long term)

---

*"Pull from the Nexus. Give back to the Nexus. Keep local AI smart."*
