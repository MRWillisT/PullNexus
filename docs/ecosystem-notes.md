# PullNexus — Ecosystem Notes
*Context and background on key integrations and emerging capabilities.*

---

## n8n MCP Integration

**What happened:** n8n (open-source Zapier alternative) shipped an official MCP connector.
LLMs can now create and edit full n8n workflows natively via a new TypeScript SDK —
type safety, built-in validation, fluent builder API, direct deployment. No copy-paste JSON hell.

**Why it matters for PullNexus:**
- NOT a competitor — completely different scope
- PROOF the local AI + MCP ecosystem is exploding exactly as the "Why Now" section predicts
- n8n has 1000+ app integrations — automation is a massive use case for local models

**Skill shipped:** `skills/n8n-mcp-workflows/`

**MCP Tool Registry (future):** Beyond JSONL skills, PullNexus could host a curated list of
MCP-compatible tools (n8n, browser control, file systems, APIs) with community reviews and
integration examples. Natural expansion of the registry concept.

**Launch post angle:**
> "The ecosystem is moving fast. n8n just became LLM-native via MCP.
> Where do you find the best skills for using it with your local model?
> That's what PullNexus is for."

---

## x402 Autonomous Agent Payments

**What happened:** @svpino demonstrated an autonomous agent that pays for its own data
using Coinbase's experimental x402 open protocol — on-chain USDC micro-payments over HTTP
on the Base blockchain. No API keys, no credit card, no user intervention.

The agent has its own wallet, detects when it needs paid data (Instagram scraping via Apify),
and handles the payment itself. Built using Apify's MCPC CLI, their MCP server, and Claude Code.

Essentially: **agents that can spend their own money** — a major step toward truly autonomous AI.

**Source:** https://x.com/svpino/status/2049564790604075515

**Why it matters for PullNexus:**
- NOT a competitor — it's a capability, not a registry
- PROOF the MCP ecosystem is maturing fast — first n8n, now autonomous payments
- Apify + x402 + MCPC is exactly the tool combo local model users will want skills for
- Positions PullNexus as the nexus connecting all these emerging MCP capabilities

**Skill shipped:** `skills/autonomous-agent-payments/`

**Monetized Skills (long-term):** x402 opens a door — premium contributors could charge
micro-payments for specialized skills via the same protocol. Free tier stays CC0,
expert skills could be creator-monetized. Community-owned but sustainably funded.

**Launch post angle:**
> "n8n just became LLM-native. Agents just got their own wallets.
> The MCP ecosystem is moving fast. PullNexus is where the community
> shares how to actually use all of it."

**"Why Now" additions for vision.md:**
- "n8n just shipped native MCP support — major tools are becoming LLM-editable. PullNexus is where the community shares how to use them."
- "Agents can now pay for their own data via Coinbase's x402 protocol — the autonomous agent economy is starting. PullNexus is where you find the skills to build with it."
