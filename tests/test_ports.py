from orcalogy.domain.models import Budget
from orcalogy.domain.ports import ILedgerRepository


def test_ledger_repository_protocol_implementation() -> None:
    """Ensure that any repository class that matches the interface signature

    is recognized as a valid ILedgerRepository.
    """

    class MockLedgerRepository:
        def get_budget(self, _month: str) -> Budget | None:
            return None

        def save_budget(self, budget: Budget) -> None:
            pass

    # Verify that structural subtyping/runtime checking works as expected
    repo = MockLedgerRepository()
    assert isinstance(repo, ILedgerRepository)


def test_invalid_ledger_repository_implementation() -> None:
    """Ensure that classes missing the required methods are not recognized

    as complying with the ILedgerRepository protocol.
    """

    class InvalidRepository:
        def get_budget(self, _month: str) -> Budget | None:
            return None

    repo = InvalidRepository()
    assert not isinstance(repo, ILedgerRepository)
