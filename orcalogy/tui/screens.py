"""Textual TUI screens for OrcaLogy.

Each class in this module represents a full-screen view. The DashboardScreen
is the default entry point and shows the user whether their spending is on
track for the current month.
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, ClassVar, cast

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.screen import Screen
from textual.widgets import DataTable, Label

from orcalogy.app.services import GetCategoryDeviationRankingUseCase
from orcalogy.domain.errors import BudgetNotFoundError

if TYPE_CHECKING:
    from orcalogy.tui.app import OrcaLogyApp

_MAX_RECENT_TRANSACTIONS = 10


class DashboardScreen(Screen[None]):
    """Main dashboard — shows category spending deviations and recent transactions.

    Reads the current month's budget from the repository every time it mounts
    or the user presses 'r'. If no budget exists for the month it shows a
    placeholder row so the layout never appears broken.
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("r", "refresh_dashboard", "Refresh"),
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
