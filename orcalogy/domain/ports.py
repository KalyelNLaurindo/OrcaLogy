from typing import Protocol, runtime_checkable

from orcalogy.domain.models import Budget


@runtime_checkable
class ILedgerRepository(Protocol):
    """Port interface defining persistence operations for the monthly financial ledger.

    Specifies structural contracts for fetching monthly budgets
    and persisting their state.
    """

    def get_budget(self, month: str) -> Budget | None:
        """Retrieve the budget for a specific month (e.g., '2026-06').

        Args:
            month: A string representing the budget month (format YYYY-MM).

        Returns:
            The Budget instance if found, or None if it does not exist.
        """
        ...

    def save_budget(self, budget: Budget) -> None:
        """Persist the budget state, including all categories, transactions, and status.

        Args:
            budget: The Budget aggregate root to be saved.
        """
        ...
