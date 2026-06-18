# TSK-28: Implement Textual TUI Dashboard Screen

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 6 Hours  
* **Story / Epic Reference:** RF05 / TUI  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Create the main TUI Dashboard layout in `orcalogy/tui/screens.py`. Renders overall budget progress bars, category deviation tables, and recent transactions lists.

## ✅ Definition of Ready (DoR)

* [x] Base TUI application wrapper is tested.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - TUI]:** Dashboard populates widgets using active ledger data.
* [x] **[Verification]:** Textual Pilot runner tests assertions inside `tests/test_tui.py::test_dashboard_population`.
