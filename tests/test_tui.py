"""Tests for the Textual TUI application shell and dashboard screen (TSK-27/28).

Covers initialization, required widget composition, key bindings,
repository dependency injection, dashboard population, empty state,
and the manual refresh binding.
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


# ---------------------------------------------------------------------------
# TSK-28 — DashboardScreen tests
# ---------------------------------------------------------------------------


async def test_dashboard_is_initial_screen(tui_app: OrcaLogyApp) -> None:
    """Verify DashboardScreen is pushed as the active screen on app mount."""
    from orcalogy.tui.screens import DashboardScreen

    async with tui_app.run_test() as pilot:
        assert isinstance(pilot.app.screen, DashboardScreen)


async def test_dashboard_empty_state(tui_app: OrcaLogyApp) -> None:
    """Verify category table shows one status row when no budget exists yet."""
    from textual.widgets import DataTable

    async with tui_app.run_test() as pilot:
        table = pilot.app.screen.query_one("#category-table", DataTable)
        assert table.row_count == 1


async def test_dashboard_population(tmp_path: Path) -> None:
    """Verify category and transaction tables are populated from live budget data."""
    import datetime

    from textual.widgets import DataTable

    from orcalogy.app.services import (
        InitializeBudgetUseCase,
        RegisterTransactionUseCase,
    )
    from orcalogy.domain.models import Money, Transaction

    repo = FileLedgerRepository(str(tmp_path))
    month = datetime.date.today().strftime("%Y-%m")

    InitializeBudgetUseCase(repo).execute(month, {
        "Food": Money("500.00"),
        "Transport": Money("150.00"),
    })
    RegisterTransactionUseCase(repo).execute(
        Transaction(
            tx_id="tx-dash-01",
            date=datetime.date.today(),
            category="Food",
            amount=Money("200.00"),
            description="Supermarket",
        )
    )

    async with OrcaLogyApp(repository=repo).run_test() as pilot:
        screen = pilot.app.screen
        category_table = screen.query_one("#category-table", DataTable)
        tx_table = screen.query_one("#tx-table", DataTable)

        # Two categories were initialized — expect two rows
        assert category_table.row_count == 2
        # One transaction was registered — expect one row
        assert tx_table.row_count == 1


async def test_dashboard_recent_tx_capped_at_ten(tmp_path: Path) -> None:
    """Verify the transaction table never exceeds 10 rows regardless of total count."""
    import datetime

    from textual.widgets import DataTable

    from orcalogy.app.services import (
        InitializeBudgetUseCase,
        RegisterTransactionUseCase,
    )
    from orcalogy.domain.models import Money, Transaction

    repo = FileLedgerRepository(str(tmp_path))
    month = datetime.date.today().strftime("%Y-%m")

    InitializeBudgetUseCase(repo).execute(month, {"Food": Money("9999.00")})

    for i in range(13):
        RegisterTransactionUseCase(repo).execute(
            Transaction(
                tx_id=f"tx-{i:02d}",
                date=datetime.date.today(),
                category="Food",
                amount=Money("10.00"),
                description=f"Purchase {i}",
            )
        )

    async with OrcaLogyApp(repository=repo).run_test() as pilot:
        tx_table = pilot.app.screen.query_one("#tx-table", DataTable)
        assert tx_table.row_count == 10


async def test_dashboard_refresh_binding(tui_app: OrcaLogyApp) -> None:
    """Verify pressing 'r' repopulates the dashboard tables without raising."""
    async with tui_app.run_test() as pilot:
        await pilot.press("r")
        # No exception raised = refresh completed successfully in empty state.
