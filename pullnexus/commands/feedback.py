"""pullnexus feedback — submit a compatibility report for a resource."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from pullnexus.api import fetch_skill_json

console = Console()

# Feedback stored locally under ~/.pullnexus/feedback/ until a GitHub-backed
# submission endpoint is live. Each file is named <resource-id>_<timestamp>.json.
_FEEDBACK_DIR = Path.home() / ".pullnexus" / "feedback"


def feedback(
    resource_id: str = typer.Argument(..., help="Resource name (e.g. python-advanced-debugging)"),
    model: str = typer.Option(..., "--model", "-m", help="Model used (e.g. llama3-8b, mistral-7b)"),
    hardware: str = typer.Option(..., "--hardware", help="Hardware context (e.g. 'RTX 3090 24GB', 'M2 16GB')"),
    use_case: str = typer.Option(..., "--use-case", "-u", help="What you used this resource for"),
    outcome: str = typer.Option(
        ...,
        "--outcome",
        "-o",
        help="Result: success, partial, or fail",
        show_choices=True,
    ),
    notes: Optional[str] = typer.Option(None, "--notes", "-n", help="Optional freeform notes"),
    as_json: bool = typer.Option(False, "--json", help="Print the report as JSON instead of saving"),
):
    """Submit a compatibility report for a resource.

    Reports are saved locally under ~/.pullnexus/feedback/ and can later be
    submitted to the registry via GitHub (future feature).
    """
    # Validate outcome value.
    valid_outcomes = {"success", "partial", "fail"}
    if outcome.lower() not in valid_outcomes:
        console.print(f"[red]Invalid --outcome '{outcome}'. Use: success, partial, or fail.[/red]")
        raise typer.Exit(1)

    # Validate resource exists.
    meta = fetch_skill_json(resource_id)
    if meta is None:
        console.print(f"[yellow]⚠ Resource '{resource_id}' not found in registry. Saving report anyway.[/yellow]")

    report = {
        "resource_id": resource_id,
        "resource_type": meta.get("resource_type", "skill") if meta else "unknown",
        "model": model,
        "hardware": hardware,
        "use_case": use_case,
        "outcome": outcome.lower(),
        "notes": notes or "",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    if as_json:
        print(json.dumps(report, indent=2))
        raise typer.Exit(0)

    # Save locally.
    _FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = _FEEDBACK_DIR / f"{resource_id}_{ts}.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    outcome_color = {"success": "green", "partial": "yellow", "fail": "red"}[outcome.lower()]

    console.print(Panel(
        f"[bold]Resource:[/bold] {resource_id}\n"
        f"[bold]Model:[/bold] {model}\n"
        f"[bold]Hardware:[/bold] {hardware}\n"
        f"[bold]Use case:[/bold] {use_case}\n"
        f"[bold]Outcome:[/bold] [{outcome_color}]{outcome}[/{outcome_color}]\n"
        + (f"[bold]Notes:[/bold] {notes}\n" if notes else ""),
        title="[bold cyan]Feedback saved[/bold cyan]",
        border_style="cyan",
    ))
    console.print(f"[dim]Saved to: {out_path}[/dim]")
    console.print(
        "\n[dim]GitHub-backed submission coming soon. "
        "In the meantime, open a PR with your feedback file to contribute it to the registry.[/dim]"
    )
