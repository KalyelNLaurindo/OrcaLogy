# TSK-38: Git Cloud Backup & Auto-Sync

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** Phase 7.3 / SYNC  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement an auto-backup and synchronization feature that optionally tracks the `ledger.journal` using Git. Provides a sync command (`orca sync`) that stage, commits, and pushes/pulls updates automatically to/from a configured remote repository.

## ✅ Definition of Ready (DoR)

* [ ] CLI commands module (TSK-23) is functional.
* [ ] Local repository initialized (TSK-02 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Write mock Git process validation tests ensuring commands are invoked in correct order.
* [ ] **[Functional - Sync]:** Check for Git status, perform `git pull`, resolve simple fast-forward states, add and commit the ledger, and `git push` to remote.
* [ ] **[Verification]:** `pytest tests/test_infra.py` or `tests/test_cli.py` checking subprocess wrapper behaviour.
