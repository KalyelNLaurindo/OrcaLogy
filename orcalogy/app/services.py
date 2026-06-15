from orcalogy.domain.errors import BudgetNotFoundError
from orcalogy.domain.models import Transaction
from orcalogy.domain.ports import ILedgerRepository
from orcalogy.domain.ranking import CategoryRankingItem, calculate_ranking


class RegisterTransactionUseCase:
    """Use case to register a transaction in the monthly budget.

    Handles retrieval from repository, domain rule validations,
    and atomic state persistence.
    """

    def __init__(self, repository: ILedgerRepository) -> None:
        self.repository = repository

    def execute(self, transaction: Transaction, force: bool = False) -> None:
        """Execute the use case to register a new transaction.

        Args:
            transaction: The transaction object to register.
            force: If True, bypasses category budget limit checking.

        Raises:
            BudgetNotFoundError: If the budget for the transaction's
                month does not exist.
            BudgetOverrunError: If the transaction exceeds the category
                limit and force is False.
            BudgetClosedError: If the budget cycle is closed.
        """
        # Ex: Transaction date: 2026-06-15 -> Month: '2026-06'
        month = transaction.date.strftime("%Y-%m")
        budget = self.repository.get_budget(month)

        if budget is None:
            raise BudgetNotFoundError(f"Budget for month {month} was not found.")

        # Business validation logic & state modification
        budget.add_transaction(transaction, force=force)

        # Atomic persistence check
        self.repository.save_budget(budget)


class GetCategoryDeviationRankingUseCase:
    """Use case to retrieve sorted category deviation ranking for a month.

    Handles budget existence checks and delegation to domain ranking math.
    """

    def __init__(self, repository: ILedgerRepository) -> None:
        self.repository = repository

    def execute(self, month: str) -> list[CategoryRankingItem]:
        """Execute the use case to retrieve the ranking list.

        Args:
            month: Period format YYYY-MM (e.g. '2026-06').

        Returns:
            A list of CategoryRankingItem objects sorted descending.

        Raises:
            BudgetNotFoundError: If the budget for the period does not exist.
        """
        budget = self.repository.get_budget(month)
        if budget is None:
            raise BudgetNotFoundError(f"Budget for month {month} was not found.")

        return calculate_ranking(budget)
