# Local Agent System Blueprint (Beginner-Friendly)

This guide helps you turn a local model from "chatbot with personality" into an autonomous tool-using system.

## 1) Mental Model

Think of your system as 4 layers:

1. **Brain**: your local LLM (reasoning + language).
2. **Hands**: tools (search, files, shell, code execution).
3. **Manager**: orchestrator that plans, delegates, and verifies.
4. **Memory**: persistent state across sessions.

The "personality" should shape communication style, not replace reliability logic.

## 2) Core Capabilities to Implement

- **Planning**: break user goals into small ordered steps.
- **Acting**: call the right tools in the right order.
- **Checking**: verify outputs (tests, diffs, file existence, counts).
- **Repairing**: detect mistakes and self-correct.
- **Remembering**: keep preferences, constraints, and active objectives.

## 3) Personality vs Role

- **Personality** = tone and style (friendly, concise, formal).
- **Role** = responsibility (planner, coder, reviewer, memory).

Best practice:
- Keep one stable "orchestrator personality".
- Give each specialist role a narrow mandate.
- Never let personality override safety or verification requirements.

## 4) Suggested Runtime Loop

1. Parse user goal.
2. Load memory state.
3. Build short plan.
4. Delegate to specialist role(s) if needed.
5. Execute tool actions.
6. Verify results.
7. If failed: reflect, patch, retry.
8. Save updated memory and report completion.

## 5) Minimum Memory You Should Store

- User preferences (tone, detail level, risk tolerance)
- System constraints (offline-only, hardware limits)
- Current objective + milestone state
- Rejected approaches (and why)
- Next session "resume from here" note

## 6) Tool Stack You Want First

- File search + content search
- File read/write/edit
- Shell execution
- Test runner
- Validator scripts

Start small and reliable. Add tools only when you can verify outcomes.

## 7) Training + Inference Strategy

- Train on your curated dataset first (already prepared).
- Use deterministic-ish inference for tool work:
  - low temperature
  - explicit plan-first prompting
  - strict "verify before done" rule
- Keep a separate prompt mode for casual conversation if desired.

## 8) What Makes It More Than a Chatbot

Your AI becomes a real agent when it:
- takes multi-step action,
- uses tools instead of only words,
- checks its own work,
- remembers context over time,
- and can recover from errors without constant hand-holding.

## 9) Files Added For You

- `train_config_template.yaml`
- `multi_agent_roles_template.json`
- `autonomous_agent_dataset_manifest.json`
- `autonomous_agent_sampling_guide.md`
- `validate_autonomous_agent_jsonl.py`
- `create_autonomous_agent_splits.py`

## 10) Next Step (Practical)

If you want, I can next create:

- `memory_state_template.json` (ready-to-use state file)
- `system_prompt_orchestrator.txt`
- `system_prompt_reviewer.txt`
- `system_prompt_coder.txt`

That gives you a plug-and-play starter set for multi-agent orchestration locally.
