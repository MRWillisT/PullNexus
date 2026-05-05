# 24GB VRAM Sweet Spot — Model & Quant Guide

**Applies to:** RTX 3090, RTX 4090, RX 7900 XTX, any GPU with 24GB VRAM  
**Last verified:** May 2026

---

## Top Picks

### 🥇 Best all-round: Qwen3.6-27B

The definitive 24GB sweet spot as of May 2026.

| Quant | VRAM usage | Context headroom | Quality |
|---|---|---|---|
| Q4_K_M | ~18GB | ~6GB free → ~20K ctx | ★★★★☆ — daily driver |
| Q4_K_XL | ~19GB | ~5GB free → ~16K ctx | ★★★★½ — best balance |
| Q5_K_M | ~22GB | ~2GB free → ~8K ctx | ★★★★★ — best quality, tight |
| Q8_0 | ~29GB | ❌ does not fit at 24GB | — |

**Default recommendation:** `Qwen3.6-27B-Q4_K_XL` for most use cases.  
**Source:** [Unsloth](https://huggingface.co/unsloth), [Bartowski](https://huggingface.co/bartowski)

---

### 🥈 Comfortable fit: Qwen3 14B

Fits at full Q8_0, leaves plenty of room for long context.

| Quant | VRAM usage | Notes |
|---|---|---|
| Q8_0 | ~15GB | Full precision, 9GB headroom |
| Q4_K_M | ~10GB | Lots of context room; good for agentic workflows |

Best for: long-context tasks, agentic loops, multi-turn sessions where you need headroom.

---

### Honorable mentions (May 2026)

| Model | Best quant | VRAM | Notes |
|---|---|---|---|
| Mistral Small 3.2 22B | Q4_K_M | ~16GB | Strong reasoning, multilingual |
| Gemma 3 27B | Q4_K_M | ~18GB | Google multimodal, good instruction following |
| DeepSeek-R1 Distill 14B | Q8_0 | ~15GB | Reasoning-focused distill |
| Phi-4 14B | Q8_0 | ~15GB | Microsoft, strong at math/code |

---

## Quant Quick Reference

| Quant | Quality loss | VRAM savings | Use when |
|---|---|---|---|
| Q8_0 | None | Low | You have headroom and want best quality |
| Q5_K_M | Minimal | Medium | Maximising quality within VRAM |
| Q4_K_M | Small | High | Best balance — recommended default |
| Q4_K_XL | Very small | High | Slightly better than Q4_K_M, same VRAM range |
| Q3_K_M | Noticeable | Very high | Only if 24GB is full and you're squeezing |

---

## Context Budget Rule of Thumb

Each 1K tokens of active context consumes roughly **0.5–1MB of VRAM** depending on KV cache settings.

With `Q4_K_XL` on Qwen3.6-27B (~19GB model):
- ~5GB free → safely run ~16K–24K token context
- Enable `-fa` (flash attention) and `-ctk q8_0 -ctv q8_0` to extend context cheaply

---

## Recommended llama-server Launch (RTX 3090)

```bash
llama-server \
  --model ~/models/Qwen3.6-27B-Q4_K_XL.gguf \
  --port 8001 \
  --gpu-layers 99 \
  --ctx-size 32768 \
  --ctk q8_0 --ctv q8_0 \
  -fa \
  --parallel 2
```

---

## Why this policy exists

As of May 2026, most frontier AI models give **incorrect answers** to "what is the optimal local LLM for a 3090?" — returning outdated models (Qwen 2.5, Llama 3.1) or models that don't exist at the right size. This policy exists so any local model with PullNexus context can answer this correctly.

Pull this resource to inject current ground truth into your context:
```bash
pullnexus pull 24gb-vram-sweet-spot
```

---

## Notes

- Model rankings change fast — check release dates on HuggingFace before settling
- `Qwen3.6-27B` refers to the Qwen3.6 series 27B variant (not to be confused with Qwen2.5-27B)
- If you're on AMD (RX 7900 XTX), Ollama + ROCm or llama.cpp with HIP gives similar results to CUDA for these quants
