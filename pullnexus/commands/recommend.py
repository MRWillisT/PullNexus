"""pullnexus recommend — suggest skills for a problem statement."""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from pullnexus.api import fetch_index
from pullnexus.schema import SCHEMA_VERSION

console = Console()

_FEEDBACK_DIR = Path(__file__).resolve().parents[2] / "feedback"
_FEEDBACK_MIN_REPORTS = 3

CATEGORY_KEYWORDS = {
    "automation": ["automation", "agent", "workflow", "mcp", "orchestr", "integration"],
    "design": ["design", "ui", "ux", "frontend", "layout", "brand"],
    "documents": ["pdf", "docx", "xlsx", "document", "ppt", "slides", "excel"],
    "testing": ["test", "pytest", "tdd", "qa", "regression"],
    "developer": ["debug", "refactor", "code", "python", "develop"],
    "finance": ["trading", "crypto", "market", "risk", "kronos"],
    "planning": ["plan", "reason", "brainstorm", "decision", "strategy"],
    "writing": ["writing", "content", "messaging", "copy", "edit"],
    "creative": ["video", "image", "animation", "art", "cinematic"],
    "research": ["catalog", "toolbox", "open-source", "compare", "stack"],
    "presentation": ["slides", "ppt", "presentation"],
    "web": ["web", "website", "deploy", "artifact"],
}


def recommend(
    problem: str = typer.Argument(..., help="Problem statement to solve"),
    category: Optional[str] = typer.Option(
        None,
        "--category",
        "-c",
        help="Hard-filter recommendations to an exact category slug.",
    ),
    resource_type: Optional[str] = typer.Option(
        None,
        "--type",
        help="Filter to a resource type (e.g. skill, tool, playbook). Defaults to all types.",
    ),
    context: Optional[str] = typer.Option(
        None,
        "--context",
        help="Hardware/model context to filter by compatibility. Format: model=llama3,hardware=8GB",
    ),
    limit: int = typer.Option(5, "--limit", "-n", help="Maximum recommendations"),
    explain: str = typer.Option(
        "basic",
        "--explain",
        help="Score explanation detail level: basic or verbose.",
    ),
    as_json: bool = typer.Option(
        False,
        "--json",
        help="Output recommendations as JSON for machine-friendly consumption.",
    ),
):
    """Recommend the most relevant resources for a user problem.

    Searches across all resource types by default (skills, tools, playbooks, datasets).
    Use [bold]--type skill[/bold] to narrow to skills only.
    Use [bold]--context model=llama3,hardware=8GB[/bold] to filter by verified compatibility.
    """
    skills = fetch_index()
    if not skills:
        console.print("[yellow]No skills available yet.[/yellow]")
        raise typer.Exit(1)

    explain_level = explain.lower().strip()
    if explain_level not in {"basic", "verbose"}:
        console.print("[red]Invalid --explain value. Use 'basic' or 'verbose'.[/red]")
        raise typer.Exit(1)

    # Parse --context into a dict: "model=llama3,hardware=8GB" -> {"model": "llama3", "hardware": "8gb"}
    ctx: dict[str, str] = {}
    if context:
        for part in context.split(","):
            part = part.strip()
            if "=" in part:
                k, _, v = part.partition("=")
                ctx[k.strip().lower()] = v.strip().lower()
        if ctx:
            ctx_display = ", ".join(f"{k}={v}" for k, v in ctx.items())
            console.print(f"[dim]Filtering by context: {ctx_display}[/dim]")

    requested_category = category.lower().strip() if category else ""
    requested_type = resource_type.lower().strip() if resource_type else ""
    inferred_category = _infer_category(problem) if not requested_category else ""
    q = problem.lower()
    scored: list[tuple[int, dict, str, list[str]]] = []

    for skill in skills:
        skill_category = _skill_category_slug(skill)
        skill_type = _resource_type_slug(skill)
        if requested_category and skill_category != requested_category:
            continue
        if requested_type and skill_type != requested_type:
            continue

        # Context filtering: skip resources with confirmed breakage on this hardware/model
        if ctx:
            compat = _load_compatibility(skill.get("name", ""))
            hw = ctx.get("hardware", "")
            model = ctx.get("model", "")
            if compat.get("status") == "verified":
                broken = [b.lower() for b in compat.get("broken_on", [])]
                if hw and any(hw in b for b in broken):
                    continue
                # Boost score if explicitly verified to work on this hardware
                # (handled below in scoring)

        tags = [t.lower() for t in skill.get("tags", [])]
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()

        score = 0
        reasons: list[str] = []
        verbose_parts: list[str] = []

        if requested_category and skill_category == requested_category:
            score += 40
            reasons.append(f"category={_skill_category_label(skill)}")
            verbose_parts.append(f"category match +40 ({requested_category})")
        elif inferred_category and skill_category == inferred_category:
            score += 40
            reasons.append(f"category={_skill_category_label(skill)}")
            verbose_parts.append(f"inferred category match +40 ({inferred_category})")

        if any(token in name for token in q.split() if token):
            score += 25
            reasons.append("name match")
            verbose_parts.append("name token overlap +25")

        overlap = [token for token in q.split() if token and (token in tags or token in desc)]
        if overlap:
            overlap_points = min(20, len(overlap) * 4)
            score += overlap_points
            reasons.append("keyword overlap")
            verbose_parts.append(f"keyword overlap +{overlap_points} ({', '.join(sorted(set(overlap)))})")

        # Prefer richer skills when scores tie.
        examples_bonus = min(10, int(skill.get("examples", 0)))
        score += examples_bonus
        if examples_bonus:
            verbose_parts.append(f"examples bonus +{examples_bonus}")

        # Compatibility boost: verified to work on requested hardware/model
        if ctx and score > 0:
            compat = _load_compatibility(skill.get("name", ""))
            if compat.get("status") == "verified":
                hw = ctx.get("hardware", "")
                model = ctx.get("model", "")
                works = [w.lower() for w in compat.get("works_on", [])]
                models = [m.lower() for m in compat.get("tested_models", [])]
                if hw and any(hw in w for w in works):
                    score += 15
                    reasons.append("verified on your hardware")
                    verbose_parts.append("hardware compatibility +15")
                if model and any(model in m for m in models):
                    score += 10
                    reasons.append("tested with your model")
                    verbose_parts.append("model compatibility +10")

        if score > 0:
            reason = ", ".join(reasons)
            if explain_level == "verbose":
                reason = " | ".join(verbose_parts) if verbose_parts else "relevance"
            scored.append((score, skill, reason, verbose_parts))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:limit]

    if not top:
        console.print("[red]No recommendations found for that problem statement.[/red]")
        raise typer.Exit(1)

    if as_json:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "problem": problem,
            "requested_category": requested_category or None,
            "requested_type": requested_type or None,
            "context": ctx or None,
            "inferred_category": inferred_category or None,
            "explain": explain_level,
            "total_recommendations": len(top),
            "recommendations": [
                {
                    "name": skill.get("name", ""),
                    "resource_type": _resource_type_slug(skill),
                    "category": _skill_category_slug(skill),
                    "score": score,
                    "why": reason or "relevance",
                    "details": detail_parts if explain_level == "verbose" else None,
                }
                for score, skill, reason, detail_parts in top
            ],
        }
        print(json.dumps(payload, indent=2))
        raise typer.Exit(0)

    table = Table(
        title=(
            f"Recommended Skills for: {problem}" +
            (f"  [category={requested_category}]" if requested_category else "") +
            (f"  [type={requested_type}]" if requested_type else "") +
            (f"  [inferred={inferred_category}]" if inferred_category else "")
        ),
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Skill", style="bold")
    table.add_column("Type", style="yellow", width=11)
    table.add_column("Category", style="magenta", width=14)
    table.add_column("Score", style="green", width=6, justify="right")
    table.add_column("Why")

    for score, skill, reason, _ in top:
        table.add_row(
            skill.get("name", ""),
            _resource_type_label(skill),
            _skill_category_label(skill),
            str(score),
            reason or "relevance",
        )

    console.print(table)
    console.print(
        "\n[dim]Use [bold]pullnexus info <skill-name>[/bold] to inspect details before pulling.[/dim]"
    )


def _infer_category(problem: str) -> str:
    """Infer likely category from problem keywords."""
    text = problem.lower()
    best = ""
    best_hits = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in text)
        if hits > best_hits:
            best = category
            best_hits = hits

    return best


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


def _load_compatibility(resource_id: str) -> dict:
    """Load compatibility summary from feedback JSONL for context-aware filtering."""
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