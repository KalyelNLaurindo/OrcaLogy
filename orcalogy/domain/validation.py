from orcalogy.domain.errors import BudgetOverrunError, CategoryNotFoundError
from orcalogy.domain.models import Budget, Money, Transaction


class LimitValidator:
    """Domain service to validate budget category limit boundaries."""

    @staticmethod
    def check_overrun(budget: Budget, category_name: str, amount: Money) -> bool:
        """Check if adding an amount to a category would overrun its budget limit."""
        if category_name not in budget.categories:
            raise CategoryNotFoundError(
                f"Category '{category_name}' is not registered in this budget."
            )
        category = budget.categories[category_name]
        current_spending = budget.get_category_spending(category_name)
        return current_spending + amount > category.limit

    @staticmethod
    def validate_transaction(
        budget: Budget, transaction: Transaction, force: bool = False
    ) -> None:
        """Validate if a transaction is allowed in the budget.

        Raises CategoryNotFoundException if category is unregistered.
        Raises BudgetOverrunException if transaction amount causes an overrun
        and force is False.
        """
        # check_overrun will raise CategoryNotFoundException if unregistered
        has_overrun = LimitValidator.check_overrun(
            budget, transaction.category, transaction.amount
        )
        if has_overrun and not force:
            category = budget.categories[transaction.category]
            raise BudgetOverrunError(
                f"Transaction exceeds '{category.name}' limit of {category.limit}."
            )
