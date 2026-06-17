"""Application entry point.

Exposes the Typer 'app' object so Poetry's script binding
('orca = "orcalogy.main:app"') can locate and launch the CLI.
"""

from orcalogy.cli.commands import app

__all__ = ["app"]
