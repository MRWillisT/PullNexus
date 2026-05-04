# code-only-mode

Agent behavior prompt that suppresses all prose, explanations, and filler. **Code output only.** Minimizes token usage and keeps responses clean for piping or programmatic use.

## Usage

Use as a system prompt or agent mode in any local LLM setup, VS Code Copilot agent mode, Continue.dev, or Cursor.

In VS Code, save as a `.agent.md` file in `.github/` or your prompts folder and select it from the agent mode picker.

## What it does

- Zero prose before or after code
- No inline comments unless they are required for the code to make sense (e.g. non-obvious regex, magic numbers)
- No filler phrases ("Here is...", "This should...", "I've updated...")
- Confirms completed edits with one word or one filename only
- Outputs code blocks with filename labels when multiple files change

## When to use it

- Token-constrained sessions with small or quantized models
- Batch edits where you want clean diffs, not explanations
- Situations where you're reading the code yourself and don't need narration
- Stacked with `lean-agent` for maximum focus and minimum output

## Pairs well with

- `lean-agent` — adds narrow-scope discipline on top of zero-prose output
- `uncertainty-behavior-policy` — ensures the model states blockers rather than fabricating code

## Install

```bash
pullnexus install code-only-mode
```

Copy `agent.md` into your agent configuration or `.github/` prompts folder.

*License: MIT | Author: MRWillisT*
