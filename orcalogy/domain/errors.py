class DomainError(Exception):
    """Base exception for all domain-related errors in OrcaLogy."""

    pass


class BudgetClosedError(DomainError):
    """Raised when trying to perform operations on a closed budget."""

    pass


class CategoryNotFoundError(DomainError):
    """Raised when a specified category does not exist in the budget."""

    pass


class BudgetOverrunError(DomainError):
    """Raised when a transaction exceeds the budget limit of a category."""

    pass


class DuplicateCategoryError(DomainError):
    """Raised when a category is added to the budget but already exists."""

    pass


class NegativeAmountError(DomainError, ValueError):
    """Raised when a negative amount is provided to a value object or category."""

    pass


class BudgetNotFoundError(DomainError):
    """Raised when a budget cannot be found in the repository."""

    pass
