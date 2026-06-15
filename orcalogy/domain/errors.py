class DomainError(Exception):
    """Base exception for all domain-related errors in OrcaLogy."""

    pass


class BudgetClosedException(DomainError):  # noqa: N818
    """Raised when trying to perform operations on a closed budget."""

    pass


class CategoryNotFoundException(DomainError):  # noqa: N818
    """Raised when a specified category does not exist in the budget."""

    pass


class BudgetOverrunException(DomainError):  # noqa: N818
    """Raised when a transaction exceeds the budget limit of a category."""

    pass


class DuplicateCategoryException(DomainError):  # noqa: N818
    """Raised when a category is added to the budget but already exists."""

    pass

