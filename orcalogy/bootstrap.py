from typing import Any

from orcalogy.domain.ports import ILedgerRepository


def bootstrap(repository: ILedgerRepository) -> dict[str, Any]:
    """Bootstrap the application with concrete dependencies.

    Args:
        repository: A implementation of ILedgerRepository.

    Returns:
        A dictionary containing the resolved dependency instances.
    """
    dependencies = {
        "repository": repository,
    }
    return dependencies
