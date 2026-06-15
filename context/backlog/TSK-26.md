# TSK-26: Implement orca report CLI Command

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** RF03 / CLI  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `report` command compiling ASCII tables of deviation metrics. Uses color-coded layouts to flag warnings: Green (Safe), Yellow (Alert), and Red (Overspent).

## ✅ Definition of Ready (DoR)

* [ ] Deviation use case complete (TSK-17 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Cmd]:** Renders color-coded budget deviation table.
* [ ] **[Verification]:** Tests run under `pytest tests/test_cli.py::test_report_generation` matching ANSI regex values.
