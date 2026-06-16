import json
import os
from pathlib import Path

from orcalogy.domain.models import Budget, BudgetCategory, Money
from orcalogy.domain.ports import ILedgerRepository
from orcalogy.infra.locker import FileLockManager
from orcalogy.infra.parser import parse_journal_file


class FileLedgerRepository:
    """Concrete adapter implementing ILedgerRepository via local flat-text files.

    Stores each month's data in two files inside the data directory:
    - ledger_YYYY-MM.journal  — pipe-delimited transaction lines
    - ledger_YYYY-MM.meta.json — budget status and category limits

    All writes are atomic: data goes to a .tmp file first, then os.replace
    swaps it in. A per-month advisory lock (FileLockManager) serializes
    concurrent writers.
    """

    def __init__(self, data_dir: str) -> None:
        self._data_dir = Path(data_dir)

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------

    def _journal_path(self, month: str) -> Path:
        return self._data_dir / f"ledger_{month}.journal"

    def _meta_path(self, month: str) -> Path:
        return self._data_dir / f"ledger_{month}.meta.json"

    def _lock_path(self, month: str) -> Path:
        return self._data_dir / f"ledger_{month}.lock"

    def _journal_tmp(self, month: str) -> Path:
        return Path(str(self._journal_path(month)) + ".tmp")

    def _meta_tmp(self, month: str) -> Path:
        return Path(str(self._meta_path(month)) + ".tmp")

    # ------------------------------------------------------------------
    # ILedgerRepository contract
    # ------------------------------------------------------------------

    def get_budget(self, month: str) -> Budget | None:
        """Load the budget for a month from disk.

        Returns None if no budget has been saved for that month yet.
        """
        meta_file = self._meta_path(month)
        if not meta_file.exists():
            return None

        meta = json.loads(meta_file.read_text(encoding="utf-8"))

        budget = Budget(month=month, status=meta["status"])
        for name, limit_str in meta["categories"].items():
            budget.add_category(BudgetCategory(name=name, limit=Money(limit_str)))

        journal_file = self._journal_path(month)
        if journal_file.exists():
            result = parse_journal_file(str(journal_file))
            budget.transactions = result.transactions

        return budget

    def save_budget(self, budget: Budget) -> None:
        """Persist the budget to disk atomically under an advisory lock.

        Writes metadata (status + categories) and transactions (journal lines)
        to separate .tmp files, then atomically replaces the target files.
        """
        self._data_dir.mkdir(parents=True, exist_ok=True)

        with FileLockManager(str(self._lock_path(budget.month))):
            self._write_meta(budget)
            self._write_journal(budget)

    # ------------------------------------------------------------------
    # Private write helpers
    # ------------------------------------------------------------------

    def _write_meta(self, budget: Budget) -> None:
        """Atomic write of the budget metadata JSON file."""
        meta = {
            "status": budget.status,
            "categories": {
                name: str(cat.limit.amount)
                for name, cat in budget.categories.items()
            },
        }
        tmp = self._meta_tmp(budget.month)
        tmp.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self._meta_path(budget.month))

    def _write_journal(self, budget: Budget) -> None:
        """Atomic write of the flat-text journal file."""
        lines = []
        for tx in budget.transactions:
            tags_str = " ".join(tx.tags)
            line = f"{tx.date} | {tx.category} | {tx.amount.amount} | {tx.description}"
            if tags_str:
                line += f" | {tags_str}"
            lines.append(line)

        content = "\n".join(lines) + ("\n" if lines else "")
        tmp = self._journal_tmp(budget.month)
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, self._journal_path(budget.month))
