"""pullnexus recommend — suggest skills for a problem statement."""

import json
import re
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
    "rag": ["rag", "retrieval", "embedding", "embeddings", "chunk", "chunking", "vector", "rerank", "reranking", "pdf", "ingestion"],
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

STOPWORDS = {
    "about", "after", "against", "also", "and", "any", "are", "around", "bad",
    "been", "being", "between", "both", "but", "can", "concrete", "did", "does",
    "feel", "feels", "for", "from", "fully", "get", "gets", "got", "had", "has",
    "have", "help", "here", "how", "inspect", "install", "into", "its", "just",
    "like", "local", "looking", "need", "now", "off", "on", "one", "only", "or",
    "our", "out", "problem", "quality", "really", "right", "should", "something",
    "specific", "still", "than", "that", "the", "their", "them", "there", "these",
    "they", "this", "use", "using", "want", "what", "when", "which", "with", "without",
    "work", "workflow", "would", "you", "your", "pipeline", "build", "building",
}

WANTS_INSTALL_TOKENS = {"install", "pull", "download", "save", "inspect"}


def _tokenize_text(text: str) -> list[str]:
    raw_tokens = re.findall(r"[a-z0-9][a-z0-9+\-]*", str(text or "").lower())
    tokens: list[str] = []
    for token in raw_tokens:
        if len(token) >= 3 or token in {"ui", "ux", "3d"}:
            tokens.append(token)
    return tokens


def _problem_tokens(problem: str) -> set[str]:
    return {token for token in _tokenize_text(problem) if token not in STOPWORDS}


def _keyword_hit(problem_tokens: set[str], raw_problem: str, keyword: str) -> bool:
    value = keyword.strip().lower()
    if not value:
        return False
    if " " in value:
        return value in raw_problem
    return any(token == value or token.startswith(value) for token in problem_tokens)


def _score_resource_for_problem(
    skill: dict,
    problem_tokens: set[str],
    raw_problem: str,
    requested_category: str = "",
    inferred_category: str = "",
    context: Optional[dict[str, str]] = None,
) -> tuple[int, list[str], list[str]]:
    skill_category = _skill_category_slug(skill)
    name_tokens = set(_tokenize_text(skill.get("name", "")))
    desc_tokens = set(_tokenize_text(skill.get("description", "")))
    tag_tokens: set[str] = set()
    for tag in skill.get("tags", []):
        if isinstance(tag, str):
            tag_tokens.update(_tokenize_text(tag))

    score = 0
    reasons: list[str] = []
    verbose_parts: list[str] = []

    if requested_category and skill_category == requested_category:
        score += 30
        reasons.append(f"category={_skill_category_label(skill)}")
        verbose_parts.append(f"requested category match +30 ({requested_category})")
    elif inferred_category and skill_category == inferred_category:
        score += 12
        reasons.append(f"category={_skill_category_label(skill)}")
        verbose_parts.append(f"inferred category match +12 ({inferred_category})")

    name_overlap = sorted(problem_tokens.intersection(name_tokens))
    if name_overlap:
        points = min(32, len(name_overlap) * 8)
        score += points
        reasons.append("name match")
        verbose_parts.append(f"name overlap +{points} ({', '.join(name_overlap[:6])})")

    tag_overlap = sorted(problem_tokens.intersection(tag_tokens))
    if tag_overlap:
        points = min(28, len(tag_overlap) * 7)
        score += points
        reasons.append("tag overlap")
        verbose_parts.append(f"tag overlap +{points} ({', '.join(tag_overlap[:6])})")

    desc_overlap = sorted(problem_tokens.intersection(desc_tokens))
    if desc_overlap:
        points = min(24, len(desc_overlap) * 4)
        score += points
        reasons.append("description overlap")
        verbose_parts.append(f"description overlap +{points} ({', '.join(desc_overlap[:6])})")

    if problem_tokens.intersection(WANTS_INSTALL_TOKENS) and bool(skill.get("installable", False)):
        score += 8
        reasons.append("installable")
        verbose_parts.append("installable boost +8")

    examples_bonus = min(4, int(skill.get("examples", 0)))
    if score > 0 and examples_bonus:
        score += examples_bonus
        verbose_parts.append(f"examples bonus +{examples_bonus}")

    if context and score > 0:
        compat = _load_compatibility(skill.get("name", ""))
        if compat.get("status") == "verified":
            hw = str(context.get("hardware", "")).lower()
            model = str(context.get("model", "")).lower()
            works = [w.lower() for w in compat.get("works_on", [])]
            models = [m.lower() for m in compat.get("tested_models", [])]
            if hw and any(hw in item for item in works):
                score += 15
                reasons.append("verified on your hardware")
                verbose_parts.append("hardware compatibility +15")
            if model and any(model in item for item in models):
                score += 10
                reasons.append("tested with your model")
                verbose_parts.append("model compatibility +10")

    return score, reasons, verbose_parts


def rank_resources_for_problem(
    problem: str,
    skills: list[dict],
    requested_category: str = "",
    requested_type: str = "",
    context: Optional[dict[str, str]] = None,
    explain_level: str = "basic",
) -> tuple[list[tuple[int, dict, str, list[str]]], str]:
    raw_problem = problem.lower()
    problem_tokens = _problem_tokens(problem)
    inferred_category = "" if requested_category else _infer_category(problem)
    scored: list[tuple[int, dict, str, list[str]]] = []

    for skill in skills:
        skill_category = _skill_category_slug(skill)
        skill_type = _resource_type_slug(skill)
        if requested_category and skill_category != requested_category:
            continue
        if requested_type and skill_type != requested_type:
            continue

        if context:
            compat = _load_compatibility(skill.get("name", ""))
            hw = str(context.get("hardware", "")).lower()
            if compat.get("status") == "verified":
                broken = [b.lower() for b in compat.get("broken_on", [])]
                if hw and any(hw in item for item in broken):
                    continue

        score, reasons, verbose_parts = _score_resource_for_problem(
            skill,
            problem_tokens,
            raw_problem,
            requested_category=requested_category,
            inferred_category=inferred_category,
            context=context,
        )
        if score > 0:
            reason = ", ".join(reasons)
            if explain_level == "verbose":
                reason = " | ".join(verbose_parts) if verbose_parts else "relevance"
            scored.append((score, skill, reason or "relevance", verbose_parts))

    scored.sort(key=lambda item: item[0], reverse=True)
    return scored, inferred_category


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
    scored, inferred_category = rank_resources_for_problem(
        problem,
        skills,
        requested_category=requested_category,
        requested_type=requested_type,
        context=ctx,
        explain_level=explain_level,
    )
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
    tokens = _problem_tokens(problem)
    best = ""
    best_hits = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if _keyword_hit(tokens, text, kw))
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