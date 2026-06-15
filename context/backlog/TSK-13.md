# TSK-13: Define Domain Exceptions & Errors

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** RF01 / Core Domain  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Define standard custom exceptions inside `orcalogy/domain/errors.py`. Enforces constraints with exceptions: `BudgetClosedError`, `CategoryNotFoundError`, and `NegativeAmountError`.

## ✅ Definition of Ready (DoR)

* [x] Domain core models are established.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Errors]:** System throws specialized class exceptions instead of generic runtime errors.
* [x] **[Verification]:** Type check assertions and pytest test scenarios catch and verify errors.
