# Model Selection Guide

**Which model should I run on my hardware?**

The most common question in local AI — and the one with the most scattered answers. This skill gives a structured decision framework: match your use case and hardware to the right model family and size.

---

## Step 1: Know Your Hardware Limits

| VRAM | RAM | What fits (GGUF Q4) |
|---|---|---|
| 4 GB | 8 GB | 3B–4B models (Phi-3 mini, Gemma 2 2B) |
| 6 GB | 16 GB | 7B models (Llama 3.1 8B, Mistral 7B, Qwen 2.5 7B) |
| 8 GB | 16 GB | 7B comfortably, 13B with offloading |
| 12 GB | 32 GB | 13B–14B comfortably, 34B with offloading |
| 16 GB | 32 GB | 34B comfortably |
| 24 GB | 64 GB | 34B fast, 70B with offloading |
| 48 GB+ | 128 GB | 70B+ comfortably |
| CPU only | 32 GB | 7B slowly (Q4) |

**Rule:** Fit the model fully in VRAM for fast inference. RAM offloading works but is 3–10x slower.

---

## Step 2: Match Model Size to Task Complexity

| Task | Minimum | Sweet spot |
|---|---|---|
| Simple Q&A, chat | 3B–7B | 7B |
| Code generation (simple) | 7B | 13B |
| Code generation (complex, multi-file) | 13B | 34B |
| Reasoning, math, logic | 13B | 34B–70B |
| Long document analysis | 7B (long context) | 13B+ |
| Agentic tool use | 13B | 34B+ |
| Creative writing | 7B | 13B |
| Local RAG | 7B | 7B (speed matters more than size here) |

**Rule:** Bigger isn't always better. A well-prompted 7B beats an unprompted 70B on structured tasks. See `prompt-engineering` and `small-model-reasoning-boost`.

---

## Step 3: Choose a Model Family

### Llama 3.x (Meta)
- **Best for:** General purpose, coding, instruction following
- **Strengths:** Excellent instruction tuning, widely supported, strong community
- **Variants:** 8B, 70B, 405B | Llama 3.3 (latest)
- **When to use:** Default choice when you're unsure

### Qwen 2.5 (Alibaba)
- **Best for:** Coding, multilingual, math
- **Strengths:** Exceptional coding quality at 7B–14B, strong math, 32K+ context
- **Variants:** 0.5B, 1.5B, 3B, 7B, 14B, 32B, 72B | Qwen2.5-Coder variants
- **When to use:** Coding tasks, non-English languages, math

### Mistral / Mixtral (Mistral AI)
- **Best for:** Fast inference, European language support
- **Strengths:** Efficient architecture, very fast at 7B, good instruction following
- **Variants:** Mistral 7B, Mixtral 8x7B (MoE), Mistral Small/Large
- **When to use:** Speed is a priority, European languages

### Gemma 2 (Google)
- **Best for:** Small device deployment, instruction tasks
- **Strengths:** Very capable at 2B–9B range, efficient
- **Variants:** 2B, 9B, 27B
- **When to use:** Limited hardware, need a capable small model

### Phi-3 / Phi-4 (Microsoft)
- **Best for:** Reasoning on tiny hardware
- **Strengths:** Exceptional reasoning per parameter, fits in 4GB VRAM
- **Variants:** Phi-3 mini (3.8B), Phi-3.5 (3.8B), Phi-4 (14B)
- **When to use:** Raspberry Pi, old laptops, CPU-only machines

### DeepSeek-R1 / V3
- **Best for:** Reasoning, math, complex logic
- **Strengths:** State-of-the-art reasoning, strong STEM performance
- **Variants:** 1.5B through 671B | distill variants available
- **When to use:** Hard reasoning tasks, math, scientific analysis

### Gemma 3 / Llama 3.2 Vision
- **Best for:** Vision tasks (image understanding)
- **Variants:** Gemma 3 (vision-capable), Llama 3.2 Vision 11B/90B
- **When to use:** Need to analyze images locally

---

## Step 4: Pick a Specific Recommendation

**"I have 8GB VRAM and want to code:"**
→ Qwen2.5-Coder-7B-Instruct (Q4_K_M via Ollama)

**"I have 8GB VRAM and want general assistant:"**
→ Llama-3.1-8B-Instruct (Q4_K_M)

**"I have 12GB VRAM and want the best coding model:"**
→ Qwen2.5-Coder-14B-Instruct (Q4_K_M)

**"I have 16GB VRAM and want complex reasoning:"**
→ DeepSeek-R1-Distill-Qwen-14B or Phi-4 (14B)

**"I have 24GB VRAM and want the best overall:"**
→ Llama-3.3-70B-Instruct (Q4_K_M with offloading) or Qwen2.5-72B

**"CPU only, 32GB RAM:"**
→ Phi-3-mini-4k-instruct (Q4) — fastest on CPU

**"I need vision (image analysis):"**
→ Llama-3.2-11B-Vision-Instruct or Gemma-3 (whichever fits your VRAM)

**"Fastest inference, don't care about size:"**
→ Mistral-7B or Gemma-2-9B

---

## Where to Find Models

- **Ollama library:** `ollama pull <model>` — easiest, pre-quantized
- **Hugging Face:** huggingface.co — search GGUF, pick a size that fits
- **LM Studio:** Built-in browser — search and download in one click
- **TheBloke / bartowski:** Reliable GGUF providers on HuggingFace

---

## VRAM Estimation Formula

Rough estimate for GGUF Q4:
```
VRAM (GB) ≈ (model_params_B × 0.5) + 1 GB overhead
```
- 7B model: ~4.5 GB
- 13B model: ~7.5 GB
- 34B model: ~19 GB
- 70B model: ~38 GB

For context: add ~0.5 GB per 4K tokens of context window in use.

---

## Pairs Well With

- `quantization-guide` — once you've picked a model, pick the right quant
- `small-model-reasoning-boost` — get more from your smaller model
- `env-8gb-vram-local-chat` / `env-apple-silicon-local-ai` — hardware-specific setup

---

## License

CC0-1.0 — public domain, free to use for any purpose.
