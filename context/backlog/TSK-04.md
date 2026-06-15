# TSK-04: Configure Dependencies in pyproject.toml

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** Phase 1.1 / ARCH-ENABLER  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Configure dependencies inside `pyproject.toml` or `requirements.txt`. Required production packages: `textual` (TUI), `typer` (CLI), and `filelock` (POSIX lock). Required dev packages: `pytest`, `ruff`, and `mypy`.

## ✅ Definition of Ready (DoR)

* [x] Poetry/pip environment is verified and active (TSK-01 complete).
* [x] pyproject.toml is generated and ready to receive properties.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **[Functional - Dependencies]:** Dependencies defined inside project descriptors.
* [x] **[Verification - Installation]:** Run `poetry install` or `pip install -r requirements.txt` running to completion without errors.
