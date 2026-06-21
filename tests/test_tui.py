"""Tests for the Textual TUI application shell and screens.

Covers MainMenuScreen, DashboardScreen, BudgetInitDialog, CloseCycleDialog,
and TransactionEntryDialog.
"""

from pathlib import Path

import pytest

from orcalogy.domain.models import Money
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
# Menu and Navigation Tests
# ---------------------------------------------------------------------------


async def test_main_menu_is_initial_screen(tui_app: OrcaLogyApp) -> None:
    """Verify MainMenuScreen is pushed as the active screen on app mount."""
    from orcalogy.tui.screens import MainMenuScreen

    async with tui_app.run_test() as pilot:
        assert isinstance(pilot.app.screen, MainMenuScreen)


async def test_navigate_to_dashboard_and_back(tui_app: OrcaLogyApp) -> None:
    """Verify we can enter the dashboard and return to the main menu."""
    from orcalogy.tui.screens import DashboardScreen, MainMenuScreen

    async with tui_app.run_test() as pilot:
        await pilot.click("#btn-goto-dashboard")
        await pilot.pause()
        assert isinstance(pilot.app.screen, DashboardScreen)

        # Press escape to return to menu
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(pilot.app.screen, MainMenuScreen)


# ---------------------------------------------------------------------------
# DashboardScreen & Budget Initialization Tests
# ---------------------------------------------------------------------------


async def test_dashboard_empty_state(tui_app: OrcaLogyApp) -> None:
    """Verify category table shows one status row when no budget exists yet."""
    from textual.widgets import DataTable

    async with tui_app.run_test() as pilot:
        await pilot.click("#btn-goto-dashboard")
        await pilot.pause()
        table = pilot.app.screen.query_one("#category-table", DataTable)
        assert table.row_count == 1


async def test_budget_init_dialog_submits_valid(tmp_path: Path) -> None:
    """Verify we can create a budget using the BudgetInitDialog."""
    import datetime

    from textual.widgets import Input

    from orcalogy.tui.screens import MainMenuScreen

    repo = FileLedgerRepository(str(tmp_path))
    app = OrcaLogyApp(repository=repo)

    async with app.run_test() as pilot:
        await pilot.click("#btn-init-budget")
        await pilot.pause()

        screen = pilot.app.screen
        month = datetime.date.today().strftime("%Y-%m")
        screen.query_one("#input-month", Input).value = month
        screen.query_one("#input-cat-name", Input).value = "Food"
        screen.query_one("#input-cat-limit", Input).value = "600.00"

        await pilot.click("#btn-add-cat")
        await pilot.pause()

        await pilot.click("#btn-save")
        await pilot.pause()

        assert isinstance(pilot.app.screen, MainMenuScreen)
        budget = repo.get_budget(month)
        assert budget is not None
        assert "Food" in budget.categories
        assert budget.categories["Food"].limit == Money("600.00")


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
        await pilot.click("#btn-goto-dashboard")
        await pilot.pause()

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
        await pilot.click("#btn-goto-dashboard")
        await pilot.pause()

        tx_table = pilot.app.screen.query_one("#tx-table", DataTable)
        assert tx_table.row_count == 10


# ---------------------------------------------------------------------------
# TransactionEntryDialog tests
# ---------------------------------------------------------------------------


@pytest.fixture
def tui_app_with_budget(tmp_path: Path) -> OrcaLogyApp:
    """TUI app with a seeded budget — gives the modal a valid context to submit into."""
    import datetime

    from orcalogy.app.services import InitializeBudgetUseCase
    from orcalogy.domain.models import Money

    repo = FileLedgerRepository(str(tmp_path))
    month = datetime.date.today().strftime("%Y-%m")
    InitializeBudgetUseCase(repo).execute(
        month, {"Food": Money("500.00"), "Transport": Money("100.00")}
    )
    return OrcaLogyApp(repository=repo)


async def test_transaction_entry_modal_compose(
    tui_app_with_budget: OrcaLogyApp,
) -> None:
    """Verify the modal renders all required input fields and action buttons."""
    from textual.widgets import Button, Input

    from orcalogy.tui.screens import TransactionEntryDialog

    async with tui_app_with_budget.run_test() as pilot:
        await pilot.click("#btn-new-tx")
        await pilot.pause()

        assert isinstance(pilot.app.screen, TransactionEntryDialog)
        assert len(pilot.app.screen.query(Input)) == 4
        assert len(pilot.app.screen.query(Button)) == 2


async def test_transaction_entry_modal_cancel(
    tui_app_with_budget: OrcaLogyApp,
) -> None:
    """Verify pressing Escape dismisses the modal."""
    from orcalogy.tui.screens import MainMenuScreen

    async with tui_app_with_budget.run_test() as pilot:
        await pilot.click("#btn-new-tx")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()

        assert isinstance(pilot.app.screen, MainMenuScreen)


async def test_transaction_entry_modal_submit_valid(tmp_path: Path) -> None:
    """Verify a valid transaction is persisted and the modal closes on submit."""
    import datetime

    from textual.widgets import Input

    from orcalogy.app.services import InitializeBudgetUseCase
    from orcalogy.domain.models import Money
    from orcalogy.tui.screens import MainMenuScreen

    repo = FileLedgerRepository(str(tmp_path))
    month = datetime.date.today().strftime("%Y-%m")
    InitializeBudgetUseCase(repo).execute(month, {"Food": Money("500.00")})

    async with OrcaLogyApp(repository=repo).run_test() as pilot:
        await pilot.click("#btn-new-tx")
        await pilot.pause()

        screen = pilot.app.screen
        screen.query_one("#input-category", Input).value = "Food"
        screen.query_one("#input-amount", Input).value = "75.00"
        screen.query_one("#input-description", Input).value = "Lunch"

        await pilot.click("#btn-submit")
        await pilot.pause()

        assert isinstance(pilot.app.screen, MainMenuScreen)
        budget = repo.get_budget(month)
        assert budget is not None
        assert len(budget.transactions) == 1
        assert budget.transactions[0].amount == Money("75.00")


async def test_transaction_entry_modal_overrun_warning(tmp_path: Path) -> None:
    """Verify a transaction breaching the category limit shows an inline warning."""
    import datetime

    from textual.widgets import Input, Label

    from orcalogy.app.services import InitializeBudgetUseCase
    from orcalogy.domain.models import Money
    from orcalogy.tui.screens import TransactionEntryDialog

    repo = FileLedgerRepository(str(tmp_path))
    month = datetime.date.today().strftime("%Y-%m")
    InitializeBudgetUseCase(repo).execute(month, {"Food": Money("10.00")})

    async with OrcaLogyApp(repository=repo).run_test() as pilot:
        await pilot.click("#btn-new-tx")
        await pilot.pause()

        screen = pilot.app.screen
        screen.query_one("#input-category", Input).value = "Food"
        screen.query_one("#input-amount", Input).value = "999.00"
        screen.query_one("#input-description", Input).value = "Expensive"

        await pilot.click("#btn-submit")
        await pilot.pause()

        # Modal must stay open — overrun triggers a warning, not a dismissal
        assert isinstance(pilot.app.screen, TransactionEntryDialog)
        error_label = pilot.app.screen.query_one("#dialog-error", Label)
        assert "Limite Excedido" in str(error_label.content)
