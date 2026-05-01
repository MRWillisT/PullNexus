"""PullNexus CLI — entry point."""

import typer
from rich.console import Console

from pullnexus.commands import search, install, list_skills, submit, info, recommend, categories, types

console = Console()

app = typer.Typer(
    name="pullnexus",
    help=(
        "**PullNexus** — the open registry of skills, tools, and knowledge for local LLMs.\n\n"
        "Pull from the Nexus. Give back to the Nexus. Keep local AI smart."
    ),
    rich_markup_mode="markdown",
    add_completion=True,
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    list_only: bool = typer.Option(
        False,
        "--list",
        help="List skills (alias for `pullnexus list`).",
    ),
    all_sources: bool = typer.Option(
        False,
        "--all",
        help="Include external sources when used with --list.",
    ),
):
    """Top-level options and command routing for PullNexus CLI."""
    if list_only:
        list_skills.list_skills(
            tag=None,
            category=None,
            sort="name",
            group_by=None,
            show_all=all_sources,
        )
        raise typer.Exit(0)

    # Keep normal no-args help behavior when invoked without a subcommand.
    if ctx.invoked_subcommand is None and not list_only:
        raise typer.Exit(0)

app.command()(search.search)
app.command()(install.install)
app.command(name="pull")(install.install)           # pullnexus pull <skill>  alias
app.command(name="list")(list_skills.list_skills)   # pullnexus list
app.command()(submit.submit)
app.command()(info.info)
app.command()(recommend.recommend)
app.command()(categories.categories)
app.command()(types.types)

if __name__ == "__main__":
    app()
