# TSK-15: Create bootstrap.py DI Container

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** Phase 3.1 / ARCH-ENABLER  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `orcalogy/bootstrap.py` bootstrapping service configurations. Registers real repositories and manages dependency injection patterns for use case invocation.

## ✅ Definition of Ready (DoR)

* [x] ILedgerRepository Port interface is defined (TSK-14 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - DI]:** Bootstrapper binds interfaces dynamically.
* [x] **[Verification]:** `pytest tests/test_app.py::test_bootstrap_resolver` returns green resolving mock dependencies.
