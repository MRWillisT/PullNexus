"""pullnexus submit — validate and submit a skill to the Nexus."""

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

console = Console()

REQUIRED_FILES = {"skill.json", "examples.jsonl", "README.md"}
OPTIONAL_FILES = {"eval.jsonl", "tools"}

REQUIRED_SKILL_FIELDS = {"name", "version", "description", "tags", "license"}
PROVENANCE_FIELDS = {"source", "author"}
QUALITY_FIELDS = {"maturity", "maintained", "last_verified"}

# Types that don't require training examples — their validation is lighter.
_NO_EXAMPLES_REQUIRED = {"tool", "playbook", "dataset", "eval", "policy", "template", "environment", "repository"}


def submit(
    path: str = typer.Argument(..., help="Path to your skill folder"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Validate only — don't open a PR"
    ),
):
    """Validate a skill folder and submit it to the Nexus via GitHub PR."""
    skill_path = Path(path)

    console.print(f"\n[bold]Validating skill at:[/bold] {skill_path.resolve()}\n")

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Folder must exist
    if not skill_path.exists():
        console.print("[red]✗ Path does not exist.[/red]")
        raise typer.Exit(1)
    if not skill_path.is_dir():
        console.print("[red]✗ Path must be a directory (skill folder).[/red]")
        raise typer.Exit(1)

    # 2. Required files (examples.jsonl not required for non-skill types)
    existing = {f.name for f in skill_path.iterdir()}

    # Peek at resource_type before full validation
    raw_meta: dict = {}
    if "skill.json" in existing:
        try:
            raw_meta = json.loads((skill_path / "skill.json").read_text(encoding="utf-8"))
        except Exception:
            pass
    resource_type = str(raw_meta.get("resource_type", "skill")).lower()

    required_files = {"skill.json", "README.md"}
    if resource_type not in _NO_EXAMPLES_REQUIRED:
        required_files.add("examples.jsonl")

    for required in required_files:
        if required not in existing:
            errors.append(f"Missing required file: {required}")

    for optional in OPTIONAL_FILES:
        if optional not in existing:
            warnings.append(f"Optional file missing (recommended): {optional}")

    # 3. Validate skill.json
    skill_meta = {}
    if "skill.json" in existing:
        try:
            skill_meta = json.loads((skill_path / "skill.json").read_text(encoding="utf-8"))
            for field in REQUIRED_SKILL_FIELDS:
                if not skill_meta.get(field):
                    errors.append(f"skill.json missing required field: '{field}'")
            if not isinstance(skill_meta.get("tags", []), list):
                errors.append("skill.json: 'tags' must be a list")
            if skill_meta.get("tags") and len(skill_meta["tags"]) < 1:
                warnings.append("skill.json: add at least one tag for discoverability")

            # Provenance checks (warnings, not errors)
            for field in PROVENANCE_FIELDS:
                if not skill_meta.get(field):
                    warnings.append(f"skill.json: missing provenance field '{field}' (recommended)")

            # Quality metadata checks (warnings)
            for field in QUALITY_FIELDS:
                if not skill_meta.get(field):
                    warnings.append(f"skill.json: missing quality field '{field}' (recommended)")

            # Type-specific validation
            detected_type = str(skill_meta.get("resource_type", "skill")).lower()
            if detected_type == "tool" and not skill_meta.get("repo"):
                warnings.append("skill.json: 'tool' resources should include a 'repo' field")
            if detected_type == "dataset" and not skill_meta.get("formats"):
                warnings.append("skill.json: 'dataset' resources should list supported 'formats'")
            if detected_type == "eval" and not skill_meta.get("related"):
                warnings.append("skill.json: 'eval' resources should list 'related' resources they evaluate")
            if detected_type == "playbook" and not skill_meta.get("compatibility"):
                warnings.append("skill.json: 'playbook' resources should include a 'compatibility' block")

        except json.JSONDecodeError as exc:
            errors.append(f"skill.json is not valid JSON: {exc}")

    # 4. Validate examples.jsonl (only required/meaningful for skill type)
    example_count = 0
    if "examples.jsonl" in existing:
        try:
            lines = [
                line for line in
                (skill_path / "examples.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            for i, line in enumerate(lines, 1):
                obj = json.loads(line)
                if "conversations" not in obj and "messages" not in obj:
                    errors.append(
                        f"examples.jsonl line {i}: must have 'conversations' or 'messages' key"
                    )
                    break
            example_count = len(lines)
            detected_type = str(skill_meta.get("resource_type", "skill")).lower()
            if detected_type not in _NO_EXAMPLES_REQUIRED and example_count < 3:
                warnings.append(
                    f"examples.jsonl has only {example_count} example(s). "
                    "Aim for at least 5 for better quality."
                )
        except json.JSONDecodeError as exc:
            errors.append(f"examples.jsonl contains invalid JSON: {exc}")

    # 5. Validate eval.jsonl if present
    eval_count = 0
    if "eval.jsonl" in existing:
        try:
            lines = [
                line for line in
                (skill_path / "eval.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            eval_count = len(lines)
            for i, line in enumerate(lines, 1):
                obj = json.loads(line)
                for field in ("id", "input", "expected_behavior"):
                    if field not in obj:
                        warnings.append(f"eval.jsonl line {i}: missing recommended field '{field}'")
                        break
        except json.JSONDecodeError as exc:
            errors.append(f"eval.jsonl contains invalid JSON: {exc}")

    # Print validation report
    table = Table(show_header=False, border_style="dim", padding=(0, 1))
    table.add_column("Status", style="bold", width=4)
    table.add_column("Detail")

    for err in errors:
        table.add_row("[red]✗[/red]", err)
    for warn in warnings:
        table.add_row("[yellow]⚠[/yellow]", warn)
    if not errors and not warnings:
        table.add_row("[green]✓[/green]", "All checks passed!")
    elif not errors:
        table.add_row("[green]✓[/green]", "Required checks passed (see warnings above)")

    console.print(table)

    if errors:
        console.print(
            f"\n[red]✗ Validation failed with {len(errors)} error(s). "
            "Fix them before submitting.[/red]"
        )
        raise typer.Exit(1)

    skill_name = skill_meta.get("name", skill_path.name)
    console.print(f"\n[green]✓ Skill '{skill_name}' is ready to submit![/green]")
    console.print(f"  [dim]• {example_count} example(s) in examples.jsonl[/dim]")
    if eval_count:
        console.print(f"  [dim]• {eval_count} eval case(s) in eval.jsonl[/dim]")

    if dry_run:
        console.print("\n[dim]Dry run — skipping PR instructions.[/dim]")
        return

    console.print(
        "\n[bold]To submit this skill:[/bold]\n"
        "  1. Fork [link=https://github.com/MRWillisT/PullNexus]github.com/MRWillisT/PullNexus[/link]\n"
        f"  2. Copy your skill folder to [cyan]skills/{skill_name}/[/cyan]\n"
        "  3. Open a Pull Request against the [cyan]main[/cyan] branch\n"
        "  4. A maintainer will review and merge it into the registry\n\n"
        "[dim]Full contribution guide: "
        "[link=https://github.com/MRWillisT/PullNexus/blob/main/CONTRIBUTING.md]CONTRIBUTING.md[/link][/dim]"
    )
