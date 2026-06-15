# TSK-36: CSV Import/Export Engine

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 6 Hours  
* **Story / Epic Reference:** Phase 7.1 / PORTABILITY  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement an import/export utility to allow users to import transaction history from external CSV sheets/bank statements and export the ledger data to a standard format for compatibility with external spreadsheet tools.

## ✅ Definition of Ready (DoR)

* [ ] CLI and core domain services fully functional.
* [ ] Atomic file writer repository (TSK-22) is active and verified.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Write test cases first in `tests/test_infra.py` or a dedicated test file validating parsing of valid/invalid CSV formats.
* [ ] **[Functional - Import]:** Parses external CSV files, maps columns (Date, Category, Amount, Description, Tags) to `Transaction` models, runs domain validations, and appends valid transactions atomicity to the ledger.
* [ ] **[Functional - Export]:** Generates a clean, standard comma-separated file representing the ledger transactions.
* [ ] **[Verification]:** `pytest tests/test_infra.py` verifying correct CSV conversion and import rejection of malformed or invalid budget-violating records.
