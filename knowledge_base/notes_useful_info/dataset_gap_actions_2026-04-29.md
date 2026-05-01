# Dataset Gap Actions - 2026-04-29

## Problem

The dataset had strong real-world project data but was skewed toward Freedom Bot, crypto trading, NEXRAD weather radar, and PyQt6 GUI work.

## Actions

- Added general assistant examples for everyday planning, explanations, decisions, and non-code help.
- Added writing and explanation examples for README text, docs, plan summaries, and safety warnings.
- Added uncertainty and correction examples so the model learns to ask for context and recover from mistakes.
- Added non-Python examples covering HTML, CSS, JavaScript, TypeScript, PowerShell, bash, React, Express, npm, and SQL.
- Seeded the knowledge base with starter notes instead of leaving every folder manifest-only.

## Training Note

These new files should be upweighted at first to reduce domain skew, then adjusted after eval results.
