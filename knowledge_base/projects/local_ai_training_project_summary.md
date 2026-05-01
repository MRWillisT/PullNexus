# Local AI Training Project Summary

## Goal

Build a useful local AI assistant that can help with coding projects, explain decisions, use tools safely, and work with the user's preferred self-taught workflow.

## Current Assets

- Real converted chat exports.
- Synthetic training examples.
- Autonomous-agent ShareGPT and ChatML examples.
- Train/validation/test split scripts.
- System prompts for coder, reviewer, and orchestrator roles.
- Starter guides for Ollama and local fine-tuning.

## Main Risks

- Domain skew toward trading, NEXRAD weather radar, PyQt6, and Python.
- Empty or thin retrieval knowledge base.
- Possible overfitting if the dataset is trained too many epochs.
- Hallucination risk if uncertainty examples are underweighted.

## Recommended Next Step

Build a retrieval index from current docs and project notes before doing heavy fine-tuning.
