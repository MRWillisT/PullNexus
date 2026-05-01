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

    # 2. Required files
    existing = {f.name for f in skill_path.iterdir()}
    for required in REQUIRED_FILES:
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
        except json.JSONDecodeError as exc:
            errors.append(f"skill.json is not valid JSON: {exc}")

    # 4. Validate examples.jsonl
    example_count = 0
    if "examples.jsonl" in existing:
        try:
            lines = (skill_path / "examples.jsonl").read_text(encoding="utf-8").strip().splitlines()
            for i, line in enumerate(lines, 1):
                obj = json.loads(line)
                if "conversations" not in obj and "messages" not in obj:
                    errors.append(
                        f"examples.jsonl line {i}: must have 'conversations' or 'messages' key"
                    )
                    break
            example_count = len(lines)
            if example_count < 3:
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
            lines = (skill_path / "eval.jsonl").read_text(encoding="utf-8").strip().splitlines()
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
