# TSK-22: Atomic File Repository Writer

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 6 Hours  
* **Story / Epic Reference:** RF01 / RF02 / PERSISTENCE  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `orcalogy/infra/file_repo.py` extending `ILedgerRepository`. Implements atomic filesystem writes: serializes to temporary files (`ledger.journal.tmp`), and uses `os.replace` to replace the target file safely.

## ✅ Definition of Ready (DoR)

* [ ] POSIX Locker and Lexical Parser modules are tested and complete.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Atomic]:** Enforces locks and updates journal files atomically without leaving corrupted, half-written states.
* [ ] **[Verification]:** Running `pytest tests/test_infra.py::test_file_repo_atomic_writes` passes.
