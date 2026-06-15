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
