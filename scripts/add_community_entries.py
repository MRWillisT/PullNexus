import json
import pathlib

path = pathlib.Path("skills/index.json")
idx = json.loads(path.read_text())

new_entries = [
    {
        "name": "qwen3-35b-12gb-llama-server",
        "resource_type": "template",
        "version": "1.0.0",
        "description": (
            "Optimized llama-server launch command for Qwen3.6-35B-A3B on 12GB VRAM. "
            "Uses Q4_K_XL GGUF, Unsloth dynamic quant, 8-bit KV cache (q8_0), flash attention, "
            "128K context window, and preserve_thinking chat template. Community-sourced config "
            "delivering fast TPS on consumer hardware."
        ),
        "tags": [
            "template", "llama.cpp", "llama-server", "qwen", "qwen3",
            "35b", "12gb-vram", "kv-cache", "flash-attention", "gguf",
            "quantization", "consumer-gpu", "use:template"
        ],
        "license": "CC0-1.0",
        "author": "Community (via @Michaelzsguo on X)",
        "source": "https://x.com/Michaelzsguo",
        "installable": False,
        "category": "inference",
        "maturity": "community",
        "maintained": "community",
        "last_verified": "2026-05-02",
        "hardware_requirements": {
            "vram_gb": 12,
            "quantization": "Q4_K_XL",
            "kv_cache": "q8_0"
        },
        "config_params": {
            "model": "Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf",
            "port": 8001,
            "alias": "qwen3.6-35b-a3b",
            "ctx_size": 131072,
            "n_predict": 32768,
            "no_context_shift": True,
            "temp": 0.6,
            "top_p": 0.95,
            "top_k": 20,
            "repeat_penalty": 1.0,
            "presence_penalty": 0.0,
            "flash_attn": True,
            "ctk": "q8_0",
            "ctv": "q8_0",
            "chat_template_kwargs": {"preserve_thinking": True}
        }
    },
    {
        "name": "kv-cache-vram-best-practices",
        "resource_type": "policy",
        "version": "1.0.0",
        "description": (
            "KV cache is the primary cause of VRAM OOM errors in llama.cpp, not weight quantization. "
            "Best practices: use q8_0 KV cache (--ctk q8_0 --ctv q8_0), cap context window aggressively, "
            "enable flash attention (-fa), and let the model fit+offload before tuning weight quant. "
            "Community-verified on 8-24GB VRAM setups."
        ),
        "tags": [
            "policy", "best-practices", "llama.cpp", "kv-cache", "vram",
            "oom", "quantization", "flash-attention", "consumer-gpu", "use:policy"
        ],
        "license": "CC0-1.0",
        "author": "Community (via @sakuray on X)",
        "source": "https://x.com/Michaelzsguo",
        "installable": False,
        "category": "inference",
        "maturity": "community",
        "maintained": "community",
        "last_verified": "2026-05-02",
        "key_rules": [
            "KV cache consumes VRAM proportional to context length x layers, not model size",
            "Use --ctk q8_0 --ctv q8_0 to store KV cache in 8-bit (halves KV VRAM vs fp16)",
            "Cap --c (ctx_size) to what you actually need -- 128K on 12GB will OOM without KV quant",
            "Enable flash attention (-fa) before adjusting weight quantization",
            "Use -fit to allow model to split across GPU/CPU when VRAM is tight",
            "Tune weight quant (Q4 vs Q5 vs Q8) only after KV and context are stable"
        ]
    }
]

idx["skills"].extend(new_entries)
idx["total"] = len(idx["skills"])
idx["updated"] = "2026-05-02"

path.write_text(json.dumps(idx, indent=2))

by_type = {}
for s in idx["skills"]:
    t = s.get("resource_type", "unknown")
    by_type[t] = by_type.get(t, 0) + 1

print(f"Added {len(new_entries)} entries. New total: {idx['total']}")
for k, v in sorted(by_type.items()):
    print(f"  {k}: {v}")
