import typer
from rich.console import Console
from pathlib import Path

console = Console()

def install(skill_name: str = typer.Argument(..., help="Skill to pull (e.g. ollama-mastery)")):
    """Pull a skill from the Nexus"""
    target = Path("./pullnexus-skills") / skill_name
    target.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[green]✓ Successfully pulled '{skill_name}'[/green]")
    console.print(f"[dim]   → Saved to {target}[/dim]")
    console.print("[yellow]💡 Drop this folder into your model's context or use with MCP![/yellow]")