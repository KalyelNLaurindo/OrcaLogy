# **🤖 OrcaLogy — Claude Code / AI Assistant Reference Guide**

This file provides system context, build/test commands, architecture guidelines, and coding standards to align the development flow of **OrcaLogy** (a local-first, terminal-centric personal and team budget management CLI/TUI tool designed to enforce real-time spending limits via a deterministic Python execution engine and secure plain-text ledger files).

---

## 🛠️ Common Commands

### Running the Application

- **Run CLI commands via Poetry:**
  ```bash
  poetry run orca --help
  ```
- **Run TUI (Textual Dashboard) via Poetry:**
  ```bash
  poetry run orca tui
  ```
- **Run raw python entrypoint:**
  ```bash
  python -m orcalogy
  ```

### Running Tests

- **Run all tests:**
  ```bash
  poetry run pytest
  ```
- **Run with coverage report:**
  ```bash
  poetry run pytest --cov=orcalogy --cov-report=term-missing
  ```
- **Run specific test target:**
  ```bash
  poetry run pytest tests/test_domain.py
  ```

### Linting & Type Checking

- **Run strict static type checking:**
  ```bash
  poetry run mypy --strict orcalogy/
  ```
- **Run linter check (Ruff):**
  ```bash
  poetry run ruff check .
  ```
- **Format code with Ruff:**
  ```bash
  poetry run ruff format .
  ```

---

## 🏛️ Technology Stack & Constraints

- **Runtime Environment:** Python 3.11+
- **Production Dependencies:** Minimal core packages:
  - `typer` (CLI orchestration)
  - `textual` (TUI dashboard)
  - `filelock` (POSIX/Windows file locking)
  - `tomli` / `tomli-w` (TOML parsing/writing)
- **Persistence Strategy:** Local JSON or plain-text journal file (`ledger.journal`) plus configuration TOML file (`config.toml`).
- **Performance Targets:** In-memory lookups and operations execution under 10ms. CLI execution startup under 50ms.
- **Concurrency & Advisory Locking:** Explicit POSIX advisory file locking using the `filelock` library MUST be obtained before reading or writing to the journal file to prevent concurrent access corruption.

---

## 🏗️ Architectural Guardrails

1. **Architecture Paradigm:** Hexagonal Architecture (Ports & Adapters) integrated with Domain-Driven Design (DDD) principles.
2. **Layer Isolation:** The Domain core (`orcalogy/domain`) MUST remain pure. It cannot import `os`, `sys`, `Textual`, `Typer`, `filelock`, or any infrastructure/external libraries (zero non-stdlib framework imports).
3. **Ports & Adapters (Dependency Inversion):** Interactivity with external systems (file system, user interface, configuration files) must happen strictly through interfaces (`ILedgerRepository` Protocol) and concrete adapters.
4. **Data Durability & Transaction Safety:** State mutations must execute atomic OS replaces: serialize to a temporary file (`ledger.journal.tmp`) first, then execute an atomic operating-system replace using `os.replace` to replace the main file.
5. **Specific Domain Invariants:**
   - **Value Object `Money`**: Must wrap Python's native `decimal.Decimal` to prevent precision/rounding issues.
   - **Aggregate Root `Budget`**: Validates limits and controls state mutations, raising domain errors before writing to storage.
   - **Overrun Mathematics**: Deviation calculations must sort categories descending by overspending percentages.
6. **Engineering Principles:** Always design and write code following: DRY, KISS, SOLID principles, standard Design Patterns, and Clean Code conventions.

---

## 🧪 Testing Paradigm (TDD Mandatory)

- **Testing Approach:** Strict Test-First (TDD) (write and run failing tests before writing production code).
- **Testing Framework:** `pytest` (Python).
- **Boundary Conditions:** Explicit unit tests checking boundary conditions (e.g., negative amounts, empty ledger files, missing configuration, threshold limit transitions, and concurrent file locking contention).
- **Self-Healing Limit:** If pytest, ruff, or mypy fails more than 3 consecutive times during autonomous debugging/correction, stop execution and request human developer intervention.

---

## 📂 Codebase Directory Structure

```text
[project-root]/
├── orcalogy/                   # Main package source root
│   ├── __init__.py
│   ├── main.py                 # Application entrypoint
│   ├── bootstrap.py            # Dependency injection container
│   ├── cli/                    # CLI commands layer
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── tui/                    # TUI Desktop layout using Textual
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── screens.py
│   ├── app/                    # Application use cases orchestrator
│   │   ├── __init__.py
│   │   └── services.py
│   ├── domain/                 # Core domain logic (pure Python)
│   │   ├── __init__.py
│   │   ├── models.py           # Dataclasses & Money Value Object (Decimal wrapper)
│   │   ├── validation.py       # Limits checks logic
│   │   ├── ranking.py          # Category deviation calculations
│   │   └── errors.py
│   └── infra/                  # Infrastructure adapters
│       ├── __init__.py
│       ├── file_repo.py        # File storage & operations coordinator
│       ├── parser.py           # Flat ledger text parser
│       └── locker.py           # Advisory concurrency locking manager
├── tests/                      # Testing suites
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_domain.py
│   ├── test_infra.py
│   └── test_app.py
├── pyproject.toml              # Dependencies, Pytest, Ruff and Mypy config
└── README.md                   # Setup instructions and developer onboarding
```

---

## 🏷️ Code Governance & Naming Conventions

- **Language & Style:** All code comments, docstrings, and code symbols (classes, methods, variables) must be written in English. However, **all implementation plans (`implementation_plan.md`), walkthroughs (`walkthrough.md`), and user-facing design explanations must be written in Portuguese (PT-BR)**, using clear, simple, and highly explanatory language.
- **Naming Styles & Suffixes:**

| Role / Pattern | Naming Strategy | Example Name |
| :--- | :--- | :--- |
| **Domain Entity** | Clean PascalCase names (e.g. Entity, Aggregate) | `Budget`, `BudgetCategory` |
| **Value Object** | Clean PascalCase names | `Money`, `Transaction` |
| **Application Service** | Service/UseCase nomenclature | `BudgetService` |
| **Interface Port** | Protocols prefixed with `I` or matching domain naming | `ILedgerRepository` |
| **Concrete Adapter** | Repository/Adapter suffix | `FileLedgerRepository`, `FileLockManager` |

---

## 🌿 Git Workflow & Commit Conventions

- **Branching Strategy:**
  - All development must take place on feature branches (e.g., `feature/TSK-XX-description`).
  - **CRITICAL REQUIREMENT:** A separate git feature branch must be used for each phase of the project implementation (e.g., `feature/phase-1-infrastructure`, `feature/phase-2-domain`) to keep delivery phases isolated and tidy.
  - Direct commits to the main integration branch are prohibited; merge code via Pull Requests.
- **Semantic Commit Messages:** Use Conventional Commits standard:
  - `feat(scope):` Introduces a new feature or domain component.
  - `fix(scope):` Patches a software bug or corrects an active system failure.
  - `docs(scope):` Updates markdown documents, guides, changelogs, or walkthroughs.
  - `test(scope):` Adds or updates test files without changing production code.
  - `chore(scope):` Builds setups, configuration files, or project dependency actions.

---

## 📋 Planning & Execution Flow Checklist

For every backlog task, the AI agent and developer must strictly follow this lifecycle:

1. **Check Task & Branch Alignment:**
   - **FIRST-TIME SETUP (if repository is new):** Before any other action, verify the following exist in the project root: (1) `.git/` directory — if not, run `git init`; (2) `.gitignore` — if not, create one tailored to the project's tech stack and ensure `CLAUDE.md` is added to it to prevent it from being tracked; (3) `CLAUDE.md` — if not, create it from the standard playbook template. Once all three exist, perform an initial commit: `chore(setup): initialize repository`.
   - Inspect the backlog folder (`context/backlog/` or equivalent) and the master backlog `README.md` to identify the next pending task (`TSK-XX`).
   - Ensure you are working on the correct git feature branch (`feature/TSK-XX-description`). Create or switch to the branch if needed.
2. **Planning Phase (Before Code Modifications):**
   - Create `implementation_plan.md` in the current conversation directory **written in Portuguese (PT-BR)**.
   - **CRITICAL REQUIREMENT:** Explain the implementation steps in simple, layman-friendly language so that non-technical stakeholders can easily understand what changes and why.
   - Mark `request_feedback = true` in the plan metadata and **STOP** to wait for the user's explicit approval before writing code.
3. **Execution Phase (TDD Protocol):**
   - Create/update `task.md` in the conversation directory.
   - **Language Constraint:** Write all code, unit/integration tests, docstrings, inline comments, and technical schemas strictly in professional **Technical English**.
   - Write test cases under `tests/` and run the suite to verify they fail (Red).
   - Implement minimal production code in `src/` to satisfy the tests (Green).
   - Refactor the code while keeping all tests passing (Refactor).
   - **COMMIT PER CYCLE (Mandatory):** Upon completing each full Red-Green-Refactor cycle, perform a semantic commit on the feature branch before starting the next cycle (e.g., `feat(scope): implement [feature]`). **Do not accumulate multiple cycles before committing.**
4. **Completion & Pre-Commit Sync Phase (Strict Sequence):**
   - Before committing any changes, perform the following updates in this exact order:
     1. Mark the task's individual file checkboxes (DoR/DoD) as completed (`[x]`) inside the task's markdown file (`context/backlog/TSK-XX.md`).
     2. Update the task's status to `Done` in the backlog master tracker (`context/backlog/README.md`).
     3. **If and only if this is the last task** of the phase or project sprint, update the main project root `README.md` and the folder-level `README.md` to reflect the newly delivered features/states.
     4. Create `walkthrough.md` in the conversation directory summarizing the changes (written in Portuguese, PT-BR).
     5. **If and only if this is the final task of the entire project:** add the `LICENSE` file to the repository root, configure the CI/CD workflow (e.g., `.github/workflows/ci.yml` with lint, test, and build jobs), and validate the build/packaging script before the final commit.
   - Only after all the files above are updated and verified, stage the files, commit using Conventional Commits naming standards, and push the branch to the remote repository.
5. **Prepare for Next Task:**
   - Clean up the workspace and proceed to check the next pending task in the queue.

---

**Signed Document:** *Kalyel N. Laurindo / Software Engineer*
