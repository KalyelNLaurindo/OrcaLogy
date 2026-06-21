# TSK-49: Shared Read-Locks for Concurrency Isolation in Repository Reads

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** RF02 / Concurrency Safety  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Currently, `FileLockManager` only acquires exclusive locks during save/write operations (`save_budget()`). When reading budget data (`get_budget()`), no lock is acquired. Under high concurrency, a read operation could execute exactly in the millisecond when a writer has replaced `.meta.json` but has not yet updated the transaction journal, resulting in a dirty read (inconsistent/skewed state).

To resolve this race condition and guarantee transactional isolation (Read Committed/Repeatable Read level consistency) under multi-process concurrency, we must implement shared locks for read operations.

Tasks:
1. Extend `FileLockManager` or `locker.py` to support shared locks (Read locks) alongside exclusive locks (Write locks).
2. Update the repository read method (`get_budget()`) to acquire a shared lock before reading `.meta.json` and the transaction journal files, and release it immediately after reading.
3. Keep write operations (`save_budget()`) utilizing exclusive locks.
4. Ensure that multiple read operations can acquire shared locks concurrently without blocking each other, but a write operation blocks until all shared locks are released, and a read operation blocks if an exclusive lock is active.

## ✅ Definition of Ready (DoR)

* [x] Advisory concurrency lock manager is defined (TSK-20).
* [x] Software Design Document updated with ADR-006 outlining the Shared Read-Lock strategy.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

### BDD Scenarios (Gherkin Format):

```gherkin
Scenario: Concurrent readers do not block each other
  Given two separate processes want to read the budget repository
  When both processes invoke get_budget() concurrently
  Then both processes acquire shared locks successfully without timeout
  And both processes read the budget files without blocking each other

Scenario: Reader is blocked by an active writer
  Given process A is currently executing save_budget() and holding an exclusive write lock
  When process B attempts to execute get_budget()
  Then process B's read lock request is blocked
  And process B waits until process A releases the exclusive lock before reading the budget files

Scenario: Writer is blocked by active readers
  Given process A is executing get_budget() and holding a shared read lock
  When process B attempts to execute save_budget()
  Then process B's write lock request is blocked
  And process B waits until process A releases the shared lock before writing the budget files
```

* [ ] **[Functional - Concurrency]:** Shared locks are acquired during `get_budget()` and released upon completion.
* [ ] **[Functional - Isolation]:** Multiple readers read concurrently without blocking, but readers and writers block each other correctly.
* [ ] **[Verification]:** Multi-process integration tests are added in `tests/test_infra.py` asserting concurrent shared locks and reader-writer mutual exclusion, passing with a 100% success rate.
