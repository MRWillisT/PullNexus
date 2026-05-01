import typer
from rich.console import Console
from pathlib import Path

console = Console()

def submit(path: str = typer.Argument(..., help="Path to your skill folder")):
    """Submit a new skill to the Nexus (placeholder for MVP)"""
    skill_path = Path(path)
    if not skill_path.exists():
        console.print("[red]✗ Path does not exist[/red]")
        return

    console.print(f"[green]✓ Skill folder found: {skill_path}[/green]")
    console.print("[yellow]→ For MVP: Please open a PR to the skills/ folder on GitHub[/yellow]")
    console.print("[dim]Full auto-submit coming in v0.2[/dim]")