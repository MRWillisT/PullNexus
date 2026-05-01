"""pullnexus search — search the skill registry."""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from pullnexus.api import fetch_index

console = Console()


def search(
    query: str = typer.Argument(..., help="Search term — matches name, tags, and description"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by a specific tag"),
    limit: int = typer.Option(20, "--limit", "-n", help="Maximum number of results"),
):
    """Search skills in the Nexus by keyword, tag, or description."""
    skills = fetch_index()

    if not skills:
        console.print(
            "[yellow]No skills found — the registry may be empty or unreachable.[/yellow]\n"
            "Run [bold]pullnexus list[/bold] to check connectivity."
        )
        raise typer.Exit(1)

    q = query.lower()
    results = []
    for skill in skills:
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()
        tags = [t.lower() for t in skill.get("tags", [])]

        # Apply tag filter first if provided
        if tag and tag.lower() not in tags:
            continue

        # Score relevance
        if q in name:
            results.append((0, skill))   # name match — highest priority
        elif q in tags:
            results.append((1, skill))
        elif q in desc:
            results.append((2, skill))

    results.sort(key=lambda x: x[0])
    results = [s for _, s in results][:limit]

    if not results:
        msg = f"No skills found for [bold]'{query}'[/bold]"
        if tag:
            msg += f" with tag [bold]'{tag}'[/bold]"
        console.print(f"[red]{msg}[/red]")
        console.print("\nTry [bold]pullnexus list[/bold] to browse all available skills.")
        raise typer.Exit(1)

    table = Table(
        title=f"Skills matching '{query}'" + (f"  [tag={tag}]" if tag else ""),
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Skill", style="bold")
    table.add_column("Version", style="dim", width=8)
    table.add_column("Tags", style="cyan")
    table.add_column("Description")

    for skill in results:
        table.add_row(
            skill.get("name", ""),
            skill.get("version", ""),
            ", ".join(skill.get("tags", [])),
            skill.get("description", "")[:80],
        )

    console.print(table)
    console.print(
        f"\n[dim]Run [bold]pullnexus info <skill-name>[/bold] for full details, "
        "or [bold]pullnexus pull <skill-name>[/bold] to install.[/dim]"
    )
