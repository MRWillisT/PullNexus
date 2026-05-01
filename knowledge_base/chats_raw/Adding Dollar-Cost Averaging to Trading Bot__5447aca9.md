# Adding Dollar-Cost Averaging to Trading Bot

**Session ID:** `5447aca9-0e97-43e5-a66c-9e59fb88c308`  
**Created:** 2026-04-11 00:21:10 UTC  
**Source:** `C:\Users\willa\AppData\Roaming\Code\User\workspaceStorage\2832faeff98184b2f116b13fae9699e8\chatSessions\5447aca9-0e97-43e5-a66c-9e59fb88c308.jsonl`

---

## Turn 1 — 2026-04-11 00:28:30 UTC

**User:**

pleae push the latest to github

**Copilot:**

All changes have been committed and pushed to GitHub. The DCA entry mode feature is now live in your repository.

---

## Turn 2 — 2026-04-11 00:37:11 UTC

**User:**

Copilot said: Good, I have everything I need. Here's
Good, I have everything I need. Here's the full prompt for L + M + N all in one go:

🤖 Prompt to paste into your VS Code Copilot
Code
I need three small improvements across four files. Read all three changes
carefully before writing any code. They are independent of each other.

---

## CHANGE L — Per-coin exposure cap in the regular bot (`gui/trading_panel.py`)

### What it does
The regular bot currently has no limit on how much of the portfolio it can
put into a single coin. If it gets 5 BUY signals in a row on BTCUSDT it will
keep buying. This change adds a `max_coin_exposure_pct` guardrail that caps
the total value the bot will deploy into any one symbol.

### Step L1 — New default in `config/settings.py`
Add one new constant after the existing DEFAULT_* block:
```python
DEFAULT_MAX_COIN_EXPOSURE_PCT = 25.0   # max % of portfolio in any single coin
Step L2 — New BotWorker parameter
In BotWorker.__init__, add one new optional parameter after dca_drop_pct:

Python
max_coin_exposure_pct: float = DEFAULT_MAX_COIN_EXPOSURE_PCT,
Store it:

Python
self.max_coin_exposure_pct = max(1.0, float(max_coin_exposure_pct))
Import DEFAULT_MAX_COIN_EXPOSURE_PCT from config.settings — add it to the existing import line.

Step L3 — Exposure check in _process_symbol()
In _process_symbol(), find the BUY block. Immediately after the if usdt_to_use < 10.0: return check, add an exposure check:

Python
if self.max_coin_exposure_pct > 0:
    total_value = self.paper_trader.get_portfolio_value()
    if total_value > 0:
        pos = self.paper_trader.positions.get(symbol)
        current_coin_value = 0.0
        if pos:
            price_now = self.paper_trader.get_price(symbol) or float(pos.get("avg_price", 0.0))
            current_coin_value = float(pos.get("qty", 0.0)) * price_now
        max_coin_value = total_value * (self.max_coin_exposure_pct / 100.0)
        remaining_capacity = max(0.0, max_coin_value - current_coin_value)
        if remaining_capacity < 10.0:
            self._emit_guardrail_notice(
                f"Skipping new entry on {symbol}: coin exposure cap reached "
                f"({current_coin_value / total_value * 100.0:.1f}% >= {self.max_coin_exposure_pct:.1f}% max)",
                min_interval_seconds=300,
            )
            return
        # Cap usdt_to_use so we don't overshoot the cap
        usdt_to_use = min(usdt_to_use, remaining_capacity)
        if usdt_to_use < 10.0:
            return
Step L4 — Pass the setting when constructing BotWorker in _start_bot()
Add at the end of the BotWorker(...) constructor call:

Python
max_coin_exposure_pct=float(self.settings.get("max_coin_exposure_pct", DEFAULT_MAX_COIN_EXPOSURE_PCT)),
Step L5 — Add control to gui/settings_dialog.py
In _build_ui(), find the Trading Settings group (it has risk_pct_spin, paper_balance_spin, etc.). Add a new row at the bottom of that group:

Python
self.max_coin_exposure_spin = QDoubleSpinBox()
self.max_coin_exposure_spin.setRange(5.0, 100.0)
self.max_coin_exposure_spin.setSingleStep(5.0)
self.max_coin_exposure_spin.setSuffix("%")
self.max_coin_exposure_spin.setValue(DEFAULT_MAX_COIN_EXPOSURE_PCT)
self.max_coin_exposure_spin.setToolTip(
    "The regular bot will not put more than this % of total portfolio value "
    "into any single coin. E.g. 25% means it stops buying BTC once BTC is "
    "worth 25% of the paper portfolio. Does not affect Freedom Bot."
)
trading_layout.addRow("Max single-coin exposure:", self.max_coin_exposure_spin)
Wire it up in _load_values():

Python
self.max_coin_exposure_spin.setValue(float(settings.get("max_coin_exposure_pct", DEFAULT_MAX_COIN_EXPOSURE_PCT)))
Wire it up in both _save_and_accept() and get_settings():

Python
"max_coin_exposure_pct": self.max_coin_exposure_spin.value(),
Import DEFAULT_MAX_COIN_EXPOSURE_PCT from config.settings — add it to the existing import line in settings_dialog.py.

CHANGE M — Freedom Bot regime-aware thresholds wired to settings
File: core/freedom_bot.py
The _get_regime_context() method already adjusts buy_threshold, sell_threshold, and rotation_improvement based on market regime. However the BASE values it starts from are always the class-level constants (BUY_THRESHOLD = 0.62, SELL_THRESHOLD = 0.36, ROTATION_IMPROVEMENT = 0.15).

This means the user's custom settings for these values (if we add them) are never used. Make the regime context method read from settings first:

In _get_regime_context(), change the first three lines that set the base values from:

Python
buy_threshold = self.BUY_THRESHOLD
sell_threshold = self.SELL_THRESHOLD
rotation_improvement = self.ROTATION_IMPROVEMENT
To:

Python
buy_threshold = float(
    self.settings.get("freedom_buy_threshold", self.BUY_THRESHOLD)
    or self.BUY_THRESHOLD
)
sell_threshold = float(
    self.settings.get("freedom_sell_threshold", self.SELL_THRESHOLD)
    or self.SELL_THRESHOLD
)
rotation_improvement = float(
    self.settings.get("freedom_rotation_improvement", self.ROTATION_IMPROVEMENT)
    or self.ROTATION_IMPROVEMENT
)
That's the ONLY change to freedom_bot.py. Do not touch anything else.

Then add three new constants to config/settings.py alongside the other Freedom Bot defaults:

Python
DEFAULT_FREEDOM_BUY_THRESHOLD = 0.62
DEFAULT_FREEDOM_SELL_THRESHOLD = 0.36
DEFAULT_FREEDOM_ROTATION_IMPROVEMENT = 0.15
Then add three controls to the Freedom Bot group in gui/settings_dialog.py. Find the QGroupBox("Freedom Bot") section (it has freedom_fresh_deploy_spin and freedom_circuit_breaker_spin). Add three new rows after the circuit breaker row:

Python
self.freedom_buy_threshold_spin = QDoubleSpinBox()
self.freedom_buy_threshold_spin.setRange(0.50, 0.95)
self.freedom_buy_threshold_spin.setSingleStep(0.01)
self.freedom_buy_threshold_spin.setDecimals(2)
self.freedom_buy_threshold_spin.setValue(DEFAULT_FREEDOM_BUY_THRESHOLD)
self.freedom_buy_threshold_spin.setToolTip(
    "Minimum composite strategy score (0–1) for Freedom Bot to consider buying a coin. "
    "Higher = stricter, fewer entries. Regime adjustments are applied on top of this."
)
freedom_layout.addRow("Buy threshold:", self.freedom_buy_threshold_spin)

self.freedom_sell_threshold_spin = QDoubleSpinBox()
self.freedom_sell_threshold_spin.setRange(0.10, 0.60)
self.freedom_sell_threshold_spin.setSingleStep(0.01)
self.freedom_sell_threshold_spin.setDecimals(2)
self.freedom_sell_threshold_spin.setValue(DEFAULT_FREEDOM_SELL_THRESHOLD)
self.freedom_sell_threshold_spin.setToolTip(
    "If a held coin's score falls below this, Freedom Bot considers rotating out. "
    "Lower = more tolerant of weak holdings. Regime adjustments are applied on top."
)
freedom_layout.addRow("Sell threshold:", self.freedom_sell_threshold_spin)

self.freedom_rotation_spin = QDoubleSpinBox()
self.freedom_rotation_spin.setRange(0.05, 0.50)
self.freedom_rotation_spin.setSingleStep(0.01)
self.freedom_rotation_spin.setDecimals(2)
self.freedom_rotation_spin.setValue(DEFAULT_FREEDOM_ROTATION_IMPROVEMENT)
self.freedom_rotation_spin.setToolTip(
    "The opportunity must score at least this much higher than the current holding "
    "for a rotation to happen. Higher = only rotates on clear upgrades."
)
freedom_layout.addRow("Rotation min improvement:", self.freedom_rotation_spin)
Import DEFAULT_FREEDOM_BUY_THRESHOLD, DEFAULT_FREEDOM_SELL_THRESHOLD, DEFAULT_FREEDOM_ROTATION_IMPROVEMENT from config.settings.

Wire all three in _load_values():

Python
self.freedom_buy_threshold_spin.setValue(float(settings.get("freedom_buy_threshold", DEFAULT_FREEDOM_BUY_THRESHOLD)))
self.freedom_sell_threshold_spin.setValue(float(settings.get("freedom_sell_threshold", DEFAULT_FREEDOM_SELL_THRESHOLD)))
self.freedom_rotation_spin.setValue(float(settings.get("freedom_rotation_improvement", DEFAULT_FREEDOM_ROTATION_IMPROVEMENT)))
Wire all three in both _save_and_accept() and get_settings():

Python
"freedom_buy_threshold": self.freedom_buy_threshold_spin.value(),
"freedom_sell_threshold": self.freedom_sell_threshold_spin.value(),
"freedom_rotation_improvement": self.freedom_rotation_spin.value(),
CHANGE N — Auto-resume prompt on startup (gui/main_window.py)
What it does
When the app restarts after a previous session where the regular bot OR Freedom Bot was running, show a one-time QMessageBox.question() asking: "Resume your previous session?" with Yes / No buttons.

If the user clicks Yes:

If session_state.get("bot_running") was True → call self._trading_panel.update_settings(session_state) then call self._trading_panel._start_bot()
If session_state.get("freedom_auto_enabled") was True → call self._trading_panel._start_freedom_auto()
If the user clicks No: do nothing extra (the UI still loads with the saved state, just the bots stay stopped).

Where to add it
In main_window.py, find _restore_session() (or wherever session_state is loaded from disk and applied to _trading_panel).

After the settings/state is applied to the panel, add:

Python
# Auto-resume prompt
_was_bot_running = bool(session_state.get("bot_running", False))
_was_freedom_running = bool(session_state.get("freedom_auto_enabled", False))
if _was_bot_running or _was_freedom_running:
    _parts = []
    if _was_bot_running:
        _parts.append("regular bot")
    if _was_freedom_running:
        _parts.append("Freedom Bot")
    _running_label = " and ".join(_parts)
    reply = QMessageBox.question(
        self,
        "Resume previous session?",
        f"Your {_running_label} was running when the app last closed.\n\n"
        "Would you like to resume it now?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if reply == QMessageBox.Yes:
        if _was_bot_running:
            try:
                self._trading_panel._start_bot()
            except Exception:
                pass
        if _was_freedom_running:
            try:
                self._trading_panel._start_freedom_auto()
            except Exception:
                pass
The QMessageBox import is almost certainly already present in main_window.py. If not, add it to the PyQt5.QtWidgets import line.

The default button is No so if the user just presses Enter or closes the dialog, nothing auto-starts. This prevents surprise auto-trading on launch.

IMPORTANT constraints
Only modify these files:
config/settings.py
core/freedom_bot.py
gui/trading_panel.py
gui/settings_dialog.py
gui/main_window.py
Do NOT restructure any existing method in any file
All new BotWorker params must have safe defaults
The exposure check (Change L) must run BEFORE the DCA split, not inside it
max_coin_exposure_pct = 0 should disable the cap entirely (already handled by if self.max_coin_exposure_pct > 0)
Change M must NOT change the class-level constants on FreedomBot — only the runtime values in _get_regime_context()
Change N default answer is No — no auto-start without user confirmation --- push when finished please

**Copilot:**

I'll apply the requested guardrail, Freedom Bot settings wiring, and startup resume prompt, then verify and push.

---

## Turn 3 — 2026-04-11 00:51:07 UTC

**User:**

I need a regression test suite added to the project. This creates a new
`tests/` directory with four test files. No existing files should be modified
at all — this is purely additive.

The project uses Python with pandas and numpy. Do NOT add pytest to
requirements.txt — it is a dev-only dependency and the user will install it
separately with `pip install pytest`. All tests must run with:

    pytest tests/ -v

---

## FILE 1 — `tests/__init__.py`

Empty file. Just creates the package.

---

## FILE 2 — `tests/conftest.py`

Shared fixtures used by all test files.

```python
"""Shared pytest fixtures for the crypto-trading-bot test suite."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


# ---------------------------------------------------------------------------
# OHLCV DataFrame factories
# ---------------------------------------------------------------------------

def make_ohlcv(
    n: int = 300,
    base_price: float = 100.0,
    trend: float = 0.0,
    volatility: float = 1.0,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Build a synthetic OHLCV DataFrame suitable for feeding into strategies.

    Parameters
    ----------
    n           : number of candles
    base_price  : starting close price
    trend       : linear drift per candle (e.g. 0.1 = slow uptrend)
    volatility  : multiplier on random noise
    seed        : random seed for reproducibility
    """
    rng = np.random.default_rng(seed)
    closes = base_price + trend * np.arange(n) + volatility * rng.standard_normal(n).cumsum()
    closes = np.maximum(closes, 0.01)  # never go negative
    highs = closes * (1.0 + rng.uniform(0.001, 0.02, n))
    lows = closes * (1.0 - rng.uniform(0.001, 0.02, n))
    opens = np.roll(closes, 1)
    opens[0] = closes[0]
    volumes = rng.uniform(1_000_000, 10_000_000, n)

    df = pd.DataFrame(
        {
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
        }
    )
    df.index = pd.date_range("2024-01-01", periods=n, freq="1h")
    return df


def make_uptrend(n: int = 300, seed: int = 1) -> pd.DataFrame:
    """Strong uptrend — strategies should lean bullish."""
    return make_ohlcv(n=n, base_price=100.0, trend=0.5, volatility=0.5, seed=seed)


def make_downtrend(n: int = 300, seed: int = 2) -> pd.DataFrame:
    """Strong downtrend — strategies should lean bearish."""
    return make_ohlcv(n=n, base_price=200.0, trend=-0.5, volatility=0.5, seed=seed)


def make_flat(n: int = 300, seed: int = 3) -> pd.DataFrame:
    """Flat/sideways market."""
    return make_ohlcv(n=n, base_price=100.0, trend=0.0, volatility=0.3, seed=seed)


def make_short(n: int = 30, seed: int = 9) -> pd.DataFrame:
    """Very short DataFrame — should trigger insufficient-data guards."""
    return make_ohlcv(n=n, base_price=100.0, trend=0.0, volatility=1.0, seed=seed)


# ---------------------------------------------------------------------------
# pytest fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def uptrend_df():
    return make_uptrend()


@pytest.fixture
def downtrend_df():
    return make_downtrend()


@pytest.fixture
def flat_df():
    return make_flat()


@pytest.fixture
def short_df():
    return make_short()
FILE 3 — tests/test_strategies.py
Tests for every strategy in core/strategies/. The goals are:

Every strategy returns a valid Signal object (not None, not an exception) on normal data.
Every strategy returns Signal.HOLD (or any valid action) on short/sparse data — it must NOT raise an exception.
The Signal object always has action in {"BUY","SELL","HOLD"}, strength between 0.0 and 1.0, and a non-empty reason string.
On a strong uptrend, strategies that are trend-following should not produce a SELL signal (soft check — logged as xfail if they do, not a hard failure, because synthetic data is not guaranteed to trigger every strategy).
Python
"""Regression tests for all 14 trading strategies."""
from __future__ import annotations

import pytest

from core.strategies import STRATEGY_MAP, get_strategy
from core.strategies.base_strategy import Signal
from tests.conftest import make_uptrend, make_downtrend, make_flat, make_short

# All strategy names from the registry
ALL_STRATEGY_NAMES = list(STRATEGY_MAP.keys())

# Strategies that are inherently trend-following (should not produce BUY on
# a clean downtrend with high confidence — soft assertion only)
TREND_FOLLOWING = {
    "Moving Average Crossover (50/200 MA)",
    "MACD Momentum",
    "ATR Squeeze Breakout",
    "Trend + Momentum Confluence",
    "Parabolic SAR + ADX",
}


class TestSignalContract:
    """Every strategy must return a valid Signal on any input."""

    @pytest.mark.parametrize("name", ALL_STRATEGY_NAMES)
    def test_returns_signal_on_normal_data(self, name, uptrend_df):
        """Strategy must return a Signal object without raising."""
        strategy = get_strategy(name)
        result = strategy.generate_signal(uptrend_df)
        assert result is not None, f"{name}: returned None"
        assert isinstance(result, Signal), f"{name}: did not return a Signal"

    @pytest.mark.parametrize("name", ALL_STRATEGY_NAMES)
    def test_signal_action_is_valid(self, name, uptrend_df):
        """Signal.action must always be BUY, SELL, or HOLD."""
        strategy = get_strategy(name)
        result = strategy.generate_signal(uptrend_df)
        assert result.action in {Signal.BUY, Signal.SELL, Signal.HOLD}, (
            f"{name}: invalid action {result.action!r}"
        )

    @pytest.mark.parametrize("name", ALL_STRATEGY_NAMES)
    def test_signal_strength_in_range(self, name, uptrend_df):
        """Signal.strength must be between 0.0 and 1.0 inclusive."""
        strategy = get_strategy(name)
        result = strategy.generate_signal(uptrend_df)
        assert 0.0 <= result.strength <= 1.0, (
            f"{name}: strength {result.strength} out of [0, 1]"
        )

    @pytest.mark.parametrize("name", ALL_STRATEGY_NAMES)
    def test_signal_has_reason(self, name, uptrend_df):
        """Signal.reason must be a non-empty string."""
        strategy = get_strategy(name)
        result = strategy.generate_signal(uptrend_df)
        assert isinstance(result.reason, str), f"{name}: reason is not a string"
        assert len(result.reason.strip()) > 0, f"{name}: reason is empty"

    @pytest.mark.parametrize("name", ALL_STRATEGY_NAMES)
    def test_does_not_raise_on_short_data(self, name, short_df):
        """Strategy must not raise an exception on under-minimum data."""
        strategy = get_strategy(name)
        try:
            result = strategy.generate_signal(short_df)
            # If it returns something, it must be a valid Signal
            if result is not None:
                assert result.action in {Signal.BUY, Signal.SELL, Signal.HOLD}
        except Exception as exc:
            pytest.fail(
                f"{name}: raised {type(exc).__name__} on short data: {exc}"
            )

    @pytest.mark.parametrize("name", ALL_STRATEGY_NAMES)
    def test_consistent_output_same_input(self, name, flat_df):
        """Calling generate_signal twice with the same data must return the same action."""
        strategy = get_strategy(name)
        result1 = strategy.generate_signal(flat_df)
        result2 = strategy.generate_signal(flat_df)
        assert result1.action == result2.action, (
            f"{name}: non-deterministic — got {result1.action} then {result2.action}"
        )

    @pytest.mark.parametrize("name", ALL_STRATEGY_NAMES)
    def test_does_not_mutate_dataframe(self, name, uptrend_df):
        """Strategy must not modify the input DataFrame."""
        import pandas as pd
        original_cols = set(uptrend_df.columns)
        original_close_last = float(uptrend_df["close"].iloc[-1])
        strategy = get_strategy(name)
        strategy.generate_signal(uptrend_df)
        assert set(uptrend_df.columns) == original_cols, (
            f"{name}: added columns to input DataFrame"
        )
        assert float(uptrend_df["close"].iloc[-1]) == original_close_last, (
            f"{name}: modified close prices in input DataFrame"
        )


class TestStrategyRegistry:
    """Tests for the strategy registry itself."""

    def test_all_14_strategies_registered(self):
        """Exactly 14 strategies must be in STRATEGY_MAP."""
        assert len(STRATEGY_MAP) == 14, (
            f"Expected 14 strategies, found {len(STRATEGY_MAP)}: {list(STRATEGY_MAP.keys())}"
        )

    def test_get_strategy_returns_instance(self):
        """get_strategy() must return an instance, not a class."""
        from core.strategies.base_strategy import BaseStrategy
        for name in STRATEGY_MAP:
            instance = get_strategy(name)
            assert isinstance(instance, BaseStrategy), (
                f"get_strategy({name!r}) returned {type(instance)}, not a BaseStrategy"
            )

    def test_get_strategy_raises_on_unknown(self):
        """get_strategy() must raise ValueError for unknown names."""
        with pytest.raises(ValueError):
            get_strategy("Not A Real Strategy")

    def test_strategy_has_name_attribute(self):
        """Every strategy instance must have a non-empty .name attribute."""
        for name in STRATEGY_MAP:
            instance = get_strategy(name)
            assert hasattr(instance, "name"), f"{name}: missing .name attribute"
            assert isinstance(instance.name, str), f"{name}: .name is not a string"
            assert len(instance.name.strip()) > 0, f"{name}: .name is empty"
FILE 4 — tests/test_paper_trader.py
Tests for core/paper_trader.py — the engine that handles all simulated trades, positions, DCA state, and P&L.

Python
"""Regression tests for PaperTrader — the simulated trading engine."""
from __future__ import annotations

import pytest
from core.paper_trader import PaperTrader, Trade


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_trader(balance: float = 1000.0) -> PaperTrader:
    return PaperTrader(starting_balance=balance)


# ---------------------------------------------------------------------------
# Basic buy / sell mechanics
# ---------------------------------------------------------------------------

class TestBuyMechanics:

    def test_buy_reduces_usdt_balance(self):
        pt = make_trader(1000.0)
        pt.buy("BTCUSDT", 100.0, 50000.0)
        assert pt.usdt_balance < 1000.0

    def test_buy_creates_position(self):
        pt = make_trader(1000.0)
        pt.buy("BTCUSDT", 100.0, 50000.0)
        assert "BTCUSDT" in pt.positions
        assert pt.positions["BTCUSDT"]["qty"] > 0

    def test_buy_records_trade(self):
        pt = make_trader(1000.0)
        pt.buy("BTCUSDT", 100.0, 50000.0)
        assert len(pt.trade_history) == 1
        assert pt.trade_history[0].side == "BUY"

    def test_buy_returns_trade_object(self):
        pt = make_trader(1000.0)
        trade = pt.buy("BTCUSDT", 100.0, 50000.0)
        assert trade is not None
        assert isinstance(trade, Trade)

    def test_buy_rejected_when_insufficient_balance(self):
        pt = make_trader(50.0)
        trade = pt.buy("BTCUSDT", 500.0, 50000.0)
        assert trade is None
        assert len(pt.trade_history) == 0

    def test_buy_rejected_when_price_zero(self):
        pt = make_trader(1000.0)
        trade = pt.buy("BTCUSDT", 100.0, 0.0)
        assert trade is None

    def test_buy_averages_down_correctly(self):
        """Two buys at different prices should average the entry cost."""
        pt = make_trader(1000.0)
        pt.buy("ETHUSDT", 200.0, 2000.0)
        pt.buy("ETHUSDT", 200.0, 1000.0)
        pos = pt.positions["ETHUSDT"]
        # avg_price should be between 1000 and 2000
        assert 1000.0 < pos["avg_price"] < 2000.0

    def test_buy_fee_applied(self):
        pt = make_trader(1000.0)
        pt.configure_execution_model(fee_bps=10.0, slippage_bps=0.0)
        trade = pt.buy("BTCUSDT", 100.0, 50000.0)
        assert trade.fee > 0.0


class TestSellMechanics:

    def test_sell_increases_usdt_balance(self):
        pt = make_trader(1000.0)
        pt.buy("BTCUSDT", 500.0, 50000.0)
        cash_after_buy = pt.usdt_balance
        pos = pt.positions["BTCUSDT"]
        pt.update_price("BTCUSDT", 50000.0)
        pt.sell("BTCUSDT", pos["qty"], 50000.0)
        assert pt.usdt_balance > cash_after_buy

    def test_sell_removes_position_when_full(self):
        pt = make_trader(1000.0)
        pt.buy("BTCUSDT", 500.0, 50000.0)
        pos = pt.positions["BTCUSDT"]
        pt.sell("BTCUSDT", pos["qty"], 50000.0)
        assert "BTCUSDT" not in pt.positions

    def test_sell_records_pnl(self):
        pt = make_trader(1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        pt.buy("BTCUSDT", 500.0, 50000.0)
        pos = pt.positions["BTCUSDT"]
        trade = pt.sell("BTCUSDT", pos["qty"], 55000.0)
        assert trade.pnl is not None
        assert trade.pnl > 0.0  # sold higher than bought

    def test_sell_rejected_when_no_position(self):
        pt = make_trader(1000.0)
        trade = pt.sell("BTCUSDT", 0.001, 50000.0)
        assert trade is None

    def test_sell_all(self):
        pt = make_trader(1000.0)
        pt.buy("SOLUSDT", 300.0, 100.0)
        trade = pt.sell_all("SOLUSDT", 100.0)
        assert trade is not None
        assert "SOLUSDT" not in pt.positions

    def test_sell_fraction(self):
        pt = make_trader(1000.0)
        pt.buy("SOLUSDT", 300.0, 100.0)
        initial_qty = pt.positions["SOLUSDT"]["qty"]
        pt.sell_fraction("SOLUSDT", 0.5, 100.0)
        remaining = pt.positions.get("SOLUSDT")
        assert remaining is not None
        assert abs(remaining["qty"] - initial_qty * 0.5) < 1e-6

    def test_loss_recorded_correctly(self):
        pt = make_trader(1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        pt.buy("BTCUSDT", 500.0, 50000.0)
        pos = pt.positions["BTCUSDT"]
        trade = pt.sell("BTCUSDT", pos["qty"], 45000.0)
        assert trade.pnl < 0.0  # sold lower than bought


# ---------------------------------------------------------------------------
# Portfolio metrics
# ---------------------------------------------------------------------------

class TestPortfolioMetrics:

    def test_get_portfolio_value_includes_positions(self):
        pt = make_trader(1000.0)
        pt.buy("BTCUSDT", 500.0, 50000.0)
        pt.update_price("BTCUSDT", 60000.0)
        value = pt.get_portfolio_value()
        assert value > 1000.0

    def test_get_total_pnl_positive_after_gain(self):
        pt = make_trader(1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        pt.buy("BTCUSDT", 500.0, 50000.0)
        pt.update_price("BTCUSDT", 60000.0)
        assert pt.get_total_pnl() > 0

    def test_win_rate_zero_with_no_trades(self):
        pt = make_trader(1000.0)
        assert pt.get_win_rate() == 0.0

    def test_win_rate_100_after_winning_trade(self):
        pt = make_trader(1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        pt.buy("BTCUSDT", 500.0, 50000.0)
        pos = pt.positions["BTCUSDT"]
        pt.sell("BTCUSDT", pos["qty"], 55000.0)
        assert pt.get_win_rate() == 100.0

    def test_win_rate_0_after_losing_trade(self):
        pt = make_trader(1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        pt.buy("BTCUSDT", 500.0, 50000.0)
        pos = pt.positions["BTCUSDT"]
        pt.sell("BTCUSDT", pos["qty"], 45000.0)
        assert pt.get_win_rate() == 0.0

    def test_consecutive_losses_counted(self):
        pt = make_trader(1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        for _ in range(3):
            pt.buy("BTCUSDT", 100.0, 50000.0)
            pos = pt.positions["BTCUSDT"]
            pt.sell("BTCUSDT", pos["qty"], 45000.0)
        assert pt.get_consecutive_losses() == 3

    def test_consecutive_losses_reset_after_win(self):
        pt = make_trader(1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        # two losses
        for _ in range(2):
            pt.buy("BTCUSDT", 100.0, 50000.0)
            pos = pt.positions["BTCUSDT"]
            pt.sell("BTCUSDT", pos["qty"], 45000.0)
        # one win
        pt.buy("BTCUSDT", 100.0, 50000.0)
        pos = pt.positions["BTCUSDT"]
        pt.sell("BTCUSDT", pos["qty"], 55000.0)
        assert pt.get_consecutive_losses() == 0


# ---------------------------------------------------------------------------
# DCA state management
# ---------------------------------------------------------------------------

class TestDCAState:

    def test_register_and_get_tranches(self):
        pt = make_trader()
        tranches = [
            {"target_price": 48000.0, "usdt_amount": 100.0, "tranche": 2},
            {"target_price": 46000.0, "usdt_amount": 100.0, "tranche": 3},
        ]
        pt.register_dca_tranches("BTCUSDT", tranches)
        result = pt.get_dca_tranches("BTCUSDT")
        assert len(result) == 2
        assert result[0]["tranche"] == 2

    def test_get_tranches_returns_empty_when_none(self):
        pt = make_trader()
        assert pt.get_dca_tranches("BTCUSDT") == []

    def test_clear_tranches(self):
        pt = make_trader()
        pt.register_dca_tranches("BTCUSDT", [{"target_price": 48000.0, "usdt_amount": 100.0, "tranche": 2}])
        pt.clear_dca_tranches("BTCUSDT")
        assert pt.get_dca_tranches("BTCUSDT") == []

    def test_get_tranches_returns_copy(self):
        """Mutating returned list must not affect stored tranches."""
        pt = make_trader()
        pt.register_dca_tranches("BTCUSDT", [{"target_price": 48000.0, "usdt_amount": 100.0, "tranche": 2}])
        result = pt.get_dca_tranches("BTCUSDT")
        result.clear()
        assert len(pt.get_dca_tranches("BTCUSDT")) == 1

    def test_reset_clears_dca_pending(self):
        pt = make_trader()
        pt.register_dca_tranches("BTCUSDT", [{"target_price": 48000.0, "usdt_amount": 100.0, "tranche": 2}])
        pt.reset()
        assert pt.get_dca_tranches("BTCUSDT") == []

    def test_dca_persists_through_serialization(self):
        """DCA pending tranches must survive to_dict → load_from_dict round-trip."""
        pt = make_trader()
        tranches = [{"target_price": 48000.0, "usdt_amount": 100.0, "tranche": 2}]
        pt.register_dca_tranches("BTCUSDT", tranches)
        snapshot = pt.to_dict()
        pt2 = make_trader()
        pt2.load_from_dict(snapshot)
        result = pt2.get_dca_tranches("BTCUSDT")
        assert len(result) == 1
        assert result[0]["target_price"] == 48000.0


# ---------------------------------------------------------------------------
# Serialisation round-trip
# ---------------------------------------------------------------------------

class TestSerialization:

    def test_to_dict_and_back_preserves_balance(self):
        pt = make_trader(1234.56)
        snapshot = pt.to_dict()
        pt2 = make_trader()
        pt2.load_from_dict(snapshot)
        assert abs(pt2.usdt_balance - pt.usdt_balance) < 0.01

    def test_to_dict_and_back_preserves_positions(self):
        pt = make_trader(1000.0)
        pt.buy("ETHUSDT", 300.0, 2000.0)
        snapshot = pt.to_dict()
        pt2 = make_trader()
        pt2.load_from_dict(snapshot)
        assert "ETHUSDT" in pt2.positions
        assert abs(pt2.positions["ETHUSDT"]["qty"] - pt.positions["ETHUSDT"]["qty"]) < 1e-8

    def test_to_dict_and_back_preserves_trade_history(self):
        pt = make_trader(1000.0)
        pt.buy("BTCUSDT", 200.0, 50000.0)
        snapshot = pt.to_dict()
        pt2 = make_trader()
        pt2.load_from_dict(snapshot)
        assert len(pt2.trade_history) == 1
        assert pt2.trade_history[0].symbol == "BTCUSDT"

    def test_load_from_none_is_safe(self):
        """load_from_dict(None) must not raise."""
        pt = make_trader()
        pt.load_from_dict(None)  # should be a no-op

    def test_reset_restores_starting_balance(self):
        pt = make_trader(500.0)
        pt.buy("BTCUSDT", 400.0, 50000.0)
        pt.reset()
        assert abs(pt.usdt_balance - 500.0) < 0.01
        assert len(pt.positions) == 0
        assert len(pt.trade_history) == 0
FILE 5 — tests/test_guardrails.py
Tests for the guardrail logic in BotWorker (exposure cap, DCA settings clamping) without needing a running Qt app. These test the data-layer logic in isolation using a mock client.

Python
"""Regression tests for BotWorker guardrail parameters and PaperTrader
exposure logic — no Qt event loop required."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np

from core.paper_trader import PaperTrader
from config.settings import (
    DEFAULT_MAX_COIN_EXPOSURE_PCT,
    DEFAULT_DCA_TRANCHES,
    DEFAULT_DCA_DROP_PCT,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_ohlcv(n: int = 300, price: float = 100.0) -> pd.DataFrame:
    """Minimal OHLCV DataFrame for BotWorker tests."""
    closes = np.full(n, price)
    df = pd.DataFrame(
        {
            "open": closes,
            "high": closes * 1.01,
            "low": closes * 0.99,
            "close": closes,
            "volume": np.full(n, 5_000_000.0),
        }
    )
    df.index = pd.date_range("2024-01-01", periods=n, freq="1h")
    return df


def make_bot_worker(**kwargs):
    """
    Construct a BotWorker with a mock client and real PaperTrader.
    All guardrail params can be overridden via kwargs.
    """
    # Import here so PyQt5 is only loaded when this function is called.
    # If Qt is not installed in CI, tests in this file will be skipped.
    pytest.importorskip("PyQt5.QtCore")
    from gui.trading_panel import BotWorker

    client = MagicMock()
    paper_trader = PaperTrader(starting_balance=1000.0)
    paper_trader.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)

    defaults = dict(
        strategy_name="RSI Oversold/Overbought",
        symbols=["BTCUSDT"],
        risk_pct=10.0,
        stop_loss_pct=5.0,
        take_profit_pct=10.0,
        paper_mode=True,
        dca_enabled=False,
    )
    defaults.update(kwargs)

    worker = BotWorker(client, paper_trader, **defaults)
    worker.paper_trader = paper_trader
    return worker, paper_trader


# ---------------------------------------------------------------------------
# BotWorker parameter clamping
# ---------------------------------------------------------------------------

class TestBotWorkerParamClamping:

    def test_dca_tranches_clamped_min(self):
        worker, _ = make_bot_worker(dca_tranches=1)
        assert worker.dca_tranches >= 2

    def test_dca_tranches_clamped_max(self):
        worker, _ = make_bot_worker(dca_tranches=99)
        assert worker.dca_tranches <= 5

    def test_dca_drop_pct_clamped_min(self):
        worker, _ = make_bot_worker(dca_drop_pct=0.0)
        assert worker.dca_drop_pct >= 0.5

    def test_max_coin_exposure_zero_disabled(self):
        """Setting max_coin_exposure_pct=0 must result in 0.0 (disabled)."""
        worker, _ = make_bot_worker(max_coin_exposure_pct=0.0)
        assert worker.max_coin_exposure_pct == 0.0

    def test_max_coin_exposure_clamped_min(self):
        """Tiny positive value must be clamped up to at least 1.0."""
        worker, _ = make_bot_worker(max_coin_exposure_pct=0.001)
        assert worker.max_coin_exposure_pct >= 1.0

    def test_max_coin_exposure_default(self):
        worker, _ = make_bot_worker()
        assert worker.max_coin_exposure_pct == DEFAULT_MAX_COIN_EXPOSURE_PCT


# ---------------------------------------------------------------------------
# Exposure cap math
# ---------------------------------------------------------------------------

class TestExposureCapMath:
    """Test the remaining-capacity arithmetic used by the exposure cap."""

    def test_capacity_full_when_no_position(self):
        pt = PaperTrader(starting_balance=1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        pt.update_price("BTCUSDT", 50000.0)
        total_value = pt.get_portfolio_value()
        max_coin_value = total_value * (25.0 / 100.0)
        # No position yet → remaining capacity = max_coin_value
        pos = pt.positions.get("BTCUSDT")
        current_coin_value = 0.0
        remaining = max(0.0, max_coin_value - current_coin_value)
        assert abs(remaining - 250.0) < 0.01

    def test_capacity_reduces_after_buy(self):
        pt = PaperTrader(starting_balance=1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        pt.buy("BTCUSDT", 200.0, 50000.0)
        pt.update_price("BTCUSDT", 50000.0)
        total_value = pt.get_portfolio_value()
        pos = pt.positions.get("BTCUSDT")
        price_now = pt.get_price("BTCUSDT")
        current_coin_value = pos["qty"] * price_now
        max_coin_value = total_value * (25.0 / 100.0)
        remaining = max(0.0, max_coin_value - current_coin_value)
        # Already put in ~200, cap is ~250, so remaining ~50
        assert remaining < 200.0

    def test_capacity_zero_when_at_cap(self):
        pt = PaperTrader(starting_balance=1000.0)
        pt.configure_execution_model(fee_bps=0.0, slippage_bps=0.0)
        # Buy right up to the 25% cap (250 USDT of 1000)
        pt.buy("BTCUSDT", 250.0, 50000.0)
        pt.update_price("BTCUSDT", 50000.0)
        total_value = pt.get_portfolio_value()
        pos = pt.positions.get("BTCUSDT")
        price_now = pt.get_price("BTCUSDT")
        current_coin_value = pos["qty"] * price_now
        max_coin_value = total_value * (25.0 / 100.0)
        remaining = max(0.0, max_coin_value - current_coin_value)
        assert remaining < 10.0  # below the $10 minimum → cap triggered


# ---------------------------------------------------------------------------
# Freedom Bot threshold settings
# ---------------------------------------------------------------------------

class TestFreedomBotThresholds:

    def test_default_thresholds_match_constants(self):
        from core.freedom_bot import FreedomBot
        from config.settings import (
            DEFAULT_FREEDOM_BUY_THRESHOLD,
            DEFAULT_FREEDOM_SELL_THRESHOLD,
            DEFAULT_FREEDOM_ROTATION_IMPROVEMENT,
        )
        assert DEFAULT_FREEDOM_BUY_THRESHOLD == FreedomBot.BUY_THRESHOLD
        assert DEFAULT_FREEDOM_SELL_THRESHOLD == FreedomBot.SELL_THRESHOLD
        assert DEFAULT_FREEDOM_ROTATION_IMPROVEMENT == FreedomBot.ROTATION_IMPROVEMENT

    def test_custom_buy_threshold_used_in_regime_context(self):
        """When freedom_buy_threshold is in settings, _get_regime_context uses it."""
        from core.freedom_bot import FreedomBot
        mock_client = MagicMock()
        mock_trader = MagicMock()
        mock_scanner = MagicMock()
        mock_scanner.get_cached_market_regime.return_value = {"status": "Neutral", "allow_trading": True}
        settings = {"freedom_buy_threshold": 0.75}
        bot = FreedomBot(mock_client, mock_trader, mock_scanner, settings)
        ctx = bot._get_regime_context()
        # The base threshold fed into regime adjustments starts at 0.75
        # For "Neutral"/"Unknown" status no adjustment is applied, so result should be 0.75
        assert ctx["buy_threshold"] == 0.75

    def test_custom_sell_threshold_used_in_regime_context(self):
        from core.freedom_bot import FreedomBot
        mock_client = MagicMock()
        mock_trader = MagicMock()
        mock_scanner = MagicMock()
        mock_scanner.get_cached_market_regime.return_value = {"status": "Neutral", "allow_trading": True}
        settings = {"freedom_sell_threshold": 0.25}
        bot = FreedomBot(mock_client, mock_trader, mock_scanner, settings)
        ctx = bot._get_regime_context()
        assert ctx["sell_threshold"] == 0.25
FILE 6 — tests/README.md
A short markdown file explaining how to run the tests.

tests/README.md
# Crypto Trading Bot — Test Suite

## Running the tests

Install pytest (one-time):
```bash
IMPORTANT constraints
Create ONLY these new files (do not modify anything else):
tests/__init__.py
tests/conftest.py
tests/test_strategies.py
tests/test_paper_trader.py
tests/test_guardrails.py
tests/README.md
Do NOT add pytest to requirements.txt
Do NOT modify any existing source file
All imports in test files use absolute paths from the project root (e.g. from core.paper_trader import PaperTrader) — pytest is run from the repo root so the project root is automatically on sys.path
The make_bot_worker helper uses pytest.importorskip("PyQt5.QtCore") so the whole test_guardrails.py BotWorker tests gracefully skip in environments without Qt installed - commit when finished

**Copilot:**

I'll add the new `tests/` suite exactly as requested, verify it with , and commit the result.

---

## Turn 4 — 2026-04-11 00:58:50 UTC

**User:**

push to github please

**Copilot:**

*(no response captured)*

---

## Turn 5 — 2026-04-11 01:13:14 UTC

**User:**

Copilot said: Got the full picture. The bug is
Got the full picture. The bug is on line 667 — elif free_pct > fresh_deploy_pct — the 25% threshold gates out stranded rotation cash. Here's the targeted fix prompt:

🤖 Prompt to paste into your VS Code Copilot
Code
Fix a single bug in `core/freedom_bot.py`. Do not touch anything else.

## The Problem

In `FreedomBot.run()`, Step 5 (Deploy free cash) at line ~667 only runs if:

    free_pct > fresh_deploy_pct   (i.e. >25% of portfolio is cash)

This means when a rotation SELL completes but the corresponding BUY fails
(e.g. OHLCV fetch returned None for the target symbol), the freed cash sits
stranded forever. In the next cycle the 25% threshold is never reached
(the cash might be only $50 of a $3,000 portfolio = 1.6%), so Step 5 skips
it. Freedom Bot then sells ANOTHER holding to fund the same buy instead.

## The Fix

Change the Step 5 condition so it also triggers when cash was freed by a
rotation SELL in the CURRENT cycle that didn't produce a matching BUY.

Find this block in Step 5 (starts around line 655):

```python
        if not allow_new_entries:
            self._log("[Freedom] ⏸ Fresh entries paused until scanner/regime conditions improve.")
        elif free_pct > fresh_deploy_pct and strong_opps:
Replace it with:

Python
        # Detect stranded cash from a sell-without-buy in this cycle
        sells_this_cycle = {a["symbol"] for a in actions if a["type"] == "SELL"}
        buys_this_cycle = {a["symbol"] for a in actions if a["type"] == "BUY"}
        has_stranded_cash = bool(sells_this_cycle - buys_this_cycle)  # sold something but didn't rebuy

        if not allow_new_entries and not has_stranded_cash:
            self._log("[Freedom] ⏸ Fresh entries paused until scanner/regime conditions improve.")
        elif (free_pct > fresh_deploy_pct or has_stranded_cash) and strong_opps:
That's the only change. Two lines become four lines. Nothing else moves. push update to github plz

**Copilot:**

I'll apply that targeted `FreedomBot` fix, verify it, and push the update to GitHub.
```

```
I've applied the small logic change and am validating it now before pushing.

---
