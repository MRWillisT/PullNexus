"""pullnexus recommend — suggest skills for a problem statement."""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from pullnexus.api import fetch_index

console = Console()

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
    limit: int = typer.Option(5, "--limit", "-n", help="Maximum recommendations"),
    explain: str = typer.Option(
        "basic",
        "--explain",
        help="Score explanation detail level: basic or verbose.",
    ),
):
    """Recommend the most relevant skills for a user problem."""
    skills = fetch_index()
    if not skills:
        console.print("[yellow]No skills available yet.[/yellow]")
        raise typer.Exit(1)

    explain_level = explain.lower().strip()
    if explain_level not in {"basic", "verbose"}:
        console.print("[red]Invalid --explain value. Use 'basic' or 'verbose'.[/red]")
        raise typer.Exit(1)

    requested_category = category.lower().strip() if category else ""
    inferred_category = _infer_category(problem) if not requested_category else ""
    q = problem.lower()
    scored: list[tuple[int, dict, str]] = []

    for skill in skills:
        skill_category = _skill_category_slug(skill)
        if requested_category and skill_category != requested_category:
            continue

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

        if score > 0:
            reason = ", ".join(reasons)
            if explain_level == "verbose":
                reason = " | ".join(verbose_parts) if verbose_parts else "relevance"
            scored.append((score, skill, reason))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:limit]

    if not top:
        console.print("[red]No recommendations found for that problem statement.[/red]")
        raise typer.Exit(1)

    table = Table(
        title=(
            f"Recommended Skills for: {problem}" +
            (f"  [category={requested_category}]" if requested_category else "") +
            (f"  [inferred={inferred_category}]" if inferred_category else "")
        ),
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Skill", style="bold")
    table.add_column("Category", style="magenta", width=14)
    table.add_column("Score", style="green", width=6, justify="right")
    table.add_column("Why")

    for score, skill, reason in top:
        table.add_row(
            skill.get("name", ""),
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
