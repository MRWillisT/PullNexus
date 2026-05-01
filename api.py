import httpx
from pathlib import Path

# Update this to your actual repo
REGISTRY_URL = "https://api.github.com/repos/MRWillisT/PullNexus/contents/skills"
HEADERS = {"Accept": "application/vnd.github.v3+json"}

def fetch_skills():
    """Fetch skill list from GitHub registry with graceful fallback"""
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(REGISTRY_URL, headers=HEADERS)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        # Graceful fail while repo is private or empty
        console = Console()
        console.print("[yellow]⚠️ Could not reach registry (repo private or empty).[/yellow]")
        return []