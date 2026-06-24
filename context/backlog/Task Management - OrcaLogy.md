# **📋 Agile Backlog & Task Management: OrcaLogy**

**Role:** Agile Coach / Tech Lead / Project Manager

**Objective:** Maintain a prioritizable backlog of atomic, SMART tasks, tracking their progress across a basic Markdown Kanban board from planning to verification.

**Context:** OrcaLogy — Phase-by-phase implementation backlog focused on delivering a secure, local-first budget execution ledger with TDD validation and Textual TUI.

## **🏛️ Backlog Metadata**

- **Project Owner:** Kalyel N. Laurindo / Project Owner
- **Lead Tech Lead:** Kalyel N. Laurindo / Software Engineer
- **Current Sprint / Iteration:** Sprint 1
- **Target Delivery Date:** July 15, 2026
- **Document Version:** v1.0

---

## **1. 📊 Prioritization & Task Sizing Framework**

- **Field 1.0 - Prioritization & Estimation Framework:** RICE Score & Simple Priority (P0-P3)

### **1.1. RICE Score Calculation Formula (Reference Only)**

RICE = (Reach _ Impact _ Confidence) / Effort

- **Reach:** 1 to 100 based on the proportion of system layers or user touchpoints affected.
- **Impact:** 3 = Massive, 2 = High, 1 = Medium, 0.5 = Low.
- **Confidence:** 1 = High/100%, 0.8 = Medium/80%, 0.5 = Low/50%.
- **Effort:** Total developer-weeks or story points required (1 = Low, 5 = High).

---

## **2. 🗂️ Prioritized Product Backlog Ledger**

The backlog is structured sequentially based on the active phases defined in the _Implementation Flow_ document. Core foundation and infrastructure tasks are marked as `[ARCH-ENABLER]` and have P0 priority.

### **📦 Backlog Phase 1: Backing Infrastructure & Configuration Setup**

- **[[TSK-01](TSK-01.md)]: Setup Python Environment & Poetry**
  - _Epic/Requirement Link:_ Phase 1.1 / ARCH-ENABLER
  - _Estimation/Priority:_ P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)
  - _TDD Test File:_ None (Env Setup)
  - _Status:_ Done

- **[[TSK-02](TSK-02.md)]: Git Repository Initialization & Config**
  - _Epic/Requirement Link:_ Phase 1.1 / ARCH-ENABLER
  - _Estimation/Priority:_ P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)
  - _TDD Test File:_ None (Git Setup)
  - _Status:_ Done

- **[[TSK-03](TSK-03.md)]: Create CLAUDE.md & Initial Commit**
  - _Epic/Requirement Link:_ Phase 1.1 / ARCH-ENABLER
  - _Estimation/Priority:_ P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)
  - _TDD Test File:_ None (Documentation Setup)
  - _Status:_ Done

- **[[TSK-04](TSK-04.md)]: Configure Dependencies in pyproject.toml**
  - _Epic/Requirement Link:_ Phase 1.1 / ARCH-ENABLER
  - _Estimation/Priority:_ P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)
  - _TDD Test File:_ None (Dep Config)
  - _Status:_ Done

- **[[TSK-05](TSK-05.md)]: Scaffold Directory Structure**
  - _Epic/Requirement Link:_ Phase 1.1 / ARCH-ENABLER
  - _Estimation/Priority:_ P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)
  - _TDD Test File:_ None (Scaffolding)
  - _Status:_ Done

- **[[TSK-06](TSK-06.md)]: Config Parser for config.toml**
  - _Epic/Requirement Link:_ RF01 / ARCH-ENABLER
  - _Estimation/Priority:_ P0 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 128)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ Done

### **⚙️ Backlog Phase 2: Bounded Domain Context & Core Models**

- **[[TSK-07](TSK-07.md)]: Implement Money Value Object**
  - _Epic/Requirement Link:_ RF01 / Core Domain
  - _Estimation/Priority:_ P1 / Reach: 90, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 270)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ Done

- **[[TSK-08](TSK-08.md)]: Implement BudgetCategory Entity**
  - _Epic/Requirement Link:_ RF01 / Core Domain
  - _Estimation/Priority:_ P1 / Reach: 85, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 136)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ Done

- **[[TSK-09](TSK-09.md)]: Implement Budget Aggregate Root**
  - _Epic/Requirement Link:_ RF01 / Core Domain
  - _Estimation/Priority:_ P1 / Reach: 85, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 102)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ Done

- **[[TSK-10](TSK-10.md)]: Implement Transaction Entity**
  - _Epic/Requirement Link:_ RF01 / Core Domain
  - _Estimation/Priority:_ P1 / Reach: 85, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 136)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ Done

- **[[TSK-11](TSK-11.md)]: Implement Domain Validation Service**
  - _Epic/Requirement Link:_ RF01 / RF03 / Core Domain
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ Done

- **[[TSK-12](TSK-12.md)]: Implement Category Deviation & Ranking Math**
  - _Epic/Requirement Link:_ RF03 / Core Domain
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ Done

- **[[TSK-13](TSK-13.md)]: Define Domain Exceptions & Errors**
  - _Epic/Requirement Link:_ RF01 / Core Domain
  - _Estimation/Priority:_ P2 / Reach: 70, Impact: 1, Confidence: 0.8, Effort: 1 (RICE: 56)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ Done

- **[[TSK-14](TSK-14.md)]: Define ILedgerRepository Interface Protocol**
  - _Epic/Requirement Link:_ RF01 / ARCH-ENABLER
  - _Estimation/Priority:_ P0 / Reach: 90, Impact: 3, Confidence: 0.8, Effort: 1 (RICE: 216)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ Done

### **⚡ Backlog Phase 3: Test-Driven Core Logic (Use Cases)**

- **[[TSK-15](TSK-15.md)]: Create bootstrap.py DI Container**
  - _Epic/Requirement Link:_ Phase 3.1 / ARCH-ENABLER
  - _Estimation/Priority:_ P0 / Reach: 95, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 114)
  - _TDD Test File:_ `tests/test_app.py`
  - _Status:_ Done

- **[[TSK-16](TSK-16.md)]: Implement Register Transaction Use Case**
  - _Epic/Requirement Link:_ RF01 / RF03 / Core Use Cases
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)
  - _TDD Test File:_ `tests/test_app.py`
  - _Status:_ Done

- **[[TSK-17](TSK-17.md)]: Implement Get Category Deviation Ranking Use Case**
  - _Epic/Requirement Link:_ RF03 / Core Use Cases
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)
  - _TDD Test File:_ `tests/test_app.py`
  - _Status:_ Done

- **[[TSK-18](TSK-18.md)]: Implement Close Fiscal Cycle Use Case**
  - _Epic/Requirement Link:_ Phase 3.1 / Core Use Cases
  - _Estimation/Priority:_ P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 60)
  - _TDD Test File:_ `tests/test_app.py`
  - _Status:_ Done

- **[[TSK-19](TSK-19.md)]: Implement Initialize Budget & Limits Use Case**
  - _Epic/Requirement Link:_ Phase 3.1 / Core Use Cases
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 64)
  - _TDD Test File:_ `tests/test_app.py`
  - _Status:_ Done

### **🔌 Backlog Phase 4: Interface Adapters & Persistence Adapters**

- **[[TSK-20](TSK-20.md)]: Concurrency Advisory File Locker**
  - _Epic/Requirement Link:_ RF02 / PERSISTENCE
  - _Estimation/Priority:_ P0 / Reach: 90, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 108)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ Done

- **[[TSK-21](TSK-21.md)]: Lexical Flat-Text Journal Parser**
  - _Epic/Requirement Link:_ RF01 / PERSISTENCE
  - _Estimation/Priority:_ P0 / Reach: 90, Impact: 3, Confidence: 0.8, Effort: 3 (RICE: 72)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ Done

- **[[TSK-22](TSK-22.md)]: Atomic File Repository Writer**
  - _Epic/Requirement Link:_ RF01 / RF02 / PERSISTENCE
  - _Estimation/Priority:_ P0 / Reach: 90, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 108)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ Done

- **[[TSK-23](TSK-23.md)]: Setup Typer CLI Controller & Commands**
  - _Epic/Requirement Link:_ RF01 / CLI
  - _Estimation/Priority:_ P1 / Reach: 85, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 68)
  - _TDD Test File:_ `tests/test_cli.py`
  - _Status:_ Done

- **[[TSK-24](TSK-24.md)]: Implement orca init CLI Command**
  - _Epic/Requirement Link:_ RF01 / CLI
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 64)
  - _TDD Test File:_ `tests/test_cli.py`
  - _Status:_ Done

- **[[TSK-25](TSK-25.md)]: Implement orca add CLI Command with Validation Prompt**
  - _Epic/Requirement Link:_ RF01 / RF03 / CLI
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 3 (RICE: 64)
  - _TDD Test File:_ `tests/test_cli.py`
  - _Status:_ Done

- **[[TSK-26](TSK-26.md)]: Implement orca report CLI Command**
  - _Epic/Requirement Link:_ RF03 / CLI
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)
  - _TDD Test File:_ `tests/test_cli.py`
  - _Status:_ Done

- **[[TSK-41](TSK-41.md)]: Implement orca close CLI Command**
  - _Epic/Requirement Link:_ RF01 / CLI
  - _Estimation/Priority:_ P1 / Reach: 75, Impact: 2, Confidence: 1.0, Effort: 1 (RICE: 150)
  - _TDD Test File:_ `tests/test_cli.py`
  - _Status:_ Done

- **[[TSK-42](TSK-42.md)]: Implement orca status CLI Command**
  - _Epic/Requirement Link:_ RF03 / CLI
  - _Estimation/Priority:_ P1 / Reach: 75, Impact: 2, Confidence: 1.0, Effort: 1 (RICE: 150)
  - _TDD Test File:_ `tests/test_cli.py`
  - _Status:_ Done

- **[[TSK-43](TSK-43.md)]: Configurable Data Directory via config.toml**
  - _Epic/Requirement Link:_ RF01 / CONFIGURATION
  - _Estimation/Priority:_ P1 / Reach: 70, Impact: 1, Confidence: 0.8, Effort: 1 (RICE: 56)
  - _TDD Test File:_ `tests/test_cli.py`
  - _Status:_ Done

- **[[TSK-27](TSK-27.md)]: Setup Textual TUI Application Framework**
  - _Epic/Requirement Link:_ RF05 / TUI
  - _Estimation/Priority:_ P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 3 (RICE: 40)
  - _TDD Test File:_ `tests/test_tui.py`
  - _Status:_ Done

- **[[TSK-28](TSK-28.md)]: Implement Textual TUI Dashboard Screen**
  - _Epic/Requirement Link:_ RF05 / TUI
  - _Estimation/Priority:_ P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 3 (RICE: 40)
  - _TDD Test File:_ `tests/test_tui.py`
  - _Status:_ Done

- **[[TSK-29](TSK-29.md)]: Implement Textual TUI Transaction Entry Dialog**
  - _Epic/Requirement Link:_ RF05 / TUI
  - _Estimation/Priority:_ P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 3 (RICE: 40)
  - _TDD Test File:_ `tests/test_tui.py`
  - _Status:_ Done

### **🛡️ Backlog Phase 5: Diagnostics, Observability & Hardening**

- **[[TSK-30](TSK-30.md)]: Configure Rotating File JSON Logging**
  - _Epic/Requirement Link:_ Phase 5.1 / OBSERVABILITY
  - _Estimation/Priority:_ P2 / Reach: 85, Impact: 1, Confidence: 0.8, Effort: 1 (RICE: 68)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ Done

- **[[TSK-31](TSK-31.md)]: Implement Read-Only Circuit Breaker for Corrupted Ledgers**
  - _Epic/Requirement Link:_ Phase 5.1 / HARDENING
  - _Estimation/Priority:_ P2 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 64)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ Done

- **[[TSK-32](TSK-32.md)]: Implement Automated Backup Utility**
  - _Epic/Requirement Link:_ Phase 5.1 / HARDENING
  - _Estimation/Priority:_ P2 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 128)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ Done

- **[[TSK-44](TSK-44.md)]: Graceful Concurrency Lock Timeout Handling**
  - _Epic/Requirement Link:_ RF02 / HARDENING
  - _Estimation/Priority:_ P1 / Reach: 90, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 144)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

- **[[TSK-49](TSK-49.md)]: Shared Read-Locks for Concurrency Isolation in Repository Reads**
  - _Epic/Requirement Link:_ RF02 / Concurrency Safety
  - _Estimation/Priority:_ P1 / Reach: 90, Impact: 2.5, Confidence: 0.9, Effort: 1 (RICE: 202.5)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do


### **📦 Backlog Phase 6: Packaging, CI/CD & Release Preparation**

- **[[TSK-33](TSK-33.md)]: Create MIT License File**
  - _Epic/Requirement Link:_ Phase 6.1 / PACKAGING
  - _Estimation/Priority:_ P3 / Reach: 100, Impact: 1, Confidence: 1.0, Effort: 1 (RICE: 100)
  - _TDD Test File:_ None
  - _Status:_ Done

- **[[TSK-34](TSK-34.md)]: Configure GitHub Actions CI Pipeline**
  - _Epic/Requirement Link:_ Phase 6.1 / CI/CD
  - _Estimation/Priority:_ P2 / Reach: 95, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 76)
  - _TDD Test File:_ None
  - _Status:_ Done

- **[[TSK-35](TSK-35.md)]: Compile Final README.md Documentation**
  - _Epic/Requirement Link:_ Phase 6.1 / DOCUMENTATION
  - _Estimation/Priority:_ P2 / Reach: 100, Impact: 2, Confidence: 1.0, Effort: 1 (RICE: 200)
  - _TDD Test File:_ None
  - _Status:_ Done

### **🚀 Backlog Phase 7: Advanced Features & Extensions**

- **[[TSK-36](TSK-36.md)]: CSV Import/Export Engine**
  - _Epic/Requirement Link:_ Phase 7.1 / PORTABILITY
  - _Estimation/Priority:_ P2 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 64)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

- **[[TSK-37](TSK-37.md)]: Secure Cryptographic Ledger**
  - _Epic/Requirement Link:_ Phase 7.2 / SECURITY
  - _Estimation/Priority:_ P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 3 (RICE: 64)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

- **[[TSK-38](TSK-38.md)]: Git Cloud Backup & Auto-Sync**
  - _Epic/Requirement Link:_ Phase 7.3 / SYNC
  - _Estimation/Priority:_ P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 60)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

- **[[TSK-39](TSK-39.md)]: Tag-based Analytics & Reporting**
  - _Epic/Requirement Link:_ Phase 7.4 / ANALYTICS
  - _Estimation/Priority:_ P2 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 64)
  - _TDD Test File:_ `tests/test_domain.py`
  - _Status:_ To Do

- **[[TSK-40](TSK-40.md)]: Multi-Format Report Exporter**
  - _Epic/Requirement Link:_ Phase 7.5 / PORTABILITY
  - _Estimation/Priority:_ P2 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 128)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

### **🌐 Backlog Phase 7.1: Internacionalização (i18n) & Localização TUI**

- **[[TSK-45](TSK-45.md)]: i18n JSON translation engine & config adapter**
  - _Epic/Requirement Link:_ Phase 7.6 / i18n
  - _Estimation/Priority:_ P2 / Reach: 90, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 72)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

- **[[TSK-46](TSK-46.md)]: Textual TUI Widget String Translation Mapping**
  - _Epic/Requirement Link:_ Phase 7.6 / i18n
  - _Estimation/Priority:_ P2 / Reach: 90, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 72)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

### **🔧 Backlog Phase 8: CI Quality & Cross-Platform Stability**

- **[[TSK-50](TSK-50.md)]: Fix Cross-Platform CI Failures — Unicode & TUI on Linux**
  - _Epic/Requirement Link:_ CI Stability / Cross-Platform Quality
  - _Estimation/Priority:_ P1 / Reach: 100, Impact: 3, Confidence: 0.8, Effort: 3 (RICE: 80)
  - _TDD Test File:_ `tests/test_tui.py`, `.github/workflows/ci.yml`
  - _Status:_ To Do

### **🎨 Backlog Phase 7.2: Acessibilidade & UX Modal Interativo**

- **[[TSK-47](TSK-47.md)]: Interactive Language Selector Dialog & Helper Cards**
  - _Epic/Requirement Link:_ Phase 7.7 / UX
  - _Estimation/Priority:_ P2 / Reach: 95, Impact: 2.5, Confidence: 0.9, Effort: 1 (RICE: 213.75)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

- **[[TSK-48](TSK-48.md)]: TUI & Textual Screen-Reader Adaptations & Contrast Policy**
  - _Epic/Requirement Link:_ Phase 7.7 / Acessibilidade
  - _Estimation/Priority:_ P2 / Reach: 95, Impact: 3.0, Confidence: 1.0, Effort: 1 (RICE: 285.0)
  - _TDD Test File:_ `tests/test_infra.py`
  - _Status:_ To Do

- **[[TSK-51](TSK-51.md)]: HTTP REST API Backend Server Integration**
  - _Epic/Requirement Link:_ HTTP Backend Services
  - _Estimation/Priority:_ P2 / Reach: 95, Impact: 3.0, Confidence: 0.9, Effort: 3 (RICE: 85.5)
  - _TDD Test File:_ `tests/test_cli.py`
  - _Status:_ To Do

---

## **2. 📋 Basic Markdown Kanban Board**

### **🔴 To Do (Ready for Development)**

- [ ] **[[TSK-36](TSK-36.md)]:** CSV Import/Export Engine
- [ ] **[[TSK-37](TSK-37.md)]:** Secure Cryptographic Ledger
- [ ] **[[TSK-38](TSK-38.md)]:** Git Cloud Backup & Auto-Sync
- [ ] **[[TSK-39](TSK-39.md)]:** Tag-based Analytics & Reporting
- [ ] **[[TSK-40](TSK-40.md)]:** Multi-Format Report Exporter
- [ ] **[[TSK-44](TSK-44.md)]:** Graceful Concurrency Lock Timeout Handling
- [ ] **[[TSK-49](TSK-49.md)]:** Shared Read-Locks for Concurrency Isolation in Repository Reads (1 SP)
- [ ] **[[TSK-50](TSK-50.md)]:** Fix Cross-Platform CI Failures — Unicode & TUI on Linux (P1)
- [ ] **[[TSK-45](TSK-45.md)]:** i18n JSON translation engine & config adapter (2 SP)
- [ ] **[[TSK-46](TSK-46.md)]:** Textual TUI Widget String Translation Mapping (2 SP)
- [ ] **[[TSK-47](TSK-47.md)]:** Interactive Language Selector Dialog & Helper Cards (1 SP)
- [ ] **[[TSK-48](TSK-48.md)]:** TUI & Textual Screen-Reader Adaptations & Contrast Policy (1 SP)
- [ ] **[[TSK-51](TSK-51.md)]:** HTTP REST API Backend Server Integration (3 SP)



### **🟡 In Progress (Actively Being Built)**

_None_

### **🔵 In Review (QA & Test Verification)**

_None_

### **🟢 Done (Merged & Verified in Main Trunk)**

- [x] **[[TSK-34](TSK-34.md)]:** Configure GitHub Actions CI Pipeline
- [x] **[[TSK-35](TSK-35.md)]:** Compile Final README.md Documentation
- [x] **[[TSK-33](TSK-33.md)]:** Create MIT License File
- [x] **[[TSK-32](TSK-32.md)]:** Implement Automated Backup Utility
- [x] **[[TSK-31](TSK-31.md)]:** Implement Read-Only Circuit Breaker for Corrupted Ledgers
- [x] **[[TSK-30](TSK-30.md)]:** Configure Rotating File JSON Logging
- [x] **[[TSK-29](TSK-29.md)]:** Implement Textual TUI Transaction Entry Dialog
- [x] **[[TSK-41](TSK-41.md)]:** Implement orca close CLI Command
- [x] **[[TSK-42](TSK-42.md)]:** Implement orca status CLI Command
- [x] **[[TSK-43](TSK-43.md)]:** Configurable Data Directory via config.toml
- [x] **[[TSK-23](TSK-23.md)]:** Setup Typer CLI Controller & Commands
- [x] **[[TSK-24](TSK-24.md)]:** Implement orca init CLI Command
- [x] **[[TSK-25](TSK-25.md)]:** Implement orca add CLI Command with Validation
- [x] **[[TSK-26](TSK-26.md)]:** Implement orca report CLI Command
- [x] **[[TSK-28](TSK-28.md)]:** Implement Textual TUI Dashboard Screen
- [x] **[[TSK-27](TSK-27.md)]:** Setup Textual TUI Application Framework
- [x] **[[TSK-22](TSK-22.md)]:** Atomic File Repository Writer
- [x] **[[TSK-21](TSK-21.md)]:** Lexical Flat-Text Journal Parser
- [x] **[[TSK-01](TSK-01.md)]:** Setup Python Environment & Poetry
- [x] **[[TSK-02](TSK-02.md)]:** Git Repository Initialization & Config
- [x] **[[TSK-03](TSK-03.md)]:** Create README.md & Initial Commit
- [x] **[[TSK-04](TSK-04.md)]:** Configure Dependencies in pyproject.toml
- [x] **[[TSK-05](TSK-05.md)]:** Scaffold Directory Structure
- [x] **[[TSK-06](TSK-06.md)]:** Config Parser for config.toml
- [x] **[[TSK-07](TSK-07.md)]:** Implement Money Value Object
- [x] **[[TSK-08](TSK-08.md)]:** Implement BudgetCategory Entity
- [x] **[[TSK-09](TSK-09.md)]:** Implement Budget Aggregate Root
- [x] **[[TSK-10](TSK-10.md)]:** Implement Transaction Entity
- [x] **[[TSK-11](TSK-11.md)]:** Implement Domain Validation Service
- [x] **[[TSK-12](TSK-12.md)]:** Implement Category Deviation & Ranking Math
- [x] **[[TSK-13](TSK-13.md)]:** Define Domain Exceptions & Errors
- [x] **[[TSK-14](TSK-14.md)]:** Define ILedgerRepository Interface Protocol
- [x] **[[TSK-15](TSK-15.md)]:** Create bootstrap.py DI Container
- [x] **[[TSK-16](TSK-16.md)]:** Implement Register Transaction Use Case
- [x] **[[TSK-17](TSK-17.md)]:** Implement Get Category Deviation Ranking Use Case
- [x] **[[TSK-18](TSK-18.md)]:** Implement Close Fiscal Cycle Use Case
- [x] **[[TSK-19](TSK-19.md)]:** Implement Initialize Budget & Limits Use Case
- [x] **[[TSK-20](TSK-20.md)]:** Concurrency Advisory File Locker
