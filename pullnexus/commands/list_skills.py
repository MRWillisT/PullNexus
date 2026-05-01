"""pullnexus list — list all available skills."""

from collections import defaultdict
import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from pullnexus.api import fetch_registry

console = Console()


def list_skills(
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    category: Optional[str] = typer.Option(
        None,
        "--category",
        "-c",
        help="Filter by category (e.g. design, automation, testing).",
    ),
    resource_type: Optional[str] = typer.Option(
        None,
        "--type",
        help="Filter by resource type (e.g. skill, repository, dataset, playbook).",
    ),
    sort: str = typer.Option("name", "--sort", "-s", help="Sort by: name, version"),
    group_by: Optional[str] = typer.Option(
        None,
        "--group-by",
        help="Group skills by taxonomy. Supported values: category, use",
    ),
    show_all: bool = typer.Option(
        False,
        "--all",
        help="Include external registry sources.",
    ),
    as_json: bool = typer.Option(
        False,
        "--json",
        help="Output skills as JSON for machine-friendly consumption.",
    ),
):
    """List all available skills in the Nexus."""
    registry = fetch_registry()
    skills = registry.get("skills", [])
    external_sources = registry.get("external_sources", [])

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

    if category:
        requested = category.lower().strip()
        skills = [
            s
            for s in skills
            if _skill_category_slug(s).lower() == requested
        ]
        if not skills:
            console.print(f"[red]No skills found in category '{category}'[/red]")
            raise typer.Exit(1)

    if resource_type:
        requested_type = resource_type.lower().strip()
        skills = [s for s in skills if _resource_type_slug(s) == requested_type]
        if not skills:
            console.print(f"[red]No resources found with type '{resource_type}'[/red]")
            raise typer.Exit(1)

    if sort == "version":
        skills.sort(key=lambda s: s.get("version", ""))
    else:
        skills.sort(key=lambda s: s.get("name", ""))

    if as_json:
        payload = {
            "filters": {
                "tag": tag,
                "category": category.lower().strip() if category else None,
                "resource_type": resource_type.lower().strip() if resource_type else None,
                "sort": sort,
                "group_by": group_by,
                "all_sources": show_all,
            },
            "total_skills": len(skills),
            "skills": [
                {
                    "name": skill.get("name", ""),
                    "resource_type": _resource_type_slug(skill),
                    "category": _skill_category_slug(skill),
                    "version": skill.get("version", ""),
                    "examples": skill.get("examples", skill.get("evaluation_cases", 0)),
                    "tags": skill.get("tags", []),
                    "description": skill.get("description", ""),
                }
                for skill in skills
            ],
            "groups": _build_group_payload(skills, group_by) if group_by else None,
            "external_sources": external_sources if show_all else [],
        }
        console.print(json.dumps(payload, indent=2))
        raise typer.Exit(0)

    if group_by:
        _print_grouped_skills(skills, group_by)
    else:
        _print_skills_table(skills, tag, category)

    if show_all:
        _print_external_sources(external_sources)

    console.print(
        "\n[dim]Run [bold]pullnexus pull <skill-name>[/bold] to install a skill locally.[/dim]"
    )


def _print_skills_table(skills: list[dict], tag: Optional[str], category: Optional[str]) -> None:
    """Render the default flat skills table."""

    table = Table(
        title=f"PullNexus Skills Registry ({len(skills)} skill{'s' if len(skills) != 1 else ''})"
        + (f"  [tag={tag}]" if tag else "")
        + (f"  [category={category}]" if category else ""),
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Skill", style="bold")
    table.add_column("Type", style="yellow", width=11)
    table.add_column("Category", style="magenta", width=14)
    table.add_column("Version", style="dim", width=8)
    table.add_column("Examples", style="green", width=9, justify="right")
    table.add_column("Tags", style="cyan")
    table.add_column("Description")

    for skill in skills:
        examples = skill.get("examples", skill.get("evaluation_cases", ""))
        table.add_row(
            skill.get("name", ""),
            _resource_type_label(skill),
            _skill_category_label(skill),
            skill.get("version", ""),
            str(examples) if examples else "—",
            ", ".join(skill.get("tags", [])),
            skill.get("description", "")[:70],
        )

    console.print(table)


def _print_grouped_skills(skills: list[dict], group_by: str) -> None:
    """Render grouped skills tables for supported taxonomy views."""
    if group_by not in {"use", "category"}:
        console.print(
            f"[red]Unsupported group: '{group_by}'. Try [bold]category[/bold] or [bold]use[/bold].[/red]"
        )
        raise typer.Exit(1)

    grouped: dict[str, list[dict]] = defaultdict(list)
    for skill in skills:
        if group_by == "category":
            group_name = _skill_category_label(skill)
        else:
            group_name = _extract_use_group(skill.get("tags", []))
        grouped[group_name].append(skill)

    console.print(
        f"[bold]PullNexus Skills Grouped By {group_by.title()}[/bold]"
        f" [dim]({len(skills)} skill{'s' if len(skills) != 1 else ''})[/dim]"
    )

    for group_name in sorted(grouped):
        group_table = Table(
            title=group_name,
            show_header=True,
            header_style="bold cyan",
            border_style="dim",
        )
        group_table.add_column("Skill", style="bold")
        group_table.add_column("Tags", style="cyan")
        group_table.add_column("Description")

        for skill in sorted(grouped[group_name], key=lambda item: item.get("name", "")):
            visible_tags = [tag for tag in skill.get("tags", []) if not tag.startswith("use:")]
            group_table.add_row(
                skill.get("name", ""),
                ", ".join(visible_tags),
                skill.get("description", "")[:80],
            )

        console.print()
        console.print(group_table)


def _extract_use_group(tags: list[str]) -> str:
    """Extract a human-readable use grouping from taxonomy tags."""
    for tag in tags:
        if tag.startswith("use:"):
            return tag.split(":", 1)[1].replace("-", " ").title()
    return "Other"


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


def _resource_type_slug(skill: dict) -> str:
    """Return normalized resource type slug."""
    value = skill.get("resource_type", "skill")
    return str(value).strip().lower() or "skill"


def _resource_type_label(skill: dict) -> str:
    """Return human-readable resource type label for UI tables."""
    return _resource_type_slug(skill).replace("-", " ").title()


def _print_external_sources(external_sources: list[dict]) -> None:
    """Render the configured external source list."""

    ext_table = Table(
        title=(
            "External Skill Sources "
            f"({len(external_sources)} source{'s' if len(external_sources) != 1 else ''})"
        ),
        show_header=True,
        header_style="bold magenta",
        border_style="dim",
    )
    ext_table.add_column("Name", style="bold")
    ext_table.add_column("Repo", style="cyan")
    ext_table.add_column("License", style="dim")
    ext_table.add_column("Adapter")

    if external_sources:
        for source in external_sources:
            ext_table.add_row(
                source.get("name", ""),
                source.get("repo", ""),
                source.get("license", ""),
                source.get("adapter", ""),
            )
    else:
        ext_table.add_row("—", "—", "—", "No external sources configured")

    console.print()
    console.print(ext_table)


def _build_group_payload(skills: list[dict], group_by: str) -> dict[str, list[dict]]:
    """Build grouped skill payload for JSON output."""
    if group_by not in {"use", "category"}:
        console.print(
            f"[red]Unsupported group: '{group_by}'. Try [bold]category[/bold] or [bold]use[/bold].[/red]"
        )
        raise typer.Exit(1)

    grouped: dict[str, list[dict]] = defaultdict(list)
    for skill in skills:
        if group_by == "category":
            group_name = _skill_category_slug(skill)
        else:
            group_name = _extract_use_group(skill.get("tags", [])).lower().replace(" ", "-")
        grouped[group_name].append(
            {
                "name": skill.get("name", ""),
                "resource_type": _resource_type_slug(skill),
                "category": _skill_category_slug(skill),
                "version": skill.get("version", ""),
                "tags": skill.get("tags", []),
                "description": skill.get("description", ""),
            }
        )

    return {
        group: sorted(items, key=lambda item: item.get("name", ""))
        for group, items in sorted(grouped.items(), key=lambda item: item[0])
    }
