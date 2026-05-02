"""
Generate individual tool entries for all 68 repos from the open-source-ai-toolbox-2026 list.
Creates skills/<name>/skill.json for each and updates skills/index.json.
Run from repo root: python scripts/add_toolbox_entries.py
"""

import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
INDEX_PATH = SKILLS_DIR / "index.json"
TODAY = str(date.today())

# ---------------------------------------------------------------------------
# Tool definitions — (name, stars_k, repo, license, description, tags, category)
# ---------------------------------------------------------------------------
TOOLS = [
    # 01 — LLM Inference
    ("ollama", 98, "ollama/ollama", "MIT",
     "Run Llama, Mistral, Qwen, Gemma locally with one command. GPU acceleration, REST API, OpenAI-compatible endpoints. The fastest way to get a model running on your machine.",
     ["inference", "local-ai", "ollama", "gpu", "openai-compatible", "use:developer"], "inference"),

    ("llama-cpp", 72, "ggml-org/llama.cpp", "MIT",
     "LLM inference in pure C++. Runs on CPU, GPU, Apple Silicon. The engine behind most local AI tools. Extremely fast, low memory usage.",
     ["inference", "c++", "cpu", "gpu", "apple-silicon", "local-ai", "use:developer"], "inference"),

    ("vllm", 44, "vllm-project/vllm", "Apache-2.0",
     "High-throughput LLM serving engine for production. Continuous batching, paged attention, OpenAI-compatible API. The standard for deploying models at scale.",
     ["inference", "serving", "production", "openai-compatible", "batching", "use:developer"], "inference"),

    ("lm-studio", 28, "lmstudio-ai/lmstudio.js", "MIT",
     "Desktop app for running local LLMs with a clean UI. Download models from Hugging Face, run locally, get an OpenAI-compatible local server. Best onboarding for non-developers.",
     ["inference", "desktop", "local-ai", "ui", "openai-compatible", "use:beginner"], "inference"),

    ("jan", 26, "janhq/jan", "AGPL-3.0",
     "Open-source ChatGPT alternative that runs 100% offline. Clean UI, model management, local API server. Works on Mac, Windows, Linux. No data leaves your machine.",
     ["inference", "offline", "local-ai", "ui", "privacy", "use:beginner"], "inference"),

    ("text-generation-webui", 42, "oobabooga/text-generation-webui", "AGPL-3.0",
     "The Swiss Army knife for local LLMs. Supports every model format, every backend, every sampler. Character mode, notebook mode, API mode. The most feature-complete local UI.",
     ["inference", "ui", "local-ai", "gguf", "character-mode", "use:developer"], "inference"),

    ("localai", 26, "mudler/LocalAI", "MIT",
     "Self-hosted OpenAI drop-in replacement. Same API, local models. Swap Claude/GPT with local LLMs in any app without changing a single line of code.",
     ["inference", "openai-compatible", "self-hosted", "local-ai", "api", "use:developer"], "inference"),

    # 02 — RAG & Knowledge
    ("langchain", 98, "langchain-ai/langchain", "MIT",
     "The most popular LLM framework. Chains, agents, retrievers, memory. Connects LLMs to any data source or tool. Massive ecosystem of integrations.",
     ["rag", "framework", "agents", "retrieval", "memory", "integrations", "use:developer"], "rag"),

    ("llamaindex", 38, "run-llama/llama_index", "MIT",
     "Data framework for LLM applications. Index any data source — PDF, SQL, Notion, Slack — and query it with natural language. Best-in-class for pure RAG use cases.",
     ["rag", "indexing", "retrieval", "pdf", "sql", "framework", "use:developer"], "rag"),

    ("rag-anything", 12, "HKUDS/RAG-Anything", "MIT",
     "Multimodal RAG for any LLM. Handles text, tables, images, charts, graphs — not just PDFs. 6 lines to set up. Used in production by serious teams.",
     ["rag", "multimodal", "tables", "images", "local-ai", "use:developer"], "rag"),

    ("chroma", 16, "chroma-core/chroma", "Apache-2.0",
     "The open-source vector database. Store embeddings, search by similarity, filter by metadata. Runs in-memory or persistent. The simplest way to add semantic search to any project.",
     ["vector-db", "embeddings", "semantic-search", "rag", "use:developer"], "rag"),

    ("weaviate", 12, "weaviate/weaviate", "BSD-3-Clause",
     "Vector database with built-in ML models. Hybrid search, multi-tenancy, real-time updates. Production-ready, scales to billions of objects.",
     ["vector-db", "embeddings", "hybrid-search", "production", "rag", "use:developer"], "rag"),

    ("haystack", 18, "deepset-ai/haystack", "Apache-2.0",
     "End-to-end NLP framework for RAG pipelines. Modular, production-ready, works with any LLM or vector DB. The most mature RAG framework available.",
     ["rag", "nlp", "pipeline", "framework", "production", "use:developer"], "rag"),

    ("docling", 22, "DS4SD/docling", "MIT",
     "Convert documents to structured Markdown for AI. Handles PDFs with tables, figures, formulas — not just plain text extraction. Built by IBM Research.",
     ["pdf", "document-parsing", "markdown", "rag", "data-prep", "use:developer"], "data-prep"),

    # 03 — AI Agents
    ("autogen", 40, "microsoft/autogen", "MIT",
     "Multi-agent conversation framework by Microsoft. Agents talk to each other, delegate tasks, write and execute code. The most powerful framework for complex agentic workflows.",
     ["agents", "multi-agent", "code-execution", "microsoft", "use:developer"], "agents"),

    ("crewai", 28, "crewAIInc/crewAI", "MIT",
     "Orchestrate role-playing AI agents. Define a crew, assign roles, set goals — agents collaborate like a team. Easiest way to build multi-agent systems that actually work.",
     ["agents", "multi-agent", "roles", "orchestration", "use:developer"], "agents"),

    ("langgraph", 10, "langchain-ai/langgraph", "MIT",
     "Build stateful multi-agent workflows as graphs. Nodes are agents or functions, edges are transitions. Handles complex logic, loops, human-in-the-loop. The production-grade agent framework.",
     ["agents", "graph", "stateful", "multi-agent", "human-in-the-loop", "use:developer"], "agents"),

    ("agno", 22, "agno-agi/agno", "Apache-2.0",
     "Build fast multi-modal AI agents. Supports any LLM, any tool, memory, knowledge, storage. 10x faster than LangChain for simple agents. Clean API, excellent documentation.",
     ["agents", "multi-modal", "memory", "fast", "use:developer"], "agents"),

    ("smolagents", 14, "huggingface/smolagents", "Apache-2.0",
     "Minimal agent framework by Hugging Face. Code agents that write and execute Python to solve tasks. Incredibly simple — 1000 lines of code total. The anti-LangChain.",
     ["agents", "code-agents", "huggingface", "minimal", "python", "use:developer"], "agents"),

    ("openhands", 48, "All-Hands-AI/OpenHands", "MIT",
     "Open-source Devin alternative. AI software engineer that writes code, runs tests, fixes bugs, deploys. Works with Claude, GPT-4, local models. The most capable coding agent.",
     ["agents", "coding-agent", "software-engineer", "code-execution", "use:developer"], "agents"),

    ("superagi", 16, "TransformerOptimus/SuperAGI", "MIT",
     "Self-hosted autonomous AI agent infrastructure. Agent marketplace, performance telemetry, concurrent agents, graphical UI. Run multiple agents in parallel on your own server.",
     ["agents", "autonomous", "self-hosted", "parallel", "ui", "use:developer"], "agents"),

    # 04 — Prompts & Evals
    ("dspy", 22, "stanfordnlp/dspy", "MIT",
     "Programming — not prompting — LLMs. Define what you want, DSPy optimizes the prompts automatically. From Stanford NLP. Replaces manual prompt engineering with systematic optimization.",
     ["evals", "prompting", "optimization", "stanford", "structured-output", "use:developer"], "evals"),

    ("guidance", 20, "guidance-ai/guidance", "MIT",
     "Control LLM output structure with code. Interleave generation with logic, force JSON schemas, constrain outputs. When you need the model to output exactly what you need.",
     ["evals", "structured-output", "constrained-generation", "json", "use:developer"], "evals"),

    ("outlines", 11, "dottxt-ai/outlines", "Apache-2.0",
     "Structured text generation. Force models to output valid JSON, regex patterns, specific formats. Zero prompt engineering needed — guaranteed output structure.",
     ["structured-output", "json", "regex", "constrained-generation", "use:developer"], "evals"),

    ("promptfoo", 6, "promptfoo/promptfoo", "MIT",
     "Test and eval your prompts. Run automated tests, compare models, catch regressions. Like unit tests but for AI. Essential before shipping anything to production.",
     ["evals", "testing", "prompts", "regression", "ci", "use:developer"], "evals"),

    ("braintrust", 3, "braintrustdata/braintrust-sdk", "MIT",
     "Eval framework for LLM apps. Track quality across model versions, prompts, and configurations. Because vibes aren't a metric.",
     ["evals", "quality", "tracking", "versioning", "use:developer"], "evals"),

    ("instructor", 9, "instructor-ai/instructor", "MIT",
     "Structured outputs from LLMs using Pydantic. Define a schema, get back a validated Python object. Works with OpenAI, Anthropic, Google, local models. The cleanest structured output solution.",
     ["structured-output", "pydantic", "validation", "python", "use:developer"], "evals"),

    # 05 — Fine-tuning
    ("unsloth", 24, "unslothai/unsloth", "Apache-2.0",
     "Fine-tune LLMs 2x faster with 80% less memory. Supports Llama, Mistral, Qwen, Gemma. Runs on a single GPU. The only fine-tuning library you need if you're resource-constrained.",
     ["fine-tuning", "lora", "qlora", "gpu", "memory-efficient", "use:developer"], "fine-tuning"),

    ("axolotl", 8, "axolotl-org/axolotl", "Apache-2.0",
     "Streamlined fine-tuning for LLMs. YAML config, every dataset format, every training technique. The ops layer on top of Hugging Face Transformers. Used by most serious fine-tuners.",
     ["fine-tuning", "yaml", "lora", "qlora", "huggingface", "use:developer"], "fine-tuning"),

    ("llama-factory", 40, "hiyouga/LLaMA-Factory", "Apache-2.0",
     "Fine-tune 100+ LLMs with zero code. Web UI, supports LoRA, QLoRA, full fine-tuning. The most user-friendly fine-tuning tool available.",
     ["fine-tuning", "lora", "qlora", "ui", "no-code", "use:beginner"], "fine-tuning"),

    ("trl", 12, "huggingface/trl", "Apache-2.0",
     "Transformer Reinforcement Learning. RLHF, DPO, PPO — the techniques used to align GPT-4 and Claude. By Hugging Face. For training models to do what you actually want.",
     ["fine-tuning", "rlhf", "dpo", "ppo", "alignment", "huggingface", "use:developer"], "fine-tuning"),

    ("torchtune", 5, "pytorch/torchtune", "BSD-3-Clause",
     "PyTorch-native fine-tuning library from Meta. Simple, hackable, well-documented. The reference implementation for fine-tuning in pure PyTorch.",
     ["fine-tuning", "pytorch", "meta", "lora", "use:developer"], "fine-tuning"),

    ("mergekit", 4, "arcee-ai/mergekit", "LGPL-3.0",
     "Merge multiple fine-tuned models into one. SLERP, TIES, DARE, linear merge — all the techniques. No GPU needed for merging. Create models that outperform their parents.",
     ["fine-tuning", "model-merging", "slerp", "ties", "dare", "use:developer"], "fine-tuning"),

    # 06 — Tools & Context
    ("markitdown", 38, "microsoft/markitdown", "MIT",
     "Convert any file to Markdown. PDF, Word, Excel, PowerPoint, images, audio. Feeds clean structured text to your LLM instead of garbage. By Microsoft.",
     ["data-prep", "pdf", "markdown", "conversion", "microsoft", "use:developer"], "data-prep"),

    ("files-to-prompt", 3, "simonw/files-to-prompt", "Apache-2.0",
     "Turn your entire codebase into one prompt. Respects .gitignore, recursive, filterable. By Simon Willison. The simplest tool for feeding projects to Claude.",
     ["context", "codebase", "prompt", "cli", "use:developer"], "tools"),

    ("crawl4ai", 30, "unclecode/crawl4ai", "Apache-2.0",
     "Web scraping for AI. Extracts clean Markdown from any URL, handles JS-heavy sites, structured data extraction. The web data layer for any AI pipeline.",
     ["web-scraping", "markdown", "data-prep", "crawler", "use:developer"], "tools"),

    ("firecrawl", 25, "mendableai/firecrawl", "AGPL-3.0",
     "Turn any website into LLM-ready data. Full site crawling, structured extraction, clean Markdown output. The production-grade web scraper for AI apps.",
     ["web-scraping", "markdown", "data-prep", "production", "use:developer"], "tools"),

    ("playwright-mcp", 31, "microsoft/playwright-mcp", "MIT",
     "Give Claude a real browser. Navigate, click, screenshot, read dynamic content. Analyze any site in 30 seconds. The most powerful MCP server for web tasks.",
     ["mcp", "browser", "playwright", "automation", "claude", "use:developer"], "tools"),

    ("model-context-protocol", 11, "anthropics/model-context-protocol", "MIT",
     "The standard for connecting Claude to external tools. Official Anthropic MCP spec. Plug in any API, database, service. Hundreds of servers in the ecosystem.",
     ["mcp", "protocol", "anthropic", "integrations", "use:developer"], "tools"),

    ("awesome-mcp-servers", 27, "punkpeye/awesome-mcp-servers", "MIT",
     "500+ ready-made MCP servers. GitHub, Slack, Notion, databases, browsers, finance. Every integration you'll ever need in one catalog.",
     ["mcp", "catalog", "integrations", "github", "databases", "use:developer"], "tools"),

    ("n8n", 47, "n8n-io/n8n", "Sustainable-Use-1.0",
     "Self-hosted workflow automation with 400+ integrations. Connect LLMs to any app, trigger AI workflows on schedules or webhooks, run custom JS/Python in nodes. Replaces $50K/year Zapier.",
     ["automation", "workflow", "integrations", "self-hosted", "llm", "use:developer"], "automation"),

    # 07 — Deployment
    ("litellm", 16, "BerriAI/litellm", "MIT",
     "One API for 100+ LLMs. OpenAI format, works with Claude, GPT, Gemini, local models. Load balancing, fallbacks, cost tracking. The proxy layer between your app and every LLM provider.",
     ["deployment", "proxy", "openai-compatible", "load-balancing", "cost-tracking", "use:developer"], "deployment"),

    ("bentoml", 7, "bentoml/BentoML", "Apache-2.0",
     "Build and deploy AI services. Package models, create APIs, deploy anywhere. From local testing to production Kubernetes. The MLOps layer that doesn't require a DevOps team.",
     ["deployment", "mlops", "kubernetes", "api", "use:developer"], "deployment"),

    ("ray-serve", 34, "ray-project/ray", "Apache-2.0",
     "Distributed AI inference at scale. Serve multiple models, autoscale, handle millions of requests. Used by OpenAI, Anyscale, production AI companies.",
     ["deployment", "distributed", "inference", "autoscaling", "production", "use:developer"], "deployment"),

    ("triton-inference-server", 8, "triton-inference-server/server", "BSD-3-Clause",
     "NVIDIA's production inference server. Maximum GPU utilization, dynamic batching, multi-model serving. The standard for GPU inference in enterprise.",
     ["deployment", "inference", "gpu", "nvidia", "enterprise", "use:developer"], "deployment"),

    ("lorax", 3, "predibase/lorax", "Apache-2.0",
     "Serve hundreds of LoRA fine-tuned models on one GPU. One base model, hundreds of adapters loaded dynamically. 10x cost reduction for serving fine-tuned models.",
     ["deployment", "lora", "serving", "gpu", "fine-tuning", "use:developer"], "deployment"),

    ("supabase", 73, "supabase/supabase", "Apache-2.0",
     "The default backend for AI applications. Open-source Firebase alternative built on Postgres. Real-time database, auth, storage, edge functions, vector search. Replaces Firebase + Auth0.",
     ["backend", "database", "vector-db", "postgres", "auth", "use:developer"], "deployment"),

    # 08 — Claude-specific
    ("claude-code-skills", 0, "anthropics/claude-code-skills", "MIT",
     "Official Anthropic skills framework. SKILL.md patterns that teach Claude to handle documents, automations, and workflows without errors. The foundation of how Claude Code handles complex tasks.",
     ["claude", "skills", "anthropic", "vscode-skill", "use:developer"], "claude"),

    ("free-claude-code", 2, "Alishahryar1/free-claude-code", "MIT",
     "Run Claude Code completely free via GitHub Models API. Step-by-step guide and setup scripts. $0, forever.",
     ["claude", "free", "github-models", "cli", "use:beginner"], "claude"),

    ("claude-mem", 1, "thedotmack/claude-mem", "MIT",
     "Persistent memory for Claude. Auto-captures everything Claude does across sessions. Claude remembers who you are and what you're working on.",
     ["claude", "memory", "persistence", "context", "use:developer"], "claude"),

    # 09 — Data Prep
    ("unstructured", 10, "Unstructured-IO/unstructured", "Apache-2.0",
     "Extract and transform unstructured data for LLMs. PDFs, HTML, Word, images, emails — all parsed into clean chunks ready for RAG. The data layer most AI pipelines are missing.",
     ["data-prep", "pdf", "html", "rag", "extraction", "use:developer"], "data-prep"),

    ("datatrove", 3, "huggingface/datatrove", "MIT",
     "Large-scale data processing for LLM training by Hugging Face. Process terabytes of text with deduplication, quality filtering, and content classification. What the big labs use.",
     ["data-prep", "training", "deduplication", "filtering", "scale", "use:developer"], "data-prep"),

    ("trafilatura", 3, "adbar/trafilatura", "Apache-2.0",
     "Web content extraction for AI. Strips boilerplate, keeps content, outputs clean text or Markdown. The best single-page web extractor for feeding text to models.",
     ["data-prep", "web-scraping", "markdown", "extraction", "use:developer"], "data-prep"),

    ("semchunk", 1, "umarbutler/semchunk", "MIT",
     "Semantic text chunking for RAG. Splits text at natural boundaries instead of arbitrary token counts. Better chunks → better retrieval → better answers.",
     ["data-prep", "rag", "chunking", "semantic", "retrieval", "use:developer"], "data-prep"),

    ("datachain", 2, "iterative/datachain", "Apache-2.0",
     "AI-native dataset management. Version, query, and transform multimodal datasets. Works with images, video, text, embeddings. Built for LLM training workflows.",
     ["data-prep", "dataset", "versioning", "multimodal", "training", "use:developer"], "data-prep"),

    # 10 — Vision & Multimodal
    ("moondream", 10, "vikhyat/moondream", "Apache-2.0",
     "Tiny vision language model that runs anywhere. 1.6B parameters. Describe images, answer visual questions, detect objects. Runs on a Raspberry Pi. The smallest useful vision model.",
     ["vision", "vlm", "multimodal", "local-ai", "edge", "use:developer"], "vision"),

    ("internvl", 7, "OpenGVLab/InternVL", "MIT",
     "State-of-the-art open-source vision model. Matches GPT-4V on most benchmarks. Understand images, charts, documents, screenshots. The open alternative to Claude's vision.",
     ["vision", "vlm", "multimodal", "gpt4v", "use:developer"], "vision"),

    ("whisper", 74, "openai/whisper", "MIT",
     "Open-source speech recognition by OpenAI. Transcribes audio in 99 languages. Runs locally, handles accents, background noise, technical jargon. Feed audio to your LLM pipeline.",
     ["vision", "speech", "transcription", "audio", "local-ai", "use:developer"], "vision"),

    ("insanely-fast-whisper", 8, "Vaibhavs10/insanely-fast-whisper", "MIT",
     "Whisper but 10-20x faster. One command, automatic GPU optimization, batch processing. Transcribe a 2-hour podcast in 2 minutes on consumer hardware.",
     ["vision", "speech", "transcription", "audio", "gpu", "fast", "use:developer"], "vision"),

    ("stable-diffusion-webui", 143, "AUTOMATIC1111/stable-diffusion-webui", "AGPL-3.0",
     "The browser interface for Stable Diffusion. Generate, edit, upscale images from text. 143K stars. Hundreds of extensions, ControlNet, inpainting. Runs on your GPU.",
     ["vision", "image-generation", "stable-diffusion", "gpu", "ui", "use:beginner"], "vision"),
]


def make_entry(name, stars_k, repo, license_, desc, tags, category):
    return {
        "name": name,
        "resource_type": "tool",
        "version": "1.0.0",
        "description": desc,
        "tags": tags,
        "license": license_,
        "author": repo.split("/")[0],
        "source": f"https://github.com/{repo}",
        "repo": repo,
        "github_stars_k": stars_k,
        "mcp_compatible": "mcp" in tags,
        "installable": False,
        "category": category,
        "maturity": "stable" if stars_k >= 5 else "beta",
        "maintained": "yes",
        "last_verified": TODAY,
    }


def main():
    # Load existing index
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    existing_names = {s["name"] for s in index["skills"]}

    new_entries = []
    skipped = []

    for tool in TOOLS:
        name = tool[0]
        if name in existing_names:
            skipped.append(name)
            continue

        entry = make_entry(*tool)
        new_entries.append(entry)

        # Create skill.json in skills/<name>/
        skill_dir = SKILLS_DIR / name
        skill_dir.mkdir(exist_ok=True)
        skill_json = skill_dir / "skill.json"
        skill_json.write_text(json.dumps(entry, indent=2), encoding="utf-8")
        print(f"  ✓ {name}")

    # Prepend new entries after the first 4 (n8n-mcp-tool, local-rag-starter-pack, rag-eval-baseline, synthetic-training-datasets)
    # Group by category for readability
    index["skills"] = index["skills"][:4] + new_entries + index["skills"][4:]
    index["total"] = len(index["skills"])
    index["updated"] = TODAY

    INDEX_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")

    print(f"\nAdded {len(new_entries)} entries. Skipped {len(skipped)} (already exist): {skipped}")
    print(f"Total index entries: {index['total']}")


if __name__ == "__main__":
    main()
