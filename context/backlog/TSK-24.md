# TSK-24: Implement orca init CLI Command

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** RF01 / CLI  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `init` command under `orcalogy/cli/commands.py` prompting users for base settings, limits details, and writing configurations.

## ✅ Definition of Ready (DoR)

* [ ] Initial setup use case complete (TSK-19 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [ ] **[Functional - Cmd]:** Running `orca init` successfully scaffolds config templates.
* [ ] **[Verification]:** CLI tests in `tests/test_cli.py::test_init_command_output` assert file creations.
