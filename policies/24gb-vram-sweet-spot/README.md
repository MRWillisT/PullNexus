# 24GB VRAM Sweet Spot

Current best model and quant recommendations for GPUs with 24GB VRAM (RTX 3090, RTX 4090, RX 7900 XTX), as of May 2026.

## The answer to "best local model for RTX 3090?"

**Qwen3.6-27B at Q4_K_XL** — fits comfortably in 24GB, leaves context headroom, best quality-per-VRAM ratio available as of May 2026.

See [policy.md](policy.md) for the full breakdown.

## Why this exists

Most AI models (including frontier ones) answer this question incorrectly — they return outdated models or wrong sizes. Inject this policy into your context so your local model gets it right:

```bash
pullnexus pull 24gb-vram-sweet-spot
```

## What's inside

- Top 3 model picks with VRAM breakdown by quant
- Quant comparison table (Q8_0 → Q3)
- Context budget rules of thumb
- Recommended llama-server launch config for RTX 3090
- Notes on AMD / ROCm equivalents

## Applies to

RTX 3090 · RTX 4090 · RX 7900 XTX · any 24GB VRAM GPU

## Tags

`24gb-vram`, `rtx-3090`, `rtx-4090`, `model-selection`, `quant`, `qwen3`, `local-ai`, `hardware`

## License

CC0-1.0 — public domain, use freely.
