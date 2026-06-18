"""Tests for the Textual TUI application shell (TSK-27).

Covers initialization, required widget composition, key bindings,
and the repository dependency injection contract.
"""

from pathlib import Path

import pytest

from orcalogy.infra.file_repo import FileLedgerRepository
from orcalogy.tui.app import OrcaLogyApp


@pytest.fixture
def tui_app(tmp_path: Path) -> OrcaLogyApp:
    """TUI app backed by a temporary repository — never touches ~/.orcalogy."""
    repo = FileLedgerRepository(str(tmp_path))
    return OrcaLogyApp(repository=repo)


async def test_tui_initialization(tui_app: OrcaLogyApp) -> None:
    """Verify the app shell starts with the correct title and subtitle."""
    async with tui_app.run_test() as pilot:
        assert pilot.app.TITLE == "OrcaLogy"
        assert pilot.app.SUB_TITLE == "Local-first budget manager"


async def test_tui_has_header_and_footer(tui_app: OrcaLogyApp) -> None:
    """Verify the shell composes exactly one Header and one Footer widget."""
    from textual.widgets import Footer, Header

    async with tui_app.run_test() as pilot:
        assert len(pilot.app.query(Header)) == 1
        assert len(pilot.app.query(Footer)) == 1


async def test_tui_repository_injection(tmp_path: Path) -> None:
    """Verify the injected repository instance is stored and accessible."""
    repo = FileLedgerRepository(str(tmp_path))
    app = OrcaLogyApp(repository=repo)

    async with app.run_test():
        assert app.repository is repo


async def test_tui_quit_binding(tui_app: OrcaLogyApp) -> None:
    """Verify pressing 'q' terminates the app cleanly without raising."""
    async with tui_app.run_test() as pilot:
        await pilot.press("q")
    # Reaching this line confirms the app exited without an exception.
