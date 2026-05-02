"""pullnexus info — show detailed information about a skill."""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from pullnexus.api import fetch_skill_json, fetch_skill_readme
from pullnexus.schema import SCHEMA_VERSION

console = Console()

_FEEDBACK_DIR = Path(__file__).resolve().parents[2] / "feedback"
_FEEDBACK_MIN_REPORTS = 3

# Types where pulling a file package makes no sense.
_NON_INSTALLABLE_TYPES = {"repository", "eval", "policy"}


def info(
    skill_name: str = typer.Argument(..., help="Skill name (e.g. python-advanced-debugging)"),
    as_json: bool = typer.Option(
        False,
        "--json",
        help="Output metadata as JSON for agent-native consumption.",
    ),
):
    """Show full details for a skill — description, tags, examples, and usage."""

    skill_json = fetch_skill_json(skill_name)
    readme = fetch_skill_readme(skill_name)

    if skill_json is None and readme is None:
        console.print(f"[red]✗ Skill '{skill_name}' not found in the registry.[/red]")
        raise typer.Exit(1)

    if as_json:
        payload: dict = {"schema_version": SCHEMA_VERSION}
        if skill_json:
            payload.update(skill_json)
        if readme:
            payload["readme"] = readme
        # Enrich with live compatibility data from feedback files
        if skill_json:
            payload["compatibility"] = _load_compatibility(skill_name)
        print(json.dumps(payload, indent=2))
        raise typer.Exit(0)

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
        resource_type = str(skill_json.get("resource_type", "skill")).lower()
        repo = skill_json.get("repo", "")
        maturity = skill_json.get("maturity", "")
        maintained = skill_json.get("maintained", "")
        last_verified = skill_json.get("last_verified", "")
        compatibility = skill_json.get("compatibility", {})

        meta_lines = []
        if resource_type:
            meta_lines.append(f"**Type:** {resource_type}")
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
        if maturity:
            meta_lines.append(f"**Maturity:** {maturity}")
        if maintained:
            meta_lines.append(f"**Maintained:** {maintained}")
        if last_verified:
            meta_lines.append(f"**Last verified:** {last_verified}")
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

        # Compatibility section
        if compatibility:
            works_on = compatibility.get("works_on", [])
            known_issues = compatibility.get("known_issues", [])
            unverified = compatibility.get("unverified_on", [])
            console.print()
            if works_on:
                console.print("[green]✓ Works on:[/green] " + ", ".join(works_on))
            if known_issues:
                console.print("[red]✗ Known issues:[/red] " + ", ".join(known_issues))
            if unverified:
                console.print("[yellow]⚠ Unverified on:[/yellow] " + ", ".join(unverified))

    # README content
    if readme:
        console.print()
        console.print(Markdown(readme))

    if skill_json and str(skill_json.get("resource_type", "skill")).lower() in _NON_INSTALLABLE_TYPES:
        console.print(
            f"\n[dim]This is a [bold]{skill_json.get('resource_type')}[/bold] resource — "
            "reference metadata only, not a pullable file package.[/dim]"
        )
    else:
        console.print(
            f"\n[dim]Install this skill: [bold]pullnexus pull {skill_name}[/bold][/dim]"
        )


def _load_compatibility(resource_id: str) -> dict:
    """Load compatibility summary from feedback JSONL for agent-native --json output."""
    fb_path = _FEEDBACK_DIR / f"{resource_id}.jsonl"
    if not fb_path.exists():
        return {"status": "unverified", "report_count": 0}

    reports = []
    try:
        for line in fb_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                reports.append(json.loads(line))
    except Exception:
        return {"status": "unverified", "report_count": 0}

    count = len(reports)
    if count < _FEEDBACK_MIN_REPORTS:
        return {"status": "unverified", "report_count": count}

    works_on = sorted({r["hardware"] for r in reports if r.get("outcome") == "success" and r.get("hardware")})
    broken_on = sorted({r["hardware"] for r in reports if r.get("outcome") == "failure" and r.get("hardware")})
    models = sorted({r["model"] for r in reports if r.get("model")})
    return {
        "status": "verified",
        "report_count": count,
        "works_on": works_on,
        "broken_on": broken_on,
        "tested_models": models,
    }
