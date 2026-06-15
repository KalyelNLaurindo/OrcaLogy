# TSK-12: Implement Category Deviation & Ranking Math

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 5 Hours  
* **Story / Epic Reference:** RF03 / Core Domain  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement deviation calculations inside `orcalogy/domain/ranking.py`. Computes percentage overruns/savings per category. Returns categories sorted descending by their deviation percentage.

## ✅ Definition of Ready (DoR)

* [ ] Domain entities and validation logic are active.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Math]:** Returns sorted category ranking where overspent items top the list.
* [ ] **[Verification]:** `pytest tests/test_domain.py::test_ranking_calculations` runs green.
