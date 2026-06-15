from decimal import Decimal

import pytest

from orcalogy.domain.errors import (
    BudgetClosedException,
    BudgetOverrunException,
    CategoryNotFoundException,
    DuplicateCategoryException,
)
from orcalogy.domain.models import Budget, BudgetCategory, Money, Transaction
from orcalogy.domain.ranking import calculate_ranking
from orcalogy.domain.validation import LimitValidator


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


def test_budget_category_validation() -> None:
    """Verify BudgetCategory validation, identity preservation, and mutation."""
    # Valid creation
    category = BudgetCategory("Food", Money("500.00"))
    assert category.name == "Food"
    assert category.limit == Money("500.00")

    # Invalid empty or whitespace name
    with pytest.raises(ValueError):
        BudgetCategory("", Money("500.00"))

    with pytest.raises(ValueError):
        BudgetCategory("   ", Money("500.00"))

    # Invalid negative budget limit
    with pytest.raises(ValueError):
        BudgetCategory("Leisure", Money("-10.00"))

    # Safe mutation of budget limit
    category.change_limit(Money("600.00"))
    assert category.limit == Money("600.00")

    # Validate negative limit in mutation is rejected
    with pytest.raises(ValueError):
        category.change_limit(Money("-5.00"))

    # Identity (name) must be constant after creation
    with pytest.raises(AttributeError):
        category.name = "Leisure"  # type: ignore


def test_transaction_instantiation() -> None:
    """Verify Transaction properties and validation constraints."""
    import datetime

    # Valid instantiation
    tx = Transaction(
        tx_id="tx-1",
        date=datetime.date(2026, 6, 15),
        category="Food",
        amount=Money("15.50"),
        description="Lunch at Diner",
        tags=["eating-out"],
    )
    assert tx.tx_id == "tx-1"
    assert tx.category == "Food"
    assert tx.amount == Money("15.50")
    assert tx.description == "Lunch at Diner"
    assert tx.tags == ["eating-out"]

    # Reject negative or zero amounts
    with pytest.raises(ValueError):
        Transaction(
            tx_id="tx-2",
            date=datetime.date(2026, 6, 15),
            category="Food",
            amount=Money("-5.00"),
            description="Refund",
        )

    with pytest.raises(ValueError):
        Transaction(
            tx_id="tx-3",
            date=datetime.date(2026, 6, 15),
            category="Food",
            amount=Money("0.00"),
            description="Freebie",
        )

    # Reject empty or whitespace category names
    with pytest.raises(ValueError):
        Transaction(
            tx_id="tx-4",
            date=datetime.date(2026, 6, 15),
            category="   ",
            amount=Money("10.00"),
            description="Empty Category",
        )



def test_budget_aggregate_transitions() -> None:
    """Verify Budget aggregate transitions, calculations, and constraints."""
    import datetime

    # Budget initialization
    budget = Budget(month="2026-06")
    assert budget.month == "2026-06"
    assert budget.status == "ACTIVE"
    assert len(budget.categories) == 0
    assert len(budget.transactions) == 0

    # Adding a category
    food_cat = BudgetCategory("Food", Money("100.00"))
    budget.add_category(food_cat)
    assert budget.categories["Food"] == food_cat

    # Prevent duplicate category addition
    with pytest.raises(DuplicateCategoryException):
        budget.add_category(food_cat)

    # Prevent transaction with unregistered category
    tx_unregistered = Transaction(
        tx_id="tx-unreg",
        date=datetime.date(2026, 6, 15),
        category="Leisure",
        amount=Money("20.00"),
        description="Movie",
    )
    with pytest.raises(CategoryNotFoundException):
        budget.add_transaction(tx_unregistered)

    # Registering transaction successfully within limits
    tx1 = Transaction(
        tx_id="tx-1",
        date=datetime.date(2026, 6, 15),
        category="Food",
        amount=Money("45.50"),
        description="Weekly Groceries",
    )
    budget.add_transaction(tx1)
    assert len(budget.transactions) == 1
    assert budget.get_category_spending("Food") == Money("45.50")
    assert budget.get_total_spending() == Money("45.50")

    # Add second transaction within limits
    tx2 = Transaction(
        tx_id="tx-2",
        date=datetime.date(2026, 6, 16),
        category="Food",
        amount=Money("30.00"),
        description="Snacks",
    )
    budget.add_transaction(tx2)
    assert budget.get_category_spending("Food") == Money("75.50")
    assert budget.get_total_spending() == Money("75.50")

    # Try registering transaction exceeding limit without force (should fail)
    tx_exceed = Transaction(
        tx_id="tx-3",
        date=datetime.date(2026, 6, 17),
        category="Food",
        amount=Money("30.00"),  # 75.50 + 30.00 = 105.50 (> 100.00 limit)
        description="Dinner Out",
    )
    with pytest.raises(BudgetOverrunException):
        budget.add_transaction(tx_exceed, force=False)

    # Transaction should NOT be registered
    assert budget.get_category_spending("Food") == Money("75.50")
    assert len(budget.transactions) == 2

    # Register transaction exceeding limit with force=True (should succeed)
    budget.add_transaction(tx_exceed, force=True)
    assert budget.get_category_spending("Food") == Money("105.50")
    assert budget.get_total_spending() == Money("105.50")
    assert len(budget.transactions) == 3

    # Closing the cycle
    budget.close_cycle()
    assert budget.status == "CLOSED"

    # Cannot add transaction to closed budget
    tx_closed = Transaction(
        tx_id="tx-closed",
        date=datetime.date(2026, 6, 18),
        category="Food",
        amount=Money("5.00"),
        description="Coffee",
    )
    with pytest.raises(BudgetClosedException):
        budget.add_transaction(tx_closed)


def test_limit_validation_rules() -> None:
    """Verify LimitValidator standalone methods and logic checks."""
    import datetime

    budget = Budget(month="2026-06")
    food_cat = BudgetCategory("Food", Money("100.00"))
    budget.add_category(food_cat)

    # Spending is 0.00, check overrun for 90.00 (should be False)
    assert not LimitValidator.check_overrun(budget, "Food", Money("90.00"))

    # Check overrun for 110.00 (should be True)
    assert LimitValidator.check_overrun(budget, "Food", Money("110.00"))

    # Check overrun for unregistered category (should raise CategoryNotFoundException)
    with pytest.raises(CategoryNotFoundException):
        LimitValidator.check_overrun(budget, "Leisure", Money("10.00"))

    # Register tx of 80.00
    tx1 = Transaction(
        tx_id="tx-1",
        date=datetime.date(2026, 6, 15),
        category="Food",
        amount=Money("80.00"),
        description="Grocery",
    )
    # validate_transaction should pass
    LimitValidator.validate_transaction(budget, tx1)
    budget.add_transaction(tx1)

    # Next tx of 30.00 makes it 110.00 (exceeds 100.00)
    tx2 = Transaction(
        tx_id="tx-2",
        date=datetime.date(2026, 6, 16),
        category="Food",
        amount=Money("30.00"),
        description="Restaurant",
    )
    # should raise BudgetOverrunException when force=False
    with pytest.raises(BudgetOverrunException):
        LimitValidator.validate_transaction(budget, tx2, force=False)

    # should pass when force=True
    LimitValidator.validate_transaction(budget, tx2, force=True)


def test_ranking_calculations() -> None:
    """Verify deviation math, zero-limit handling, and ranking order."""
    import datetime

    budget = Budget(month="2026-06")

    # Categories
    cat1 = BudgetCategory("Food", Money("100.00"))  # Limit 100.00
    cat2 = BudgetCategory("Leisure", Money("200.00"))  # Limit 200.00
    cat3 = BudgetCategory("Transport", Money("50.00"))  # Limit 50.00
    cat4 = BudgetCategory("ZeroLimitSpend", Money("0.00"))  # Limit 0.00
    cat5 = BudgetCategory("ZeroLimitNoSpend", Money("0.00"))  # Limit 0.00

    budget.add_category(cat1)
    budget.add_category(cat2)
    budget.add_category(cat3)
    budget.add_category(cat4)
    budget.add_category(cat5)

    # Transactions
    # Food spent 120.00 -> deviation: ((120/100) - 1) * 100 = +20.00%
    tx_food = Transaction(
        "tx-f",
        datetime.date(2026, 6, 15),
        "Food",
        Money("120.00"),
        "Groceries",
    )
    budget.add_transaction(tx_food, force=True)

    # Leisure spent 150.00 -> deviation: ((150/200) - 1) * 100 = -25.00%
    tx_leisure = Transaction(
        "tx-l", datetime.date(2026, 6, 15), "Leisure", Money("150.00"), "Game"
    )
    budget.add_transaction(tx_leisure, force=True)

    # Transport spent 10.00 -> deviation: ((10/50) - 1) * 100 = -80.00%
    tx_transport = Transaction(
        "tx-t", datetime.date(2026, 6, 15), "Transport", Money("10.00"), "Bus"
    )
    budget.add_transaction(tx_transport, force=True)

    # ZeroLimitSpend spent 50.00 -> deviation limit 0, spent > 0 -> +100.00%
    tx_zero = Transaction(
        "tx-z",
        datetime.date(2026, 6, 15),
        "ZeroLimitSpend",
        Money("50.00"),
        "Extra",
    )
    budget.add_transaction(tx_zero, force=True)

    # ZeroLimitNoSpend -> spent 0.00 -> deviation: limit 0, spent 0 -> 0.00%


    # Calculate ranking
    ranking = calculate_ranking(budget)

    # Ordered descending:
    # 1. ZeroLimitSpend (+100.00%)
    # 2. Food (+20.00%)
    # 3. ZeroLimitNoSpend (0.00%)
    # 4. Leisure (-25.00%)
    # 5. Transport (-80.00%)
    assert len(ranking) == 5

    assert ranking[0].category_name == "ZeroLimitSpend"
    assert ranking[0].deviation == Decimal("100.00")

    assert ranking[1].category_name == "Food"
    assert ranking[1].deviation == Decimal("20.00")

    assert ranking[2].category_name == "ZeroLimitNoSpend"
    assert ranking[2].deviation == Decimal("0.00")

    assert ranking[3].category_name == "Leisure"
    assert ranking[3].deviation == Decimal("-25.00")

    assert ranking[4].category_name == "Transport"
    assert ranking[4].deviation == Decimal("-80.00")




