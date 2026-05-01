import typer
from rich.console import Console
from ..api import fetch_skills

console = Console()

def list_skills():
    """List all available skills in the Nexus"""
    skills = fetch_skills()
    
    if not skills:
        console.print("[yellow]No skills found yet. Be the first to submit one![/yellow]")
        return

    console.print(f"[bold]Available skills ({len(skills)}):[/bold]")
    for skill in skills:
        console.print(f"• [bold]{skill['name']}[/bold]")