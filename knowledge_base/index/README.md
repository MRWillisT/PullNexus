# Master Chat Index

Use `ingest_copilot_exports.py` to ingest exported chat files into `knowledge_base/chats_raw` and update:

- `knowledge_base/index/master_chat_index.json`

## Example

```bash
python ingest_copilot_exports.py --source "W:/path/to/copilot-exports"
```

## Dry Run

```bash
python ingest_copilot_exports.py --source "W:/path/to/copilot-exports" --dry-run --summary-json
```

## Auto-Tag Indexed Chats

After ingesting, apply heuristic tags to indexed chat entries:

```bash
python auto_tag_chat_index.py --summary-json
```

Dry run:

```bash
python auto_tag_chat_index.py --dry-run --summary-json
```

## Route Tagged Chats Into Project Snapshots

After tags are applied, route chats into project snapshot folders:

```bash
python route_tagged_chats_to_projects.py --summary-json
```

Dry run:

```bash
python route_tagged_chats_to_projects.py --dry-run --summary-json
```

## One-Command Pipeline

Run ingest + auto-tag + project routing in sequence:

```bash
python run_kb_pipeline.py --source "W:/path/to/copilot-exports" --summary-json
```

Dry run:

```bash
python run_kb_pipeline.py --source "W:/path/to/copilot-exports" --dry-run --summary-json
```

## Daily Automation (Windows)

Use PowerShell wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_kb_pipeline_daily.ps1 -SourcePath "W:\path\to\copilot-exports"
```

Or set `source_path` in `kb_pipeline_daily_config.json` and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_kb_pipeline_daily.ps1
```

Dry run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_kb_pipeline_daily.ps1 -DryRun
```

Logs are written to `logs/` with timestamped `.log` and `.summary.json` files.
