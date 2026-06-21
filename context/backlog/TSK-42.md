# TSK-42: Implement orca status CLI Command

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** RF03 / CLI  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `orca status --month YYYY-MM` as a lightweight summary command. Unlike `orca report` (which renders a full deviation table), `status` outputs a one-screen snapshot: total spent vs total budget, number of categories in overrun, and whether the cycle is ACTIVE or CLOSED. Designed for quick terminal glance without scrolling.

## ✅ Definition of Ready (DoR)

* [x] CLI root app functional (TSK-23).
* [x] `GetCategoryDeviationRankingUseCase` complete (TSK-17).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor.
* [x] **[Functional - Cmd]:** `orca status --month 2026-06` prints total spending, budget remaining, overrun count, and cycle status in under 10 lines of output.
* [x] **[Verification]:** `pytest tests/test_cli.py::TestStatusCommand` passes green.
