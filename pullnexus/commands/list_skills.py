"""pullnexus list — list all available skills."""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from pullnexus.api import fetch_index

console = Console()


def list_skills(
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    sort: str = typer.Option("name", "--sort", "-s", help="Sort by: name, version"),
):
    """List all available skills in the Nexus."""
    skills = fetch_index()

    if not skills:
        console.print(
            "[yellow]No skills available yet — the registry may be empty or unreachable.[/yellow]\n\n"
            "Be the first to contribute! Run [bold]pullnexus submit --help[/bold] to get started."
        )
        raise typer.Exit(0)

    if tag:
        skills = [s for s in skills if tag.lower() in [t.lower() for t in s.get("tags", [])]]
        if not skills:
            console.print(f"[red]No skills found with tag '{tag}'[/red]")
            raise typer.Exit(1)

    if sort == "version":
        skills.sort(key=lambda s: s.get("version", ""))
    else:
        skills.sort(key=lambda s: s.get("name", ""))

    table = Table(
        title=f"PullNexus Skills Registry ({len(skills)} skill{'s' if len(skills) != 1 else ''})"
        + (f"  [tag={tag}]" if tag else ""),
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Skill", style="bold")
    table.add_column("Version", style="dim", width=8)
    table.add_column("Examples", style="green", width=9, justify="right")
    table.add_column("Tags", style="cyan")
    table.add_column("Description")

    for skill in skills:
        examples = skill.get("examples", skill.get("evaluation_cases", ""))
        table.add_row(
            skill.get("name", ""),
            skill.get("version", ""),
            str(examples) if examples else "—",
            ", ".join(skill.get("tags", [])),
            skill.get("description", "")[:70],
        )

    console.print(table)
    console.print(
        "\n[dim]Run [bold]pullnexus pull <skill-name>[/bold] to install a skill locally.[/dim]"
    )
