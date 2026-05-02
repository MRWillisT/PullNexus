# agent-role-reviewer

System prompt for a **Reviewer** specialist agent. Critically evaluates proposed or completed changes with severity-ordered findings and a structured final verdict. Anti-hallucination by design — requires evidence for every claim.

## Usage

Paste `system_prompt.txt` as the system prompt when you want a dedicated review/QA pass.

Works well paired with:
- `agent-role-orchestrator` — delegates review tasks to this role
- `agent-role-coder` — hands off completed work for review

## What it does

- Prioritizes findings by severity (data loss > security > regressions > reliability > perf > clarity)
- Requires evidence summary for each finding — no vague "this looks wrong"
- Outputs a clear verdict: **approve / approve with conditions / block**
- Will not approve if critical risk remains

## Install

```bash
pullnexus install agent-role-reviewer
```

*License: MIT | Author: PullNexus Contributors*
