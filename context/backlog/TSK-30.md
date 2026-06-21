# TSK-30: Configure Rotating File JSON Logging

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** Phase 5.1 / OBSERVABILITY  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Setup file logger configurations in `orcalogy/main.py` using Python `logging.handlers.RotatingFileHandler`. Writes tracing details to local file: `~/.config/orcalogy/logs/orca.log`.

## ✅ Definition of Ready (DoR)

* [x] Directory settings complete.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Log]:** Writes structured JSON log outputs containing execution details.
* [x] **[Verification]:** Tests in `tests/test_infra.py::test_observability_logging` confirm log file creation.
