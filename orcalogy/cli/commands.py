"""Typer CLI root application controller for OrcaLogy.

This module wires up the top-level CLI entry point. It defines the 'orca'
command group, registers the --version flag so users can check what is
installed, and enables shell auto-completion via Typer's built-in hook.
"""

import typer

VERSION = "0.1.0"

app = typer.Typer(
    name="orca",
    help="OrcaLogy — local-first budget management CLI.",
    no_args_is_help=True,
    invoke_without_command=True,
    add_completion=True,
)


@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-V",
        is_eager=True,
        help="Show the installed OrcaLogy version and exit.",
    ),
) -> None:
    """OrcaLogy budget CLI — run a subcommand or use --help."""
    if version:
        typer.echo(f"orca version {VERSION}")
        raise typer.Exit()
