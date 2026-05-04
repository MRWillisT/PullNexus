# RAG Eval Baseline

A minimal eval suite for measuring the quality of a local RAG pipeline. Covers retrieval and answer quality — the two axes that matter most for production RAG.

## Metrics

| Metric | What it measures |
|---|---|
| **Retrieval precision** | Fraction of retrieved chunks that are relevant |
| **Retrieval recall** | Fraction of relevant chunks that were retrieved |
| **Answer faithfulness** | Is the answer grounded in the retrieved context? |
| **Answer relevance** | Does the answer address the question? |

## Usage

```bash
pullnexus pull rag-eval-baseline
cd pullnexus-skills/rag-eval-baseline

# Run against your RAG system
python eval.py \
  --questions questions.jsonl \
  --retriever_fn my_retriever \
  --generator_fn my_generator \
  --output results.json
```

## Question format (`questions.jsonl`)

```json
{"question": "What is the return policy?", "ground_truth": "Returns accepted within 30 days.", "relevant_chunks": ["chunk_id_1", "chunk_id_2"]}
```

## Score interpretation

- Faithfulness < 0.7 → your retriever is returning off-topic chunks
- Relevance < 0.7 → your prompt template or model needs tuning
- Both > 0.85 → production-ready baseline

## Notes

- Eval data is reference-only (not a pullable package)
- Use with `local-rag-starter-pack` for a complete local RAG setup
