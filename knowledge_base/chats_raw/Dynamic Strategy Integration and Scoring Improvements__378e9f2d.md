# Dynamic Strategy Integration and Scoring Improvements

**Session ID:** `378e9f2d-cf04-45bf-8f5d-2a36af8d4ae7`  
**Created:** 2026-04-10 23:15:50 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\2832faeff98184b2f116b13fae9699e8\chatSessions\378e9f2d-cf04-45bf-8f5d-2a36af8d4ae7.jsonl`

---

## Turn 1 — 2026-04-10 23:16:38 UTC

**User:**

Copilot said: Here's a complete, copy-paste ready prompt for
Here's a complete, copy-paste ready prompt for your other Copilot instance. It has everything it needs to make the changes without asking you questions.

🤖 Prompt to paste into your VS Code Copilot
Code
I need you to make two connected improvements to `core/freedom_bot.py` and the scoring system.
The repo is a crypto trading bot built with Python + PyQt5.

---

## CHANGE 1 — Use all 14 strategies dynamically (not just the hardcoded 7)

In `core/freedom_bot.py`, at the top of the file there is a hardcoded list:

```python
_SCORING_STRATEGIES = [
    "Trend + Momentum Confluence",
    "Consensus Mode (3 of 4)",
    "MACD Momentum",
    "RSI Oversold/Overbought",
    "Parabolic SAR + ADX",
    "VWAP Bounce",
    "Divergence Detection",
]
Replace this with a dynamic list that pulls every strategy name from STRATEGY_MAP in core/strategies/__init__.py, but EXCLUDES "Consensus Mode (3 of 4)".

The reason for excluding Consensus is that it internally runs MA Crossover, RSI, MACD, and Confluence — if we include it alongside those individual strategies they get double-counted in the vote. Remove it from scoring but keep it available in the app everywhere else — do NOT remove it from STRATEGY_MAP or anywhere outside freedom_bot.py.

The resulting code should look like:

Python
from core.strategies import STRATEGY_MAP

# All strategies participate in Freedom Bot scoring except Consensus,
# which internally re-runs MA/RSI/MACD/Confluence and would double-count them.
_SCORING_STRATEGIES = [
    name for name in STRATEGY_MAP
    if name != "Consensus Mode (3 of 4)"
]
This means any new strategy added to STRATEGY_MAP in the future will automatically be included in Freedom Bot scoring without any further changes.

CHANGE 2 — Backtest-weighted scoring (strategies that perform better on a coin get a heavier vote)
The problem with the current scoring
Right now in score_symbol(), every strategy gets equal weight — a BUY from a strategy that has been 30% accurate on this coin counts the same as a BUY from one that has been 75% accurate. This needs to change.

The solution — use backtest win rate as the vote weight
Add a new method _get_strategy_weights(symbol, df) to the FreedomBot class. This method:

Loops over all strategies in _SCORING_STRATEGIES
Runs Backtester().run(df, strategy_name, symbol, timeframe) for each one using the OHLCV data already fetched (no extra API calls)
Uses the resulting win_rate (as a fraction 0.0–1.0, so divide by 100) as the weight for that strategy
Clamps each weight to a minimum of 0.1 so a poor strategy still has a tiny voice
Caches the result per symbol for 6 hours so it is not recalculated every scan cycle
Falls back to equal weights of 1.0 for all strategies if backtest fails or not enough data
The cache should be a dict stored as self._weight_cache on the FreedomBot instance:

Python
# Structure:
self._weight_cache: dict[str, dict] = {}
# {
#   "BTCUSDT": {
#       "weights": {"MACD Momentum": 0.72, "RSI Oversold/Overbought": 0.48, ...},
#       "cached_at": datetime object
#   }
# }
Cache expiry: 6 hours (use datetime.now() and compare with timedelta(hours=6)).

Import Backtester from core.backtester inside the method (lazy import to avoid circular imports at module level).

Modify score_symbol() to accept weights
Change the signature of score_symbol() from:

Python
def score_symbol(df: pd.DataFrame, symbol: str = "") -> dict:
to:

Python
def score_symbol(df: pd.DataFrame, symbol: str = "", weights: dict | None = None) -> dict:
When applying votes, multiply each strategy's signal strength by its weight:

Python
weight = float((weights or {}).get(strat_name, 1.0))
if sig.action == Signal.BUY:
    buy_votes += strength * weight
elif sig.action == Signal.SELL:
    sell_votes += strength * weight
Wire it into FreedomBot.run()
In the run() method, before scoring holdings and opportunities, add weight fetching. The weights should be fetched per-symbol using the same df that was already fetched for scoring:

For each holding symbol: fetch weights using _get_strategy_weights(symbol, df) before calling score_symbol(df, symbol)
For each opportunity symbol: same — fetch weights before score_symbol()
Pass the weights dict as the weights= argument to every score_symbol() call
Because backtest weight calculation can be slow on first run (14 strategies × N symbols), run the weight calculation for opportunity symbols in a background thread using concurrent.futures.ThreadPoolExecutor with max_workers=4. Cache results as they complete. Fall back to equal weights (empty dict → defaults to 1.0) if the future is not ready within 2 seconds.

Update the log output
When logging a score, include the weight context so the operator can see it. Change the holding log line from:

Code
[Freedom] ✅ OK Holding BTCUSDT: score=0.71 (4 bullish, 2 bearish signal(s))
to:

Code
[Freedom] ✅ OK Holding BTCUSDT: score=0.71 (4 bullish, 2 bearish | weighted across 13 strategies)
CHANGE 3 — Fix the rotation zip pairing bug
In FreedomBot.run(), Step 4, the rotation loop currently uses zip:

Python
for (weak_sym, weak_data), (opp_sym, opp_data) in zip(weak_holdings, strong_opps):
This has a bug: if a rotation is blocked (e.g. position cap reached), zip moves both iterators forward together, so the next weak holding gets paired with the next opportunity, silently skipping the blocked one. A valid rotation can be missed.

Fix this by replacing the zip loop with a proper nested search: For each weak holding, iterate through ALL strong opportunities (in score order) until one is found that passes all checks (can_open, improvement threshold, AI veto). If none is found for a given weak holding, log it and move on to the next weak holding.

Python
# Pseudocode for the fix:
for weak_sym, weak_data in weak_holdings:
    if not allow_new_entries:
        break
    if len(actions) >= max_actions:
        break
    for opp_sym, opp_data in strong_opps:          # search ALL strong opps
        if opp_sym already bought this cycle:
            continue
        can_open, note = _can_open_new_position(opp_sym, replacing_symbol=weak_sym)
        if not can_open:
            blocked_reasons.append(note)
            continue                                 # try next opp, not next weak
        improvement = opp_data["score"] - weak_data["score"]
        if improvement < rotation_improvement:
            continue
        # AI veto check here
        # Execute sell + buy here
        break                                        # move on to next weak holding
IMPORTANT — do not change anything else
Do NOT modify any GUI files
Do NOT modify any strategy files
Do NOT modify STRATEGY_MAP or consensus_strategy.py
Do NOT change any settings keys or default values
Do NOT change the public API of score_symbol() in a breaking way — the new weights parameter must be optional with a default of None so any existing callers that don't pass weights continue to work unchanged
After making the changes, please also add datetime to the imports at the top of core/freedom_bot.py (needed for the cache expiry check):

Python
from datetime import datetime, timedelta
And add concurrent.futures for the thread pool:

Python
import concurrent.futures       - after your done please commit and puh to the repo

**Copilot:**

*(no response captured)*

---

## Turn 2 — 2026-04-10 23:55:51 UTC

**User:**

I need you to make four small, focused improvements across the crypto trading bot.
Each change is in a different file. Do all four.

---

## CHANGE B — Expose FRESH_DEPLOY_FREE_PCT as a user setting

### File: `core/freedom_bot.py`

The class constant `FRESH_DEPLOY_FREE_PCT = 0.25` is currently hardcoded.
In `FreedomBot.run()`, Step 5, the free-cash deploy check reads:

```python
elif free_pct > self.FRESH_DEPLOY_FREE_PCT and strong_opps:
Change this line to read the value from self.settings first, falling back to the class constant if the key is not present:

Python
fresh_deploy_pct = float(
    self.settings.get("freedom_fresh_deploy_pct", self.FRESH_DEPLOY_FREE_PCT)
    or self.FRESH_DEPLOY_FREE_PCT
) / 100.0  # stored as a percentage (e.g. 25 means 25%), divide to get fraction
Wait — check the existing code first. FRESH_DEPLOY_FREE_PCT is already stored as a fraction (0.25), NOT a percentage. So store it in settings as a fraction too to keep it consistent with how the other freedom_ settings work. Use:

Python
fresh_deploy_pct = float(
    self.settings.get("freedom_fresh_deploy_pct", self.FRESH_DEPLOY_FREE_PCT)
    or self.FRESH_DEPLOY_FREE_PCT
)
Then replace the hardcoded self.FRESH_DEPLOY_FREE_PCT in the condition with fresh_deploy_pct.

File: gui/settings_dialog.py
Find the Freedom Bot settings section in the settings dialog. It will have fields like freedom_max_open_positions, freedom_max_actions_per_cycle, etc.

Add a new QDoubleSpinBox field for freedom_fresh_deploy_pct in that same section, immediately after the existing Freedom Bot fields. Label it: "Deploy free cash when idle % >". Set:

minimum: 0.05
maximum: 1.0
step: 0.05
decimals: 2
default value: 0.25
tooltip: "Freedom Bot will deploy idle USDT into new positions when this fraction of the portfolio is uninvested. E.g. 0.25 means deploy when more than 25% of portfolio is in USDT."
Wire it up the same way the other freedom_ spinbox fields are wired — read from settings on load, write back to settings on save.

CHANGE C — Tag Freedom Bot trades with source="freedom" for separate P&L tracking
File: core/paper_trader.py
Find the buy() and sell() methods. They currently accept parameters including strategy and reason. Add an optional source: str = "" parameter to both methods (after reason).

When a trade record dict is built and appended to the trade log / history inside each method, add the source field to the dict:

Python
"source": str(source or ""),
Do not change any other behaviour. The parameter must be optional with a default of "" so all existing callers that don't pass it continue to work unchanged.

File: core/freedom_bot.py
Find every call to self.paper_trader.buy(...) and self.paper_trader.sell(...) in freedom_bot.py. There are several — in the rotation loop, the risk-off exit block, and the fresh entry block.

Add source="freedom" as a keyword argument to every single one of these calls.

Do NOT add it to any calls outside of freedom_bot.py.

CHANGE D — Freedom Bot circuit breaker (cooldown after a bad cycle)
File: core/freedom_bot.py
Add a simple circuit breaker that pauses Freedom Bot for a cooldown period after a cycle where all executed trades were losses (or the bot took max actions and all resulted in sells only, suggesting churn).

Add two new instance variables in __init__:
Python
self._consecutive_loss_cycles: int = 0
self._circuit_breaker_until: Optional[datetime] = None
Add a new method _check_circuit_breaker():
Returns (tripped: bool, reason: str).

If self._circuit_breaker_until is set and datetime.now() is before it, return (True, f"Circuit breaker active until {self._circuit_breaker_until.strftime('%H:%M:%S')}")
Otherwise return (False, "")
Add a new method _update_circuit_breaker(actions: list[dict]):
Called at the END of run(), after all trades are done, before returning actions.

Count how many of the executed actions were SELL-only cycles: if len(actions) > 0 and ALL actions are type "SELL" with no BUYs, increment self._consecutive_loss_cycles
If self._consecutive_loss_cycles >= 3, set:
Python
cooldown_minutes = int(self.settings.get("freedom_circuit_breaker_cooldown_min", 30))
self._circuit_breaker_until = datetime.now() + timedelta(minutes=cooldown_minutes)
self._consecutive_loss_cycles = 0
self._log(f"[Freedom] ��� Circuit breaker tripped — pausing for {cooldown_minutes}min after 3 consecutive sell-only cycles.")
If len(actions) > 0 and there is at least one BUY, reset: self._consecutive_loss_cycles = 0
Wire it into run():
At the very START of run(), after the opening log line, call:

Python
tripped, trip_reason = self._check_circuit_breaker()
if tripped:
    self._log(f"[Freedom] 🔴 Circuit breaker active — {trip_reason}. Skipping cycle.")
    return []
At the very END of run(), just before return actions, call:

Python
self._update_circuit_breaker(actions)
File: gui/settings_dialog.py
In the same Freedom Bot settings section, add a new QSpinBox for freedom_circuit_breaker_cooldown_min. Label it "Circuit breaker cooldown (min)". Set:

minimum: 5
maximum: 240
step: 5
default: 30
tooltip: "How long (in minutes) Freedom Bot pauses after 3 consecutive sell-only cycles. Set to 0 to disable."
Wire it up the same way as the other Freedom Bot spinbox fields.

CHANGE E — Fix incomplete __all__ in core/strategies/__init__.py
File: core/strategies/__init__.py
The __all__ list at the bottom of the file is missing the 8 strategies added recently. It currently only has:

Python
__all__ = [
    "BaseStrategy",
    "Signal",
    "MACrossoverStrategy",
    "RSIStrategy",
    "StochRSIStrategy",
    "MACDStrategy",
    "BollingerStrategy",
    "ATRSqueezeStrategy",
    "ConsensusStrategy",
    "ConfluenceStrategy",
    "STRATEGY_MAP",
    "get_strategy",
]
Update it to include ALL exported symbols — every strategy class that is imported at the top of the file, plus the existing entries. The missing ones are:

Python
"VWAPBounceStrategy",
"SupportResistanceStrategy",
"FibonacciRetracementStrategy",
"DivergenceStrategy",
"IchimokuCloudStrategy",
"SARWithADXStrategy",
The final __all__ should contain all 14 strategy classes plus BaseStrategy, Signal, STRATEGY_MAP, and get_strategy.

IMPORTANT constraints
Only modify these files:
core/freedom_bot.py
core/paper_trader.py
core/strategies/__init__.py
gui/settings_dialog.py
Do NOT touch any other files
All new parameters must be optional with safe defaults so existing callers are unaffected
datetime is already imported in core/freedom_bot.py from the previous commit — do not add it again, just use it
Optional is already imported in core/freedom_bot.py — do not add it again  -- commit and push when finished please

**Copilot:**

*(no response captured)*

---

## Turn 3 — 2026-04-11 00:11:21 UTC

**User:**

I need the next four focused improvements across the crypto trading bot.
Read each change carefully — they are in different files and independent of each other.

---

## CHANGE F — Portfolio Coach: add RSI + bot-watching to the "cut-risk" notices

### File: `core/portfolio_coach.py`

The coach already has `_get_symbol_rsi()` and already uses `rsi_value` in most
notice types. However the two loss notices (`cut-risk-hard` at pnl <= -6% and
`cut-risk` at pnl <= -4%) currently only use `rsi_suffix` and `watch_suffix`.

Make two targeted improvements to these two notice types:

**Improvement 1 — RSI-boosted priority on cut-risk-hard:**
In the `pnl_pct <= -6.0` block, if `rsi_value` is not None AND `rsi_value > 50`,
raise the priority from 93 to 97 AND change the `action_label` from
`"Cut / reduce now"` to `"Cut now — momentum still against you"`.
The reasoning: if RSI is above 50 on a losing position, it means this is not
an oversold bounce candidate — momentum is still flowing away from you.

**Improvement 2 — RSI recovery hint on cut-risk:**
In the `pnl_pct <= -4.0` block, if `rsi_value` is not None AND `rsi_value < 35`,
add an extra sentence to the message:
`" RSI is approaching oversold territory — wait one more candle to see if a
bounce develops before cutting, but keep your stop ready."`
This gives the user a nuanced "maybe wait" hint for positions that are down
but showing early signs of a reversal.

Do NOT change anything else in portfolio_coach.py — no new methods, no new imports,
no changes to `_get_symbol_rsi()` or `_build_tax_snapshot()`.

---

## CHANGE G — Signal Feed persists across restarts (seed from trade log on startup)

### File: `gui/signal_feed_panel.py`

Currently `_seed_from_history()` only pulls from:
1. `trading_panel.get_recent_activity(limit=80)` — in-memory only, lost on restart
2. `alert_manager.get_history(limit=80)` — persisted, survives restart ✅

The result: after a restart, the Feed tab shows only alerts, not past trades or
bot activity, because `_activity_history` in `trading_panel` is in-memory.

**The fix:** add a third seed source — the paper trader's trade history.

Add an optional `paper_trader` parameter to `SignalFeedPanel.__init__`:
```python
def __init__(
    self,
    alert_manager=None,
    trading_panel=None,
    paper_trader=None,    # NEW — optional
    parent=None,
):
Store it as self.paper_trader = paper_trader.

In _seed_from_history(), after the existing two seed sources, add a third block:

Python
if self.paper_trader is not None:
    try:
        history = list(self.paper_trader.trade_history)[-80:]
        for trade in reversed(history):
            action = str(getattr(trade, "side", "") or "").upper()
            symbol = str(getattr(trade, "symbol", "") or "").upper()
            source = str(getattr(trade, "source", "") or "")
            price = getattr(trade, "price", 0.0)
            qty = getattr(trade, "qty", 0.0)
            strategy = str(getattr(trade, "strategy", "") or "")
            reason = str(getattr(trade, "reason", "") or "")
            ts = getattr(trade, "timestamp", None)
            timestamp = ts.strftime("%Y-%m-%d %H:%M:%S") if ts else ""
            source_tag = f" [{source}]" if source else ""
            self.add_event(
                {
                    "timestamp": timestamp,
                    "kind": "trade",
                    "category": "trade",
                    "symbol": symbol,
                    "action": action,
                    "title": f"{action} {symbol}{source_tag} via {strategy}",
                    "message": (
                        f"{action} {qty:.6f} {symbol} @ ${price:.4f}"
                        + (f" — {reason}" if reason else "")
                    ),
                    "source": source or "bot",
                },
                refresh=False,
            )
    except Exception:
        pass
This means after a restart, the feed will be pre-populated with the last 80 trades from the paper trader's persisted history, including Freedom Bot trades tagged with [freedom].

The paper_trader parameter must be optional (default None) so any existing callers that don't pass it still work unchanged.

CHANGE H — Strategy Advisor: add MACD as an option for sideways + momentum
File: utils/strategy_advisor.py
In recommend_strategy_for_context(), the sideways + momentum path currently recommends only ATR Squeeze Breakout. This misses MACD, which is also excellent at catching the breakout out of a sideways range when momentum is already beginning to expand.

Change the sideways + objective in {"breakout", "momentum"} block so that:

Keep ATR Squeeze Breakout as the primary recommendation (no change there)
Update the summary to mention MACD as a complementary option: Change the current summary from: "In sideways markets, ATR Squeeze Breakout is ideal for catching the first clean release after volatility compresses." To: "In sideways markets, ATR Squeeze Breakout fires when volatility first expands after compression. MACD Momentum is a strong alternative if momentum is already building — it catches the breakout earlier but with slightly more noise."
Update why_now to: "ATR Squeeze is best when the range is tight and unbroken. If you see the MACD histogram already turning positive, switch to MACD Momentum for an earlier entry on the same move."
That's the only change to strategy_advisor.py — one block, three string updates. Do NOT add new strategies, new conditions, or new parameters.

File: gui/help_panel.py
In the _strategy_html() method, find the table at the bottom:

HTML
<tr><td>Catching early momentum</td><td>MACD Momentum · Stochastic RSI</td></tr>
Add a new row immediately before it for the sideways breakout case that now has two options:

HTML
<tr><td>Sideways → breakout starting</td><td>ATR Squeeze Breakout · MACD Momentum</td></tr>
That's the only change to help_panel.py.

CHANGE I — Freedom Bot P&L filter in the trade journal
File: gui/trading_panel.py
Find the trade journal / history section of the trading panel. This is where past trades are displayed in a table (look for where trade_history from the paper trader is iterated and displayed in a QTableWidget or similar).

Add a filter combo box above the trade journal table that lets the user filter by trade source. The combo should have these options:

Code
All trades          (value: "all")
Regular bot only    (value: "bot")
Freedom Bot only    (value: "freedom")
When "Freedom Bot only" is selected, only show trades where trade.source == "freedom" (or trade_dict.get("source") == "freedom"). When "Regular bot only" is selected, show trades where source is "" or "bot" or anything that is NOT "freedom". When "All trades" is selected, show everything (current behaviour).

The filter combo should:

Be placed directly above the trade journal table, right-aligned
Be labelled with a small QLabel: "Show:"
Connect its currentIndexChanged signal to re-render the journal table
Default to "All trades"
Use the same pattern as the rest of the trading panel for building and connecting combo boxes. Do NOT restructure the journal rendering — just wrap the existing row-building loop in an if check that skips rows not matching the filter.

The source field is already on every Trade object (added in a recent commit) and is available in trade.source or via trade.to_dict()["source"].

IMPORTANT constraints
Only modify these files:
core/portfolio_coach.py
gui/signal_feed_panel.py
utils/strategy_advisor.py
gui/help_panel.py
gui/trading_panel.py
Do NOT change any other files
All changes to method signatures must use optional parameters with safe defaults
Do NOT change the layout or structure of any other section of trading_panel.py besides adding the filter combo above the journal table
The paper_trader parameter in SignalFeedPanel must remain optional (default None)
Do NOT add new imports unless strictly required by the new code
,,, and push when finished again thx

**Copilot:**

*(no response captured)*

---
