"""
PullNexus MCP Server — exposes the skill registry as native MCP tools.

Any MCP-compatible client (Claude Code, Continue.dev, Cursor, LM Studio)
can call these tools directly without the CLI or any wrapper code.

Start with:
    pullnexus serve                  # stdio (default, local-first)
    pullnexus serve --transport http # HTTP on 127.0.0.1:7337
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise ImportError(
        "PullNexus MCP server requires the 'mcp' package.\n"
        "Install it with: pip install pullnexus[mcp]"
    ) from exc

from pullnexus.api import fetch_index, fetch_skill_json, fetch_skill_readme, fetch_registry
from pullnexus.commands.recommend import rank_resources_for_problem
from pullnexus.commands.feedback import _FEEDBACK_DIR, _feedback_path, FEEDBACK_MIN_REPORTS

mcp = FastMCP(
    name="PullNexus",
    instructions=(
        "PullNexus is the open registry of skills, tools, datasets, playbooks, and evals "
        "for local LLMs. Use pullnexus_search or pullnexus_recommend to find resources, "
        "pullnexus_info to get full details, and pullnexus_install to pull files locally.\n\n"
        "Response format rules (apply to every skill recommendation):\n"
        "- Commit to one specific approach immediately. Do not offer a menu of options.\n"
        "- Name actual tools and packages by their real name. Never use vague category labels "
        "like 'a document loader' or 'an embedding model' — say the specific package.\n"
        "- Write in plain connected prose. No bold section headers, no bullet-point readouts.\n"
        "- End with a directive next step, not a question. You already chose the approach.\n"
        "- When a skill's pullnexus_info response includes model_hints.small_model.response_contract, "
        "follow that contract exactly for small or quantized models (<=14B parameters).\n"
        "- Call pullnexus_model_context once at session start to load the instruction profile "
        "for your specific model."
    ),
)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def pullnexus_search(
    query: str,
    resource_type: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 10,
) -> str:
    """Search the PullNexus registry by keyword, tag, or resource type.

    Args:
        query: Search term — matched against name, description, and tags.
        resource_type: Optional filter (skill, tool, playbook, dataset, eval, policy, template, environment).
        tag: Optional single tag filter.
        limit: Maximum number of results to return (default 10, max 60).

    Returns:
        JSON list of matching resources with name, type, description, tags, and version.
    """
    skills = fetch_index()
    q = query.lower()

    # Tokenise multi-word queries so "fine-tune 35B on consumer GPU" still matches axolotl/llama-factory
    import re as _re
    _STOPWORDS = {
        "a", "an", "the", "on", "in", "for", "of", "to", "and", "or", "with",
        "is", "it", "at", "by", "as", "up", "how", "can", "use", "get", "set",
    }
    tokens = [t for t in _re.split(r"[\s\-_/]+", q) if len(t) > 2 and t not in _STOPWORDS]

    scored = []
    for s in skills:
        if resource_type and str(s.get("resource_type", "skill")).lower() != resource_type.lower():
            continue
        if tag and tag.lower() not in [t.lower() for t in s.get("tags", [])]:
            continue
        name = str(s.get("name", "")).lower()
        desc = str(s.get("description", "")).lower()
        tags_str = " ".join(str(t).lower() for t in s.get("tags", []))
        haystack = f"{name} {tags_str} {desc}"
        if q in name or q in tags_str or q in desc:
            scored.append((0, s))
        elif tokens:
            hits = sum(1 for tok in tokens if tok in haystack)
            if hits:
                scored.append((len(tokens) - hits, s))

    scored.sort(key=lambda x: x[0])
    results = [s for _, s in scored]

    total_matched = len(results)
    results = results[:max(1, min(int(limit), 60))]
    return json.dumps({
        "query": query,
        "total": total_matched,
        "returned": len(results),
        "results": [
            {
                "name": r.get("name"),
                "resource_type": r.get("resource_type", "skill"),
                "version": r.get("version"),
                "description": r.get("description"),
                "tags": r.get("tags", []),
                "installable": r.get("installable", True),
            }
            for r in results
        ],
    }, indent=2)


@mcp.tool()
def pullnexus_recommend(
    problem: str,
    resource_type: Optional[str] = None,
    limit: int = 5,
) -> str:
    """Call this when you're unsure what skill, tool, or resource would help with a task.

    Describe the problem in plain English and PullNexus will find the best match automatically.

    Searches across all resource types by default. Use resource_type to narrow.

    Args:
        problem: Natural language description of what you need to solve.
        resource_type: Optional filter (skill, tool, playbook, dataset, eval, etc.).
        limit: Maximum recommendations to return (default 5).

    Returns:
        JSON list of scored recommendations with name, type, score, and reason.
    """
    skills = fetch_index()
    scored, inferred_category, intent = rank_resources_for_problem(
        problem,
        skills,
        requested_type=resource_type.lower().strip() if resource_type else "",
        explain_level="basic",
    )
    top = scored[:limit]

    return json.dumps({
        "problem": problem,
        "total_candidates": len(scored),
        "inferred_category": inferred_category or None,
        "intent": intent or None,
        "recommendations": [
            {
                "name": s.get("name"),
                "resource_type": s.get("resource_type", "skill"),
                "version": s.get("version"),
                "description": s.get("description"),
                "score": score,
                "reasons": [part.strip() for part in reason.split(",") if part.strip()][:3],
                "installable": s.get("installable", True),
            }
            for score, s, reason, _ in top
        ],
    }, indent=2)


@mcp.tool()
def pullnexus_info(skill_name: str) -> str:
    """Get full metadata and README for a PullNexus resource.

    Args:
        skill_name: Exact resource name (e.g. 'python-advanced-debugging', 'local-rag-starter-pack').

    Returns:
        JSON object with full metadata, compatibility data, and README content.
    """
    meta = fetch_skill_json(skill_name)
    readme = fetch_skill_readme(skill_name)

    if meta is None and readme is None:
        return json.dumps({"error": f"Resource '{skill_name}' not found in the registry."})

    # Load compatibility from feedback/ if available
    compatibility_summary = _load_compatibility_summary(skill_name)

    result: dict = {}
    if meta:
        result.update(meta)
    if readme:
        result["readme"] = readme
    if compatibility_summary:
        result["compatibility_summary"] = compatibility_summary

    return json.dumps(result, indent=2)


@mcp.tool()
def pullnexus_install(skill_name: str, output_path: str = "./pullnexus-skills") -> str:
    """Pull a skill or resource from PullNexus and save it locally.

    Only installable resource types can be pulled (skills, playbooks, datasets).
    Non-installable types (repository, eval, policy) return an info link instead.

    Args:
        skill_name: Resource name to install (e.g. 'python-advanced-debugging').
        output_path: Local directory to save the resource into (default ./pullnexus-skills).

    Returns:
        JSON result with status and saved file list.
    """
    from pullnexus.api import fetch_skill_files, download_file

    meta = fetch_skill_json(skill_name)
    if meta is not None:
        rtype = str(meta.get("resource_type", "skill")).lower()
        if rtype in {"repository", "eval", "policy"}:
            return json.dumps({
                "status": "not_installable",
                "resource_type": rtype,
                "message": f"'{skill_name}' is a {rtype} resource — reference metadata only, not a file package.",
                "info": f"Use pullnexus_info('{skill_name}') to view details.",
            })

    files = fetch_skill_files(skill_name)
    if not files:
        return json.dumps({"status": "not_found", "message": f"Resource '{skill_name}' not found."})

    target = Path(output_path) / skill_name
    target.mkdir(parents=True, exist_ok=True)

    saved, failed = [], []
    for file_info in files:
        fname = file_info["name"]
        url = file_info.get("download_url", "")
        if not url:
            failed.append(fname)
            continue
        content = download_file(url)
        if content is None:
            failed.append(fname)
            continue
        (target / fname).write_bytes(content)
        saved.append(fname)

    return json.dumps({
        "status": "success" if saved else "failed",
        "skill_name": skill_name,
        "output_path": str(target.resolve()),
        "saved": saved,
        "failed": failed,
    }, indent=2)


@mcp.tool()
def pullnexus_types() -> str:
    """List all resource types in the PullNexus registry with counts.

    Returns:
        JSON object mapping resource type slugs to count and installable status.
    """
    from collections import Counter
    skills = fetch_index()
    counts: Counter[str] = Counter(str(s.get("resource_type", "skill")).lower() for s in skills)
    installable_map = {
        "skill": "yes", "playbook": "yes", "dataset": "yes", "template": "yes",
        "tool": "planned", "environment": "planned",
        "repository": "no", "eval": "no", "policy": "no",
    }
    return json.dumps({
        "total_resources": len(skills),
        "types": {
            rtype: {"count": count, "installable": installable_map.get(rtype, "unknown")}
            for rtype, count in sorted(counts.items(), key=lambda x: -x[1])
        },
    }, indent=2)


@mcp.tool()
def pullnexus_model_context(model: str, param_count_b: Optional[int] = None) -> str:
    """Call this once at session start to load the instruction profile for your model.

    Returns formatting rules and behavioral hints tuned for your model size.
    Small and quantized models (<=14B) get a stricter directive contract to avoid
    vague responses. Larger models get lighter guidance.

    Args:
        model: Model identifier (e.g. 'qwen2.5-coder:7b', 'llama3-8b-q4', 'mistral-7b').
        param_count_b: Optional explicit parameter count in billions. Inferred from model
                       name if omitted.

    Returns:
        JSON object with instruction_style, rules, and usage notes for this session.
    """
    import re

    # Infer param count from model name if not supplied
    if param_count_b is None:
        match = re.search(r"(\d+(?:\.\d+)?)\s*[bB]", model)
        param_count_b = int(float(match.group(1))) if match else 0

    is_small = 0 < param_count_b <= 14

    if is_small:
        profile = {
            "instruction_style": "directive",
            "model": model,
            "param_count_b": param_count_b,
            "applies_to": "models with <=14B parameters",
            "rules": [
                "Commit to one approach immediately. No option menus.",
                "Name the specific package or tool by its real name — never a category label.",
                "Write 2-4 prose sentences only. No bold headers, no bullet readouts.",
                "End with a directive next step, not a question.",
                "When pullnexus_info returns model_hints.small_model.response_contract, follow it exactly.",
            ],
            "note": (
                "Small models lose specificity with long instruction lists. "
                "Use the response_contract from model_hints when available — it encodes "
                "the minimum instructions needed for correct output on this model class."
            ),
            "recommended_workflow": [
                "1. pullnexus_recommend(problem) to find the best resource.",
                "2. pullnexus_info(skill_name) to get full metadata including model_hints.",
                "3. If model_hints.small_model.response_contract is present, follow it for your reply.",
                "4. pullnexus_feedback(resource_id, model, hardware, use_case, outcome) after responding.",
            ],
        }
    else:
        profile = {
            "instruction_style": "standard",
            "model": model,
            "param_count_b": param_count_b if param_count_b else "unknown",
            "applies_to": "models with >14B parameters",
            "rules": [
                "Prefer concrete recommendations over broad surveys.",
                "Name specific packages and tools, not category labels.",
                "Diagnose the user's actual problem before recommending a stack.",
                "Check model_hints in pullnexus_info for any resource-specific guidance.",
            ],
            "recommended_workflow": [
                "1. pullnexus_recommend(problem) to find the best resource.",
                "2. pullnexus_info(skill_name) to get full metadata.",
                "3. Respond using the resource context.",
                "4. pullnexus_feedback(resource_id, model, hardware, use_case, outcome) after responding.",
            ],
        }

    return json.dumps(profile, indent=2)


@mcp.tool()
def pullnexus_hints_needed(min_fail_reports: int = 2) -> str:
    """Return skills that have failure reports on small models but no model_hints yet.

    Use this to prioritize which skills need model_hints.small_model added to their
    skill.json. Skills appear here when real usage reports flag them as failing on
    small/quantized models — no manual testing required.

    Args:
        min_fail_reports: Minimum number of fail/partial reports to surface a skill (default 2).

    Returns:
        JSON list of skills needing model_hints, sorted by fail count descending.
    """
    import re

    if not _FEEDBACK_DIR.exists():
        return json.dumps({"total": 0, "skills_needing_hints": []})

    skills_index = {s.get("name"): s for s in fetch_index() if isinstance(s, dict)}
    needs_hints: list[dict] = []

    for feedback_file in sorted(_FEEDBACK_DIR.glob("*.jsonl")):
        resource_id = feedback_file.stem
        skill_meta = skills_index.get(resource_id, {})

        # Skip if model_hints already present
        if skill_meta.get("model_hints"):
            continue

        fail_on_small: list[dict] = []
        try:
            for line in feedback_file.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                report = json.loads(line)
                if report.get("outcome") not in {"fail", "partial"}:
                    continue
                model_str = str(report.get("model", ""))
                match = re.search(r"(\d+(?:\.\d+)?)\s*[bB]", model_str)
                param_b = int(float(match.group(1))) if match else 0
                if 0 < param_b <= 14:
                    fail_on_small.append({
                        "model": model_str,
                        "outcome": report.get("outcome"),
                        "use_case": report.get("use_case", ""),
                        "notes": report.get("notes", ""),
                    })
        except Exception:
            continue

        if len(fail_on_small) >= min_fail_reports:
            needs_hints.append({
                "resource_id": resource_id,
                "resource_type": skill_meta.get("resource_type", "unknown"),
                "description": skill_meta.get("description", ""),
                "fail_report_count": len(fail_on_small),
                "sample_reports": fail_on_small[:3],
                "action": f"Add model_hints.small_model.response_contract to skills/{resource_id}/skill.json",
            })

    needs_hints.sort(key=lambda x: -x["fail_report_count"])

    return json.dumps({
        "total": len(needs_hints),
        "min_fail_reports_threshold": min_fail_reports,
        "skills_needing_hints": needs_hints,
    }, indent=2)


@mcp.tool()
def pullnexus_feedback(
    resource_id: str,
    model: str,
    hardware: str,
    use_case: str,
    outcome: str,
    notes: str = "",
) -> str:
    """Submit a compatibility report for a PullNexus resource.

    Reports are appended to feedback/<resource-id>.jsonl in the registry.
    Compatibility data appears in pullnexus_info once a resource has 3+ reports.

    Args:
        resource_id: Resource name (e.g. 'python-advanced-debugging').
        model: Model used (e.g. 'llama3-8b', 'mistral-7b-q4').
        hardware: Hardware context (e.g. 'RTX 3090 24GB', 'M2 16GB RAM').
        use_case: What you used the resource for.
        outcome: Result — must be 'success', 'partial', or 'fail'.
        notes: Optional additional notes.

    Returns:
        JSON confirmation with report count for this resource.
    """
    from datetime import datetime, timezone

    valid = {"success", "partial", "fail"}
    if outcome.lower() not in valid:
        return json.dumps({"error": f"Invalid outcome '{outcome}'. Must be: success, partial, or fail."})

    meta = fetch_skill_json(resource_id)
    report = {
        "resource_id": resource_id,
        "resource_type": meta.get("resource_type", "skill") if meta else "unknown",
        "model": model,
        "hardware": hardware,
        "use_case": use_case,
        "outcome": outcome.lower(),
        "notes": notes,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    _FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    out_path = _feedback_path(resource_id)
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(report) + "\n")

    count = sum(1 for line in out_path.read_text(encoding="utf-8").splitlines() if line.strip())

    return json.dumps({
        "status": "saved",
        "resource_id": resource_id,
        "outcome": outcome.lower(),
        "total_reports": count,
        "compatibility_visible": count >= FEEDBACK_MIN_REPORTS,
        "path": str(out_path),
    }, indent=2)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_compatibility_summary(resource_id: str) -> Optional[dict]:
    """Load aggregated compatibility from feedback/ JSONL if enough reports exist."""
    try:
        fp = _feedback_path(resource_id)
        if not fp.exists():
            return None
        lines = [json.loads(l) for l in fp.read_text(encoding="utf-8").splitlines() if l.strip()]
        if len(lines) < FEEDBACK_MIN_REPORTS:
            return {"status": "unverified", "report_count": len(lines), "needed": FEEDBACK_MIN_REPORTS}

        successes = [l["model"] for l in lines if l.get("outcome") == "success"]
        failures = [f"{l.get('hardware', 'unknown')} — {l.get('notes', '')}" for l in lines if l.get("outcome") == "fail"]
        return {
            "status": "verified",
            "report_count": len(lines),
            "works_on": sorted(set(successes)),
            "known_issues": sorted(set(failures)),
        }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Entry point (used by `pullnexus serve`)
# ---------------------------------------------------------------------------

def run_stdio() -> None:
    """Run the MCP server over stdio (local-first, default)."""
    mcp.run(transport="stdio")


def run_http(host: str = "127.0.0.1", port: int = 7337) -> None:
    """Run the MCP server over HTTP (team/cloud deployments)."""
    import inspect
    import os
    import uvicorn

    public_host = os.getenv("PULLNEXUS_ALLOWED_HOST") or os.getenv("RAILWAY_PUBLIC_DOMAIN")

    try:
        from mcp.server.transport_security import TransportSecuritySettings
    except ImportError:
        TransportSecuritySettings = None

    transport_security = None
    if TransportSecuritySettings is not None and public_host:
        transport_security = TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=[
                "127.0.0.1",
                "127.0.0.1:*",
                "localhost",
                "localhost:*",
                "[::1]",
                "[::1]:*",
                public_host,
                f"{public_host}:*",
            ],
            allowed_origins=[
                "http://127.0.0.1",
                "http://127.0.0.1:*",
                "http://localhost",
                "http://localhost:*",
                "http://[::1]",
                "http://[::1]:*",
                f"https://{public_host}",
                f"https://{public_host}:*",
                f"http://{public_host}",
                f"http://{public_host}:*",
            ],
        )

    run_params = inspect.signature(mcp.run).parameters
    if "host" in run_params and "port" in run_params:
        run_kwargs = {
            "transport": "streamable-http",
            "host": host,
            "port": port,
        }
        if transport_security is not None and "transport_security" in run_params:
            run_kwargs["transport_security"] = transport_security
        mcp.run(**run_kwargs)
        return

    # Older and intermediate FastMCP variants still need uvicorn to own the HTTP bind.
    # If the app method supports host/transport_security, pass them through there.
    app_kwargs: dict[str, object] = {}
    streamable_http_app = getattr(mcp, "streamable_http_app")
    app_params = inspect.signature(streamable_http_app).parameters
    if "host" in app_params:
        app_kwargs["host"] = host
    if transport_security is not None and "transport_security" in app_params:
        app_kwargs["transport_security"] = transport_security

    if hasattr(mcp, "settings"):
        if hasattr(mcp.settings, "host"):
            mcp.settings.host = host
        if hasattr(mcp.settings, "port"):
            mcp.settings.port = port
        if transport_security is not None and hasattr(mcp.settings, "transport_security"):
            mcp.settings.transport_security = transport_security

    starlette_app = streamable_http_app(**app_kwargs)
    uvicorn.run(
        starlette_app,
        host=host,
        port=port,
        log_level=getattr(getattr(mcp, "settings", None), "log_level", "info").lower(),
    )
