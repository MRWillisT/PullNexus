import typer
from rich.console import Console
from ..api import fetch_skills

console = Console()

def search(query: str = typer.Argument(..., help="Search term (e.g. rag, mcp, ollama)")):
    """Search skills in the Nexus"""
    skills = fetch_skills()
    results = [s for s in skills if query.lower() in s["name"].lower()]

    if not results:
        console.print(f"[red]No skills found for '{query}'[/red]")
        return

    console.print(f"[bold]Found {len(results)} skill(s) for '{query}':[/bold]")
    for skill in results[:15]:
        name = skill["name"]
        console.print(f"• [bold cyan]{name}[/bold cyan]")