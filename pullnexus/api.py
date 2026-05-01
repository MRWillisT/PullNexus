"""
Registry API client for PullNexus.

Fetches the skill index and individual skill files from the GitHub-backed registry.
Falls back gracefully when the registry is unreachable or still private.
"""

import json
from pathlib import Path
from typing import Optional

import httpx
from rich.console import Console

from pullnexus import __registry_url__, __registry_index__

HEADERS = {"Accept": "application/vnd.github.v3+json"}
_console = Console()


def fetch_registry() -> dict:
    """
    Fetch full registry metadata from skills/index.json.

    Returns a dict with keys:
    - skills: list[dict]
    - external_sources: list[dict]
    Falls back to directory enumeration when index.json is unavailable.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(__registry_index__, headers=HEADERS)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, dict):
                    skills = data.get("skills", [])
                    return {
                        "skills": _augment_skills_with_catalog_resources(skills),
                        "external_sources": data.get("external_sources", []),
                    }
    except Exception:
        pass

    # Local fallback: useful when the remote registry is private/unreachable.
    local_registry = _fetch_registry_from_local_index()
    if local_registry is not None:
        return local_registry

    # Fallback: enumerate the skills/ directory on GitHub
    return {"skills": _fetch_skills_from_directory(), "external_sources": []}


def fetch_index() -> list[dict]:
    """
    Fetch the machine-readable skills index (skills/index.json).

    Returns a list of skill metadata dicts. Falls back to the GitHub
    directory listing if the index file is missing, and returns an
    empty list when the registry is completely unreachable.
    """
    return fetch_registry().get("skills", [])


def fetch_skill_json(skill_name: str) -> Optional[dict]:
    """Fetch a skill's metadata from remote GitHub, then fall back to local files."""
    url = f"{__registry_url__}/{skill_name}/skill.json"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=HEADERS)
            if resp.status_code == 200:
                content_b64 = resp.json().get("content", "")
                import base64
                content = base64.b64decode(content_b64).decode("utf-8")
                return json.loads(content)
    except Exception:
        pass

    local = _fetch_local_skill_json(skill_name)
    if local is not None:
        return local

    # Virtual/generated entries can still be discovered from the index.
    for skill in fetch_index():
        if skill.get("name") == skill_name:
            return skill

    return None


def fetch_skill_readme(skill_name: str) -> Optional[str]:
    """Fetch a skill README from remote GitHub, then fall back to local files."""
    url = f"{__registry_url__}/{skill_name}/README.md"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=HEADERS)
            if resp.status_code == 200:
                content_b64 = resp.json().get("content", "")
                import base64
                return base64.b64decode(content_b64).decode("utf-8")
    except Exception:
        pass

    return _fetch_local_skill_readme(skill_name)


def _fetch_registry_from_local_index() -> Optional[dict]:
    """Read skills/index.json from common local workspace locations."""
    candidate_paths = [
        Path.cwd() / "skills" / "index.json",
        Path(__file__).resolve().parents[1] / "skills" / "index.json",
    ]

    for index_path in candidate_paths:
        try:
            if not index_path.exists():
                continue
            data = json.loads(index_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            skills = data.get("skills", [])
            return {
                "skills": _augment_skills_with_catalog_resources(skills),
                "external_sources": data.get("external_sources", []),
            }
        except Exception:
            continue

    return None


def _skill_candidate_paths(skill_name: str, filename: str) -> list[Path]:
    """Return likely local file paths for a skill asset."""
    return [
        Path.cwd() / "skills" / skill_name / filename,
        Path(__file__).resolve().parents[1] / "skills" / skill_name / filename,
    ]


def _fetch_local_skill_json(skill_name: str) -> Optional[dict]:
    """Read skill.json from local workspace locations."""
    for path in _skill_candidate_paths(skill_name, "skill.json"):
        try:
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
    return None


def _fetch_local_skill_readme(skill_name: str) -> Optional[str]:
    """Read README.md from local workspace locations."""
    for path in _skill_candidate_paths(skill_name, "README.md"):
        try:
            if path.exists():
                return path.read_text(encoding="utf-8")
        except Exception:
            continue
    return None


def _fetch_skills_from_directory() -> list[dict]:
    """List skills by reading the GitHub directory, extracting skill.json for each."""
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(__registry_url__, headers=HEADERS)
            if resp.status_code != 200:
                return []
            entries = resp.json()
            if not isinstance(entries, list):
                return []

            skills = []
            for entry in entries:
                if entry.get("type") != "dir" or entry["name"].startswith("_"):
                    continue
                skill = _fetch_skill_meta(client, entry["name"])
                if skill:
                    skills.append(skill)
            return _augment_skills_with_catalog_resources(skills)
    except Exception:
        _console.print(
            "[yellow]⚠ Could not reach the registry. "
            "Check your connection or try again later.[/yellow]"
        )
        return []


def _fetch_skill_meta(client: httpx.Client, skill_name: str) -> Optional[dict]:
    """Download and parse skill.json for a single skill."""
    url = f"{__registry_url__}/{skill_name}/skill.json"
    try:
        resp = client.get(url, headers=HEADERS)
        if resp.status_code != 200:
            return {"name": skill_name, "description": "", "tags": [], "version": ""}
        # GitHub API returns base64-encoded content
        import base64
        content_b64 = resp.json().get("content", "")
        content = base64.b64decode(content_b64).decode("utf-8")
        return json.loads(content)
    except Exception:
        return {"name": skill_name, "description": "", "tags": [], "version": ""}


def fetch_skill_files(skill_name: str) -> list[dict]:
    """
    Return a list of file descriptors for a skill folder on GitHub.

    Each dict has: name, download_url, size.
    Returns an empty list if the skill is not found.
    """
    url = f"{__registry_url__}/{skill_name}"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=HEADERS)
            if resp.status_code == 404:
                return []
            resp.raise_for_status()
            entries = resp.json()
            return [
                {
                    "name": e["name"],
                    "download_url": e.get("download_url", ""),
                    "size": e.get("size", 0),
                }
                for e in entries
                if e.get("type") == "file"
            ]
    except Exception as exc:
        _console.print(f"[red]Registry error: {exc}[/red]")
        return []


def download_file(url: str) -> Optional[bytes]:
    """Download raw file content from a URL. Returns None on failure."""
    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.content
    except Exception:
        return None


def _augment_skills_with_catalog_resources(skills: list[dict]) -> list[dict]:
    """Expand catalog-style skill entries into first-class resource items."""
    if not isinstance(skills, list):
        return []

    expanded: list[dict] = list(skills)
    existing_names = {str(skill.get("name", "")) for skill in expanded if isinstance(skill, dict)}

    for skill in skills:
        if not isinstance(skill, dict):
            continue

        tags = [str(tag).lower() for tag in skill.get("tags", []) if isinstance(tag, str)]
        if "tool-registry" not in tags and "catalog" not in tags:
            continue

        catalog_entries = _load_catalog_repos(str(skill.get("name", "")))
        if not catalog_entries:
            continue

        parent_name = str(skill.get("name", "catalog"))
        for entry in catalog_entries:
            resource_name = entry["name"]
            if resource_name in existing_names:
                continue
            expanded.append(
                {
                    "name": resource_name,
                    "version": skill.get("version", "1.0.0"),
                    "description": entry["description"],
                    "tags": [
                        "resource",
                        "repository",
                        "open-source",
                        f"catalog:{parent_name}",
                        f"domain:{entry['domain']}",
                        "use:research",
                    ],
                    "license": skill.get("license", "SEE-SOURCE"),
                    "examples": 0,
                    "mcp_compatible": False,
                    "author": skill.get("author", "community"),
                    "source": entry["url"],
                    "category": "research",
                    "resource_type": "repository",
                    "repo": entry["repo"],
                    "catalog_parent": parent_name,
                    "catalog_rank": entry["rank"],
                    "display_name": entry["title"],
                }
            )
            existing_names.add(resource_name)

    return expanded


def _load_catalog_repos(skill_name: str) -> list[dict]:
    """Load repo entries from <skill>/catalog.json (local first, then remote)."""
    payload = _load_local_catalog_payload(skill_name)
    if payload is None:
        payload = _load_remote_catalog_payload(skill_name)
    if not isinstance(payload, dict):
        return []

    categories = payload.get("categories", [])
    if not isinstance(categories, list):
        return []

    rows: list[dict] = []
    for category in categories:
        if not isinstance(category, dict):
            continue
        domain_slug = str(category.get("slug", "other")).strip().lower() or "other"
        repos = category.get("repos", [])
        if not isinstance(repos, list):
            continue
        for repo in repos:
            if not isinstance(repo, dict):
                continue
            raw_name = str(repo.get("name", "")).strip()
            if not raw_name:
                continue
            rows.append(
                {
                    "name": f"repo-{_slugify(raw_name)}",
                    "title": raw_name,
                    "repo": str(repo.get("repo", "")).strip(),
                    "url": str(repo.get("url", "")).strip(),
                    "description": str(repo.get("summary", "")).strip(),
                    "domain": domain_slug,
                    "rank": int(repo.get("rank", 0) or 0),
                }
            )

    return rows


def _load_local_catalog_payload(skill_name: str) -> Optional[dict]:
    """Read a catalog.json file from local workspace locations."""
    for path in _skill_candidate_paths(skill_name, "catalog.json"):
        try:
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
    return None


def _load_remote_catalog_payload(skill_name: str) -> Optional[dict]:
    """Read a catalog.json file from remote GitHub registry."""
    url = f"{__registry_url__}/{skill_name}/catalog.json"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=HEADERS)
            if resp.status_code != 200:
                return None
            import base64

            content_b64 = resp.json().get("content", "")
            content = base64.b64decode(content_b64).decode("utf-8")
            return json.loads(content)
    except Exception:
        return None


def _slugify(value: str) -> str:
    """Convert names to lowercase, hyphenated slugs."""
    cleaned = "-".join(value.strip().lower().split())
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
    slug = "".join(ch for ch in cleaned if ch in allowed)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "resource"
