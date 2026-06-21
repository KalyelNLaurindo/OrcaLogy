# TSK-47: Interactive Language Selector Dialog & Helper Cards

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** NFR05 / UX  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Improve TUI usability for laypersons by creating an interactive language selector modal and helpful prompt cards inside OrcaLogy's Textual TUI interface.

Tasks:
1. Implement a popup Dialog Modal inside the Textual TUI that allows users to pick their active language using radio buttons or quick keys (`[1] PT | [2] EN | [3] FR | [4] ES | [5] DE`).
2. Add interactive help cards explaining financial concepts (like RICE prioritizing, cost limits) in the active language.
3. Keep hotkeys consistently mapped for easy navigation (`L` for Language, `H` for Help).

## ✅ Definition of Ready (DoR)

* [x] Textual TUI Widget localization is implemented (TSK-46).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Functional - Modal]:** Textual TUI displays the interactive language selector when the user presses `L`.
* [ ] **[Functional - Refresh]:** Selecting a new language dynamically updates all TUI widgets in the active session without restarting the process.
* [ ] **[Functional - Help Cards]:** Contextual help panels render localized guides.
* [ ] **[Verification]:** pytest runs successfully with 100% pass rate.
