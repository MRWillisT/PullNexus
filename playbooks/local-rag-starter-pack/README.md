# Local RAG Starter Pack

A step-by-step playbook for deploying a fully local Retrieval-Augmented Generation (RAG) pipeline — no cloud APIs required.

## What's covered

1. **Document ingestion** — PDF, Markdown, plain text via LangChain loaders or LlamaIndex
2. **Chunking strategy** — fixed-size vs semantic chunking, overlap tuning
3. **Embedding model selection** — `nomic-embed-text`, `mxbai-embed-large`, `bge-m3` via Ollama
4. **Vector DB setup** — Chroma (local file) or Weaviate (Docker)
5. **Retrieval** — similarity search, MMR, hybrid BM25 + vector
6. **Reranking** — cross-encoder reranker to improve precision
7. **Answer quality eval** — faithfulness + relevance scoring via `rag-eval-baseline`

## Minimum stack

```
Ollama >= 0.3
Python >= 3.10
langchain-community
chromadb  (or weaviate-client for Weaviate)
sentence-transformers  (for reranking)
```

## Quick start

```bash
# Pull embedding model
ollama pull nomic-embed-text

# Install deps
pip install langchain-community chromadb sentence-transformers

# Ingest docs
python ingest.py --source ./docs --db ./chroma_db

# Query
python query.py "What is the return policy?"
```

## Compatibility notes

- GPU <8GB VRAM: use quantized models (Q4_K_M) and avoid running embedding + generation simultaneously
- Chroma works out of the box; Weaviate requires Docker
- See `rag-eval-baseline` to measure retrieval + answer quality
