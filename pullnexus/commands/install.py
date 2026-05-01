"""pullnexus install / pull — download a skill from the Nexus."""

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pullnexus.api import fetch_skill_files, download_file, fetch_index

console = Console()

_SKILLS_DIR = Path("./pullnexus-skills")


def install(
    skill_name: str = typer.Argument(..., help="Skill to pull (e.g. python-advanced-debugging)"),
    output: Path = typer.Option(
        _SKILLS_DIR,
        "--output", "-o",
        help="Directory to save the skill into",
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing skill"),
):
    """Pull a skill from the Nexus and save it locally."""

    target = output / skill_name

    if target.exists() and not force:
        console.print(
            f"[yellow]⚠ Skill '{skill_name}' already exists at {target}[/yellow]\n"
            "Use [bold]--force[/bold] to overwrite."
        )
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(f"Fetching skill list for '{skill_name}'…", total=None)

        files = fetch_skill_files(skill_name)

        if not files:
            progress.stop()
            # Try to suggest similar skills
            console.print(f"[red]✗ Skill '{skill_name}' not found in the registry.[/red]")
            _suggest_similar(skill_name)
            raise typer.Exit(1)

        target.mkdir(parents=True, exist_ok=True)

        saved = []
        failed = []
        for file_info in files:
            fname = file_info["name"]
            url = file_info["download_url"]
            progress.update(task, description=f"Downloading {fname}…")

            if not url:
                failed.append(fname)
                continue

            content = download_file(url)
            if content is None:
                failed.append(fname)
                continue

            (target / fname).write_bytes(content)
            saved.append(fname)

    # Report results
    if saved:
        console.print(f"[green]✓ Pulled '{skill_name}' → {target}[/green]")
        for fname in saved:
            console.print(f"  [dim]• {fname}[/dim]")

    if failed:
        console.print(f"[yellow]⚠ {len(failed)} file(s) failed to download:[/yellow]")
        for fname in failed:
            console.print(f"  [dim]• {fname}[/dim]")

    if saved:
        console.print(
            "\n[bold]Next steps:[/bold]\n"
            f"  • Drop [cyan]{target}[/cyan] into your model's context window\n"
            "  • Or reference [cyan]examples.jsonl[/cyan] for fine-tuning\n"
            "  • Or load [cyan]skill.json[/cyan] via your MCP integration"
        )


def _suggest_similar(skill_name: str) -> None:
    """Print similar skill names if any are found."""
    skills = fetch_index()
    if not skills:
        return
    q = skill_name.lower()
    parts = q.replace("-", " ").split()
    matches = [
        s["name"]
        for s in skills
        if any(p in s["name"].lower() for p in parts)
    ]
    if matches:
        console.print("\n[dim]Did you mean one of these?[/dim]")
        for m in matches[:5]:
            console.print(f"  [cyan]{m}[/cyan]")
