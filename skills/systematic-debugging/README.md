# systematic-debugging

A structured debugging skill that teaches a model to work through complex issues using hypotheses, targeted instrumentation, and evidence-driven iteration — instead of random trial-and-error.

## What it teaches

- Form a specific hypothesis before touching any code
- Instrument strategically: add logging/assertions at the narrowest useful point
- Interpret evidence and revise the hypothesis if it doesn't fit
- Distinguish symptoms from root causes
- Know when to escalate vs. keep digging

## When to use

- Intermittent or hard-to-reproduce bugs
- Performance degradation with no obvious cause
- Regressions where the root cause isn't obvious from the diff
- Multi-layer issues (network + app + DB)

## Example invocations

```
My API is returning 500s intermittently but I can't reproduce it locally.
The app was fast yesterday and slow today — no deploys changed.
This worked in staging but fails in production with no clear error.
```

## Format

ShareGPT JSONL — 7 conversation pairs covering common debugging scenarios across different stacks and failure modes.

## Tags

`debugging`, `diagnostics`, `troubleshooting`, `development`

## License

See `skill.json` for license details.
