# TSK-44: Graceful Concurrency Lock Timeout Handling

- **Owner / Assignee:** Kalyel N. Laurindo / Project Owner
- **Estimated Effort:** 4 Hours
- **Story / Epic Reference:** RF02 / CONCURRENCY
- **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

To improve application resilience and prevent raw Python tracebacks (in the CLI) or crashes (in the TUI), map `filelock.Timeout` to a custom domain-level exception `LedgerConcurrencyError` in `FileLedgerRepository`. Catch this exception in both user interface adapters (`orcalogy/cli/commands.py` and `orcalogy/tui/screens.py`) to show clean, user-friendly error messages when a concurrent file lock cannot be acquired.

## ✅ Definition of Ready (DoR)

- [] Advisory file lock manager (`FileLockManager`) functional (TSK-25).
- [] Basic CLI controllers and TUI Dialogs exist and call repository save methods.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

- [] **[Testing/Quality - TDD]:** Unit tests verify that a lock acquisition timeout triggers `LedgerConcurrencyError` instead of raw `filelock.Timeout`.
- [] **[Functional - Domain]:** `LedgerConcurrencyError` is defined in `orcalogy/domain/errors.py`.
- [] **[Functional - CLI]:** All writing commands (init, add, close) catch `LedgerConcurrencyError` and output a clean, colored error message before exiting with status code 1.
- [] **[Functional - TUI]:** Dialogue screens (`BudgetInitDialog`, `CloseCycleDialog`, `TransactionEntryDialog`) catch `LedgerConcurrencyError` and show a clear warning text in the dialog error label.
- [] **[Verification]:** `pytest` suite passes 100% green with coverage metrics met.
