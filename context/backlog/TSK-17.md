# TSK-17: Implement Get Category Deviation Ranking Use Case

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** RF03 / Core Use Cases  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement category deviation retriever service in `orcalogy/app/services.py`. Fetches current transactions, parses configurations, calls ranking functions, and yields formatted metrics.

## ✅ Definition of Ready (DoR)

* [ ] Domain ranking utility completed.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Reporting]:** Use case returns sorted data models containing exact percentage deviation structures.
* [ ] **[Verification]:** Tests in `tests/test_app.py::test_get_ranking_usecase` assert correct calculations.
