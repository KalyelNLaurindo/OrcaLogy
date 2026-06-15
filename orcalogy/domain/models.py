import datetime
import decimal
import functools
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Union

from orcalogy.domain.errors import (
    BudgetClosedError,
    DuplicateCategoryError,
    NegativeAmountError,
)


@dataclass(frozen=True)
@functools.total_ordering
class Money:
    """A Value Object representing monetary values in Canadian Dollars (CAD).

    Encapsulates decimal.Decimal to guarantee exact precision and prevent
    rounding anomalies.
    """

    amount: Decimal

    def __init__(self, value: Union[str, int, Decimal, "Money"]) -> None:
        """Initialize a Money instance, validating types to avoid precision errors.

        Floats are explicitly prohibited to prevent silent precision loss
        during creation.
        """
        if isinstance(value, float):
            raise TypeError(
                "Cannot initialize Money with float. "
                "Use str or Decimal instead to prevent precision loss."
            )
        elif isinstance(value, Money):
            decimal_value = value.amount
        elif isinstance(value, (str, int, Decimal)):
            try:
                # Quantize immediately to enforce exactly 2 decimal places
                decimal_value = Decimal(value).quantize(
                    Decimal("0.01"), rounding=decimal.ROUND_HALF_UP
                )
            except (decimal.InvalidOperation, ValueError) as e:
                raise ValueError(f"Invalid monetary value: {value}") from e
        else:
            raise TypeError("Unsupported type for Money initialization.")

        object.__setattr__(self, "amount", decimal_value)

    def __add__(self, other: Any) -> "Money":
        """Add two Money instances together.

        Adding non-Money types is prohibited.
        """
        if not isinstance(other, Money):
            raise TypeError("Can only add Money to Money.")
        return Money(self.amount + other.amount)

    def __sub__(self, other: Any) -> "Money":
        """Subtract one Money instance from another.

        Subtracting non-Money types is prohibited.
        """
        if not isinstance(other, Money):
            raise TypeError("Can only subtract Money from Money.")
        return Money(self.amount - other.amount)

    def __mul__(self, other: Any) -> "Money":
        """Multiply Money by a scalar value (int, float, Decimal).

        Multiplying Money by another Money is prohibited.
        """
        if isinstance(other, Money):
            raise TypeError("Cannot multiply Money by Money.")

        if not isinstance(other, (int, float, Decimal)):
            raise TypeError(
                "Money can only be multiplied by scalar values (int, float, Decimal)."
            )

        scalar = Decimal(str(other)) if isinstance(other, float) else Decimal(other)
        return Money(self.amount * scalar)

    def __rmul__(self, other: Any) -> "Money":
        """Support right-side scalar multiplication (e.g., 2.5 * Money)."""
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> "Money":
        """Divide Money by a scalar value (int, float, Decimal).

        Dividing Money by another Money is prohibited.
        """
        if isinstance(other, Money):
            raise TypeError("Cannot divide Money by Money.")

        if not isinstance(other, (int, float, Decimal)):
            raise TypeError(
                "Money can only be divided by scalar values (int, float, Decimal)."
            )

        scalar = Decimal(str(other)) if isinstance(other, float) else Decimal(other)
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide Money by zero.")

        return Money(self.amount / scalar)

    def __eq__(self, other: Any) -> bool:
        """Compare equality with another Money instance."""
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount

    def __lt__(self, other: Any) -> bool:
        """Compare less-than order with another Money instance."""
        if not isinstance(other, Money):
            raise TypeError("Can only compare Money with another Money instance.")
        return self.amount < other.amount

    def __str__(self) -> str:
        """Format Money as a Canadian Dollar string representation."""
        return f"${self.amount:.2f}"

    def __repr__(self) -> str:
        """Return the developer-friendly string representation of Money."""
        return f"Money('{self.amount}')"


@dataclass
class BudgetCategory:
    """An entity representing a budget category with a unique name and a limit.

    The identity (name) remains constant after creation, while the limit is mutable.
    """

    name: str
    limit: Money

    def __post_init__(self) -> None:
        """Validate category fields after initialization."""
        if not self.name.strip():
            raise ValueError("Category name cannot be empty.")
        if self.limit < Money("0.00"):
            raise NegativeAmountError("Category budget limit cannot be negative.")

    def change_limit(self, new_limit: Money) -> None:
        """Change the category limit after validating it is not negative."""
        if new_limit < Money("0.00"):
            raise NegativeAmountError("Category budget limit cannot be negative.")
        self.limit = new_limit

    def __setattr__(self, name: str, value: Any) -> None:
        """Enforce immutable identity for the 'name' attribute."""
        if name == "name" and hasattr(self, "name"):
            raise AttributeError("Cannot modify the name/identity of a BudgetCategory.")
        super().__setattr__(name, value)


@dataclass(frozen=True)
class Transaction:
    """A domain entity representing an expense or income transaction.

    Attributes:
        tx_id: A unique identifier.
        date: The date of the transaction.
        category: The budget category name.
        amount: The transaction value.
        description: A text description.
        tags: List of tags for categorization.
    """

    tx_id: str
    date: datetime.date
    category: str
    amount: Money
    description: str
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate transaction parameters."""
        if self.amount <= Money("0.00"):
            raise NegativeAmountError("Transaction amount must be positive.")
        if not self.category.strip():
            raise ValueError("Transaction category cannot be empty.")


@dataclass
class Budget:
    """An aggregate root representing a monthly budget.

    Coordinates categories and transactions, and manages active status lifecycle.
    """

    month: str
    categories: dict[str, BudgetCategory] = field(default_factory=dict)
    transactions: list[Transaction] = field(default_factory=list)
    status: str = "ACTIVE"

    def add_category(self, category: BudgetCategory) -> None:
        """Add a category to the budget.

        Raises DuplicateCategoryException if it already exists.
        """
        if category.name in self.categories:
            raise DuplicateCategoryError(
                f"Category '{category.name}' already exists in budget."
            )
        self.categories[category.name] = category

    def add_transaction(self, transaction: Transaction, force: bool = False) -> None:
        """Register a transaction.

        Validates status, category registration, and limits.
        """
        if self.status == "CLOSED":
            raise BudgetClosedError("Cannot add transaction to a closed budget.")

        from orcalogy.domain.validation import LimitValidator

        LimitValidator.validate_transaction(self, transaction, force)

        self.transactions.append(transaction)


    def get_category_spending(self, category_name: str) -> Money:
        """Calculate total spending for a specific category."""
        category_txs = [tx for tx in self.transactions if tx.category == category_name]
        total = Money("0.00")
        for tx in category_txs:
            total += tx.amount
        return total

    def get_total_spending(self) -> Money:
        """Calculate total spending across all registered transactions."""
        total = Money("0.00")
        for tx in self.transactions:
            total += tx.amount
        return total

    def close_cycle(self) -> None:
        """Close the fiscal cycle for this budget."""
        self.status = "CLOSED"


