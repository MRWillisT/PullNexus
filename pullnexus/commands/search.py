"""pullnexus search — search the skill registry."""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from pullnexus.api import fetch_index

console = Console()


def search(
    query: str = typer.Argument("", help="Search term — matches name, tags, and description"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by a specific tag"),
    category: Optional[str] = typer.Option(
        None,
        "--category",
        "-c",
        help="Filter by category (e.g. design, automation, testing).",
    ),
    use: Optional[str] = typer.Option(
        None,
        "--use",
        help="Alias for --category.",
    ),
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

    selected_category = (category or use)
    if not query and not tag and not selected_category:
        console.print(
            "[red]Provide a query or use filters like [bold]--tag[/bold] or [bold]--category[/bold].[/red]"
        )
        raise typer.Exit(1)

    q = query.lower().strip()
    results = []
    for skill in skills:
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()
        tags = [t.lower() for t in skill.get("tags", [])]
        skill_category = _skill_category_slug(skill)

        # Apply tag filter first if provided
        if tag and tag.lower() not in tags:
            continue
        if selected_category and skill_category != selected_category.lower().strip():
            continue

        # Score relevance
        if not q:
            results.append((3, skill))
        elif q in name:
            results.append((0, skill))   # name match — highest priority
        elif q in tags:
            results.append((1, skill))
        elif q in desc:
            results.append((2, skill))

    results.sort(key=lambda x: x[0])
    results = [s for _, s in results][:limit]

    if not results:
        msg = f"No skills found for [bold]'{query}'[/bold]" if query else "No skills matched filters"
        if tag:
            msg += f" with tag [bold]'{tag}'[/bold]"
        if selected_category:
            msg += f" in category [bold]'{selected_category}'[/bold]"
        console.print(f"[red]{msg}[/red]")
        console.print("\nTry [bold]pullnexus list[/bold] to browse all available skills.")
        raise typer.Exit(1)

    table = Table(
        title=(f"Skills matching '{query}'" if query else "Skills matching filters")
        + (f"  [tag={tag}]" if tag else "")
        + (f"  [category={selected_category}]" if selected_category else ""),
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Skill", style="bold")
    table.add_column("Category", style="magenta", width=14)
    table.add_column("Version", style="dim", width=8)
    table.add_column("Tags", style="cyan")
    table.add_column("Description")

    for skill in results:
        table.add_row(
            skill.get("name", ""),
            _skill_category_label(skill),
            skill.get("version", ""),
            ", ".join(skill.get("tags", [])),
            skill.get("description", "")[:80],
        )

    console.print(table)
    console.print(
        f"\n[dim]Run [bold]pullnexus info <skill-name>[/bold] for full details, "
        "or [bold]pullnexus pull <skill-name>[/bold] to install.[/dim]"
    )


def _skill_category_slug(skill: dict) -> str:
    """Return category slug from explicit category field or use: tag fallback."""
    explicit = skill.get("category", "")
    if explicit:
        return str(explicit).strip().lower().replace(" ", "-")
    for tag in skill.get("tags", []):
        if isinstance(tag, str) and tag.startswith("use:"):
            return tag.split(":", 1)[1].strip().lower()
    return "other"


def _skill_category_label(skill: dict) -> str:
    """Return human-readable category label for UI tables."""
    return _skill_category_slug(skill).replace("-", " ").title()
