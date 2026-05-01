"""pullnexus info — show detailed information about a skill."""

import json
import base64
from typing import Optional

import httpx
import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from pullnexus import __registry_url__

console = Console()
HEADERS = {"Accept": "application/vnd.github.v3+json"}


def info(
    skill_name: str = typer.Argument(..., help="Skill name (e.g. python-advanced-debugging)"),
):
    """Show full details for a skill — description, tags, examples, and usage."""

    skill_json = _fetch_skill_json(skill_name)
    readme = _fetch_readme(skill_name)

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

        meta_lines = []
        if version:
            meta_lines.append(f"**Version:** {version}")
        if license_:
            meta_lines.append(f"**License:** {license_}")
        if examples:
            meta_lines.append(f"**Examples:** {examples}")
        if mcp:
            meta_lines.append("**MCP compatible:** ✓")
        if tags:
            meta_lines.append(f"**Tags:** {', '.join(tags)}")
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

    console.print(
        f"\n[dim]Install this skill: [bold]pullnexus pull {skill_name}[/bold][/dim]"
    )


def _fetch_skill_json(skill_name: str) -> Optional[dict]:
    url = f"{__registry_url__}/{skill_name}/skill.json"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=HEADERS)
            if resp.status_code != 200:
                return None
            content_b64 = resp.json().get("content", "")
            content = base64.b64decode(content_b64).decode("utf-8")
            return json.loads(content)
    except Exception:
        return None


def _fetch_readme(skill_name: str) -> Optional[str]:
    url = f"{__registry_url__}/{skill_name}/README.md"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=HEADERS)
            if resp.status_code != 200:
                return None
            content_b64 = resp.json().get("content", "")
            return base64.b64decode(content_b64).decode("utf-8")
    except Exception:
        return None
