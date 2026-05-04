# Small Model Guidance Tuning

Playbook for making a small local model noticeably smarter with PullNexus before you spend time on fine-tuning.

## What this solves

Small models often fail in a specific pattern:

- They pick the wrong retrieved resource.
- They latch onto the right resource but turn it into fake-certainty code.
- They flatten everything into a wall of text.
- They sound more helpful than they actually are.

This playbook is about fixing that behavior in layers.

## Core lesson

Use PullNexus to improve routing and context selection.

Then tune the assistant so retrieved guidance is treated as:

- relevant problem-solving context
- a source of candidate tools and architectures
- a reason to be more on-topic

Not as:

- guaranteed API truth
- exact package syntax
- a license to invent implementation details

## Tuning order

1. **Fix retrieval relevance first**
   - Add token-aware matching and stopword filtering.
   - Weight problem terms like `rag`, `retrieval`, `chunking`, `embedding`, `install`, and `inspect`.
   - Verify the top-ranked resource is actually the one a human would choose.

2. **Separate routing from answer quality**
   - A better retrieved skill does not automatically mean a better final answer.
   - Treat "picked the right resource" and "answered well" as two different checks.

3. **Tune the prompt contract**
   - Tell the model to diagnose the user's failure first.
   - Tell it to recommend a concrete stack second.
   - Tell it to avoid invented APIs when uncertain.
   - Tell it to prefer high-confidence architecture advice over speculative code.

4. **Tune display formatting separately**
   - Rendering bugs can make a decent answer look worse than it is.
   - Preserve blank lines, bullets, and numbered steps.
   - Add runtime instructions for short openers, short paragraphs, and readable lists.

5. **Run a fixed before/after eval prompt**
   - Keep one prompt constant and compare:
   - base model without PullNexus
   - model with PullNexus retrieval only
   - model with PullNexus plus prompt-contract tuning

## Practical rules for small models

- Use retrieval for current facts.
- Use prompt instructions for behavior and formatting.
- Use fine-tuning only after you have repeatable failure cases.
- Prefer a narrow trustworthy answer over a flashy long answer.
- If the model is uncertain about an exact API, it should say so.

## Example eval prompt

```text
I'm building a fully local RAG pipeline for PDFs with Ollama. Retrieval quality is bad, chunking feels wrong, and I want something concrete I can inspect or install. What should I use?
```

This folder also includes `eval.jsonl` with three compact checks:

- the baseline RAG prompt
- the same prompt with PullNexus guidance enabled
- a diagnosis prompt that separates retrieval quality from model tuning quality

## What good looks like

A better answer should:

- retrieve a relevant PullNexus resource like `local-rag-starter-pack`
- stay focused on local RAG instead of drifting into unrelated tools
- recommend concrete components such as document parsing, chunking, embeddings, vector store, and eval
- avoid pretending uncertain example code is authoritative
- remain readable on a small screen

## When to actually fine-tune

Fine-tune only if the same bad behavior survives after:

- better retrieval ranking
- better system prompt and skill injection rules
- better formatting instructions
- a small eval set with repeated checks

If runtime tuning fixes the issue, that is usually the cheaper and safer solution.