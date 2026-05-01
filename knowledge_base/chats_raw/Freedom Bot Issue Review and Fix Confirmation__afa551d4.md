# Freedom Bot Issue Review and Fix Confirmation

**Session ID:** `afa551d4-5255-44ca-b135-2709ca910335`  
**Created:** 2026-04-14 22:28:41 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\2832faeff98184b2f116b13fae9699e8\chatSessions\afa551d4-5255-44ca-b135-2709ca910335.jsonl`

---

## Turn 1 — 2026-04-14 22:29:57 UTC

**User:**

can you fix all these issues if you think they need it? - I wouldnt blindly fix them - please confirm its actually needed before fixing - 1) Position sizing logic (Freedom Bot)
What it actually uses

Fresh-entry base size is portfolio-based: total_value * (effective_risk_pct/100) * conviction (core/freedom_bot.py:2170-2172, 2220).
Rotation buy base size is usually sell proceeds (freed_usdt) not risk sizing (core/freedom_bot.py:1985, 2011).
Final size is always clamped by:
symbol cap (core/freedom_bot.py:2004, 2214)
paper_trader.usdt_balance (core/freedom_bot.py:2012, 2221)
Mismatch / bugs

UI label shows portfolio-based estimate only, not cash/cap/regime constraints (gui/trading_panel.py:1091-1098).
Label uses self.settings["risk_pct"], not the live spin value directly, so it can lag UI edits (gui/trading_panel.py:1092, 1303).
In rotation, freed_usdt uses trade.cost (gross notional), while sell credits net proceeds after fee, so buy sizing is overstated by fee amount (core/freedom_bot.py:1985; core/paper_trader.py:233-241).
2) Cash balance tracking after sells (sell → cash → buy)
Flow correctness

Sell credits USDT back correctly: self.usdt_balance += proceeds (core/paper_trader.py:234, 240).
Freedom rotation buy then uses updated usdt_balance clamp (core/freedom_bot.py:1974-1985, 2012).
Issue

Gross-vs-net mismatch in rotation sizing (above) can cause small oversizing intent and buy rejection/underfill behavior.
3) Rotation logic settle timing
Behavior

Sell then buy is synchronous in one cycle; no async settlement wait needed in paper logic (core/freedom_bot.py:1974-1993, 1999-2023).
Issues

If action cap is reached after sell, buy is skipped, leaving one-sided liquidation (core/freedom_bot.py:1994-1996).
Buy sizing may exceed actual sale proceeds due gross-vs-net bug (1985 vs paper_trader.py:234-241).
4) Symbol allocation cap (freedom_max_symbol_allocation_pct)
Implemented

Capacity computed vs portfolio value (not cash) (core/freedom_bot.py:918-927).
Applied before rotation/fresh buys (core/freedom_bot.py:2004-2013, 2214-2225).
Issues

DCA buys bypass symbol-cap checks entirely (core/freedom_bot.py:1431-1450, 1501-1512).
Fresh-entry loop uses total_value captured once before loop; cap math can be stale after earlier buys in same cycle (core/freedom_bot.py:2170, 2214).
5) Max positions check
Implemented

Uses paper_trader.positions only (core/freedom_bot.py:936-944).
Issue

In live mode, this does not inherently include actual exchange holdings unless imported into paper ledger, so limit can be miscounted (core/freedom_bot.py:400-407, 929-944; core/paper_trader.py:439-481).
6) Scoring system (13 strategies)
How combined

STRATEGY_MAP has 14 entries incl Consensus (core/strategies/__init__.py:18-33).
Freedom excludes Consensus => 13 strategy scorers (core/freedom_bot.py:34-39).
Plus extra “Momentum State” vote weighted 1.5x (core/freedom_bot.py:134-145).
Final score = buy_votes / (buy_votes + sell_votes) (core/freedom_bot.py:166-168).
Issues / oddities

HOLD contributes to both sides, pulling score toward 0.5 (core/freedom_bot.py:159-162).
Strategy exceptions are silently dropped, changing normalization denominator unpredictably (core/freedom_bot.py:163-164, 166).
signal_count ignores HOLD and momentum, but is used as reliability gate for exits (core/freedom_bot.py:184, 653-671).
7) Watchdog logic (run_intracycle_watchdog)
Behavior

Only updates ticker cache and runs hard-stop % exits (core/freedom_bot.py:1143-1152).
Uses same hard-stop threshold as main cycle (core/freedom_bot.py:1071-1074).
Issues

It does not run ATR exits (main cycle does), so intracycle risk behavior differs (core/freedom_bot.py:1809-1811 vs 1122-1152).
If ticker fetch fails for a symbol, stale cached price can be used for stop check (core/freedom_bot.py:1143-1149, 1079-1088).
8) Recently-sold cooldown
Implemented

Default 120 min penalty: subtract 0.10 from score, not a hard block (core/freedom_bot.py:1752-1760).
Sold entries are tracked and pruned after 24h (core/freedom_bot.py:2271-2288).
Impact

Can suppress valid rebound re-entry if score falls below threshold due penalty.
9) DCA interaction/conflict with paper_trader.py
Major bug

Freedom stores pending DCA as tuples (target, usdt) (core/freedom_bot.py:1447-1450).
Main BotWorker stores pending DCA as dicts with keys target_price/usdt_amount/tranche (gui/trading_panel.py:725-735) and reads as dicts (547-553).
Freedom reads pending as tuple unpack (core/freedom_bot.py:1488).
This is a shared structure in PaperTrader._dca_pending, so switching between bot modes can break DCA processing (type mismatch).

10) Circuit breaker
Implemented

Trips after 3 “losing” action-cycles (portfolio drop >0.1% or stop-loss sell) (core/freedom_bot.py:323-343).
Cooldown duration from setting; checked at cycle start (core/freedom_bot.py:276-286, 1577-1580).
Issues

Counter does not reset/progress on no-action cycles (core/freedom_bot.py:326-327), so “consecutive” semantics are imperfect.
Settings tooltip says “sell-only cycles,” but logic is different (gui/settings_dialog.py:582-584 vs core/freedom_bot.py:323-340).
11) Cash deployment logic (“spare cash into top-ranked”)
Trigger

Deploy when free_pct > freedom_fresh_deploy_pct (default 0.25) or stranded-cash condition exists (core/freedom_bot.py:2174-2185).
Issues

No explicit minimum cash buffer/floor.
free_pct is computed once before buy loop and not recomputed each iteration (core/freedom_bot.py:2172, 2187-2241), so it can keep buying after falling below threshold.
Uses full usdt_balance clamp but doesn’t pre-reserve fees; near-all-in attempts can reject in PaperTrader.buy (core/freedom_bot.py:2221; core/paper_trader.py:179-181).
12) _update_freedom_trade_size_label bug confirmation + discrepancy
Confirmed

Label uses get_portfolio_value() and a fixed 0.7x–1.5x risk range (gui/trading_panel.py:1091-1098).
Actual fresh size is min(portfolio*risk*regime*conviction, symbol_capacity, usdt_balance) (core/freedom_bot.py:2220-2222).
Actual rotation size often starts from sold notional (freed_usdt) (core/freedom_bot.py:2011).
Quantified discrepancy

Displayed range: P * r * [0.7, 1.5].
Actual fresh range before clamps: P * r * regime_mult * [0.7,1.5], where regime is {0.5,0.7,1.0,1.2} (core/freedom_bot.py:1568-1570).
Then clamped by cash and symbol cap, so actual can be far lower (or differ materially in supportive/risk-off regimes).
13) Other logic oddities / edge cases
Live-balance sync bug when cash is zero: sync only applies if usdt > 0; zero cash leaves stale prior balance (core/freedom_bot.py:404-407).
Live order divergence risk: paper ledger is updated before exchange order; if live order fails, paper/live can desync (core/freedom_bot.py:421-435, 447-463).
Docs mismatch: file header says “7 sub-strategies,” code uses 13 + momentum (core/freedom_bot.py:5, 34-39, 134-145).
Config inconsistency: many Freedom defaults are hardcoded in bot/settings dialog rather than centralized in config/settings.py constants (e.g., fresh deploy, circuit breaker, cooldown) (core/freedom_bot.py:217, 279, 1752; gui/settings_dialog.py:565-585).

**Copilot:**

Let me read the relevant files to properly assess each issue before touching anything.

---

## Turn 2 — 2026-04-14 22:37:11 UTC

**User:**

commit and push please

**Copilot:**

*(no response captured)*

---
