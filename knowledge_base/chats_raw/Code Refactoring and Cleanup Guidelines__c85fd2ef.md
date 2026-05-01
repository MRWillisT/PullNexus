# Code Refactoring and Cleanup Guidelines

**Session ID:** `c85fd2ef-c74a-4759-883e-32878386060d`  
**Created:** 2026-04-18 04:37:58 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\2832faeff98184b2f116b13fae9699e8\chatSessions\c85fd2ef-c74a-4759-883e-32878386060d.jsonl`

---

## Turn 1 — 2026-04-18 04:38:39 UTC

**User:**

Pick any file from the to do list - Refactor and clean up this code for better readability, maintainability, and performance. Follow these rules strictly:Use clear, descriptive variable and function names
Break down long functions into smaller, single-responsibility ones where it makes sense
Remove duplication and dead/unused code
Improve structure and formatting without changing the core logic or behavior
Add helpful comments only where the code isn't self-explanatory
Ensure consistent style with the rest of the project
Keep it simple and idiomatic for Python Do not add unnecessary try/catch blocks unless there's real error recovery needed
Keep error handling minimal and appropriate
Prefer straightforward logic over clever abstractions
Remove any defensive programming that isn't required here
Maintain exact same functionality. Run regression tests after

[X] utils/helpers.py         — lowest risk, pure functions
[X] utils/alerts.py
[X ] utils/trade_logger.py
[X] utils/market_regime.py
[X] utils/strategy_learner.py
[X] utils/strategy_advisor.py
[X] core/strategies/*.py     — each strategy file individually
[X] core/backtester.py
[X] core/paper_trader.py
[X] core/exchange_client.py
[X] core/surfer_bot.py
[ ] core/freedom_bot.py      — high complexity, careful   <--- looks like you get the last one - feel free to plan it out if needed 
[X] core/freedom_replay.py
[X] core/surfer_replay.py
[X] gui/settings_dialog.py   — large, mostly isolated UI
[ ] gui/*.py                 — rest of GUI last

**Copilot:**

*(no response captured)*

---
