# TSK-43: Configurable Data Directory via config.toml

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** RF01 / CONFIGURATION  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Currently the data directory is hardcoded in `_make_repo()` to `~/.orcalogy/data`. This task reads a `config.toml` file (located at `~/.orcalogy/config.toml`) to allow users to override the data directory path. If the config file is absent, the default path is used as fallback.

## ✅ Definition of Ready (DoR)

* [x] Config parser infrastructure functional (TSK-06).
* [x] `_make_repo()` helper in `orcalogy/cli/commands.py` exists (TSK-23).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Follow Red-Green-Refactor. Tests verify that a config file with a custom `data_dir` overrides the default, and that missing config falls back gracefully.
* [ ] **[Functional - Config]:** `~/.orcalogy/config.toml` with `[storage]\ndata_dir = "/custom/path"` is respected by all CLI commands.
* [ ] **[Functional - Init]:** `orca init` creates `~/.orcalogy/config.toml` with default values on first run if it does not exist.
* [ ] **[Verification]:** `pytest tests/test_cli.py` or dedicated `tests/test_config.py` passes green.
