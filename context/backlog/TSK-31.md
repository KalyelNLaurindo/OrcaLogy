# TSK-31: Implement Read-Only Circuit Breaker for Corrupted Ledgers

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** Phase 5.1 / HARDENING  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement parser protection flags. If flat-text integrity is compromised, locks repository state to read-only, preventing edits and shielding data from corruption.

## ✅ Definition of Ready (DoR)

* [x] Parser module complete (TSK-21 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Safety]:** Blocks transaction updates on damaged files.
* [x] **[Verification]:** `pytest tests/test_infra.py::test_read_only_breaker` asserts ReadOnlyException is raised.
