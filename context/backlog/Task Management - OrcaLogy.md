# **📋 Agile Backlog & Task Management: OrcaLogy**

**Role:** Agile Coach / Tech Lead / Project Manager

**Objective:** Maintain a prioritizable backlog of atomic, SMART tasks, tracking their progress across a basic Markdown Kanban board from planning to verification.

**Context:** OrcaLogy — Phase-by-phase implementation backlog focused on delivering a secure, local-first budget execution ledger with TDD validation and Textual TUI.

## **🏛️ Backlog Metadata**

* **Project Owner:** Kalyel N. Laurindo / Project Owner  
* **Lead Tech Lead:** Kalyel N. Laurindo / Software Engineer  
* **Current Sprint / Iteration:** Sprint 1  
* **Target Delivery Date:** July 15, 2026  
* **Document Version:** v1.0

---

## **1. 📊 Prioritization & Task Sizing Framework**

*   **Field 1.0 - Prioritization & Estimation Framework:** RICE Score & Simple Priority (P0-P3)

### **1.1. RICE Score Calculation Formula (Reference Only)**

RICE = (Reach * Impact * Confidence) / Effort

* **Reach:** 1 to 100 based on the proportion of system layers or user touchpoints affected.  
* **Impact:** 3 = Massive, 2 = High, 1 = Medium, 0.5 = Low.  
* **Confidence:** 1 = High/100%, 0.8 = Medium/80%, 0.5 = Low/50%.  
* **Effort:** Total developer-weeks or story points required (1 = Low, 5 = High).

---

## **2. 🗂️ Prioritized Product Backlog Ledger**

The backlog is structured sequentially based on the active phases defined in the *Implementation Flow* document. Core foundation and infrastructure tasks are marked as `[ARCH-ENABLER]` and have P0 priority.

### **📦 Backlog Phase 1: Backing Infrastructure & Configuration Setup**

* **[[TSK-01](TSK-01.md)]: Setup Python Environment & Poetry**  
  * *Epic/Requirement Link:* Phase 1.1 / ARCH-ENABLER  
  * *Estimation/Priority:* P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)  
  * *TDD Test File:* None (Env Setup)  
  * *Status:* Done  

* **[[TSK-02](TSK-02.md)]: Git Repository Initialization & Config**  
  * *Epic/Requirement Link:* Phase 1.1 / ARCH-ENABLER  
  * *Estimation/Priority:* P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)  
  * *TDD Test File:* None (Git Setup)  
  * *Status:* Done  

* **[[TSK-03](TSK-03.md)]: Create CLAUDE.md & Initial Commit**  
  * *Epic/Requirement Link:* Phase 1.1 / ARCH-ENABLER  
  * *Estimation/Priority:* P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)  
  * *TDD Test File:* None (Documentation Setup)  
  * *Status:* Done  

* **[[TSK-04](TSK-04.md)]: Configure Dependencies in pyproject.toml**  
  * *Epic/Requirement Link:* Phase 1.1 / ARCH-ENABLER  
  * *Estimation/Priority:* P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)  
  * *TDD Test File:* None (Dep Config)  
  * *Status:* Done  

* **[[TSK-05](TSK-05.md)]: Scaffold Directory Structure**  
  * *Epic/Requirement Link:* Phase 1.1 / ARCH-ENABLER  
  * *Estimation/Priority:* P0 / Reach: 100, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 300)  
  * *TDD Test File:* None (Scaffolding)  
  * *Status:* Done  

* **[[TSK-06](TSK-06.md)]: Config Parser for config.toml**  
  * *Epic/Requirement Link:* RF01 / ARCH-ENABLER  
  * *Estimation/Priority:* P0 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 128)  
  * *TDD Test File:* `tests/test_infra.py`  
  * *Status:* Done  

### **⚙️ Backlog Phase 2: Bounded Domain Context & Core Models**

* **[[TSK-07](TSK-07.md)]: Implement Money Value Object**  
  * *Epic/Requirement Link:* RF01 / Core Domain  
  * *Estimation/Priority:* P1 / Reach: 90, Impact: 3, Confidence: 1.0, Effort: 1 (RICE: 270)  
  * *TDD Test File:* `tests/test_domain.py`  
  * *Status:* Done  

* **[[TSK-08](TSK-08.md)]: Implement BudgetCategory Entity**  
  * *Epic/Requirement Link:* RF01 / Core Domain  
  * *Estimation/Priority:* P1 / Reach: 85, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 136)  
  * *TDD Test File:* `tests/test_domain.py`  
  * *Status:* Done  

* **[[TSK-09](TSK-09.md)]: Implement Budget Aggregate Root**  
  * *Epic/Requirement Link:* RF01 / Core Domain  
  * *Estimation/Priority:* P1 / Reach: 85, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 102)  
  * *TDD Test File:* `tests/test_domain.py`  
  * *Status:* Done  

* **[[TSK-10](TSK-10.md)]: Implement Transaction Entity**  
  * *Epic/Requirement Link:* RF01 / Core Domain  
  * *Estimation/Priority:* P1 / Reach: 85, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 136)  
  * *TDD Test File:* `tests/test_domain.py`  
  * *Status:* Done  

* **[[TSK-11](TSK-11.md)]: Implement Domain Validation Service**  
  * *Epic/Requirement Link:* RF01 / RF03 / Core Domain  
  * *Estimation/Priority:* P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)  
  * *TDD Test File:* `tests/test_domain.py`  
  * *Status:* Done  

* **[[TSK-12](TSK-12.md)]: Implement Category Deviation & Ranking Math**  
  * *Epic/Requirement Link:* RF03 / Core Domain  
  * *Estimation/Priority:* P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)  
  * *TDD Test File:* `tests/test_domain.py`  
  * *Status:* Done  

* **[[TSK-13](TSK-13.md)]: Define Domain Exceptions & Errors**  
  * *Epic/Requirement Link:* RF01 / Core Domain  
  * *Estimation/Priority:* P2 / Reach: 70, Impact: 1, Confidence: 0.8, Effort: 1 (RICE: 56)  
  * *TDD Test File:* `tests/test_domain.py`  
  * *Status:* Done  

* **[[TSK-14](TSK-14.md)]: Define ILedgerRepository Interface Protocol**  
  * *Epic/Requirement Link:* RF01 / ARCH-ENABLER  
  * *Estimation/Priority:* P0 / Reach: 90, Impact: 3, Confidence: 0.8, Effort: 1 (RICE: 216)  
  * *TDD Test File:* `tests/test_domain.py`  
  * *Status:* Done  

### **⚡ Backlog Phase 3: Test-Driven Core Logic (Use Cases)**

* **[[TSK-15](TSK-15.md)]: Create bootstrap.py DI Container**  
  * *Epic/Requirement Link:* Phase 3.1 / ARCH-ENABLER  
  * *Estimation/Priority:* P0 / Reach: 95, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 114)  
  * *TDD Test File:* `tests/test_app.py`  
  * *Status:* Done  

* **[[TSK-16](TSK-16.md)]: Implement Register Transaction Use Case**  
  * *Epic/Requirement Link:* RF01 / RF03 / Core Use Cases  
  * *Estimation/Priority:* P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)  
  * *TDD Test File:* `tests/test_app.py`  
  * *Status:* Done  

* **[[TSK-17](TSK-17.md)]: Implement Get Category Deviation Ranking Use Case**  
  * *Epic/Requirement Link:* RF03 / Core Use Cases  
  * *Estimation/Priority:* P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)  
  * *TDD Test File:* `tests/test_app.py`  
  * *Status:* Done  

* **[[TSK-18](TSK-18.md)]: Implement Close Fiscal Cycle Use Case**  
  * *Epic/Requirement Link:* Phase 3.1 / Core Use Cases  
  * *Estimation/Priority:* P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 60)  
  * *TDD Test File:* `tests/test_app.py`  
  * *Status:* To Do  

* **[[TSK-19](TSK-19.md)]: Implement Initialize Budget & Limits Use Case**  
  * *Epic/Requirement Link:* Phase 3.1 / Core Use Cases  
  * *Estimation/Priority:* P1 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 64)  
  * *TDD Test File:* `tests/test_app.py`  
  * *Status:* To Do  

### **🔌 Backlog Phase 4: Interface Adapters & Persistence Adapters**

* **[[TSK-20](TSK-20.md)]: Concurrency Advisory File Locker**  
  * *Epic/Requirement Link:* RF02 / PERSISTENCE  
  * *Estimation/Priority:* P0 / Reach: 90, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 108)  
  * *TDD Test File:* `tests/test_infra.py`  
  * *Status:* To Do  

* **[[TSK-21](TSK-21.md)]: Lexical Flat-Text Journal Parser**  
  * *Epic/Requirement Link:* RF01 / PERSISTENCE  
  * *Estimation/Priority:* P0 / Reach: 90, Impact: 3, Confidence: 0.8, Effort: 3 (RICE: 72)  
  * *TDD Test File:* `tests/test_infra.py`  
  * *Status:* To Do  

* **[[TSK-22](TSK-22.md)]: Atomic File Repository Writer**  
  * *Epic/Requirement Link:* RF01 / RF02 / PERSISTENCE  
  * *Estimation/Priority:* P0 / Reach: 90, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 108)  
  * *TDD Test File:* `tests/test_infra.py`  
  * *Status:* To Do  

* **[[TSK-23](TSK-23.md)]: Setup Typer CLI Controller & Commands**  
  * *Epic/Requirement Link:* RF01 / CLI  
  * *Estimation/Priority:* P1 / Reach: 85, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 68)  
  * *TDD Test File:* `tests/test_cli.py`  
  * *Status:* To Do  

* **[[TSK-24](TSK-24.md)]: Implement orca init CLI Command**  
  * *Epic/Requirement Link:* RF01 / CLI  
  * *Estimation/Priority:* P1 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 64)  
  * *TDD Test File:* `tests/test_cli.py`  
  * *Status:* To Do  

* **[[TSK-25](TSK-25.md)]: Implement orca add CLI Command with Validation Prompt**  
  * *Epic/Requirement Link:* RF01 / RF03 / CLI  
  * *Estimation/Priority:* P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 3 (RICE: 64)  
  * *TDD Test File:* `tests/test_cli.py`  
  * *Status:* To Do  

* **[[TSK-26](TSK-26.md)]: Implement orca report CLI Command**  
  * *Epic/Requirement Link:* RF03 / CLI  
  * *Estimation/Priority:* P1 / Reach: 80, Impact: 3, Confidence: 0.8, Effort: 2 (RICE: 96)  
  * *TDD Test File:* `tests/test_cli.py`  
  * *Status:* To Do  

* **[[TSK-27](TSK-27.md)]: Setup Textual TUI Application Framework**  
  * *Epic/Requirement Link:* RF05 / TUI  
  * *Estimation/Priority:* P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 3 (RICE: 40)  
  * *TDD Test File:* `tests/test_tui.py`  
  * *Status:* To Do  

* **[[TSK-28](TSK-28.md)]: Implement Textual TUI Dashboard Screen**  
  * *Epic/Requirement Link:* RF05 / TUI  
  * *Estimation/Priority:* P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 3 (RICE: 40)  
  * *TDD Test File:* `tests/test_tui.py`  
  * *Status:* To Do  

* **[[TSK-29](TSK-29.md)]: Implement Textual TUI Transaction Entry Dialog**  
  * *Epic/Requirement Link:* RF05 / TUI  
  * *Estimation/Priority:* P2 / Reach: 75, Impact: 2, Confidence: 0.8, Effort: 3 (RICE: 40)  
  * *TDD Test File:* `tests/test_tui.py`  
  * *Status:* To Do  

### **🛡️ Backlog Phase 5: Diagnostics, Observability & Hardening**

* **[[TSK-30](TSK-30.md)]: Configure Rotating File JSON Logging**  
  * *Epic/Requirement Link:* Phase 5.1 / OBSERVABILITY  
  * *Estimation/Priority:* P2 / Reach: 85, Impact: 1, Confidence: 0.8, Effort: 1 (RICE: 68)  
  * *TDD Test File:* `tests/test_infra.py`  
  * *Status:* To Do  

* **[[TSK-31](TSK-31.md)]: Implement Read-Only Circuit Breaker for Corrupted Ledgers**  
  * *Epic/Requirement Link:* Phase 5.1 / HARDENING  
  * *Estimation/Priority:* P2 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 64)  
  * *TDD Test File:* `tests/test_infra.py`  
  * *Status:* To Do  

* **[[TSK-32](TSK-32.md)]: Implement Automated Backup Utility**  
  * *Epic/Requirement Link:* Phase 5.1 / HARDENING  
  * *Estimation/Priority:* P2 / Reach: 80, Impact: 2, Confidence: 0.8, Effort: 1 (RICE: 128)  
  * *TDD Test File:* `tests/test_infra.py`  
  * *Status:* To Do  

### **📦 Backlog Phase 6: Packaging, CI/CD & Release Preparation**

* **[[TSK-33](TSK-33.md)]: Create MIT License File**  
  * *Epic/Requirement Link:* Phase 6.1 / PACKAGING  
  * *Estimation/Priority:* P3 / Reach: 100, Impact: 1, Confidence: 1.0, Effort: 1 (RICE: 100)  
  * *TDD Test File:* None  
  * *Status:* To Do  

* **[[TSK-34](TSK-34.md)]: Configure GitHub Actions CI Pipeline**  
  * *Epic/Requirement Link:* Phase 6.1 / CI/CD  
  * *Estimation/Priority:* P2 / Reach: 95, Impact: 2, Confidence: 0.8, Effort: 2 (RICE: 76)  
  * *TDD Test File:* None  
  * *Status:* To Do  

* **[[TSK-35](TSK-35.md)]: Compile Final README.md Documentation**  
  * *Epic/Requirement Link:* Phase 6.1 / DOCUMENTATION  
  * *Estimation/Priority:* P2 / Reach: 100, Impact: 2, Confidence: 1.0, Effort: 1 (RICE: 200)  
  * *TDD Test File:* None  
  * *Status:* To Do  

---

## **3. 📋 Basic Markdown Kanban Board**

### **🔴 To Do (Ready for Development)**

* [ ] **[[TSK-18](TSK-18.md)]:** Implement Close Fiscal Cycle Use Case
* [ ] **[[TSK-19](TSK-19.md)]:** Implement Initialize Budget & Limits Use Case
* [ ] **[[TSK-20](TSK-20.md)]:** Concurrency Advisory File Locker
* [ ] **[[TSK-21](TSK-21.md)]:** Lexical Flat-Text Journal Parser
* [ ] **[[TSK-22](TSK-22.md)]:** Atomic File Repository Writer
* [ ] **[[TSK-23](TSK-23.md)]:** Setup Typer CLI Controller & Commands
* [ ] **[[TSK-24](TSK-24.md)]:** Implement orca init CLI Command
* [ ] **[[TSK-25](TSK-25.md)]:** Implement orca add CLI Command with Validation Prompt
* [ ] **[[TSK-26](TSK-26.md)]:** Implement orca report CLI Command
* [ ] **[[TSK-27](TSK-27.md)]:** Setup Textual TUI Application Framework
* [ ] **[[TSK-28](TSK-28.md)]:** Implement Textual TUI Dashboard Screen
* [ ] **[[TSK-29](TSK-29.md)]:** Implement Textual TUI Transaction Entry Dialog
* [ ] **[[TSK-30](TSK-30.md)]:** Configure Rotating File JSON Logging
* [ ] **[[TSK-31](TSK-31.md)]:** Implement Read-Only Circuit Breaker for Corrupted Ledgers
* [ ] **[[TSK-32](TSK-32.md)]:** Implement Automated Backup Utility
* [ ] **[[TSK-33](TSK-33.md)]:** Create MIT License File
* [ ] **[[TSK-34](TSK-34.md)]:** Configure GitHub Actions CI Pipeline
* [ ] **[[TSK-35](TSK-35.md)]:** Compile Final README.md Documentation

### **🟡 In Progress (Actively Being Built)**

*None*

### **🔵 In Review (QA & Test Verification)**

*None*

### **🟢 Done (Merged & Verified in Main Trunk)**

* [x] **[[TSK-01](TSK-01.md)]:** Setup Python Environment & Poetry
* [x] **[[TSK-02](TSK-02.md)]:** Git Repository Initialization & Config
* [x] **[[TSK-03](TSK-03.md)]:** Create CLAUDE.md & Initial Commit
* [x] **[[TSK-04](TSK-04.md)]:** Configure Dependencies in pyproject.toml
* [x] **[[TSK-05](TSK-05.md)]:** Scaffold Directory Structure
* [x] **[[TSK-06](TSK-06.md)]:** Config Parser for config.toml
* [x] **[[TSK-07](TSK-07.md)]:** Implement Money Value Object
* [x] **[[TSK-08](TSK-08.md)]:** Implement BudgetCategory Entity
* [x] **[[TSK-09](TSK-09.md)]:** Implement Budget Aggregate Root
* [x] **[[TSK-10](TSK-10.md)]:** Implement Transaction Entity
* [x] **[[TSK-11](TSK-11.md)]:** Implement Domain Validation Service
* [x] **[[TSK-12](TSK-12.md)]:** Implement Category Deviation & Ranking Math
* [x] **[[TSK-13](TSK-13.md)]:** Define Domain Exceptions & Errors
* [x] **[[TSK-14](TSK-14.md)]:** Define ILedgerRepository Interface Protocol
* [x] **[[TSK-15](TSK-15.md)]:** Create bootstrap.py DI Container
* [x] **[[TSK-16](TSK-16.md)]:** Implement Register Transaction Use Case
* [x] **[[TSK-17](TSK-17.md)]:** Implement Get Category Deviation Ranking Use Case





