# TSK-10: Implement Transaction Entity

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** RF01 / Core Domain  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `Transaction` domain entity in `orcalogy/domain/models.py`. Standard properties: ID, timestamp (datetime), category name string, amount (`Money`), description text, list of tags.

## ✅ Definition of Ready (DoR)

* [ ] Money value object completed (TSK-07 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Entity]:** Transaction instances correctly format properties and prevent negative amount registrations.
* [ ] **[Verification]:** Tests in `tests/test_domain.py::test_transaction_instantiation` assert constraints pass.
