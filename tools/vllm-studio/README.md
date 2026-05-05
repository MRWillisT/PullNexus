# vLLM Studio

Unified local AI control panel for model lifecycle, chat/agent workflows, orchestration, observability, and remote deployment. Supports vLLM, SGLang, llama.cpp, and exllamaV3 from a single interface.

**GitHub:** [0xSero/vllm-studio](https://github.com/0xSero/vllm-studio) · **License:** Apache-2.0

## What it does

- Manage model loading/unloading and lifecycle across backends from a web UI
- Run chat and agent workflows with session state and prompt management
- Proxy OpenAI-compatible requests to any backend (vLLM, SGLang, llama.cpp, exllamaV3)
- Monitor GPU/VRAM usage, active runs, and backend health in a dashboard
- Deploy controller as a background daemon or full Docker stack

## Supported backends

| Backend | Notes |
|---|---|
| **vLLM** | Full lifecycle + hot swap |
| **SGLang** | Structured generation |
| **llama.cpp** | CPU + GPU via llama-server |
| **exllamaV3** | Fast GPTQ/EXL2 inference |

## Quick start

```bash
# Full stack with Docker
docker compose up -d --build controller frontend

# Or run controller locally
cd controller && bun src/main.ts
cd frontend && npm run dev

# Controller as background daemon
./scripts/daemon-start.sh
./scripts/daemon-status.sh
./scripts/daemon-stop.sh
```

## Endpoints

- UI: `http://localhost:3000`
- API: `http://localhost:8080/api/docs`
- Health: `http://localhost:8080/health`

## When to use instead of Ollama/LM Studio

- You need to switch between multiple inference backends without reconfiguring clients
- You want a self-hosted alternative to LM Studio with vLLM/SGLang support
- You need orchestration and observability beyond a basic chat UI
- You're running a team or shared inference server
