# TSK-32: Implement Automated Backup Utility

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** Phase 5.1 / HARDENING  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement automated backups in `orcalogy/infra/file_repo.py`. Creates copy file `ledger.journal.bak` prior to modifying primary files.

## ✅ Definition of Ready (DoR)

* [ ] Atomic writer repository is configured.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Backup]:** Automated copy created before write.
* [ ] **[Verification]:** `pytest tests/test_infra.py::test_auto_backup_on_write` verifies backups match.
