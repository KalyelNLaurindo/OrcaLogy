# TSK-41: Implement orca close CLI Command

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** RF01 / CLI  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Expose the `CloseBudgetCycleUseCase` (TSK-18) through the CLI as `orca close --month YYYY-MM`. Locks the budget cycle for the specified month, preventing any further transaction additions. Prints a clear confirmation message or an error if the month does not exist or is already closed.

## ✅ Definition of Ready (DoR)

* [x] `CloseBudgetCycleUseCase` complete (TSK-18).
* [x] CLI root app functional (TSK-23).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation written to pass (Green). Refactored code maintains green tests.
* [ ] **[Functional - Cmd]:** `orca close --month 2026-06` locks the budget and prints a confirmation. Subsequent `orca add` on the same month returns an error.
* [ ] **[Verification]:** `pytest tests/test_cli.py::TestCloseCommand` passes green.
