# TSK-39: Tag-based Analytics & Reporting

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 4 Hours  
* **Story / Epic Reference:** Phase 7.4 / ANALYTICS  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement parsing and consolidation of hashtags (e.g., `#groceries`, `#delivery`) inside transaction descriptions. Provide an analytics view listing tag totals and percentages within categories or the global budget scope.

## ✅ Definition of Ready (DoR)

* [ ] Lexical flat-text journal parser (TSK-21) is functional.
* [ ] Domain models and ranking (TSK-12) are verified.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Test suite parses tags from description strings and compiles analytics maps before implementation.
* [ ] **[Functional - Analytics]:** Sub-group transaction amounts under unique tags and present summaries in reports.
* [ ] **[Verification]:** `pytest tests/test_domain.py` verifying that tags are properly extracted from comments/descriptions and accumulated correctly.
