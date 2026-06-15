from decimal import Decimal

import pytest

from orcalogy.domain.models import Money


def test_money_initialization() -> None:
    """Verify that Money can be initialized with strings, ints, and Decimals,

    but reject floats directly to prevent silent precision loss.
    """
    # Valid initializations
    assert Money("10.50").amount == Decimal("10.50")
    assert Money(10).amount == Decimal("10.00")
    assert Money(Decimal("10.50")).amount == Decimal("10.50")
    # Copy constructor / Money instance initialization
    assert Money(Money("10.50")).amount == Decimal("10.50")

    # Reject floats to enforce exact financial math
    with pytest.raises(TypeError):
        Money(10.5)  # type: ignore

    # Reject invalid strings
    with pytest.raises(ValueError):
        Money("invalid_number")

    # Reject unsupported types
    with pytest.raises(TypeError):
        Money([])  # type: ignore


def test_money_arithmetic() -> None:
    """Verify standard addition and subtraction between Money instances,

    enforcing that we cannot perform additions/subtractions with non-Money types.
    """
    m1 = Money("10.50")
    m2 = Money("5.00")

    # Addition
    assert m1 + m2 == Money("15.50")

    # Subtraction
    assert m1 - m2 == Money("5.50")

    # Rejection of invalid types
    with pytest.raises(TypeError):
        _ = m1 + 5  # type: ignore

    with pytest.raises(TypeError):
        _ = m1 - Decimal("5.00")  # type: ignore


def test_money_scalar_operations() -> None:
    """Verify scalar multiplication/division for tax rates and split payments.

    Resulting money must be rounded to exactly two decimal places.
    """
    m = Money("10.00")

    # Multiplication
    assert m * 2 == Money("20.00")
    assert 2.5 * m == Money("25.00")
    assert m * Decimal("1.05") == Money("10.50")

    # Division
    assert m / 4 == Money("2.50")
    # Verify round half up logic (10 / 3 = 3.3333... -> 3.33)
    assert m / 3 == Money("3.33")
    assert Money("10.05") / 2 == Money("5.03")  # 5.025 rounded up to 5.03

    # Rejection of money by money operations
    with pytest.raises(TypeError):
        _ = m * Money("2.00")

    with pytest.raises(TypeError):
        _ = m / Money("2.00")

    # Rejection of invalid types for scalar multiplication/division
    with pytest.raises(TypeError):
        _ = m * "invalid"  # type: ignore

    with pytest.raises(TypeError):
        _ = m / "invalid"  # type: ignore

    # Zero division check
    with pytest.raises(ZeroDivisionError):
        _ = m / 0


def test_money_comparison() -> None:
    """Verify standard comparison operations for sorting and checking thresholds."""
    m1 = Money("10.00")
    m2 = Money("20.00")
    m3 = Money("10.00")

    assert m1 < m2
    assert m1 <= m2
    assert m1 <= m3
    assert m2 > m1
    assert m2 >= m1
    assert m1 >= m3
    assert m1 == m3
    assert m1 != m2

    # Equality with non-Money should return False
    assert m1 != "10.00"

    # Comparisons with non-Money should raise TypeError
    with pytest.raises(TypeError):
        _ = m1 < 10  # type: ignore


def test_money_immutability() -> None:
    """Verify Money is a true Value Object by checking its immutability.

    Once created, its value cannot be modified.
    """
    m = Money("10.00")
    with pytest.raises(AttributeError):
        m.amount = Decimal("20.00")  # type: ignore


def test_money_string_representation() -> None:
    """Verify representation matches Canadian Dollar formatting."""
    m = Money("10.50")
    assert str(m) == "$10.50"
    assert repr(m) == "Money('10.50')"
