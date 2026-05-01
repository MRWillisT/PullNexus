# Copilot Export Organization Guide

Short answer: **yes, separate them**.  
One giant folder gets messy fast and hurts retrieval quality.

## Recommended Folder Layout

Use this structure:

- `knowledge_base/chats_raw/`
- `knowledge_base/chats_clean/`
- `knowledge_base/projects/`
- `knowledge_base/agent_system/`
- `knowledge_base/tools/`
- `knowledge_base/skills/`
- `knowledge_base/notes_useful_info/`
- `knowledge_base/index/`

## What Goes Where

- `chats_raw/`
  - untouched exports exactly as downloaded
- `chats_clean/`
  - normalized/transformed versions for training or retrieval
- `projects/`
  - project-specific context, decisions, architecture notes
- `agent_system/`
  - orchestrator logic, memory schemas, runtime policies
- `tools/`
  - tool docs, command recipes, safe/unsafe command rules
- `skills/`
  - reusable playbooks/prompts for specialist roles
- `notes_useful_info/`
  - ad hoc insights, learnings, TODO research items
- `index/`
  - manifests, embeddings index metadata, search catalogs

## Practical Rules

- Keep **raw exports immutable**.
- Put each major project in its own subfolder under `projects/`.
- Add a small `manifest.json` in each folder with:
  - source
  - date range
  - tags
  - quality score
- Use consistent names like:
  - `2026-04_project-alpha_chat-export_001.jsonl`

## Why This Helps

- Better retrieval precision.
- Easier incremental updates.
- Cleaner training/eval splits.
- Faster debugging when context is wrong.
