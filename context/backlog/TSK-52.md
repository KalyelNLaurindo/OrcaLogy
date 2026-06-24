# TSK-52: Terminal UI/UX Overhaul — CLI & TUI Visual Redesign

* **Owner / Assignee:** Kalyel Nunes Laurindo / PO  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** Phase 7 / UX Terminal & TUI  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

OrcaLogy exposes two interfaces: a CLI (Typer commands) and a Textual TUI dashboard. Both are functional but can be improved visually. The CLI commands produce plain-text outputs without structured formatting, consistent icon conventions, or visual hierarchy. The TUI is functional but lacks a polished welcome panel and status feedback design. This task redesigns the visual layer of both interfaces without breaking any existing business logic.

### Pain Points Identified (User Reported)

1. **CLI outputs lack visual structure** — `orca status`, `orca report`, and `orca add` produce flat text with no borders, alignment, or icon feedback.
2. **No consistent icon/color convention** — Success, warning, and error states are undifferentiated visually in the CLI output.
3. **TUI welcome panel missing** — Launching `orca` (default TUI) shows no branded splash or orientation guidance for first-time users.
4. **No visual separation between CLI command outputs** — Running multiple commands in sequence produces an undifferentiated wall of text.
5. **Deviation report table readability** — The `orca report` ASCII table has no color-coding for over-budget vs. under-budget categories.

### Deliverables

1. **CLI: Consistent message icons** — `✅` success, `⚠️` warning, `❌` error, `ℹ️` info — prepended to all feedback lines in every Typer command.
2. **CLI: Structured output tables** — `orca status` and `orca report` wrapped in Unicode box borders (`╭`, `─`, `│`, `╰`) with aligned columns.
3. **CLI: Color-coded deviation report** — Over-budget categories rendered in red/orange; under-budget in green; neutral in white.
4. **TUI: Branded welcome panel** — A `Static` widget shown on first launch with app name, version, tagline, and a keyboard shortcut cheatsheet.
5. **TUI: Status feedback bar** — A bottom status bar (Textual `Footer`) displaying the last action result (success/error) with color.
6. **Graceful degradation** — All CLI enhancements behind a `supports_unicode()` / `NO_COLOR` check; plain ASCII fallback for restricted terminals.

## ✅ Definition of Ready (DoR)

* [x] CLI commands (`init`, `add`, `status`, `report`, `close`) are implemented and functional.
* [x] TUI (`OrcaLogyApp`) is implemented and launches by default without arguments (TSK-49/50).
* [x] `rich` or `colorama` is available in the dependency stack via Poetry.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Functional - CLI Icons]:** All Typer commands (`init`, `add`, `status`, `report`, `close`) consistently prepend `✅`/`⚠️`/`❌`/`ℹ️` icons to their feedback lines.
* [ ] **[Functional - CLI Tables]:** `orca status` and `orca report` render inside Unicode box borders with aligned numeric columns.
* [ ] **[Functional - Report Colors]:** `orca report` color-codes over-budget rows in red and under-budget rows in green.
* [ ] **[Functional - TUI Welcome Panel]:** Launching `orca` (no args) or `orca tui` displays a branded welcome `Static` widget before the main dashboard.
* [ ] **[Functional - TUI Status Bar]:** The Textual app displays a bottom `Footer` bar reflecting the last operation's outcome (success/error message + color).
* [ ] **[Functional - Fallback]:** `NO_COLOR=1` strips all ANSI codes from CLI output and replaces Unicode box chars with plain ASCII equivalents.
* [ ] **[Testing/Quality - TDD]:** CLI rendering helpers are unit-tested via `capsys` (icon/border assertions); TUI panels are tested via `app.run_test()` (widget presence assertions).
* [ ] **[Verification]:** Full test suite (`pytest`) runs with 100% pass rate (no regressions).
