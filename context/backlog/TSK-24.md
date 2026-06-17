# TSK-24: Implement orca init CLI Command

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** RF01 / CLI  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement `init` command under `orcalogy/cli/commands.py` prompting users for base settings, limits details, and writing configurations.

## ✅ Definition of Ready (DoR)

* [x] Initial setup use case complete (TSK-19 complete).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Test suite written first and runs with failures (Red). Minimal implementation code written to pass (Green). Refactored code maintains green tests. All unit/integration tests pass.
* [x] **[Functional - Cmd]:** Running `orca init` successfully scaffolds config templates.
* [x] **[Verification]:** CLI tests in `tests/test_cli.py::test_init_command_output` assert file creations.
