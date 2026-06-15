# TSK-11: Implement Domain Validation Service

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 5 Hours  
* **Story / Epic Reference:** RF01 / RF03 / Core Domain  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Create `orcalogy/domain/validation.py` checking incoming transactions against category limit boundaries. Emits specific warning notifications if transactions would cause budget limits to be exceeded.

## ✅ Definition of Ready (DoR)

* [ ] Transaction, BudgetCategory and Budget models are completed.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Validation]:** Validation class detects and flags budget limit violations.
* [ ] **[Verification]:** `pytest tests/test_domain.py::test_limit_validation_rules` completes successfully.
