# Quantization Guide

**Run bigger, better models in less VRAM by choosing the right quantization level.**

Quantization compresses model weights from 16-bit floats to lower-bit integers. You trade a small amount of quality for a large reduction in VRAM usage and often faster inference. Understanding the tradeoffs means you always run the best model your hardware can handle.

---

## The GGUF Format (llama.cpp / Ollama / LM Studio)

GGUF is the standard format for running quantized models locally. Quantization levels use a naming scheme like `Q4_K_M` — here's what each part means:

- **Q** = quantized
- **4** = bits per weight (2, 3, 4, 5, 6, 8)
- **_K** = K-quants (smarter per-layer quantization — prefer this over non-K variants)
- **_M / _S / _L** = Medium / Small / Large (which layers get finer quantization)

---

## Quantization Level Comparison

| Level | Bits/weight | VRAM vs F16 | Quality loss | Use when |
|---|---|---|---|---|
| `F16` | 16 | 100% (baseline) | None | You have plenty of VRAM, need max quality |
| `Q8_0` | 8 | ~50% | Negligible | High VRAM, want near-lossless with good speed |
| `Q6_K` | 6 | ~38% | Very small | Good balance of quality and size |
| `Q5_K_M` | 5 | ~31% | Small | Recommended if you can fit it |
| `Q4_K_M` | 4 | ~25% | Moderate | **Best default** — fits most hardware |
| `Q4_K_S` | 4 | ~23% | Moderate+ | Slightly smaller than Q4_K_M |
| `Q3_K_M` | 3 | ~19% | Noticeable | Only if Q4 doesn't fit |
| `Q2_K` | 2 | ~13% | Significant | Last resort — only for very limited VRAM |
| `IQ4_NL` / `IQ3_M` | ~4/~3 | Similar to Q4/Q3 | Often better than same-bit K | Newer importance-weighted quants — prefer over Q3/Q4 if available |

---

## Practical VRAM Table (Q4_K_M)

| Model size | Q4_K_M VRAM | Q5_K_M VRAM | Q8_0 VRAM |
|---|---|---|---|
| 3B | ~2.2 GB | ~2.7 GB | ~3.5 GB |
| 7B | ~4.5 GB | ~5.1 GB | ~7.5 GB |
| 13B | ~7.8 GB | ~9.0 GB | ~13.5 GB |
| 14B | ~8.5 GB | ~9.8 GB | ~14.5 GB |
| 34B | ~19 GB | ~22 GB | ~35 GB |
| 70B | ~38 GB | ~45 GB | ~70 GB |

---

## How to Choose

**Default recommendation: `Q4_K_M`**

It fits the widest range of hardware and quality loss is usually imperceptible for most tasks.

**Upgrade to `Q5_K_M` if:**
- You have ~15–20% extra VRAM headroom
- You're doing creative writing, nuanced reasoning, or coding where subtle quality matters
- Benchmarks for your specific model show notable improvement at Q5

**Use `Q6_K` or `Q8_0` if:**
- You're evaluating models and need a quality baseline
- You're fine-tuning and need high-quality activations
- VRAM is not a constraint

**Drop to `Q3_K_M` or `Q2_K` only if:**
- The model doesn't fit at Q4 — you'd rather run a Q4 of a smaller model

**Use IQ quants (`IQ4_NL`, `IQ3_M`) if:**
- They're available for your model — they often match Q5 quality at Q4 sizes

---

## Installing Quantized Models

### Ollama
```bash
# Browse Ollama library tags for quant levels
ollama pull llama3.1:8b-instruct-q4_K_M
ollama pull qwen2.5-coder:14b-instruct-q5_K_M
```

### From Hugging Face (GGUF)
```bash
# Find GGUF files on a model's HF page (usually in Files tab)
# Download just the file you need
wget https://huggingface.co/bartowski/Llama-3.1-8B-Instruct-GGUF/resolve/main/Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

### llama.cpp directly
```bash
./llama-server \
  -m models/Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  --n-gpu-layers 35 \
  --ctx-size 8192
```

### LM Studio
Use the built-in model browser — filter by quant level in the dropdown.

---

## The `--n-gpu-layers` Setting

When your model is larger than your VRAM, you can offload *some* layers to GPU and the rest to CPU RAM:

```bash
# Full GPU offload (all layers)
--n-gpu-layers 999

# Partial offload (experiment to find max that fits in VRAM)
--n-gpu-layers 20

# CPU only
--n-gpu-layers 0
```

Start high and reduce if you get CUDA out-of-memory errors. Each layer is roughly equal VRAM share.

---

## EXL2 Format (ExLlamaV2)

If you're using ExLlamaV2 or TabbyAPI instead of llama.cpp:
- EXL2 is their equivalent format with more granular bits-per-weight (e.g., `4.0`, `5.0`, `6.5`)
- Same tradeoffs apply: higher = better quality, more VRAM
- Not compatible with Ollama/llama.cpp

---

## Quick Recipes

**"I have 8GB VRAM and want a 7B model:"**
```
Llama-3.1-8B-Instruct-Q4_K_M (4.5 GB) ✓
Mistral-7B-Instruct-Q5_K_M (5.1 GB) ✓
```

**"I have 12GB VRAM and want a 13B model:"**
```
Qwen2.5-14B-Instruct-Q4_K_M (8.5 GB) ✓
```

**"I have 24GB VRAM and want a 34B model:"**
```
Llama-3.3-70B-Instruct-Q4_K_M (38 GB) ✗ — doesn't fit fully
CodeQwen-34B-Q4_K_M (19 GB) ✓
```

**"I only have 6GB VRAM:"**
```
Gemma-2-2B-Instruct-Q8_0 (2.8 GB) ✓ — high quality at small size
Llama-3.2-3B-Instruct-Q5_K_M (2.7 GB) ✓
```

---

## Pairs Well With

- `model-selection-guide` — pick the model family first, then the right quant
- `llama-cpp` — run GGUF models directly
- `ollama` — easiest way to pull pre-quantized models

---

## License

CC0-1.0 — public domain, free to use for any purpose.
