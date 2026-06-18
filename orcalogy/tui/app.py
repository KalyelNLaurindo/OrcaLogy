"""Textual TUI application shell for OrcaLogy.

This module defines the root App class that boots the interactive terminal
dashboard. It acts as the composition root for all TUI screens and binds
the global keyboard shortcuts that users can trigger from any screen.
"""

from __future__ import annotations

from typing import ClassVar

from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.widgets import Footer, Header

from orcalogy.infra.file_repo import FileLedgerRepository
from orcalogy.tui.screens import DashboardScreen


class OrcaLogyApp(App[None]):
    """Root TUI application — owns all screens and global key bindings.

    Receives a fully-constructed repository so the TUI layer never creates
    its own I/O connections, keeping the hexagonal boundary intact.
    """

    TITLE = "OrcaLogy"
    SUB_TITLE = "Local-first budget manager"

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("ctrl+d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self, repository: FileLedgerRepository) -> None:
        super().__init__()
        self.repository: FileLedgerRepository = repository

    def compose(self) -> ComposeResult:
        """Yield the persistent shell chrome visible on every screen."""
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        """Push the dashboard as the first active screen after the shell mounts."""
        self.push_screen(DashboardScreen())
