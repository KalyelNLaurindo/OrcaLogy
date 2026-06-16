# TSK-21: Lexical Flat-Text Journal Parser

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 7 Hours  
* **Story / Epic Reference:** RF01 / PERSISTENCE  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement lexical text scanning in `orcalogy/infra/parser.py` parsing flat journal files (`ledger.journal`). Groups lines into Transaction domains, handles comments/empty lines, and raises detailed line syntax warnings.

## ✅ Definition of Ready (DoR)

* [x] Flat-text syntax specifications defined.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Lexer]:** Converts raw file text lines to Transaction objects.
* [x] **[Verification]:** 22 tests pass in `tests/test_infra.py` covering valid lines, empty lines, comments, tag parsing, deterministic ID generation, syntax warnings (wrong field count, invalid date, invalid amount, zero/negative amount, empty category, empty description), mixed input, and disk-backed file reading.
