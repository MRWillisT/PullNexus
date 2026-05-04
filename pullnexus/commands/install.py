"""pullnexus install / pull — download a skill from the Nexus."""

import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pullnexus.api import fetch_skill_files, download_file, fetch_index, fetch_skill_json

_HF_HELP = (
    "This entry lives on HuggingFace. "
    "Install the HuggingFace hub library first:\n"
    "  [bold]pip install huggingface_hub[/bold]"
)

console = Console()

_SKILLS_DIR = Path("./pullnexus-skills")

# Resource types that cannot be downloaded as a file package.
_NON_INSTALLABLE_TYPES = {"repository", "eval", "policy"}


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

    # Reject non-installable resource types before hitting the network.
    meta = fetch_skill_json(skill_name)
    if meta is not None:
        resource_type = str(meta.get("resource_type", "skill")).lower()
        if resource_type in _NON_INSTALLABLE_TYPES:
            console.print(
                f"[yellow]⚠ '{skill_name}' is a [bold]{resource_type}[/bold] resource — "
                f"it cannot be pulled as a file package.[/yellow]\n"
                f"Run [bold]pullnexus info {skill_name}[/bold] to view details and links."
            )
            raise typer.Exit(1)

        # HuggingFace-sourced entries: delegate to huggingface_hub
        if str(meta.get("source", "")).lower() == "huggingface":
            hf_repo = meta.get("hf_repo")
            if not hf_repo:
                console.print(f"[red]✗ '{skill_name}' is missing 'hf_repo' in its metadata.[/red]")
                raise typer.Exit(1)
            _install_from_huggingface(skill_name, hf_repo, meta, output, force)
            raise typer.Exit(0)

        # External-only entries (installable: false) with a repo field: offer git clone
        if not meta.get("installable", True):
            source_url = meta.get("source", "")
            repo = meta.get("repo", "")
            clone_target = output / skill_name

            console.print(
                f"\n[bold cyan]{skill_name}[/bold cyan] is hosted at an external repository.\n"
                f"[dim]{meta.get('description', '')}[/dim]\n"
            )
            if source_url:
                console.print(f"[bold]Source:[/bold] {source_url}\n")

            if repo and (not clone_target.exists() or force):
                clone_url = f"https://github.com/{repo}"
                do_clone = typer.confirm(
                    f"Clone {clone_url} into {clone_target}?",
                    default=True,
                )
                if do_clone:
                    import subprocess
                    clone_target.parent.mkdir(parents=True, exist_ok=True)
                    console.print(f"[dim]Cloning {clone_url}…[/dim]")
                    result = subprocess.run(
                        ["git", "clone", clone_url, str(clone_target)],
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode == 0:
                        console.print(f"[green]✓ Cloned → {clone_target}[/green]")
                        console.print(
                            f"\n[bold]Next steps:[/bold]\n"
                            f"  • Open [cyan]{clone_target}[/cyan] to explore the repo\n"
                            f"  • Check the README for setup instructions"
                        )
                    else:
                        console.print(f"[red]✗ Clone failed:[/red] {result.stderr.strip()}")
                        raise typer.Exit(1)
                else:
                    console.print(
                        f"\n[dim]To clone manually:[/dim]\n"
                        f"  git clone {clone_url} ./pullnexus-skills/{skill_name}"
                    )
            elif clone_target.exists():
                console.print(f"[yellow]⚠ Already exists at {clone_target}[/yellow]  (use --force to re-clone)")
            raise typer.Exit(0)

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


def _install_from_huggingface(
    skill_name: str,
    hf_repo: str,
    meta: dict,
    output: Path,
    force: bool,
) -> None:
    """Download a HuggingFace dataset or model repo into the local skills directory."""
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        console.print(f"[red]\u2717 {_HF_HELP}[/red]")
        raise typer.Exit(1)

    target = output / skill_name
    if target.exists() and not force:
        console.print(
            f"[yellow]\u26a0 '{skill_name}' already exists at {target}[/yellow]\n"
            "Use [bold]--force[/bold] to overwrite."
        )
        raise typer.Exit(1)

    repo_type = meta.get("hf_repo_type", "dataset")
    console.print(
        f"[bold]Pulling from HuggingFace[/bold] ([cyan]{hf_repo}[/cyan])\n"
        f"  type : {repo_type}\n"
        f"  dest : {target}\n"
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Downloading {hf_repo}…", total=None)
        try:
            local_dir = snapshot_download(
                repo_id=hf_repo,
                repo_type=repo_type,
                local_dir=str(target),
                local_dir_use_symlinks=False,
            )
        except Exception as exc:
            console.print(f"[red]\u2717 HuggingFace download failed: {exc}[/red]")
            raise typer.Exit(1)

    console.print(f"[green]\u2713 Downloaded '{skill_name}' \u2192 {local_dir}[/green]")
    console.print(
        "\n[bold]Next steps:[/bold]\n"
        f"  \u2022 Browse [cyan]{target}[/cyan] for JSONL files and data cards\n"
        "  \u2022 Load into your fine-tuning pipeline or RAG setup\n"
        "  \u2022 Reference [cyan]README.md[/cyan] inside the folder for usage details"
    )
