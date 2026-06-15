# TSK-08: Implement BudgetCategory Entity

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** RF01 / Core Domain  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `BudgetCategory` entity in `orcalogy/domain/models.py`. Holds metadata details: unique name string and dynamic monthly limit using `Money` value object.

## ✅ Definition of Ready (DoR)

* [x] Money value object is active (TSK-07 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Entity]:** `BudgetCategory` validates limit is greater than or equal to zero.
* [x] **[Verification - Tests]:** `pytest tests/test_domain.py::test_budget_category_validation` runs successfully.
