#!/usr/bin/env python3
"""
PullNexus submission validator.

Checks resource folders that changed in a PR for required files, valid JSON,
example count minimums, and schema consistency.

Usage:
    python scripts/validate_submission.py --changed-files changed_files.txt
    python scripts/validate_submission.py --dirs skills/brainstorming skills/premortem
"""

import argparse
import json
import sys
from pathlib import Path

# ── constants ────────────────────────────────────────────────────────────────

REQUIRED_SKILL_JSON_FIELDS = {"name", "version", "description", "tags", "license"}
MIN_EXAMPLES = 5

# Resource types that do NOT require examples.jsonl
# Mirrors pullnexus/schema.py:NO_EXAMPLES_REQUIRED_TYPES
NO_EXAMPLES_REQUIRED_TYPES = frozenset({
    "tool", "playbook", "dataset", "eval", "policy",
    "template", "environment", "repository", "prompt",
})

# Top-level directories that contain resource folders
RESOURCE_DIRS = frozenset({
    "skills", "prompts", "tools", "datasets", "playbooks",
    "policies", "evals", "templates", "environments", "repositories",
})

# Folders to skip inside resource directories (meta/template folders)
SKIP_PREFIXES = ("_",)


# ── validation ───────────────────────────────────────────────────────────────

def validate_resource(resource_path: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a single resource folder."""
    errors: list[str] = []
    warnings: list[str] = []
    name = resource_path.name

    # ── skill.json ────────────────────────────────────────────────────────────
    skill_json_path = resource_path / "skill.json"
    if not skill_json_path.exists():
        errors.append(f"[{name}] Missing skill.json")
        return errors, warnings

    try:
        meta = json.loads(skill_json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"[{name}] skill.json is not valid JSON: {exc}")
        return errors, warnings

    missing_fields = REQUIRED_SKILL_JSON_FIELDS - set(meta.keys())
    if missing_fields:
        errors.append(
            f"[{name}] skill.json missing required fields: {', '.join(sorted(missing_fields))}"
        )

    # ── README.md ─────────────────────────────────────────────────────────────
    if not (resource_path / "README.md").exists():
        errors.append(f"[{name}] Missing README.md")

    # ── examples.jsonl ────────────────────────────────────────────────────────
    # Determine resource type: prefer explicit field, fall back to parent dir name
    resource_type = (
        meta.get("resource_type")
        or meta.get("category")
        or resource_path.parent.name.rstrip("s")  # e.g. "skills" → "skill"
    )
    needs_examples = resource_type not in NO_EXAMPLES_REQUIRED_TYPES

    if needs_examples:
        examples_path = resource_path / "examples.jsonl"
        if not examples_path.exists():
            errors.append(f"[{name}] Missing examples.jsonl (required for '{resource_type}' resources)")
        else:
            raw_lines = [
                line.strip()
                for line in examples_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            valid_count = 0
            for i, line in enumerate(raw_lines, 1):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"[{name}] examples.jsonl line {i}: invalid JSON — {exc}")
                    continue

                if "conversations" not in obj:
                    errors.append(
                        f"[{name}] examples.jsonl line {i}: missing 'conversations' key"
                    )
                else:
                    valid_count += 1

            if valid_count < MIN_EXAMPLES:
                errors.append(
                    f"[{name}] examples.jsonl has {valid_count} valid example(s) "
                    f"(minimum {MIN_EXAMPLES} required)"
                )

            # Check declared count matches actual
            declared = meta.get("examples")
            if declared is not None and int(declared) != len(raw_lines):
                warnings.append(
                    f"[{name}] skill.json declares examples={declared} "
                    f"but examples.jsonl has {len(raw_lines)} lines — update the count"
                )

        # eval.jsonl is recommended but not required
        if not (resource_path / "eval.jsonl").exists():
            warnings.append(f"[{name}] No eval.jsonl found (recommended but not required)")

    return errors, warnings


# ── discovery ─────────────────────────────────────────────────────────────────

def find_changed_resources(repo_root: Path, changed_files: list[str]) -> list[Path]:
    """Return sorted list of resource folder Paths that contain changed files."""
    seen: set[Path] = set()
    for f in changed_files:
        parts = Path(f).parts
        if len(parts) < 2:
            continue
        top_dir, resource_name = parts[0], parts[1]
        if top_dir not in RESOURCE_DIRS:
            continue
        if any(resource_name.startswith(p) for p in SKIP_PREFIXES):
            continue
        candidate = repo_root / top_dir / resource_name
        if candidate.is_dir():
            seen.add(candidate)
    return sorted(seen)


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PullNexus resource submissions.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--changed-files",
        metavar="FILE",
        help="Path to a text file listing changed files (one per line, from git diff).",
    )
    group.add_argument(
        "--dirs",
        nargs="+",
        metavar="DIR",
        help="One or more resource folder paths to validate directly.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    if args.changed_files:
        changed_path = Path(args.changed_files)
        if not changed_path.exists():
            print(f"ERROR: changed-files path not found: {changed_path}", file=sys.stderr)
            return 1
        changed = [l.strip() for l in changed_path.read_text().splitlines() if l.strip()]
        resources = find_changed_resources(repo_root, changed)
    else:
        resources = [Path(d).resolve() for d in args.dirs]

    if not resources:
        print("No resource folders detected in changed files — nothing to validate.")
        return 0

    total_errors = 0
    total_warnings = 0

    print(f"Validating {len(resources)} resource folder(s)...\n")

    for resource_path in resources:
        errors, warnings = validate_resource(resource_path)
        status = "PASS" if not errors else "FAIL"
        print(f"  [{status}] {resource_path.parent.name}/{resource_path.name}")
        for e in errors:
            print(f"         ERROR: {e}")
        for w in warnings:
            print(f"       WARNING: {w}")
        total_errors += len(errors)
        total_warnings += len(warnings)

    print(f"\n{'─' * 60}")
    print(f"  {len(resources)} resource(s) checked")
    print(f"  {total_errors} error(s)   {total_warnings} warning(s)")

    if total_errors:
        print("\n  Submission blocked. Fix the errors above before merging.")
        return 1

    if total_warnings:
        print("\n  Submission OK (warnings above are recommended improvements).")
    else:
        print("\n  All checks passed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
