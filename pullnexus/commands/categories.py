"""pullnexus categories — list available categories and counts."""

from collections import Counter

import typer
from rich.console import Console
from rich.table import Table

from pullnexus.api import fetch_index

console = Console()


def categories():
    """List all known categories and how many skills each contains."""
    skills = fetch_index()

    if not skills:
        console.print("[yellow]No skills available yet.[/yellow]")
        raise typer.Exit(0)

    counter: Counter[str] = Counter()
    for skill in skills:
        counter[_skill_category_slug(skill)] += 1

    table = Table(
        title=f"PullNexus Categories ({len(counter)} total)",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Category", style="bold magenta")
    table.add_column("Skills", style="green", justify="right")

    for category, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        table.add_row(category.replace("-", " ").title(), str(count))

    console.print(table)
    console.print(
        "\n[dim]Tip: use [bold]pullnexus list --group-by category[/bold] or "
        "[bold]pullnexus search --category <name>[/bold].[/dim]"
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
