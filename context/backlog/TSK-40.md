# TSK-40: Multi-Format Report Exporter

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** Phase 7.5 / PORTABILITY  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Add a report export feature to generate Markdown tables or simple static HTML reports from current or closed budget cycles, allowing users to share elegant summaries.

## ✅ Definition of Ready (DoR)

* [ ] Use case for generating rankings (TSK-17) is functional.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Unit tests verify generated string content matches markdown/HTML structures.
* [ ] **[Functional - Export]:** CLI command `orca report --export [md|html]` writes formatted files to the target directory.
* [ ] **[Verification]:** Run test suite verifying correct structure generation.
