# TSK-22: Atomic File Repository Writer

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 6 Hours  
* **Story / Epic Reference:** RF01 / RF02 / PERSISTENCE  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `orcalogy/infra/file_repo.py` extending `ILedgerRepository`. Implements atomic filesystem writes: serializes to temporary files (`ledger.journal.tmp`), and uses `os.replace` to replace the target file safely.

## ✅ Definition of Ready (DoR)

* [x] POSIX Locker and Lexical Parser modules are tested and complete.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Atomic]:** Enforces locks and updates journal files atomically without leaving corrupted, half-written states.
* [x] **[Verification]:** 7 tests pass in `tests/test_infra.py` covering get/save round-trip with categories and transactions, no leftover .tmp files, status persistence, and concurrent write safety (`test_file_repo_atomic_writes`).
