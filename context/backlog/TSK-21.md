# TSK-21: Lexical Flat-Text Journal Parser

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 7 Hours  
* **Story / Epic Reference:** RF01 / PERSISTENCE  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement lexical text scanning in `orcalogy/infra/parser.py` parsing flat journal files (`ledger.journal`). Groups lines into Transaction domains, handles comments/empty lines, and raises detailed line syntax warnings.

## ✅ Definition of Ready (DoR)

* [ ] Flat-text syntax specifications defined.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Lexer]:** Converts raw file text lines to Transaction objects.
* [ ] **[Verification]:** Tests pass under `pytest tests/test_infra.py::test_lexical_parser` with both valid and invalid transaction lines.
