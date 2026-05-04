---
name: premortem
description: "Run a premortem on any plan, launch, product, hire, strategy, or decision. Assumes it already failed 6 months from now and works backward to find every reason why. MANDATORY TRIGGERS: 'premortem this', 'premortem my', 'run a premortem', 'what could kill this', 'stress test this plan', 'find the blind spots'. STRONG TRIGGERS: 'what could go wrong', 'poke holes in this', 'devil's advocate this'. Do NOT trigger on simple feedback requests or factual questions."
---

# Premortem

A premortem assumes a plan already failed 6 months from now and works backward to find every reason why — before it happens. From psychologist Gary Klein, validated by Kahneman. Forces honest failure generation instead of agreeable risk-hedging.

---

## When to Run a Premortem

**Good targets:**
- A product or feature about to be built
- A launch with money or reputation at stake
- A pricing change or business model shift
- A hire you're about to make
- A strategy or positioning pivot
- Any commitment where the cost of being wrong is high

**Bad targets:**
- Vague ideas with no concrete plan yet (help them plan first)
- Questions with one right answer
- Decisions already made and irreversible
- Simple creative feedback requests

---

## Step 1: Gather Context First

Before running anything, scan for existing context:
- Current conversation (user may have already described the plan)
- Workspace files: `CLAUDE.md`, `memory/`, any attached briefs

You need three things to proceed:
1. **What is it?** — Describe the plan in one sentence
2. **Who is it for / who does it affect?**
3. **What does success look like?** — Failure is the inverse of success

If any of the three are missing, ask for the most important one. One question at a time. Never ask more than you need.

---

## Step 2: Set the Frame

After context is sufficient, state the frame explicitly:

> "OK. It's 6 months from now. [The plan] has failed. We're looking back and trying to understand why."

This framing is not optional. It shifts the mode from "evaluate this plan" (agreeable) to "explain why this died" (honest).

---

## Step 3: Generate Failure Reasons (Raw Premortem)

Run a comprehensive failure analysis — no prescribed categories, no constraints:

> "This plan has failed 6 months from now. Generate every genuine reason it could have died. Be specific. Ground every reason in the actual details of the plan."

Each failure reason should be:
- Specific to this plan (not generic advice that applies to anything)
- Grounded in details the user provided
- A genuine threat (not a minor inconvenience or extremely unlikely edge case)

The number of failure reasons should be whatever is real — some plans have 4, others have 9.

---

## Step 4: Deep-Dive Agents (Parallel)

Spawn one sub-agent per failure reason, all in parallel. Each agent goes deep on one assigned failure reason.

**Sub-agent prompt template:**
```
You are an investigator in a premortem analysis. Assigned failure reason: [specific reason].

The plan: [full context]

PREMORTEM FRAME: It is 6 months from now. This plan has failed.

Produce:
1. THE FAILURE STORY — 2-3 paragraphs of how this specific failure played out. Use plan details. Make it feel like a case study.
2. THE UNDERLYING ASSUMPTION — The one thing taken for granted that made this failure possible. One sentence.
3. EARLY WARNING SIGNS — 1-2 concrete, observable signals that would indicate this failure mode is starting. Things you can actually see or measure.

Under 300 words. Direct. No hedging.
```

---

## Step 5: Synthesis

After all agents complete, produce the PREMORTEM REPORT:

1. **The Most Likely Failure** — Most probable given the plan details. Why?
2. **The Most Dangerous Failure** — Most damage if it happened, even if less likely.
3. **The Hidden Assumption** — The single biggest assumption the user is making that they probably haven't questioned.
4. **The Revised Plan** — Specific changes to make the plan more resilient. Not "consider your pricing" — say "test pricing at $X with 20 people before committing publicly."
5. **The Pre-Launch Checklist** — 3-5 specific things to verify, test, or put in place before executing. Each maps to a specific failure mode.

---

## Step 6: Deliverables

Generate two files:

**`premortem-report-[timestamp].html`** — Visual report, dark background, one card per failure reason, synthesis at the top. Open it after generating.

**`premortem-transcript-[timestamp].md`** — Full transcript including context gathered, raw failure reasons, all agent deep-dives, and full synthesis.

Also provide a 3-sentence chat summary: most likely failure, hidden assumption, single most important plan revision.

---

## Output Format Rules

- Chat summary: 3 sentences max
- Each failure reason in the report: failure story + assumption + early warning signs
- Revised plan: concrete actions, not vague suggestions
- Checklist: specific and verifiable, not principles

See README.md for extended methodology, examples, and the full HTML report design spec.
