# kronos-trading-integration

A practical skill for connecting Kronos-generated market forecasts to a real crypto trading system. It focuses on turning model outputs into robust signals, then combining those signals with execution and risk controls.

## What This Skill Covers

- Mapping Kronos forecast outputs into usable bot features
- Converting predictions into directional confidence and position bias
- Signal fusion with existing technical strategy stacks
- Thresholding, cooldowns, and fail-safe behavior on stale predictions
- Backtest and paper-trade validation before live deployment

## Integration Pattern

1. Run Kronos inference on recent market data to produce a forecast horizon.
2. Extract decision features (predicted move, confidence, direction stability).
3. Merge with your current strategy score rather than replacing it.
4. Apply strict risk gates (max size, volatility filters, stop logic).
5. Log every decision with model inputs and final action reason.

## Minimal Decision Sketch

```python
# Pseudocode for safe signal fusion.
forecast_return = kronos_pred_return
forecast_confidence = kronos_confidence

kronos_score = max(0.0, min(1.0, 0.5 + (forecast_return * forecast_confidence)))
final_score = 0.65 * strategy_score + 0.35 * kronos_score

if prediction_age_minutes > max_age_minutes:
    final_score *= 0.5  # stale forecast penalty

if final_score >= buy_threshold and risk_ok:
    action = "BUY"
elif final_score <= sell_threshold:
    action = "SELL"
else:
    action = "HOLD"
```

## Who Should Use This Skill

Developers building local-first trading assistants or bots who want to augment existing strategy logic with an external forecasting model while keeping behavior explainable and controlled.

## Example Usage

```bash
pullnexus pull kronos-trading-integration
```

Then use `examples.jsonl` for prompt/fine-tune patterns and `eval.jsonl` to test whether your assistant gives safe, implementation-ready integration guidance.

## Notes

This skill intentionally documents integration patterns and validation habits instead of hard-coding one Kronos pipeline. Adapt the feature mapping to the exact Kronos output schema in your environment.

## License

CC0-1.0.
