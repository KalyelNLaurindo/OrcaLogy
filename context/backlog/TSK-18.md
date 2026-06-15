# TSK-18: Implement Close Fiscal Cycle Use Case

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** Phase 3.1 / Core Use Cases  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement cycle closing use case in `orcalogy/app/services.py`. Sets active budget state to closed, generates final fiscal reports, and prevents further transaction additions.

## ✅ Definition of Ready (DoR)

* [ ] Domain models exceptions complete.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Status]:** Sets ledger budget status to Closed.
* [ ] **[Verification - Exceptions]:** Running `pytest tests/test_app.py::test_close_budget_cycle` confirms blocking additions on closed states.
