# 📚 **OrcaLogy** Quick Start Guide

This guide provides simple, sequential instructions to install, bootstrap, and run the **OrcaLogy** application on your local machine.

---

## 📋 Prerequisites

Before setting up the project, make sure you have the following environments installed:

1. **Python Runtime:** Python 3.11+
2. **Package Manager:** Poetry (Recommended) or standard `pip`
3. **Version Control:** Git

---

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository
Clone the repository to your local workspace directory using Git:
```bash
git clone https://github.com/KalyelNLaurindo/OrcaLogy.git
cd OrcaLogy
```

### Step 2: Install Dependencies & Setup Environment
Install the required packages and dependencies inside the virtual environment:

**Option A: Using Poetry (Recommended)**
```bash
poetry install
```

**Option B: Using standard Python Virtual Environment**
```bash
python -m venv .venv
# On Windows (PowerShell):
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -e .
```

### Step 3: Run the Application
Launch the interactive terminal dashboard (TUI):

**Option A: Using Poetry**
```bash
poetry run orca tui
```

**Option B: Using standard Python module invocation**
```bash
python -m orcalogy.main tui
```

---

## ✅ Core Commands Reference

Here are the most frequently used commands to interact with the application:

| Action / Goal | Command Syntax | Description | Example |
| :--- | :--- | :--- | :--- |
| **Launch Dashboard** | `orca tui` | Launches the interactive TUI Main Menu | `orca tui` |
| **Initialize Budget** | `orca init` | Creates a new monthly budget with category limits | `orca init` |
| **Add Transaction** | `orca add -c <cat> -a <val> -d <desc> --date YYYY-MM-DD` | Registers a spending transaction with overrun validation | `orca add -c Food -a 15.50 -d "Lunch" --date 2026-06-21` |
| **Deviation Report** | `orca report --month YYYY-MM` | Shows color-coded category deviation ranking | `orca report --month 2026-06` |
| **Budget Status** | `orca status --month YYYY-MM` | Shows quick summary of spent and remaining values | `orca status --month 2026-06` |
| **Close Month** | `orca close --month YYYY-MM` | Locks the budget cycle, blocking further transactions | `orca close --month 2026-06` |
| **Run Test Suite** | `pytest` | Runs all 97 unit and integration tests | `pytest` |

---

## ❓ Troubleshooting & Known Issues

| Error / Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'orcalogy'` | Python path is not configured when running raw scripts. | Run the script as a module using `python -m orcalogy.main tui`, or configure `PYTHONPATH=.` in your terminal session. |
| `BudgetClosedError` | Attempted to add transaction to a closed month. | You cannot write to locked months. If needed, edit the raw journal ledger file manually or use a different budget month. |
| `Filelock Timeout` / Slow startup | Concurrency advisory file lock is blocked by a running zombie process. | Force close any zombie processes running `orca`, or delete the temporary lock file `.ledger.journal.lock` in the user's data directory (`~/.orcalogy/data/`). |

---

**Autored by:**  
*Kalyel N. Laurindo / Software Engineer*
