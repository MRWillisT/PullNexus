"""pullnexus types — enumerate all resource types in the registry."""

import json
from collections import Counter

import typer
from rich.console import Console
from rich.table import Table

from pullnexus.api import fetch_index
from pullnexus.schema import SCHEMA_VERSION

console = Console()

# Human-friendly labels and descriptions for known types.
TYPE_META: dict[str, dict[str, str]] = {
    "skill": {
        "label": "Skill",
        "description": "Teachable capability with JSONL examples and evals.",
        "installable": "yes",
    },
    "repository": {
        "label": "Repository",
        "description": "Curated open-source project reference with summary and link.",
        "installable": "no",
    },
    "tool": {
        "label": "Tool",
        "description": "MCP server, SDK wrapper, or integration adapter.",
        "installable": "planned",
    },
    "dataset": {
        "label": "Dataset",
        "description": "Training corpus, eval set, or synthetic data pack.",
        "installable": "planned",
    },
    "eval": {
        "label": "Eval",
        "description": "Benchmark suite, scoring rubric, or pass/fail gate.",
        "installable": "planned",
    },
    "playbook": {
        "label": "Playbook",
        "description": "Step-by-step procedure (e.g. deploy local RAG).",
        "installable": "planned",
    },
    "policy": {
        "label": "Policy",
        "description": "Guardrail rules, refusal templates, compliance specs.",
        "installable": "planned",
    },
    "template": {
        "label": "Template",
        "description": "Starter layout or config bundle for a project type.",
        "installable": "planned",
    },
    "environment": {
        "label": "Environment",
        "description": "Known-good stack profile (hardware + runtime + models).",
        "installable": "planned",
    },
}


def types(
    as_json: bool = typer.Option(
        False,
        "--json",
        help="Output resource types as JSON for machine-friendly consumption.",
    ),
):
    """Enumerate all resource types in the Nexus with counts."""
    resources = fetch_index()

    if not resources:
        if as_json:
            print(json.dumps(_empty_payload(), indent=2))
        else:
            console.print("[yellow]No resources available yet.[/yellow]")
        raise typer.Exit(0)

    counter: Counter[str] = Counter()
    for res in resources:
        rtype = str(res.get("resource_type", "skill")).strip().lower() or "skill"
        counter[rtype] += 1

    ordered = sorted(counter.items(), key=lambda item: (-item[1], item[0]))

    if as_json:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "total_resource_types": len(counter),
            "total_resources": len(resources),
            "types": [
                {
                    "slug": rtype,
                    "label": TYPE_META.get(rtype, {}).get("label", rtype.title()),
                    "description": TYPE_META.get(rtype, {}).get("description", ""),
                    "installable": TYPE_META.get(rtype, {}).get("installable", "unknown"),
                    "count": count,
                }
                for rtype, count in ordered
            ],
        }
        print(json.dumps(payload, indent=2))
        raise typer.Exit(0)

    table = Table(
        title=f"PullNexus Resource Types ({len(counter)} types, {len(resources)} total resources)",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Type", style="bold yellow")
    table.add_column("Label", style="bold")
    table.add_column("Resources", style="green", justify="right")
    table.add_column("Installable", style="dim", width=11)
    table.add_column("Description")

    for rtype, count in ordered:
        meta = TYPE_META.get(rtype, {})
        table.add_row(
            rtype,
            meta.get("label", rtype.title()),
            str(count),
            meta.get("installable", "—"),
            meta.get("description", ""),
        )

    console.print(table)
    console.print(
        "\n[dim]Filter by type: [bold]pullnexus list --type <slug>[/bold]  "
        "or [bold]pullnexus search <query> --type <slug>[/bold][/dim]"
    )


def _empty_payload() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "total_resource_types": 0,
        "total_resources": 0,
        "types": [],
    }
