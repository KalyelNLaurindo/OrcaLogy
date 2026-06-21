# **📋 Solution Architecture & Product Vision: OrcaLogy — Local-First State-Managed Budget Ledger**

**Role:** Product Owner / Solution Architect

**Objective:** Define the strategic, commercial, and technical blueprint for resolving the core problem space mapped during discovery.

**Context:** OrcaLogy — A local-first, terminal-centric personal and team budget management CLI tool designed to eliminate the core problem of manual budget slippage and tracking fatigue through real-time deterministic category constraint validation, plain-text ledger files, and state-managed budget lifecycles.

## **🏛️ Project Metadata**

- **Client / Segment:** Tech Professionals, Developers, and Small Teams (CLI-centric & Local-first Users)
- **Date of Creation:** June 15, 2026
- **Lead Product Owner:** Kalyel N. Laurindo / Project Owner
- **Document Version:** v1.1 (Pure Plain-Text Accounting Paradigm)

## **🚀 1. The Market Opportunity & Strategic Positioning**

### **1.1. Market Size & Opportunity Map (TAM / SAM / SOM)**

- **Field 1.1.1 - Total Addressable Market (TAM):** Privacy-conscious software engineers, tech professionals, system operators, and small technology startups globally who manage personal and operational expenses manually. Estimated at ~30M individuals worldwide experiencing high cognitive friction using legacy tools.
- **Field 1.1.2 - Serviceable Addressable Market (SAM):** Command-line active, privacy-centric developers and small bootstrap technology teams who explicitly refuse cloud-based, data-invasive financial trackers and prefer flat-file or local database configurations (~2.5M users).
- **Field 1.1.3 - Serviceable Obtainable Market (SOM):** High-intent, local-first power budgeters seeking to automate custom parsing scripts (such as custom `awk`/`grep` solutions) and eliminate spreadsheet math errors during Year 1 (~25,000 active instances).

### **1.2. Competitive Landscape & Product Moat**

- **Competitor 1 (Direct Competitor):** YNAB (You Need A Budget)
  - *The Gap / Friction Point:* Requires expensive monthly SaaS subscriptions, mandates cloud synchronization, lacks terminal-native execution, and raises significant privacy concerns by harvesting raw financial transaction records.
  - *Our Advantage:* 100% offline-first local execution, zero-cost core engine, developer-friendly CLI, and absolute data privacy with plain-text local ownership.
- **Competitor 2 (Indirect/Alternative):** Plain Text Accounting tools (e.g., `ledger-cli`, `beancount`)
  - *The Gap / Friction Point:* Extremely steep learning curves, lacks built-in reactive constraint validation (users only discover overruns during post-processing), and does not enforce a rigid state-machine-driven budget lifecycle.
  - *Our Advantage:* Embedded real-time transaction limit validation checks at the point of entry and native mathematical ranking of category overruns out-of-the-box, operating directly on standard text-ledger files.

## **💰 2. Monetization Strategy, Licensing & Distribution Model**

- **Field 2.1 - Licensing Model:** Permissive Open-Source (MIT)
- **Field 2.2 - Pricing / Business Model:** Free & Open Source (FOSS) / No Monetization (Community-driven core execution engine)
- **Field 2.2.1 - Paid Tier Value Proposition (If Applicable):** N/A - Fully Free/Open Source
- **Field 2.3 - Distribution Strategy:** Standalone Binaries (compiled via Cargo/Rust), Package Managers (`npm`, `brew`, `cargo install`), and Container Images (`Docker`) for localized small team environments.
- **Field 2.4 - Organic Acquisition & Growth Strategy:** Organic GitHub repository discovery, technical developer blogging, integration into terminal utility ecosystems (e.g., Awesome-CLI-tools), and community word-of-mouth on Hacker News, Reddit (`r/selfhosted`, `r/rust`), and tech forums.

## **🛠️ 3. Technical Viability & High-Level Architectural Vision**

### **✍️ Technical Challenges Form Entry**

#### **Technical Challenge 3.1: Atomic and Consistent Local Text Ledger Writes**

- **Friction Level:** Critical
- **Architectural Solution:** To avoid database engines while maintaining strict data integrity, the CLI operates on an append-only, human-readable plain-text transaction file (`ledger.journal`). It enforces atomic writes using system-level POSIX advisory locking (`flock`/`lockf` via a `.lock` lockfile) during ingestion. Changes are committed by writing a temporary journal, checking checksum integrity, and atomically replacing the active file using the POSIX `rename(2)` system call. If a lock acquisition fails (e.g., due to a concurrency timeout), the repository converts the low-level library error into a custom domain `LedgerConcurrencyError` to be handled gracefully by UI clients (CLI/TUI) without raw tracebacks.


#### **Technical Challenge 3.2: Immediate Zero-Latency Text Parsing & Indexing**

- **Friction Level:** High
- **Architectural Solution:** Implement an memory-mapped (`mmap`) parsing pipeline. Upon CLI startup, the application maps the `ledger.journal` directly into memory space. A custom single-pass lexical scanner written in Rust parses the byte slice concurrently, generating an in-memory index of category limits and current balances. This delivers sub-millisecond start and search times even with ledgers exceeding $10^5$ transactions.

#### **Technical Challenge 3.3: Data Portability and Integration with Standard CLI Tooling**

- **Friction Level:** Low
- **Architectural Solution:** The ledger file uses a highly standard, deterministic flat-text format (ISO 8601 dates, delimited parameters, and clear newline separations). This ensures the dataset can be directly manipulated or processed by standard UNIX commands such as `grep`, `awk`, `sed`, or piped directly into other workflows.

### **3.1. Core Architectural Premises**

- **Decoupling Content/Configuration from Code:** All budget category definitions, user-defined thresholds, and environmental path mappings are decoupled from the binary and reside in a standard `config.toml` file. This allows instantaneous customization without re-compilation.
- **Human-in-the-Loop (HITL) Validation:** When registering a transaction that breaches a critical category ceiling, the system halts execution and forces an explicit CLI confirmation gate (`[y/N]`), giving the operator full control to dynamically override or reject the overrun.
- **Offline-Resilience / Caching Policy:** Designed from the ground up for 100% offline local operations. The local text-ledger file acts as the absolute execution repository. Memory-mapped caches act as ephemeral indices to prevent any networking or disk-IO bottlenecks during validations.
- **Privacy-First Data Protection:** All financial records stay within the user's secure directory partition. Optional transparent encryption is supported at the file level using standard GnuPG (GPG) integrations, allowing users to store encrypted files and leverage their GPG keys natively.

### **✍️ Technology & Data Governance Spec**

- **Field 3.4.1 - Core Communication Style:** Local Direct Execution
- **Field 3.4.2 - Data Serialization Format:** Human-Readable Plain Text Ledger Format (YAML/JSON serialization is supported strictly for export layers)
- **Field 3.5.1 - Database Paradigm:** Flat Files (Structured Journal & Memory-Mapped Binary Index)
- **Field 3.5.2 - Primary Source of Truth:** User client local storage (A secure local flat transaction ledger file located under the user's home configuration directory, e.g., `~/.config/orcalogy/ledger.journal`)

## **📑 4. Requirements Engineering & Feature Specification**

### **🎭 4.1. Scenario-Based Requirements Engineering (SBRE)**

#### **Scenario A: Budget Initialization & Setting Category Limits**

- **Trigger Event:** User runs `orca init` in their terminal.
- **System Action:** System prompts user for currency preference, baseline income target, and definitions of category limits (e.g., Food, Rent, Leisure). It creates a standard `config.toml` directory structure and initializes an empty text ledger `ledger.journal` with basic headers in the application context path.

#### **Scenario B: Safe Entry Validation & Overrun Enforcement**

- **Trigger Event:** User attempts to log an expense: `orca add -c Leisure -a 60 -d "Concert ticket"`.
- **System Action:** System maps the plain-text ledger to memory, scans category totals for `Leisure` ($150 out of a $200 limit), and intercepts the new registration before appending. Since it triggers a $10 overrun, the system halts execution, prints a high-contrast terminal warning, and requests user confirmation `[y/N]` before performing an atomic append.

#### **Scenario C: End-of-Cycle Performance Audit and Transition**

- **Trigger Event:** User executes `orca close` to finalize the fiscal cycle.
- **System Action:** System parses the transaction log file, calculates actual expenditures, and runs a memory-sorting algorithm to rank categories by percentage deviation. It outputs a stylized ANSI color-coded ASCII graph and locks historical periods within the flat file by wrapping them in a protective cryptographic signature blocks (e.g., standard GPG/detached signatures).

### **3.2. MoSCoW Prioritization Framework**

#### **🔴 Must Have (Critical for Core Value Proposition & MVP Launch)**

- **Requirement RF01: Plain-Text Append-Only Ledger File** * *Description:* A highly deterministic, human-readable file writer that appends validated transactions with structured schemas to `ledger.journal`.
  - *JTBD Tracing:* JTBD Functional Job (Field 10.1) - Secure instant recording.
- **Requirement RF02: Atomic File Locking Strategy** * *Description:* A localized concurrency controller utilizing POSIX file locks (`flock`) to prevent split-brain issues or race conditions when writing to flat ledger files.
  - *JTBD Tracing:* Section 3.1 - Concurrency risk mitigation.
- **Requirement RF03: Dynamic Category Performance Ranking** * *Description:* An automated CLI analysis command that calculates percentage budget deviations from raw transaction lines and prints them sorted from worst-performing overrun to best savings.
  - *JTBD Tracing:* JTBD Functional Job (Field 10.1) - Instant category performance auditing.

#### **🟡 Should Have (High Value, Target for Immediate Post-MVP Release)**

- **Requirement RF04: UNIX Standard Pipeline Support** * *Description:* Allows incoming transactions to be piped directly into the CLI via standard input Streams (e.g., `cat input.csv | orca stream`).
  - *JTBD Tracing:* Workaround 1 - Compatibility with developer scripts.
- **Requirement RF05: Interactive Terminal-UI Dashboard** * *Description:* A lightweight visual dashboard with progress bars and color-coded gauges rendered directly in the terminal interface.
  - *JTBD Tracing:* JTBD Emotional Job (Field 10.2) - Cognitive relief and visualization.

#### **🟢 Could Have (Desirable, Nice-to-Have, Low Urgency)**

- **Requirement RF06: Automated Git-Sync Integration** * *Description:* An optional, opt-in feature that executes an automated git commit and push of the flat `ledger.journal` file to a private remote repository upon budget state transition.
  - *JTBD Tracing:* JTBD Emotional Job (Field 10.2) - Complete data ownership reassurance.

## **⚙️ 5. Non-Functional Requirements (NFRs)**

- **NFR01 (Security - Access Control):** File access is restricted using system file-level security guidelines. Application files and lockpaths are initiated with strict POSIX permissions (`chmod 600` for ledgers and configs).
- **NFR02 (Security - Encryption):** Support for optional user-driven localized ledger encryption using GnuPG standards natively. Passphrases are managed securely inside standard system keyspaces (macOS Keychain, Linux Secret Service).
- **NFR03 (Compliance - Data Lifecycle):** Strict offline execution boundary. Zero remote telemetry, tracking APIs, or outbound sockets. The plain-text file can be archived, backed up, or purged entirely using standard filesystem delete operations.
- **NFR04 (Availability & SLA):** Local query execution and calculation times must remain sub-millisecond. High-throughput file parser must complete lexical analysis of 100k records in less than 15 milliseconds.
- **NFR05 (Accessibility):** Terminal outputs support standard monochrome fallbacks, high-contrast text ratios, and are compatible with console screen readers by outputting standard ANSI-escape terminal stream payloads.
- **Field 5.6 - Target Deployment Architecture:** Local Standalone Binary (packaged across Windows, macOS, and Linux platforms).

## **📦 6. MVP Scope Boundary (Defining the Line in the Sand)**

### **6.1. Product Focus Area (MVP Scope)**

- **Target Segments:** Terminal-centric technical professionals, security engineers, and developers who manage their budgets locally.
- **Key Flows Included:**
  1. Interactive config onboarding (`orca init`).
  2. Local atomic validation and writing of transaction logs (`orca add`).
  3. Dynamic execution performance auditing and terminal dashboards (`orca report`).

### **6.1.1. FinOps & Operational Constraints**

- **Field 6.3 - Projected Monthly Infrastructure Cost (MVP):** $0.00 (Operations and storage run entirely locally on the user's host machine).

### **6.2. Explicitly OUT of Scope (Post-MVP Backlog)**

- ❌ **Out-of-Scope Feature 1:** Live automatic connections or synchronization pipelines to banking APIs.
- ❌ **Out-of-Scope Feature 2:** Automatic real-time foreign exchange currency calculation relying on live external HTTP endpoints.
- ❌ **Out-of-Scope Feature 3:** Complex corporate business accounting structures, tax filings, and multi-user synchronized corporate expense tracking.

## **🎯 7. Validation Strategy & Success Metrics**

### **7.1. North Star Metric**

- **Field 7.1.1 - North Star Metric Statement:** Time spent compiling, grouping, and calculating category performance limits reduced from an average of **5 hours per month to less than 5 seconds** (fully automated compilation and instant rendering via local CLI execution).

### **7.2. Launch Gates & KPIs**

- **Field 7.2.1 - Commercial Target:** Secure 1,000+ organic open-source repository clones and utility installations within the first 60 days of release.
- **Field 7.2.2 - Activation Rate:** 85% of users who configure their `config.toml` successfully execute their first `orca add` entry validation and transition their first financial cycle.
- **Field 7.2.3 - User Feedback Loop:** Achieve 100% verification from first-adopters via Github feedback confirming zero instances of stealth financial leakage due to unexpected calculation errors.

## **🎨 8. System Architecture Visualization**

- **Field 8.0 - Diagram Strategy:** Local Utility CLI

### **💡 Architecture Diagrams Entry**

#### **Level 1 System Context Diagram (Level 1)**

```
flowchart TD  
    User["🌍 Terminal Operator / Developer<br>(Target User)"]

    subgraph Core_Local_System ["💻 Local Machine Boundary"]  
        CLI["🚀 OrcaLogy CLI Tool<br>(Rust/Go Binary)"]  
        Config["⚙️ Configuration Directory<br>(config.toml)"]  
        FileStore[("📝 Immutable Ledger File<br>(ledger.journal)")]  
    end

    subgraph Optional_Remote_Boundary ["📁 Secure Offsite (Optional)"]  
        GitRemote["🔐 Private Git Repository<br>(e.g., Self-hosted Gitea/GitHub)"]  
    end

    %% Interaction Paths  
    User -->|Executes transaction commands & audits budget| CLI  
    CLI -->|Reads constraints & layout rules| Config  
    CLI -->|Parses, appends, and locks transactions| FileStore  
    CLI -.->|Syncs backup files via Git hooks| GitRemote  

    %% Styling  
    style CLI fill:#f9f,stroke:#333,stroke-width:4px  
    style Core_Local_System fill:#fff,stroke:#333,stroke-dasharray: 5 5  
    style User fill:#def,stroke:#333  
    style GitRemote fill:#eee,stroke:#999,stroke-dasharray: 2 2  
```

#### **Level 2 Container Diagram (Level 2)**

```
graph TD  
    User((Terminal User))  
      
    subgraph CLI_Binary_Architecture ["💻 OrcaLogy Standalone Binary"]  
        UI[Interactive TUI / CLI Controller<br>ANSI Interface]  
        Engine[Validation & Ledger Core Engine<br>Go / Rust State Machine]  
        LocalCache[In-Memory Context Cache<br>Fast Verification Store]  
    end

    subgraph Secure_File_Storage ["📂 Local Directory Layer"]  
        ConfigSchema[(YAML / TOML Config)]  
        LedgerFile[("📝 Plain-Text Ledger File<br>~/.config/orcalogy/ledger.journal")]  
        StateCache[("📂 Memory-Mapped State Cache<br>.index.bin")]  
    end

    %% Interactive Loop  
    User -->|Enters CLI operations| UI  
    UI -->|Pipes raw transaction requests| Engine  
    Engine -->|Loads baseline variables| LocalCache  
    Engine -->|Validates rules against limits| LocalCache  
    
    %% Writing State to Disk  
    Engine -->|Atomic text stream append| LedgerFile  
    Engine -.->|Compiles binary index offsets| StateCache  
    UI -->|Direct validation reading| ConfigSchema  
    Engine -->|Initializes directory structure| ConfigSchema  
      
    %% Styling  
    style CLI_Binary_Architecture fill:#fff,stroke:#333,stroke-dasharray: 5 5  
    style UI fill:#def,stroke:#333  
    style Engine fill:#f9f,stroke:#333,stroke-width:2px  
    style LocalCache fill:#def,stroke:#333  
    style LedgerFile fill:#def,stroke:#333  
```

## **⚠️ 9. Engineering Risks & Architecture Assumptions**

### **✍️ Engineering Risks & Assumptions Form Entry**

#### **Engineering Risk 9.1: Concurrency Conflict and File Corruption via Split Writes**

- **Severity Level:** High
- **Mitigation Strategy:** Implement advisory filesystem locks using POSIX `flock(2)` / `lockf(3)`. When a process initiates a write, a temporary lockfile is generated. Subsequent concurrent CLI invocations are forced to queue, preventing interleaved file corruption.

#### **Engineering Risk 9.2: Plain-Text Modification Out-of-Bounds**

- **Severity Level:** Medium
- **Mitigation Strategy:** If a user manually edits the `ledger.journal` text file using editors like vim or nano and corrupts the structural layout, the parsing engine will intercept syntax errors during start-up, raise informative parser trace warnings, and block writes until syntax integrity is restored.

#### **Engineering Risk 9.3: Platform-Specific Line-Ending (CRLF vs LF) Discrepancies**

- **Severity Level:** Low
- **Mitigation Strategy:** The parsing engine's lexical scanner explicitly normalizes all standard byte streams, stripping out carriage returns (`\r\n` to `\n`) internally before compilation and checksum validations are finalized.
- **Architecture Assumption 1:** The target operating terminal environment provides local disk read/write directory creation capabilities under home-user spaces without requiring system root privileges.
- **Architecture Assumption 2:** The target compilation architectures (Windows, MacOS, Linux) provide native ANSI support for correct rendering of high-contrast TUI assets.

**Signed Document:** Kalyel N. Laurindo / Project Owner