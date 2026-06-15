import pytest

from orcalogy.bootstrap import bootstrap
from orcalogy.domain.models import Budget
from orcalogy.domain.ports import ILedgerRepository


class FakeLedgerRepository:
    def __init__(self) -> None:
        self.budgets: dict[str, Budget] = {}

    def get_budget(self, month: str) -> Budget | None:
        return self.budgets.get(month)

    def save_budget(self, budget: Budget) -> None:
        self.budgets[budget.month] = budget


def test_bootstrap_resolver() -> None:
    """Verify that bootstrap correctly binds and resolves the ILedgerRepository."""
    repo = FakeLedgerRepository()

    # Bootstrap setup
    dependencies = bootstrap(repository=repo)

    # Verify that we can retrieve the repository dependency
    resolved_repo = dependencies.get("repository")
    assert resolved_repo is repo
    assert isinstance(resolved_repo, ILedgerRepository)


def test_register_transaction_usecase_success() -> None:
    """Verify registration of a transaction within budget limits."""
    import datetime

    from orcalogy.app.services import RegisterTransactionUseCase
    from orcalogy.domain.models import BudgetCategory, Money, Transaction

    repo = FakeLedgerRepository()
    budget = Budget(month="2026-06")
    budget.add_category(BudgetCategory("Food", Money("100.00")))
    repo.save_budget(budget)

    use_case = RegisterTransactionUseCase(repository=repo)
    tx = Transaction(
        tx_id="tx-1",
        date=datetime.date(2026, 6, 15),
        category="Food",
        amount=Money("30.00"),
        description="Lunch",
    )

    use_case.execute(tx)

    # Assert budget was updated and saved
    saved_budget = repo.get_budget("2026-06")
    assert saved_budget is not None
    assert len(saved_budget.transactions) == 1
    assert saved_budget.get_category_spending("Food") == Money("30.00")


def test_register_transaction_usecase_not_found() -> None:
    """Verify that registering a transaction for a non-existing budget

    raises BudgetNotFoundError.
    """
    import datetime

    from orcalogy.app.services import RegisterTransactionUseCase
    from orcalogy.domain.errors import BudgetNotFoundError
    from orcalogy.domain.models import Money, Transaction

    repo = FakeLedgerRepository()
    use_case = RegisterTransactionUseCase(repository=repo)
    tx = Transaction(
        tx_id="tx-1",
        date=datetime.date(2026, 6, 15),
        category="Food",
        amount=Money("30.00"),
        description="Lunch",
    )

    with pytest.raises(BudgetNotFoundError):
        use_case.execute(tx)


def test_register_transaction_usecase_overrun() -> None:
    """Verify registration failure on budget overrun when force is False."""
    import datetime

    from orcalogy.app.services import RegisterTransactionUseCase
    from orcalogy.domain.errors import BudgetOverrunError
    from orcalogy.domain.models import BudgetCategory, Money, Transaction

    repo = FakeLedgerRepository()
    budget = Budget(month="2026-06")
    budget.add_category(BudgetCategory("Food", Money("50.00")))
    repo.save_budget(budget)

    use_case = RegisterTransactionUseCase(repository=repo)
    tx = Transaction(
        tx_id="tx-1",
        date=datetime.date(2026, 6, 15),
        category="Food",
        amount=Money("60.00"),
        description="Expensive Meal",
    )

    # Force=False by default (or explicitly passed)
    with pytest.raises(BudgetOverrunError):
        use_case.execute(tx, force=False)

    # With force=True, it should pass
    use_case.execute(tx, force=True)

    saved_budget = repo.get_budget("2026-06")
    assert saved_budget is not None
    assert saved_budget.get_category_spending("Food") == Money("60.00")


def test_get_ranking_usecase_success() -> None:
    """Verify that GetCategoryDeviationRankingUseCase retrieves and sorts deviations."""
    import datetime
    from decimal import Decimal

    from orcalogy.app.services import GetCategoryDeviationRankingUseCase
    from orcalogy.domain.models import BudgetCategory, Money, Transaction

    repo = FakeLedgerRepository()
    budget = Budget(month="2026-06")
    budget.add_category(BudgetCategory("Food", Money("100.00")))
    budget.add_category(BudgetCategory("Leisure", Money("200.00")))

    # Food spent 120.00 (+20%)
    budget.add_transaction(
        Transaction(
            "tx-f", datetime.date(2026, 6, 15), "Food", Money("120.00"), "Groceries"
        ),
        force=True,
    )
    # Leisure spent 100.00 (-50%)
    budget.add_transaction(
        Transaction(
            "tx-l", datetime.date(2026, 6, 15), "Leisure", Money("100.00"), "Gaming"
        )
    )
    repo.save_budget(budget)

    use_case = GetCategoryDeviationRankingUseCase(repository=repo)
    ranking = use_case.execute("2026-06")

    assert len(ranking) == 2
    assert ranking[0].category_name == "Food"
    assert ranking[0].deviation == Decimal("20.00")
    assert ranking[1].category_name == "Leisure"
    assert ranking[1].deviation == Decimal("-50.00")


def test_get_ranking_usecase_not_found() -> None:
    """Verify that GetCategoryDeviationRankingUseCase raises BudgetNotFoundError

    for non-existing period.
    """
    from orcalogy.app.services import GetCategoryDeviationRankingUseCase
    from orcalogy.domain.errors import BudgetNotFoundError

    repo = FakeLedgerRepository()
    use_case = GetCategoryDeviationRankingUseCase(repository=repo)

    with pytest.raises(BudgetNotFoundError):
        use_case.execute("2026-06")


def test_close_budget_cycle_success() -> None:
    """Verify that CloseBudgetCycleUseCase sets budget status to CLOSED."""
    from orcalogy.app.services import CloseBudgetCycleUseCase

    repo = FakeLedgerRepository()
    budget = Budget(month="2026-06")
    repo.save_budget(budget)

    use_case = CloseBudgetCycleUseCase(repository=repo)
    use_case.execute("2026-06")

    saved_budget = repo.get_budget("2026-06")
    assert saved_budget is not None
    assert saved_budget.status == "CLOSED"


def test_close_budget_cycle_not_found() -> None:
    """Verify that CloseBudgetCycleUseCase raises BudgetNotFoundError

    for non-existing period.
    """
    from orcalogy.app.services import CloseBudgetCycleUseCase
    from orcalogy.domain.errors import BudgetNotFoundError

    repo = FakeLedgerRepository()
    use_case = CloseBudgetCycleUseCase(repository=repo)

    with pytest.raises(BudgetNotFoundError):
        use_case.execute("2026-06")


def test_close_budget_cycle_blocks_further_transactions() -> None:
    """Verify that a closed budget blocks further transaction registrations."""
    import datetime

    from orcalogy.app.services import (
        CloseBudgetCycleUseCase,
        RegisterTransactionUseCase,
    )
    from orcalogy.domain.errors import BudgetClosedError
    from orcalogy.domain.models import BudgetCategory, Money, Transaction

    repo = FakeLedgerRepository()
    budget = Budget(month="2026-06")
    budget.add_category(BudgetCategory("Food", Money("100.00")))
    repo.save_budget(budget)

    close_usecase = CloseBudgetCycleUseCase(repository=repo)
    register_usecase = RegisterTransactionUseCase(repository=repo)

    close_usecase.execute("2026-06")

    tx = Transaction(
        tx_id="tx-1",
        date=datetime.date(2026, 6, 15),
        category="Food",
        amount=Money("30.00"),
        description="Coffee",
    )

    with pytest.raises(BudgetClosedError):
        register_usecase.execute(tx)
