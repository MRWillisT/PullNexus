# Trading Bot Logic and Sizing Issues

**Session ID:** `2c96b193-605c-4920-b279-ea282c5def18`  
**Created:** 2026-04-14 22:41:00 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\2832faeff98184b2f116b13fae9699e8\chatSessions\2c96b193-605c-4920-b279-ea282c5def18.jsonl`

---

## Turn 1 — 2026-04-14 22:41:26 UTC

**User:**

Fix These — They Affect Real Trading Outcomes
1. Rotation buy sizing uses freed_usdt (gross) not net proceeds
Line 2029 / 2007 — freed_usdt is set from trade.cost which is qty × fill_price before fees. But paper_trader.sell() only adds back proceeds = notional - fee to usdt_balance. So freed_usdt is slightly inflated. The buy is then clamped by usdt_balance which is correct — but this means the buy amount is calculated wrong and then clamped, instead of just being calculated right to begin with.

Python
freed_usdt = float(trade.cost or 0.0) or (qty * sell_price)  # ← gross, not net
Fix: Use freed_usdt = proceeds - fee or just read self.paper_trader.usdt_balance after the sell.

2. Fresh entry (Step 5) sizes against total_value but rotation sizes against freed_usdt
Line 2029 vs 2238 — Rotation buys are sized by what the sell freed. Fresh entry buys are sized by total_value × risk_pct%. These are two different formulas. If a rotation sell is $90 but total_value × 4% would be $135, you get inconsistent position sizes depending on how the bot entered. You want uniform sizing — one formula, applied everywhere.

3. available_cash check happens AFTER fetch_df in Step 5
Lines 2227–2239 — The bot fetches a fresh klines call for the opportunity symbol before checking if there's actually enough cash to buy. With 6 positions and frequent trades, this wastes API calls and adds latency when cash is near zero. Check cash first, fetch klines second.

4. Circuit breaker trips on any stop-loss sell, even tiny ones
Lines 337–342 — A single stop-loss sell on a $50 orphan position counts as a "losing cycle." Three of those in a row (could be small losses during a sideways market) trips the breaker and pauses the bot for 30 minutes. This is way too sensitive. It should only count meaningful portfolio losses.

Python
had_stop_loss_sell = any("stop" in a.get("reason", "").lower() ...)
Fix: Only count stop-loss sells where the position was >X% of portfolio, or require both had_portfolio_loss AND had_stop_loss_sell.

5. Stranded cash logic fires even when Step 4 already freed a slot
Lines 2098–2183 — The stranded cash check at _sc_free_pct > STRANDED_CASH_PCT (35%) runs before Step 5 cash deployment. But it only checks already_sold from current cycle actions, not whether Step 5 is about to deploy that cash. This can cause the bot to sell a holding unnecessarily to "free a slot" when Step 5 would have deployed the cash anyway.

6. DCA tranche numbering is backwards
Line 1516 — tranche_num = len(pending) counts remaining tranches, so if 2 are left it logs "tranche 2" — but tranche 2 was already done. The actual tranche number should be total_tranches - len(pending) + 1.

7. _get_tradeable_symbols() is called every cycle — it's a full HTTP call with no cache
Lines 769–814 — Every run() call hits api.binance.us/api/v3/exchangeInfo which returns a large JSON payload. This is slow and hammers the API. It should be cached for at least 1 hour.

8. ATR partial take-profit check falls through when sell is rejected
Lines 1266–1267 — After a partial sell is rejected, the comment says "fall through to check trailing stop / full TP" — but the continue on line 1266 only runs when the sell succeeds. When it's rejected, you fall through to Rule 3 (breakeven stop) which hasn't been armed yet, so it just skips, then Rule 4 (full TP), which could sell the full position instead of the intended 50%. This is the intended behavior (probably) but it's fragile. A partial sell rejection should probably log a warning.

**Copilot:**

*(no response captured)*

---

## Turn 2 — 2026-04-14 22:41:36 UTC

**User:**

Fix These — They Affect Real Trading Outcomes
1. Rotation buy sizing uses freed_usdt (gross) not net proceeds
Line 2029 / 2007 — freed_usdt is set from trade.cost which is qty × fill_price before fees. But paper_trader.sell() only adds back proceeds = notional - fee to usdt_balance. So freed_usdt is slightly inflated. The buy is then clamped by usdt_balance which is correct — but this means the buy amount is calculated wrong and then clamped, instead of just being calculated right to begin with.

Python
freed_usdt = float(trade.cost or 0.0) or (qty * sell_price)  # ← gross, not net
Fix: Use freed_usdt = proceeds - fee or just read self.paper_trader.usdt_balance after the sell.

2. Fresh entry (Step 5) sizes against total_value but rotation sizes against freed_usdt
Line 2029 vs 2238 — Rotation buys are sized by what the sell freed. Fresh entry buys are sized by total_value × risk_pct%. These are two different formulas. If a rotation sell is $90 but total_value × 4% would be $135, you get inconsistent position sizes depending on how the bot entered. You want uniform sizing — one formula, applied everywhere.

3. available_cash check happens AFTER fetch_df in Step 5
Lines 2227–2239 — The bot fetches a fresh klines call for the opportunity symbol before checking if there's actually enough cash to buy. With 6 positions and frequent trades, this wastes API calls and adds latency when cash is near zero. Check cash first, fetch klines second.

4. Circuit breaker trips on any stop-loss sell, even tiny ones
Lines 337–342 — A single stop-loss sell on a $50 orphan position counts as a "losing cycle." Three of those in a row (could be small losses during a sideways market) trips the breaker and pauses the bot for 30 minutes. This is way too sensitive. It should only count meaningful portfolio losses.

Python
had_stop_loss_sell = any("stop" in a.get("reason", "").lower() ...)
Fix: Only count stop-loss sells where the position was >X% of portfolio, or require both had_portfolio_loss AND had_stop_loss_sell.

5. Stranded cash logic fires even when Step 4 already freed a slot
Lines 2098–2183 — The stranded cash check at _sc_free_pct > STRANDED_CASH_PCT (35%) runs before Step 5 cash deployment. But it only checks already_sold from current cycle actions, not whether Step 5 is about to deploy that cash. This can cause the bot to sell a holding unnecessarily to "free a slot" when Step 5 would have deployed the cash anyway.

6. DCA tranche numbering is backwards
Line 1516 — tranche_num = len(pending) counts remaining tranches, so if 2 are left it logs "tranche 2" — but tranche 2 was already done. The actual tranche number should be total_tranches - len(pending) + 1.

7. _get_tradeable_symbols() is called every cycle — it's a full HTTP call with no cache
Lines 769–814 — Every run() call hits api.binance.us/api/v3/exchangeInfo which returns a large JSON payload. This is slow and hammers the API. It should be cached for at least 1 hour.

8. ATR partial take-profit check falls through when sell is rejected
Lines 1266–1267 — After a partial sell is rejected, the comment says "fall through to check trailing stop / full TP" — but the continue on line 1266 only runs when the sell succeeds. When it's rejected, you fall through to Rule 3 (breakeven stop) which hasn't been armed yet, so it just skips, then Rule 4 (full TP), which could sell the full position instead of the intended 50%. This is the intended behavior (probably) but it's fragile. A partial sell rejection should probably log a warning.

**Copilot:**

*(no response captured)*

---
