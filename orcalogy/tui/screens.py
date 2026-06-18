"""Textual TUI screens for OrcaLogy.

Each class in this module represents a full-screen view. The DashboardScreen
is the default entry point and shows the user whether their spending is on
track for the current month.
"""

from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Any, ClassVar, cast

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Input, Label

from orcalogy.app.services import (
    GetCategoryDeviationRankingUseCase,
    RegisterTransactionUseCase,
)
from orcalogy.domain.errors import (
    BudgetClosedError,
    BudgetNotFoundError,
    BudgetOverrunError,
)
from orcalogy.domain.models import Money, Transaction

if TYPE_CHECKING:
    from orcalogy.tui.app import OrcaLogyApp

_MAX_RECENT_TRANSACTIONS = 10


class TransactionEntryDialog(ModalScreen[None]):
    """Modal form for entering a new expense transaction.

    Captures category, amount, description, and an optional date (defaults to
    today). Validates the transaction against the category's monthly limit before
    persisting — if the limit is breached, shows an inline warning and waits for
    the user to confirm a force submission instead of crashing silently.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self) -> None:
        super().__init__()
        # Holds a pending transaction when the first submit attempt triggers an
        # overrun warning — a second Submit click will force-persist it.
        self._pending_tx: Transaction | None = None

    def compose(self) -> ComposeResult:
        """Render the dialog frame with four inputs, an error label, and two buttons."""
        today = datetime.date.today().isoformat()
        with Vertical(id="dialog"):
            yield Label("New Transaction", id="dialog-title")
            yield Input(placeholder="Category (e.g. Food)", id="input-category")
            yield Input(placeholder="Amount (e.g. 50.00)", id="input-amount")
            yield Input(placeholder="Description", id="input-description")
            yield Input(
                placeholder=f"Date YYYY-MM-DD  (default: {today})",
                id="input-date",
            )
            yield Label("", id="dialog-error")
            with Horizontal(id="dialog-buttons"):
                yield Button("Submit", id="btn-submit", variant="primary")
                yield Button("Cancel", id="btn-cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Route Submit and Cancel button clicks to the appropriate handler."""
        button_id = event.button.id
        if button_id == "btn-cancel":
            self.action_cancel()
        elif button_id == "btn-submit":
            self._attempt_submit()

    def action_cancel(self) -> None:
        """Dismiss the dialog without persisting anything."""
        self.dismiss(None)

    def _attempt_submit(self) -> None:
        """Validate form inputs and send the transaction to the use case.

        On the first click after an overrun warning, force-persists the pending
        transaction instead of re-validating the form fields.
        """
        error_label = self.query_one("#dialog-error", Label)

        # Second click after overrun warning: user confirmed force-submission.
        if self._pending_tx is not None:
            self._persist(self._pending_tx, force=True, error_label=error_label)
            return

        category = self.query_one("#input-category", Input).value.strip()
        amount_str = self.query_one("#input-amount", Input).value.strip()
        description = self.query_one("#input-description", Input).value.strip()
        date_str = self.query_one("#input-date", Input).value.strip()

        if not category or not amount_str:
            error_label.update("Category and Amount are required.")
            return

        if date_str:
            try:
                tx_date = datetime.date.fromisoformat(date_str)
            except ValueError:
                error_label.update("Invalid date format. Use YYYY-MM-DD.")
                return
        else:
            tx_date = datetime.date.today()

        try:
            tx = Transaction(
                tx_id=uuid.uuid4().hex[:8],
                date=tx_date,
                category=category,
                amount=Money(amount_str),
                description=description,
            )
        except (ValueError, TypeError) as exc:
            error_label.update(f"Invalid input: {exc}")
            return

        self._persist(tx, force=False, error_label=error_label)

    def _persist(
        self, tx: Transaction, force: bool, error_label: Label
    ) -> None:
        """Send the transaction to the domain use case and handle domain errors.

        Catches overrun errors to surface a user-friendly warning instead of
        letting the exception propagate to the TUI event loop.
        """
        orca_app = cast("OrcaLogyApp", self.app)

        try:
            RegisterTransactionUseCase(orca_app.repository).execute(tx, force=force)
        except BudgetOverrunError as exc:
            # Store the transaction so the user can re-click Submit to force it.
            self._pending_tx = tx
            error_label.update(
                f"⚠ Limit exceeded: {exc} — click Submit again to force."
            )
            return
        except (BudgetNotFoundError, BudgetClosedError) as exc:
            error_label.update(str(exc))
            return

        self.dismiss(None)


class DashboardScreen(Screen[None]):
    """Main dashboard — shows category spending deviations and recent transactions.

    Reads the current month's budget from the repository every time it mounts
    or the user presses 'r'. If no budget exists for the month it shows a
    placeholder row so the layout never appears broken.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("r", "refresh_dashboard", "Refresh"),
        Binding("n", "new_transaction", "New Transaction"),
    ]

    def compose(self) -> ComposeResult:
        """Yield the two data tables that make up the dashboard layout."""
        yield Label("Category Deviations", id="category-label")
        yield DataTable(id="category-table")
        yield Label(
            f"Recent Transactions (last {_MAX_RECENT_TRANSACTIONS})", id="tx-label"
        )
        yield DataTable(id="tx-table")

    def on_mount(self) -> None:
        """Load live data from the repository when the screen first appears."""
        self._populate()

    def action_refresh_dashboard(self) -> None:
        """Clear and reload all dashboard tables — triggered by pressing 'r'."""
        self._populate()

    def action_new_transaction(self) -> None:
        """Open the transaction entry modal and refresh the dashboard on close."""
        def _on_dismiss(_: None) -> None:
            self._populate()

        self.app.push_screen(TransactionEntryDialog(), _on_dismiss)

    def _populate(self) -> None:
        """Read the current month's budget and fill both tables.

        Uses GetCategoryDeviationRankingUseCase for sorted category data and
        reads raw transactions directly from the budget aggregate for the
        recent-transactions panel.
        """
        orca_app = cast("OrcaLogyApp", self.app)
        month = datetime.date.today().strftime("%Y-%m")

        category_table: DataTable[Any] = self.query_one(
            "#category-table", DataTable
        )
        tx_table: DataTable[Any] = self.query_one("#tx-table", DataTable)

        category_table.clear(columns=True)
        tx_table.clear(columns=True)

        try:
            ranking = GetCategoryDeviationRankingUseCase(
                orca_app.repository
            ).execute(month)
        except BudgetNotFoundError:
            category_table.add_columns("Status")
            category_table.add_row(
                f"No budget found for {month} — run `orca init` to create one."
            )
            tx_table.add_columns("Status")
            tx_table.add_row("No data available.")
            return

        # Populate category deviation table — color-code the deviation column
        # so users can immediately spot which categories are in danger.
        category_table.add_columns("Category", "Limit", "Spent", "Deviation")
        for item in ranking:
            deviation_str = f"{item.deviation:+.2f}%"
            if item.deviation > 20:
                deviation_cell = Text(deviation_str, style="red")
            elif item.deviation > 0:
                deviation_cell = Text(deviation_str, style="yellow")
            else:
                deviation_cell = Text(deviation_str, style="green")

            category_table.add_row(
                item.category_name,
                str(item.limit.amount),
                str(item.spending.amount),
                deviation_cell,
            )

        # Populate recent transactions — most recent first, capped at the limit.
        budget = orca_app.repository.get_budget(month)
        if budget and budget.transactions:
            tx_table.add_columns("Date", "Category", "Amount", "Description")
            recent = sorted(
                budget.transactions, key=lambda t: t.date, reverse=True
            )[:_MAX_RECENT_TRANSACTIONS]
            for tx in recent:
                tx_table.add_row(
                    str(tx.date),
                    tx.category,
                    str(tx.amount.amount),
                    tx.description,
                )
        else:
            tx_table.add_columns("Status")
            tx_table.add_row("No transactions recorded yet.")
