# TSK-51: HTTP REST API Backend Server Integration

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 5 Hours  
* **Story / Epic Reference:** RF11 / HTTP Backend Services  
* **Development Methodology:** TDD & Port-Adapter Pattern

## 📖 Description & Objectives

Expose the OrcaLogy budgeting engine as an HTTP REST API server. This enables integrating the budget cycle engine with external web or mobile applications.

The server will expose the following endpoints:
1. `POST /budgets/init` - Initialize a new monthly budget (triggers `InitializeBudgetUseCase`).
2. `POST /transactions` - Register a spending transaction (triggers `RegisterTransactionUseCase`).
3. `GET /budgets/{month}/report` - Get color-coded spending deviation report.
4. `POST /budgets/{month}/close` - Close budget cycle (triggers `CloseBudgetCycleUseCase`).

## ✅ Definition of Ready (DoR)

* [ ] REST endpoints and JSON payload validation structures designed.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

### BDD Scenarios (Gherkin Format):

```gherkin
Scenario: Register spending transaction via HTTP request
  Given an active budget for "2026-06"
  When a POST request is sent to "/transactions" with payload:
    | category | amount | description | date       |
    | Food     | 50.00  | Grocery     | 2026-06-15 |
  Then the response status code is 201
  And the transaction is stored in the ledger

Scenario: Attempt transaction over limit returns warning or blocks
  Given a category close to its spending limit
  When a POST request is sent to "/transactions" exceeding the limit
  Then the response status code is 409
  And the response details the budget overrun alert
```

* [ ] **[Functional]:** HTTP REST API server integrated into the Orcalogy codebase.
* [ ] **[Functional]:** Correctly enforces advisory POSIX file locks during concurrent HTTP operations.
* [ ] **[Verification]:** Integration tests using FastAPI/Typer test clients pass.
