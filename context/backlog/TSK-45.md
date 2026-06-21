# TSK-45: i18n JSON translation engine & config adapter

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** NFR05 / i18n  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Establish a localized translation registry and engine inside OrcaLogy supporting Portuguese, English, French, Spanish, and German to support multi-national developers in personal financial calculations.

The engine will:
1. Parse JSON files matching codes (`pt`, `en`, `fr`, `es`, `de`) inside `locales/` folder.
2. Read default user language configuration from `config.json`.
3. Provide a localized service resolving keys and replacing format tokens.

## ✅ Definition of Ready (DoR)

* [x] Basic configuration system is implemented and reads `config.json`.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Unit tests verify that JSON locale files parse successfully and return expected localized strings.
* [ ] **[Functional - Setup]:** Locales directory contains translation tables: `pt.json`, `en.json`, `fr.json`, `es.json`, `de.json`.
* [ ] **[Functional - Precedence]:** Resolves active language using precedence: 1. CLI flag, 2. `config.json` entry, 3. system locale, 4. fallback `pt`.
* [ ] **[Verification]:** pytest runs successfully with 100% pass rate.
