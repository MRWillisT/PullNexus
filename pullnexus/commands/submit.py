"""pullnexus submit — validate and submit a skill to the Nexus."""

import json
import re
from datetime import date
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

REQUIRED_FILES = {"skill.json", "examples.jsonl", "README.md"}
OPTIONAL_FILES = {"eval.jsonl", "tools"}

REQUIRED_SKILL_FIELDS = {"name", "version", "description", "tags", "license"}
PROVENANCE_FIELDS = {"source", "author"}
QUALITY_FIELDS = {"maturity", "maintained", "last_verified"}

# Types that don't require training examples — their validation is lighter.
_NO_EXAMPLES_REQUIRED = {"tool", "playbook", "dataset", "eval", "policy", "template", "environment", "repository"}

# Fields collected per resource type in wizard mode
_WIZARD_STEPS: dict[str, list[dict]] = {
    "template": [
        {"key": "name", "prompt": "Slug name (e.g. mistral-7b-8gb-llama-server)", "required": True},
        {"key": "description", "prompt": "One sentence — what does this run, on what hardware, what's the trick?", "required": True},
        {"key": "tags_raw", "prompt": "Tags, comma-separated (e.g. llama.cpp,7b,8gb-vram,flash-attention)", "required": True},
        {"key": "vram_gb", "prompt": "VRAM required in GB (number only, e.g. 12)", "required": True},
        {"key": "command", "prompt": "Paste the exact command / config block", "required": True},
        {"key": "source", "prompt": "Source URL (tweet, post, repo) [optional, Enter to skip]", "required": False},
        {"key": "author", "prompt": "Author / handle for credit [optional, Enter to skip]", "required": False},
        {"key": "license", "prompt": "License [default: CC0-1.0]", "required": False, "default": "CC0-1.0"},
    ],
    "policy": [
        {"key": "name", "prompt": "Slug name (e.g. kv-cache-vram-best-practices)", "required": True},
        {"key": "description", "prompt": "One sentence — what rule/guidance does this capture?", "required": True},
        {"key": "tags_raw", "prompt": "Tags, comma-separated", "required": True},
        {"key": "key_rules_raw", "prompt": "Key rules, one per line — type END on its own line when done", "required": True, "multiline": True},
        {"key": "source", "prompt": "Source URL [optional, Enter to skip]", "required": False},
        {"key": "author", "prompt": "Author / handle [optional, Enter to skip]", "required": False},
        {"key": "license", "prompt": "License [default: CC0-1.0]", "required": False, "default": "CC0-1.0"},
    ],
    "playbook": [
        {"key": "name", "prompt": "Slug name (e.g. ollama-open-webui-setup)", "required": True},
        {"key": "description", "prompt": "One sentence — what does this playbook walk you through?", "required": True},
        {"key": "tags_raw", "prompt": "Tags, comma-separated", "required": True},
        {"key": "platform_raw", "prompt": "Platforms supported, comma-separated (e.g. Windows,Mac,Linux)", "required": False, "default": "Linux"},
        {"key": "source", "prompt": "Source URL [optional, Enter to skip]", "required": False},
        {"key": "author", "prompt": "Author / handle [optional, Enter to skip]", "required": False},
        {"key": "license", "prompt": "License [default: MIT]", "required": False, "default": "MIT"},
    ],
    "skill": [
        {"key": "name", "prompt": "Slug name (e.g. extract-action-items)", "required": True},
        {"key": "description", "prompt": "One sentence — what does this skill do?", "required": True},
        {"key": "tags_raw", "prompt": "Tags, comma-separated", "required": True},
        {"key": "source", "prompt": "Source URL [optional, Enter to skip]", "required": False},
        {"key": "author", "prompt": "Author / handle [optional, Enter to skip]", "required": False},
        {"key": "license", "prompt": "License [default: MIT]", "required": False, "default": "MIT"},
    ],
}
# Default steps for types not explicitly listed
_WIZARD_STEPS_DEFAULT = [
    {"key": "name", "prompt": "Slug name", "required": True},
    {"key": "description", "prompt": "One sentence description", "required": True},
    {"key": "tags_raw", "prompt": "Tags, comma-separated", "required": True},
    {"key": "source", "prompt": "Source URL [optional, Enter to skip]", "required": False},
    {"key": "author", "prompt": "Author / handle [optional, Enter to skip]", "required": False},
    {"key": "license", "prompt": "License [default: MIT]", "required": False, "default": "MIT"},
]

_VALID_TYPES = {"skill", "tool", "template", "policy", "playbook", "dataset", "eval", "environment", "repository"}


def _slug(value: str) -> str:
    """Normalize a name to a URL-safe slug."""
    return re.sub(r"[^a-z0-9-]", "-", value.strip().lower()).strip("-")


def _parse_llama_command(command: str) -> dict:
    """Best-effort parse of llama-server / ollama flags into a config dict."""
    params: dict = {}
    # Extract --flag value pairs
    for match in re.finditer(r"--([a-z_-]+)\s+([^\s\\]+)", command):
        key = match.group(1).replace("-", "_")
        val = match.group(2).strip("'\"")
        # Try numeric coercion
        try:
            params[key] = int(val)
        except ValueError:
            try:
                params[key] = float(val)
            except ValueError:
                params[key] = val
    # Boolean flags (present without value)
    for match in re.finditer(r"(?:^|\s)-(fa|fit)\b", command):
        params[match.group(1)] = True
    return params


def _run_wizard(resource_type: str, output_dir: Path) -> Path:
    """Interactive wizard — collects fields and writes skill.json + README.md."""
    steps = _WIZARD_STEPS.get(resource_type, _WIZARD_STEPS_DEFAULT)
    today = date.today().isoformat()

    console.print(Panel(
        f"[bold cyan]PullNexus Submit Wizard[/bold cyan]\n"
        f"Type: [yellow]{resource_type}[/yellow]  |  "
        "Press Enter to accept [dim]defaults[/dim]. Type [dim]END[/dim] to finish multi-line inputs.",
        border_style="cyan",
    ))
    console.print()

    collected: dict = {}
    for step in steps:
        key = step["key"]
        prompt_text = step["prompt"]
        default = step.get("default", "")
        multiline = step.get("multiline", False)

        if multiline:
            console.print(f"[bold]{prompt_text}[/bold]")
            lines = []
            while True:
                line = typer.prompt("  ", default="", show_default=False)
                if line.strip().upper() == "END":
                    break
                if line.strip():
                    lines.append(line.strip())
            collected[key] = lines
        else:
            value = typer.prompt(f"[bold]{prompt_text}[/bold]", default=default, show_default=bool(default))
            collected[key] = value.strip()

    # Build skill.json
    name = _slug(collected.get("name", "unnamed"))
    tags_raw = collected.get("tags_raw", "")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    if f"use:{resource_type}" not in tags:
        tags.append(f"use:{resource_type}")
    if resource_type not in tags:
        tags.insert(0, resource_type)

    meta: dict = {
        "name": name,
        "resource_type": resource_type,
        "version": "1.0.0",
        "description": collected.get("description", ""),
        "tags": tags,
        "license": collected.get("license") or "MIT",
        "author": collected.get("author") or "Community",
        "source": collected.get("source") or "",
        "installable": False,
        "category": "community",
        "maturity": "community",
        "maintained": "community",
        "last_verified": today,
    }

    # Type-specific extras
    if resource_type == "template":
        vram_raw = collected.get("vram_gb", "0")
        try:
            vram = int(vram_raw)
        except ValueError:
            vram = 0
        command = collected.get("command", "")
        meta["hardware_requirements"] = {"vram_gb": vram}
        meta["config_params"] = _parse_llama_command(command) or {"raw": command}
        if command:
            meta["config_params"]["_raw_command"] = command.strip()
    elif resource_type == "policy":
        meta["key_rules"] = collected.get("key_rules_raw", [])
    elif resource_type == "playbook":
        platforms_raw = collected.get("platform_raw", "Linux")
        meta["platforms"] = [p.strip() for p in platforms_raw.split(",") if p.strip()]

    # Write output
    skill_dir = output_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "skill.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Generate a minimal README
    readme_lines = [
        f"# {name}",
        "",
        meta["description"],
        "",
        f"**Type:** {resource_type}  ",
        f"**License:** {meta['license']}  ",
        f"**Author:** {meta['author']}  ",
    ]
    if meta.get("source"):
        readme_lines.append(f"**Source:** {meta['source']}  ")
    if resource_type == "template" and meta.get("hardware_requirements"):
        readme_lines += ["", f"**VRAM required:** {meta['hardware_requirements'].get('vram_gb')}GB"]
        raw_cmd = meta.get("config_params", {}).get("_raw_command", "")
        if raw_cmd:
            readme_lines += ["", "## Command", "", "```bash", raw_cmd, "```"]
    elif resource_type == "policy" and meta.get("key_rules"):
        readme_lines += ["", "## Rules", ""]
        for rule in meta["key_rules"]:
            readme_lines.append(f"- {rule}")
    readme_lines += ["", f"*Last verified: {today}*", ""]
    (skill_dir / "README.md").write_text("\n".join(readme_lines), encoding="utf-8")

    console.print(f"\n[green]✓ Created submission folder:[/green] {skill_dir.resolve()}")
    console.print(f"  [dim]• skill.json[/dim]")
    console.print(f"  [dim]• README.md[/dim]")
    return skill_dir


def submit(
    path: Optional[str] = typer.Argument(None, help="Path to your skill folder (omit to use --interactive)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate only — don't open a PR"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Run the step-by-step submission wizard"),
    resource_type: str = typer.Option("template", "--type", "-t", help=f"Resource type for wizard mode. One of: {', '.join(sorted(_VALID_TYPES))}"),
    output: str = typer.Option("submissions", "--output", "-o", help="Output directory for wizard-generated folders"),
):
    """Validate a skill folder and submit it to the Nexus via GitHub PR.

    Run with [bold]--interactive[/bold] to use the step-by-step wizard instead of
    pointing at an existing folder:

      pullnexus submit --interactive --type template
    """
    # ── Wizard mode ─────────────────────────────────────────────────────────
    if interactive:
        rtype = resource_type.lower().strip()
        if rtype not in _VALID_TYPES:
            console.print(f"[red]✗ Unknown type '{rtype}'. Valid: {', '.join(sorted(_VALID_TYPES))}[/red]")
            raise typer.Exit(1)
        out_dir = Path(output)
        skill_path = _run_wizard(rtype, out_dir)
        # Fall through to validation with the generated folder
    elif path is None:
        console.print(
            "[yellow]Tip:[/yellow] Provide a folder path, or use [cyan]--interactive[/cyan] "
            "to build one with the wizard.\n\n"
            "  [dim]pullnexus submit --interactive --type template[/dim]"
        )
        raise typer.Exit(0)
    else:
        skill_path = Path(path)

    # ── Validation ───────────────────────────────────────────────────────────
    console.print(f"\n[bold]Validating skill at:[/bold] {skill_path.resolve()}\n")

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Folder must exist
    if not skill_path.exists():
        console.print("[red]✗ Path does not exist.[/red]")
        raise typer.Exit(1)
    if not skill_path.is_dir():
        console.print("[red]✗ Path must be a directory (skill folder).[/red]")
        raise typer.Exit(1)

    # 2. Required files (examples.jsonl not required for non-skill types)
    existing = {f.name for f in skill_path.iterdir()}

    # Peek at resource_type before full validation
    raw_meta: dict = {}
    if "skill.json" in existing:
        try:
            raw_meta = json.loads((skill_path / "skill.json").read_text(encoding="utf-8"))
        except Exception:
            pass
    resource_type = str(raw_meta.get("resource_type", "skill")).lower()

    required_files = {"skill.json", "README.md"}
    if resource_type not in _NO_EXAMPLES_REQUIRED:
        required_files.add("examples.jsonl")

    for required in required_files:
        if required not in existing:
            errors.append(f"Missing required file: {required}")

    for optional in OPTIONAL_FILES:
        if optional not in existing:
            warnings.append(f"Optional file missing (recommended): {optional}")

    # 3. Validate skill.json
    skill_meta = {}
    if "skill.json" in existing:
        try:
            skill_meta = json.loads((skill_path / "skill.json").read_text(encoding="utf-8"))
            for field in REQUIRED_SKILL_FIELDS:
                if not skill_meta.get(field):
                    errors.append(f"skill.json missing required field: '{field}'")
            if not isinstance(skill_meta.get("tags", []), list):
                errors.append("skill.json: 'tags' must be a list")
            if skill_meta.get("tags") and len(skill_meta["tags"]) < 1:
                warnings.append("skill.json: add at least one tag for discoverability")

            # Provenance checks (warnings, not errors)
            for field in PROVENANCE_FIELDS:
                if not skill_meta.get(field):
                    warnings.append(f"skill.json: missing provenance field '{field}' (recommended)")

            # Quality metadata checks (warnings)
            for field in QUALITY_FIELDS:
                if not skill_meta.get(field):
                    warnings.append(f"skill.json: missing quality field '{field}' (recommended)")

            # Type-specific validation
            detected_type = str(skill_meta.get("resource_type", "skill")).lower()
            if detected_type == "tool" and not skill_meta.get("repo"):
                warnings.append("skill.json: 'tool' resources should include a 'repo' field")
            if detected_type == "dataset" and not skill_meta.get("formats"):
                warnings.append("skill.json: 'dataset' resources should list supported 'formats'")
            if detected_type == "eval" and not skill_meta.get("related"):
                warnings.append("skill.json: 'eval' resources should list 'related' resources they evaluate")
            if detected_type == "playbook" and not skill_meta.get("compatibility"):
                warnings.append("skill.json: 'playbook' resources should include a 'compatibility' block")

        except json.JSONDecodeError as exc:
            errors.append(f"skill.json is not valid JSON: {exc}")

    # 4. Validate examples.jsonl (only required/meaningful for skill type)
    example_count = 0
    if "examples.jsonl" in existing:
        try:
            lines = [
                line for line in
                (skill_path / "examples.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            for i, line in enumerate(lines, 1):
                obj = json.loads(line)
                if "conversations" not in obj and "messages" not in obj:
                    errors.append(
                        f"examples.jsonl line {i}: must have 'conversations' or 'messages' key"
                    )
                    break
            example_count = len(lines)
            detected_type = str(skill_meta.get("resource_type", "skill")).lower()
            if detected_type not in _NO_EXAMPLES_REQUIRED and example_count < 3:
                warnings.append(
                    f"examples.jsonl has only {example_count} example(s). "
                    "Aim for at least 5 for better quality."
                )
        except json.JSONDecodeError as exc:
            errors.append(f"examples.jsonl contains invalid JSON: {exc}")

    # 5. Validate eval.jsonl if present
    eval_count = 0
    if "eval.jsonl" in existing:
        try:
            lines = [
                line for line in
                (skill_path / "eval.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            eval_count = len(lines)
            for i, line in enumerate(lines, 1):
                obj = json.loads(line)
                for field in ("id", "input", "expected_behavior"):
                    if field not in obj:
                        warnings.append(f"eval.jsonl line {i}: missing recommended field '{field}'")
                        break
        except json.JSONDecodeError as exc:
            errors.append(f"eval.jsonl contains invalid JSON: {exc}")

    # Print validation report
    table = Table(show_header=False, border_style="dim", padding=(0, 1))
    table.add_column("Status", style="bold", width=4)
    table.add_column("Detail")

    for err in errors:
        table.add_row("[red]✗[/red]", err)
    for warn in warnings:
        table.add_row("[yellow]⚠[/yellow]", warn)
    if not errors and not warnings:
        table.add_row("[green]✓[/green]", "All checks passed!")
    elif not errors:
        table.add_row("[green]✓[/green]", "Required checks passed (see warnings above)")

    console.print(table)

    if errors:
        console.print(
            f"\n[red]✗ Validation failed with {len(errors)} error(s). "
            "Fix them before submitting.[/red]"
        )
        raise typer.Exit(1)

    skill_name = skill_meta.get("name", skill_path.name)
    console.print(f"\n[green]✓ Skill '{skill_name}' is ready to submit![/green]")
    console.print(f"  [dim]• {example_count} example(s) in examples.jsonl[/dim]")
    if eval_count:
        console.print(f"  [dim]• {eval_count} eval case(s) in eval.jsonl[/dim]")

    if dry_run:
        console.print("\n[dim]Dry run — skipping PR instructions.[/dim]")
        return

    console.print(
        "\n[bold]To submit this skill:[/bold]\n"
        "  1. Fork [link=https://github.com/MRWillisT/PullNexus]github.com/MRWillisT/PullNexus[/link]\n"
        f"  2. Copy your skill folder to [cyan]skills/{skill_name}/[/cyan]\n"
        "  3. Open a Pull Request against the [cyan]main[/cyan] branch\n"
        "  4. A maintainer will review and merge it into the registry\n\n"
        "[dim]Full contribution guide: "
        "[link=https://github.com/MRWillisT/PullNexus/blob/main/CONTRIBUTING.md]CONTRIBUTING.md[/link][/dim]"
    )
