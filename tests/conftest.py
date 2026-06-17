"""Shared pytest fixtures available to all test modules."""

from pathlib import Path

import pytest

from orcalogy.infra.file_repo import FileLedgerRepository


@pytest.fixture
def tmp_repo(tmp_path: Path) -> FileLedgerRepository:
    """Real repository backed by a temp directory — never touches ~/.orcalogy."""
    return FileLedgerRepository(str(tmp_path))
