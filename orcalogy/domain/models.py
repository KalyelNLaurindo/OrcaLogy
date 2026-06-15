import decimal
import functools
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Union


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
