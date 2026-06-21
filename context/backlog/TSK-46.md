# TSK-46: Textual TUI Widget String Translation Mapping

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** NFR05 / i18n  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Refactor the Textual TUI Dashboard widgets, headers, data columns, and alerts inside OrcaLogy to utilize key-based translation resources.

This task includes:
1. Extracting all hardcoded labels, table headers, financial categories, and dialog texts from the Textual application codebase.
2. Integrating the Textual UI rendering widgets with `TranslationService` to load texts dynamically based on the selected locale.

## ✅ Definition of Ready (DoR)

* [x] i18n JSON translation engine is fully operational (TSK-45).
* [x] Textual TUI Dashboard layout is implemented (TSK-13).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Test suite asserts that TUI widget labels resolve to their localized keys for each supported language.
* [ ] **[Functional - Textual]:** Textual TUI Dashboard widgets render all labels, alerts, and table cells dynamically according to the resolved locale.
* [ ] **[Functional - Layout Integrity]:** Ensure varying string lengths across different languages do not clip or break the Textual layout grids.
* [ ] **[Verification]:** pytest runs successfully with 100% pass rate.
