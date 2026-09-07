# 🛡️ SUDO SPANDR TUI (Terminal Forensic Engine) — SIH #26106

Standalone, 100% Offline, Air-Gap Ready Terminal Forensic Suite for **Law Enforcement Officers (LEOs)**, **SOC Incident Responders**, and **Forensic Labs** by **Team SUDO SPANDR**.

---

## 🌟 Why SUDO SPANDR TUI is Distinct from Web UI

| Feature | Web Interface (`sudospandr-web`) | SUDO SPANDR TUI (`sudospandr-tui`) |
| :--- | :--- | :--- |
| **Operational Environment** | Browser-based, requires HTTP ports, Node.js, Web servers. | **100% Offline / Air-Gapped / Headless SSH**. Runs directly on SANS SIFT, Kali Linux, CAINE, headless servers. |
| **Data Privacy & Sanitization** | Client-server HTTP requests. | **Zero-Network In-Memory Processing**, zero disk cache leakage, memory-safe. |
| **Low-Level Byte Analysis** | High-level HTML view. | **Color-Coded Hex Dump & Shannon Entropy Map (`█▓▒░`)** with byte offsets and format boundary anomaly detection. |
| **Legal Admissibility** | On-screen risk badge. | **Section 63 BSA 2023 Certificate Generator** with SHA-256/512 cryptographic digests, custody chain, examiner signature block. |
| **Threat Intelligence** | Basic indicators. | **Auto-Generates YARA Rules, Snort/Suricata IDS Signatures, and STIX 2.1 Threat Intel Objects** directly to disk. |
| **Batch Folder Forensics** | One file at a time. | **Bulk Evidence Queue**: Scans entire directories of `.eml`/`.msg` files with live triage ranking, sorting, and CSV export. |
| **Speed & Workflow** | Mouse-driven, browser DOM latency. | **Sub-millisecond keyboard navigation** (1-8 quick views, Vim `j`/`k`, `/` filter, `[E]` export, `[B]` batch). |

---

## 🚀 Quick Start & Installation

```bash
# 1. Navigate to the project folder (Quotes are needed because of space in folder name)
cd "/home/nee/Desktop/sih email/sudospandr-tui-master"

# 2. Launch directly using launcher script (or python3 app.py)
./run_tui.sh

# Or run directly with Python:
python3 app.py
```

> [!NOTE]
> On Kali Linux / Debian, `rich` is already installed. If running on a fresh machine, install via:
> `sudo apt install python3-rich` or `pip install --break-system-packages -r requirements.txt`


---

## ⌨️ Interactive TUI Navigation & Hotkeys

### Navigation Views:
- `[1]`: **4-Panel Unified Command Deck** — Master dashboard with evidence tree, reasoning, hops, and carver.
- `[2]`: **Hop Relay Map & Timeline** — Full header disassembler & bottom-up IP hop chronology.
- `[3]`: **CatBERT NLP Cognitive AI** — Psychological coercion triggers & synthetic/LLM phishing intent.
- `[4]`: **Hex Carver & Shannon Entropy** — Live 16-byte hex disassembler + entropy speedometer.
- `[5]`: **Section 63 BSA 2023 Certificate** — Legal court certificate preview with hash verification.
- `[6]`: **Batch Evidence Triage Queue** — Multi-file scanning table with risk scoring.
- `[7]`: **YARA & Snort Rule Generator** — Enterprise network & file threat hunting rules.
- `[8] / [P]`: **📌 Executive Incident Summary & Guide** — Plain-language summary designed for non-technical officers & judges.

### User-Friendly Forensic Actions:
- `[SPACE]`: **⚡ 1-Click Complete Auto-Audit** (Runs AI inference, generates Section 63 BSA PDF certificate, and saves YARA rules in one touch!)
- `[← / →]` or `[TAB]`: **Smooth View Flipping** (Page between views without needing to remember numbers)
- `[↑ / ↓]` + `[Enter]`: **Direct Evidence Picker** (Browse and load seized emails right from the screen)
- `[E]`: Export Section 63 BSA 2023 **PDF + Text Certificate** to `./forensic_exports/`
- `[O]`: Open interactive numbered file picker menu
- `[B]`: Run Batch Folder Scan on directory
- `[A]`: Run / Refresh CatBERT AI Intent Analysis
- `[Y] / [S]`: Export YARA / Snort threat hunting rules
- `[Q]`: Quit application cleanly


---

## 💻 CLI Pipeline & Automation Commands

### 1. Directly Open a Specific Evidence File
```bash
python3 app.py "/path/to/suspicious_mail.eml"
```

### 2. Batch Folder Scan with CSV Export
```bash
python3 app.py --batch /cases/incident_2026/ --export-csv /cases/triage_summary.csv
```

### 3. Generate Section 63 BSA 2023 Certificate (Headless)
```bash
python3 app.py --cert /path/to/evidence.eml --officer "Inspector Rajesh Sharma" --agency "CERT-In DFIR Lab"
```

### 4. Headless Threat Rule Generation (YARA / Snort)
```bash
python3 app.py --export-yara /path/to/evidence.eml > threat_rule.yar
python3 app.py --export-snort /path/to/evidence.eml > snort_rule.rules
```

### 5. Unix Pipe & STDIN Ingestion
```bash
cat raw_email.eml | python3 app.py --stdin
```

---

## 🏛️ Legal Compliance: Section 63 BSA 2023

The Bharatiya Sakshya Adhiniyam, 2023 (BSA) governs the admissibility of electronic evidence in Indian courts. SUDO SPANDR TUI automatically generates:
1. **Cryptographic Digests**: SHA-256, SHA-512, and MD5 computed directly from raw byte streams.
2. **Chain of Custody**: UTC timestamping, host hardware node signature, and tool provenance.
3. **Court-Ready Plain Text & Machine-Readable Manifests**: Exported with standard formatting ready for submission alongside cyber chargesheets.

---

## 📁 Architecture

```
sudospandr-tui-master/
├── app.py                     # Main CLI entrypoint & interactive event loop
├── requirements.txt           # Minimal dependencies
├── README.md                  # Comprehensive investigator documentation
└── core/
    ├── __init__.py
    ├── parser.py              # Loss-aware RFC 5322 MIME parser & defect analyzer
    ├── forensics.py           # Threat matrix, BEC detector, Relay hop chronologist
    ├── carver.py              # Shannon entropy, magic byte carver, ANSI Hex dump
    ├── bsa_cert.py            # Section 63 BSA 2023 legal certificate generator
    ├── rule_gen.py            # YARA, Snort/Suricata & STIX 2.1 rule generator
    └── batch.py               # Recursive multi-evidence folder scanner & CSV reporter
```
