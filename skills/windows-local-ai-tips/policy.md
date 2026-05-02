# Windows Local AI Tips

## Core Commands

| Command | Purpose |
|---|---|
| `py -3` | Run Python when `python` is not on PATH |
| `nvidia-smi` | Confirm GPU driver and VRAM visibility |
| `ollama run <model>` | Run a local model interactively |
| `ollama create <name>` | Create an Ollama model from a Modelfile |
| `ollama list` | See all locally pulled models |
| `ollama ps` | Check what is currently loaded into VRAM |
| `rg <pattern>` | Fast text and file search (ripgrep) |

## Safety Habits

- Preview file lists before any cleanup operation.
- Avoid recursive delete (`rm -r`, `Remove-Item -Recurse`) unless the target path is confirmed.
- Prefer PowerShell-native commands — `Get-ChildItem`, `Select-String`, `Where-Object` — over Unix shortcuts.
- Keep raw exports separate from cleaned training data.
- Use `nvidia-smi` before loading large models to confirm available VRAM.

## Common Pitfalls

- `python` may not work — use `py -3` or the full venv path.
- Paths with spaces need quoting in PowerShell: `"C:\My Folder\model.gguf"`.
- Ollama loads models lazily — a model that lists fine may OOM at inference if VRAM is split with other processes.
- PowerShell single-quote strings are literal — no variable expansion. Use double quotes.

## Quick VRAM Check

```powershell
nvidia-smi --query-gpu=memory.used,memory.free --format=csv
```

## Pairs Well With

- `local-agent-system-blueprint` — system design overview
- `kv-cache-vram-best-practices` — tune KV cache for your VRAM budget
