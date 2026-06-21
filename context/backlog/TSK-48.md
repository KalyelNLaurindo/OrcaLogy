# TSK-48: TUI & Textual Screen-Reader Adaptations & Contrast Policy

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** NFR05 / Acessibilidade  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Ensure the OrcaLogy Textual TUI (Terminal User Interface) dashboard compiles with strict accessibility design guidelines, specifically for screen readers and high-contrast terminal theme fallbacks.

Tasks:
1. Provide a monochrome high-contrast CSS theme mapping in the Textual TUI configuration, activated via environment variable `NO_COLOR=1` or command line flag `--no-color`.
2. Configure screen-reader focus nodes and descriptive accessibility tags (`accessibility` attributes in Textual widgets) to allow NVDA/JAWS to announce table values and financial charts linearly.
3. Validate keyboard navigation loops, ensuring all buttons and text entry fields inside modal dialogs are navigable using only the Tab and Arrow keys.

## ✅ Definition of Ready (DoR)

* [x] Textual TUI Widget Localization and modal dialogs are specified (TSK-47).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Functional - High Contrast]:** The TUI automatically applies a monochrome/high-contrast palette style sheet when `--no-color` or `NO_COLOR=1` is resolved.
* [ ] **[Functional - Focus]:** Tab ordering runs logically from inputs to action buttons within the budget initialization and transaction entry modals.
* [ ] **[Functional - Screen Reader]:** Screen reader accessibility tags are configured for active data widgets so they announce updates sequentially.
* [ ] **[Verification]:** pytest runs successfully with 100% pass rate.
