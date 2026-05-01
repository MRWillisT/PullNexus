"""pullnexus info — show detailed information about a skill."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from pullnexus.api import fetch_skill_json, fetch_skill_readme

console = Console()


def info(
    skill_name: str = typer.Argument(..., help="Skill name (e.g. python-advanced-debugging)"),
):
    """Show full details for a skill — description, tags, examples, and usage."""

    skill_json = fetch_skill_json(skill_name)
    readme = fetch_skill_readme(skill_name)

    if skill_json is None and readme is None:
        console.print(f"[red]✗ Skill '{skill_name}' not found in the registry.[/red]")
        raise typer.Exit(1)

    # Header panel with metadata
    if skill_json:
        name = skill_json.get("name", skill_name)
        version = skill_json.get("version", "")
        description = skill_json.get("description", "")
        tags = skill_json.get("tags", [])
        license_ = skill_json.get("license", "")
        examples = skill_json.get("examples", skill_json.get("evaluation_cases", ""))
        mcp = skill_json.get("mcp_compatible", False)
        author = skill_json.get("author", "")
        inspired_by = skill_json.get("inspired_by", "")
        source = skill_json.get("source", "")
        resource_type = skill_json.get("resource_type", "")
        repo = skill_json.get("repo", "")

        meta_lines = []
        if version:
            meta_lines.append(f"**Version:** {version}")
        if author:
            meta_lines.append(f"**Author:** {author}")
        if license_:
            meta_lines.append(f"**License:** {license_}")
        if examples:
            meta_lines.append(f"**Examples:** {examples}")
        if mcp:
            meta_lines.append("**MCP compatible:** ✓")
        if tags:
            meta_lines.append(f"**Tags:** {', '.join(tags)}")
        if inspired_by:
            meta_lines.append(f"**Inspired by:** {inspired_by}")
        if source:
            meta_lines.append(f"**Source:** {source}")
        if repo:
            meta_lines.append(f"**Repo:** {repo}")
        if description:
            meta_lines.append(f"\n{description}")

        console.print(Panel(
            Markdown("\n".join(meta_lines)),
            title=f"[bold cyan]{name}[/bold cyan]",
            border_style="cyan",
        ))

    # README content
    if readme:
        console.print()
        console.print(Markdown(readme))

    if skill_json and skill_json.get("resource_type") == "repository":
        console.print("\n[dim]This is a repository resource entry (reference metadata, not a pullable skill package).[/dim]")
    else:
        console.print(
            f"\n[dim]Install this skill: [bold]pullnexus pull {skill_name}[/bold][/dim]"
        )
