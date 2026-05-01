# Adding Stranded Cash Slot-Freeing Rule

**Session ID:** `4d78e9ec-23e6-47e0-8583-eeef0780ed24`  
**Created:** 2026-04-12 19:33:53 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\2832faeff98184b2f116b13fae9699e8\chatSessions\4d78e9ec-23e6-47e0-8583-eeef0780ed24.jsonl`

---

## Turn 1 — 2026-04-12 20:04:41 UTC

**User:**

Add a hard percentage-based stop-loss to Freedom Bot. Two files only:
`core/freedom_bot.py` and `gui/settings_dialog.py`. Read everything
before writing any code.

---

## THE CHANGE IN PLAIN ENGLISH

Right now Freedom Bot's only price-based exit is the ATR stop loss in
`_check_freedom_risk_exits()`. ATR stops are dynamic and can be far from
entry on volatile coins. We need a simpler, faster safety net:

If any open position is DOWN more than X% from its average entry price,
sell the entire position immediately — no questions asked, regardless of
score, regime, or action cap. This fires BEFORE the ATR exits and BEFORE
the rotation logic.

Default threshold: 8%. Configurable in settings. Set to 0 to disable.

---

## CHANGES TO `core/freedom_bot.py`

### 1 — Add class constant (alongside the other thresholds, line ~128)

Add after `CASH_EXIT_THRESHOLD = 0.28`:
```python
HARD_STOP_LOSS_PCT = 8.0   # sell any position down more than this % from entry; 0 = disabled
2 — Add _check_hard_stop_losses() method
Add this new method directly above _check_freedom_risk_exits():

Python
def _check_hard_stop_losses(self) -> list[dict]:
    """
    Scan every open position for a hard percentage stop-loss.

    If a position is down more than `freedom_hard_stop_loss_pct` percent
    from its average entry price, sell the entire position immediately.

    This check runs BEFORE ATR exits and BEFORE rotation logic so that
    no other rule can delay or block a hard stop exit.

    Returns a list of action dicts ready to append to the cycle actions.
    Returns an empty list if the hard stop is disabled (threshold <= 0).
    """
    stop_pct = float(
        self.settings.get("freedom_hard_stop_loss_pct", self.HARD_STOP_LOSS_PCT)
        or 0.0
    )
    if stop_pct <= 0:
        return []

    actions: list[dict] = []
    positions = self.paper_trader.get_open_positions_display() or []

    for pos in positions:
        symbol = str(pos.get("symbol", "") or "").upper()
        if not symbol:
            continue

        avg_price = float(pos.get("avg_price", 0.0) or 0.0)
        current_price = float(pos.get("current_price", 0.0) or 0.0)
        qty = float(pos.get("qty", 0.0) or 0.0)

        if avg_price <= 0 or current_price <= 0 or qty <= 0:
            continue

        pnl_pct = (current_price - avg_price) / avg_price * 100.0

        if pnl_pct <= -stop_pct:
            trade = self.paper_trader.sell(
                symbol=symbol,
                qty=qty,
                price=current_price,
                strategy="Freedom Bot",
                reason=(
                    f"Hard stop loss {pnl_pct:.1f}% | "
                    f"entry ${avg_price:.4f} | current ${current_price:.4f} | "
                    f"threshold -{stop_pct:.1f}%"
                ),
                source="freedom",
            )
            if trade:
                self._log(
                    f"[Freedom] 🚨 HARD STOP LOSS hit {symbol} — "
                    f"down {pnl_pct:.1f}% from entry ${avg_price:.4f} "
                    f"(threshold -{stop_pct:.1f}%) — full position sold @ ${current_price:.4f}"
                )
                actions.append({
                    "type": "SELL",
                    "symbol": symbol,
                    "reason": f"Hard stop loss {pnl_pct:.1f}%",
                })

    return actions
3 — Call _check_hard_stop_losses() inside run()
In the run() method, find this existing block (around line 783):

Python
        # ── ATR risk exits — run before any rotation logic ─────────────
        risk_exit_acts = self._check_freedom_risk_exits(holding_scores, interval)
        if risk_exit_acts:
            actions.extend(risk_exit_acts)
            # Drop exited symbols so they don't re-appear as rotation candidates
            exited_syms = {a["symbol"] for a in risk_exit_acts}
            for sym in exited_syms:
                holding_scores.pop(sym, None)
INSERT the following block IMMEDIATELY BEFORE that existing block:

Python
        # ── Hard stop-loss — runs before everything else ────────────────
        hard_stop_acts = self._check_hard_stop_losses()
        if hard_stop_acts:
            actions.extend(hard_stop_acts)
            hard_stop_syms = {a["symbol"] for a in hard_stop_acts}
            for sym in hard_stop_syms:
                holding_scores.pop(sym, None)
The hard stop block must come FIRST — before ATR exits, before rotation, before everything. Positions removed here must be gone from holding_scores before any other logic sees them.

CHANGES TO gui/settings_dialog.py
1 — Add the spinbox in _build_ui()
In the Freedom Bot QGroupBox section (the freedom_group / freedom_layout block, around line 520), add the following AFTER the circuit breaker row and BEFORE the buy threshold row:

Python
        self.freedom_hard_stop_spin = QDoubleSpinBox()
        self.freedom_hard_stop_spin.setRange(0.0, 50.0)
        self.freedom_hard_stop_spin.setSingleStep(0.5)
        self.freedom_hard_stop_spin.setDecimals(1)
        self.freedom_hard_stop_spin.setSuffix(" %")
        self.freedom_hard_stop_spin.setValue(8.0)
        self.freedom_hard_stop_spin.setToolTip(
            "Sell any Freedom Bot position immediately if it falls this % below "
            "the average entry price. Fires before all other exit logic. "
            "Set to 0.0 to disable."
        )
        freedom_layout.addRow("Hard stop-loss:", self.freedom_hard_stop_spin)
2 — Load the value in _load_values()
In _load_values(), after the line that loads freedom_winner_extra_spin, add:

Python
        self.freedom_hard_stop_spin.setValue(
            float(settings.get("freedom_hard_stop_loss_pct", 8.0) or 8.0)
        )
3 — Save the value in _save_and_accept()
In the settings dict inside _save_and_accept(), after the "freedom_winner_extra_improvement" entry, add:

Python
            "freedom_hard_stop_loss_pct": self.freedom_hard_stop_spin.value(),
4 — Return the value in get_settings()
In the return dict inside get_settings(), after the "freedom_winner_extra_improvement" entry, add:

Python
            "freedom_hard_stop_loss_pct": self.freedom_hard_stop_spin.value(),
IMPORTANT constraints
Only modify core/freedom_bot.py and gui/settings_dialog.py
Do NOT touch any other file
The hard stop method reads current_price from get_open_positions_display() — do NOT fetch fresh OHLCV just for this check. The position snapshot price is sufficient and keeps the check fast
The hard stop fires regardless of regime, circuit breaker state, action cap, or scanner freshness — it is unconditional
holding_scores.pop(sym, None) after the hard stop ensures the symbol is completely invisible to ATR exits, rotation, stranded cash, and Step 5 for the rest of this cycle
The 🚨 emoji in the log line is intentional — makes it visually unmissable in the activity feed
Default value is 8.0% — shown in the spinbox and used as the fallback in _check_hard_stop_losses() when the setting is absent
set to 0.0 to disable must work — the method returns [] immediately when stop_pct <= 0 - push when complete again plz

**Copilot:**

Let me read both files fully before touching anything.  Now I need to find the exact ATR block in  to anchor the insertion point: I have everything I need. Now I'll make all changes simultaneously:

---

## Turn 2 — 2026-04-12 20:20:34 UTC

**User:**

Add orphan position cleanup to Freedom Bot. Two files only:
`core/freedom_bot.py` and `gui/settings_dialog.py`. Read everything
before writing any code.

---

## THE CHANGE IN PLAIN ENGLISH - if you agree ...

An "orphan" position is one whose current market value is below a
configurable minimum threshold (default $50). These positions occupy
a full slot in the 6-position cap but contribute almost nothing to the
portfolio. They should be treated the same as weak-scoring positions —
freed when there is a better opportunity, or cleaned up when they have
been orphaned long enough.

The rule:
- If a position's market value is below `freedom_min_position_value_usd`
  AND a strong opportunity exists that scores at least +0.10 above it
  → sell the orphan, log with 🧹, and let Step 5 deploy the freed slot
- If a position's market value is below the threshold AND no opportunity
  exists → do NOT sell (never sell just because it's small, only when
  there's somewhere better to go)
- Default threshold: $50. Set to 0 to disable.
- Fires AFTER the hard stop-loss block and AFTER the ATR exits, but
  BEFORE the rotation logic (Step 4), so orphans are cleaned before
  the weak-score loop runs.

---

## CHANGES TO `core/freedom_bot.py`

### 1 — Add class constant

After `HARD_STOP_LOSS_PCT = 8.0`, add:
```python
MIN_POSITION_VALUE_USD = 50.0  # positions below this value are orphans eligible for cleanup; 0 = disabled
2 — Add _check_orphan_positions() method
Add this new method directly above _check_hard_stop_losses():

Python
def _check_orphan_positions(
    self,
    holding_scores: dict,
    strong_opps: list[tuple[str, dict]],
    already_exited: set[str],
) -> list[dict]:
    """
    Identify and clean up orphan positions — positions whose current
    market value is below `freedom_min_position_value_usd`.

    An orphan is only sold if a strong opportunity exists that scores
    at least MIN_ORPHAN_IMPROVEMENT above the orphan's current score.
    If no opportunity exists, the orphan is left alone — we never sell
    purely because a position is small.

    Returns a list of action dicts. Symbols that are sold are removed
    from holding_scores in-place so they are invisible to all downstream
    logic (rotation, stranded cash, Step 5 fresh-entry).
    """
    MIN_ORPHAN_IMPROVEMENT = 0.10

    min_value = float(
        self.settings.get("freedom_min_position_value_usd", self.MIN_POSITION_VALUE_USD)
        or 0.0
    )
    if min_value <= 0:
        return []

    actions: list[dict] = []

    for symbol, data in list(holding_scores.items()):
        if symbol in already_exited:
            continue

        pos = data.get("pos", {})
        market_value = float(pos.get("market_value", 0.0) or 0.0)

        if market_value <= 0 or market_value >= min_value:
            continue  # not an orphan

        orphan_score = data["score"]

        # Only clean up if there is a clearly better place to put the capital
        best_opp = next(
            (
                (sym, d)
                for sym, d in strong_opps
                if sym not in already_exited
                and sym != symbol
                and d["score"] >= orphan_score + MIN_ORPHAN_IMPROVEMENT
            ),
            None,
        )
        if best_opp is None:
            self._log(
                f"[Freedom] 🧹 Orphan {symbol} (${market_value:.2f}) — "
                f"no better opportunity available, holding for now."
            )
            continue

        best_sym, best_data = best_opp
        qty = float(pos.get("qty", 0.0) or 0.0)
        current_price = float(pos.get("current_price", 0.0) or 0.0)

        if qty <= 0 or current_price <= 0:
            continue

        trade = self.paper_trader.sell(
            symbol=symbol,
            qty=qty,
            price=current_price,
            strategy="Freedom Bot",
            reason=(
                f"Orphan cleanup — position value ${market_value:.2f} "
                f"below minimum ${min_value:.0f} | "
                f"rotating toward {best_sym} (score {best_data['score']:.2f})"
            ),
            source="freedom",
        )
        if trade:
            self._log(
                f"[Freedom] 🧹 Orphan cleanup {symbol} — "
                f"value ${market_value:.2f} below minimum ${min_value:.0f} "
                f"| score {orphan_score:.2f} | freeing slot for {best_sym} "
                f"(score {best_data['score']:.2f})"
            )
            actions.append({
                "type": "SELL",
                "symbol": symbol,
                "reason": f"Orphan cleanup — value ${market_value:.2f} below minimum ${min_value:.0f}",
            })
            holding_scores.pop(symbol, None)

    return actions
3 — Call _check_orphan_positions() inside run()
In run(), find this existing block:

Python
        # ── Step 4: Rotate weak holdings into strong opportunities ──────
        weak_holdings = [
INSERT the following block IMMEDIATELY BEFORE that line:

Python
        # ── Orphan cleanup — after ATR exits, before rotation ───────────
        already_exited = {a["symbol"] for a in actions if a["type"] == "SELL"}
        orphan_acts = self._check_orphan_positions(
            holding_scores, strong_opps, already_exited
        )
        if orphan_acts:
            actions.extend(orphan_acts)
Note: holding_scores.pop() is already called inside _check_orphan_positions() — do NOT add another pop loop here. The already_exited set is built fresh from actions at that point and correctly includes hard stop and ATR exits from earlier in the cycle.

CHANGES TO gui/settings_dialog.py
1 — Add the spinbox in _build_ui()
In the Freedom Bot QGroupBox (the freedom_group / freedom_layout block), add the following AFTER the hard stop-loss row and BEFORE trading_freedom_layout.addWidget(freedom_group):

Python
        self.freedom_min_position_spin = QDoubleSpinBox()
        self.freedom_min_position_spin.setRange(0.0, 500.0)
        self.freedom_min_position_spin.setSingleStep(5.0)
        self.freedom_min_position_spin.setDecimals(0)
        self.freedom_min_position_spin.setPrefix("$")
        self.freedom_min_position_spin.setValue(50.0)
        self.freedom_min_position_spin.setToolTip(
            "Freedom Bot will free up slots occupied by positions worth less "
            "than this amount when a better opportunity is available. "
            "Set to $0 to disable orphan cleanup."
        )
        freedom_layout.addRow("Min position value:", self.freedom_min_position_spin)
2 — Load the value in _load_values()
After the line that loads freedom_hard_stop_spin, add:

Python
        self.freedom_min_position_spin.setValue(
            float(settings.get("freedom_min_position_value_usd", 50.0) or 50.0)
        )
3 — Save the value in _save_and_accept()
After the "freedom_hard_stop_loss_pct" entry, add:

Python
            "freedom_min_position_value_usd": self.freedom_min_position_spin.value(),
4 — Return the value in get_settings()
After the "freedom_hard_stop_loss_pct" entry, add:

Python
            "freedom_min_position_value_usd": self.freedom_min_position_spin.value(),
IMPORTANT constraints
Only modify core/freedom_bot.py and gui/settings_dialog.py
Do NOT touch any other file
_check_orphan_positions() mutates holding_scores in-place via .pop() — this is intentional. Do NOT add a second pop loop in run()
The already_exited set passed in must be built from actions at the point of the call — it will contain hard stop and ATR exit symbols from earlier in the same cycle, preventing double-sells
MIN_ORPHAN_IMPROVEMENT = 0.10 is a local constant inside the method, not a class constant — it is not user-configurable
Never sell an orphan if best_opp is None — the "hold for now" log line must fire instead
The 🧹 emoji is intentional — distinct from 🚨 (hard stop), 🛑 (ATR stop), and 🔄 (rotation) in the activity feed
Default $50, set to $0 to disable — both must work correctly
market_value comes from pos.get("market_value") on the position display dict — do NOT calculate it from qty × price - push when complete again please

**Copilot:**

*(no response captured)*

---
