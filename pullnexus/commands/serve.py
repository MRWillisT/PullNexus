"""pullnexus serve — start the PullNexus MCP server."""

import typer
from rich.console import Console

console = Console()


def serve(
    transport: str = typer.Option(
        "stdio",
        "--transport",
        "-t",
        help="Transport to use: stdio (default) or http.",
    ),
    host: str = typer.Option("127.0.0.1", "--host", help="HTTP host (only used with --transport http)"),
    port: int = typer.Option(7337, "--port", "-p", help="HTTP port (only used with --transport http)"),
):
    """Start the PullNexus MCP server.

    Expose all registry tools (search, recommend, info, install, feedback) to any
    MCP-compatible client — Claude Code, Continue.dev, Cursor, LM Studio, etc.

    \\b
    EXAMPLES:
      pullnexus serve                     # stdio (local Claude / Continue.dev)
      pullnexus serve --transport http    # HTTP on 127.0.0.1:7337
    """
    try:
        from pullnexus.mcp_server import run_stdio, run_http
    except ImportError:
        console.print(
            "[red]MCP server requires the 'mcp' package.[/red]\n"
            "[dim]Install with: pip install pullnexus\\[mcp][/dim]"
        )
        raise typer.Exit(1)

    t = transport.lower().strip()
    if t == "stdio":
        console.print("[dim]Starting PullNexus MCP server over stdio...[/dim]")
        run_stdio()
    elif t in {"http", "streamable-http"}:
        console.print(f"[dim]Starting PullNexus MCP server on http://{host}:{port}/mcp[/dim]")
        run_http(host=host, port=port)
    else:
        console.print(f"[red]Unknown transport '{transport}'. Use: stdio or http.[/red]")
        raise typer.Exit(1)
