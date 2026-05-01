"""PullNexus CLI — entry point."""

import typer
from rich.console import Console

from pullnexus.commands import search, install, list_skills, submit, info

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

app.command()(search.search)
app.command()(install.install)
app.command(name="pull")(install.install)           # pullnexus pull <skill>  alias
app.command(name="list")(list_skills.list_skills)   # pullnexus list
app.command()(submit.submit)
app.command()(info.info)

if __name__ == "__main__":
    app()
