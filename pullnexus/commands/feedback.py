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

# Feedback stored in feedback/<resource-id>.jsonl — one file per resource,
# one JSON object per line. Avoids merge conflicts when multiple contributors
# submit simultaneously. Minimum 3 reports before compatibility data is surfaced.
FEEDBACK_MIN_REPORTS = 3
_FEEDBACK_DIR = Path(__file__).resolve().parents[2] / "feedback"


def _feedback_path(resource_id: str) -> Path:
    """Return the feedback JSONL path for a resource."""
    return _FEEDBACK_DIR / f"{resource_id}.jsonl"


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
    ),
    notes: Optional[str] = typer.Option(None, "--notes", "-n", help="Optional freeform notes"),
    as_json: bool = typer.Option(False, "--json", help="Print the report as JSON instead of saving"),
):
    """Submit a compatibility report for a resource.

    Reports are appended to [bold]feedback/<resource-id>.jsonl[/bold] in the registry.
    Once a resource has 3+ reports, compatibility data appears in [bold]pullnexus info[/bold].
    """
    valid_outcomes = {"success", "partial", "fail"}
    if outcome.lower() not in valid_outcomes:
        console.print(f"[red]Invalid --outcome '{outcome}'. Use: success, partial, or fail.[/red]")
        raise typer.Exit(1)

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

    # Append to feedback/<resource-id>.jsonl
    _FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    out_path = _feedback_path(resource_id)
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(report) + "\n")

    # Count existing reports
    report_count = sum(1 for line in out_path.read_text(encoding="utf-8").splitlines() if line.strip())

    outcome_color = {"success": "green", "partial": "yellow", "fail": "red"}[outcome.lower()]

    console.print(Panel(
        f"[bold]Resource:[/bold] {resource_id}\n"
        f"[bold]Model:[/bold] {model}\n"
        f"[bold]Hardware:[/bold] {hardware}\n"
        f"[bold]Use case:[/bold] {use_case}\n"
        f"[bold]Outcome:[/bold] [{outcome_color}]{outcome}[/{outcome_color}]\n"
        + (f"[bold]Notes:[/bold] {notes}\n" if notes else "")
        + f"\n[dim]Total reports for this resource: {report_count}"
        + (f" ✓ (compatibility data now visible in `pullnexus info`)" if report_count >= FEEDBACK_MIN_REPORTS else f" ({FEEDBACK_MIN_REPORTS - report_count} more needed before compatibility data appears)")
        + "[/dim]",
        title="[bold cyan]Feedback saved[/bold cyan]",
        border_style="cyan",
    ))
    console.print(f"[dim]Saved to: {out_path}[/dim]")
    console.print(
        "\n[dim]To submit this feedback to the registry, open a PR adding "
        f"[bold]feedback/{resource_id}.jsonl[/bold] to the PullNexus repo.[/dim]"
    )

