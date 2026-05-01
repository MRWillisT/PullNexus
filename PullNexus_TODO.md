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

Other stuff to add - Best GitHub repos for Claude Code that will 10x your next project in 2026 

1. Claude Mem
http://github.com/thedotmack/claude-mem
Persistent memory across sessions � stop re-teaching Claude your codebase

2. UI UX Pro Max
http://github.com/nextlevelbuilder/ui-ux-pro-max-skill
50+ styles, 161 color palettes, 99 UX guidelines � Claude stops building ugly UIs

3. n8n-MCP
http://github.com/czlonkowski/n8n-mcp
Connect Claude Code to 400+ n8n integrations via MCP

4. LightRAG
http://github.com/hkuds/lightrag
Graph + vector RAG � lets Claude understand large codebases structurally

5. Everything Claude Code
http://github.com/affaan-m/everything-claude-code
Skills, instincts, security scanning, multi-language coverage � full agent harness

6. Awesome Claude Code
http://github.com/hesreallyhim/awesome-claude-code
Community bible � curated skills, hooks, slash commands, orchestrators

7. Superpowers
http://github.com/obra/superpowers
Forces structured thinking before writing a single line of code

8. Claude Code Ultimate Guide
http://github.com/FlorianBruniaux/claude-code-ultimate-guide
23K+ lines of docs, 219 templates, 271 quizzes � beginner to power user

9. Antigravity Awesome Skills
http://github.com/sickn33/antigravity-awesome-skills
1,200+ ready-to-use skills � one of the largest collections

10. Claude Agent Blueprints  
http://github.com/danielrosehill/Claude-Code-Repos-Index
75+ agent workspace templates beyond coding

11. VoiceMode MCP 
http://github.com/mikecbaley/voicemode-mcp
Natural voice conversations with Claude Code via Whisper + Kokoro

12. Awesome Claude Plugins 
http://github.com/quemsah/awesome-claude-plugins
9,000+ repos indexed with adoption metrics � find what people actually install

---

## 📋 Backlog (Later)

- [ ] Automated quality scoring + evals
- [ ] Federated nodes (self-hosted mirrors)
- [ ] Bounty board for missing skills
- [ ] Reputation + leaderboard system
- [ ] Web search API for local models
- [ ] Formal governance / foundation structure

---

*"Pull from the Nexus. Give back to the Nexus. Keep local AI smart."*
