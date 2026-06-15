# TSK-06: Config Parser for config.toml

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** RF01 / ARCH-ENABLER  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement config loader to parse `config.toml` mappings. Extracts general config preferences and dynamic category limits. The configuration must map limits using string category keys to decmial numeric value parameters.

## ✅ Definition of Ready (DoR)

* [ ] Directory scaffold is active (TSK-05 complete).
* [ ] Python's native `tomllib` (or standard `toml` library) configured for use.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Parser]:** Successfully parses a sample `config.toml` structure.
* [ ] **[Verification - Tests]:** Running `pytest tests/test_infra.py` matches assertions on categories retrieval.
