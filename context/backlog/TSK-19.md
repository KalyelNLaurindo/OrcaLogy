# TSK-19: Implement Initialize Budget & Limits Use Case

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** Phase 3.1 / Core Use Cases  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement initializer service inside `orcalogy/app/services.py`. Creates default directory settings, maps category thresholds, and initializes empty journal structure files.

## ✅ Definition of Ready (DoR)

* [x] ILedgerRepository Port interface initialized.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Init]:** Sets up directories and maps limits on clean ledger startups.
* [x] **[Verification]:** Running tests in `tests/test_app.py::test_initialize_budget_structures` runs green.
