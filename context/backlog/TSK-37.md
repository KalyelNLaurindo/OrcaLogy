# TSK-37: Secure Cryptographic Ledger

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 8 Hours  
* **Story / Epic Reference:** Phase 7.2 / SECURITY  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Add support for symmetric encryption of `ledger.journal` using a user password or key derivation function. The system should read encrypted files transparently, prompt for password input at startup, decrypt in memory, and re-encrypt atomic writes on disk.

## ✅ Definition of Ready (DoR)

* [ ] Atomic file writer repository (TSK-22) is active and verified.
* [ ] Concurrency advisory file locker (TSK-20) is verified.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Write test cases first verifying in-memory encryption, password verification failure, and correct encryption format on disk.
* [ ] **[Functional - Security]:** Use a robust package like `cryptography` (Fernet/AES) to encrypt the ledger file. Ensure no plain-text versions remain on disk.
* [ ] **[Functional - UX]:** Prompts for credentials in a secure terminal mode (hidden input) when opening an encrypted ledger.
* [ ] **[Verification]:** `pytest tests/test_infra.py` asserting correct encryption cycle and cryptographic rejection of wrong keys.
