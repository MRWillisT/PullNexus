import typer
from rich.console import Console

from .commands import search, install, list_skills, submit

console = Console()

app = typer.Typer(
    name="pullnexus",
    help="Pull Nexus — Pull from the Nexus. Give back to the Nexus.",
    rich_markup_mode="markdown",
    add_completion=True,
)

app.command()(search.search)
app.command()(install.install)
app.command(name="pull")(install.install)   # pullnexus pull <skill> alias
app.command()(list_skills.list_skills)
app.command()(submit.submit)

if __name__ == "__main__":
    app()