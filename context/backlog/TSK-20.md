# TSK-20: Concurrency Advisory File Locker

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 5 Hours  
* **Story / Epic Reference:** RF02 / PERSISTENCE  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement multi-process advisory lock wrapper in `orcalogy/infra/locker.py` using `filelock` library. Locks resources using local lock file `.ledger.journal.lock` during reads/writes.

## ✅ Definition of Ready (DoR)

* [x] filelock package is installed in Poetry environment (TSK-04 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Concurrency]:** Prevents overlapping file modifications.
* [x] **[Verification - Multi-process]:** Tests in `tests/test_infra.py::test_advisory_file_locking` spawn concurrent tasks confirming queuing order.
