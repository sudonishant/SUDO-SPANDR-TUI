"""Chapter 3: System Architecture & Tech Stack ("Kaise Bana Hai")"""

def get_chapter_3_html() -> str:
    return r"""
<h1>3. System Architecture & Tech Stack ("Kaise Bana Hai")</h1>

<h2>3.1 Architectural Philosophy: Modular Decoupling & MVC Separation</h2>
<p>
The engineering architecture of <strong>SUDO SPANDR</strong> was constructed from the ground up using the <strong>Model-View-Controller (MVC)</strong> software design pattern, augmented by strict modular decoupling principles. The design guarantees that all underlying forensic parsing, cryptographic calculation, payload carving, and threat reasoning routines reside exclusively within a headless, framework-agnostic core engine (<code>core/</code>). 
</p>
<p>
This architectural decision allows both presentation interfaces—the <strong>Terminal User Interface (<code>app.py</code>)</strong> and the <strong>Ghidra Forensic Desktop Workstation (<code>gui_app.py</code>)</strong>—to bind cleanly to the identical underlying forensic state model without duplicating a single line of business or forensic logic.
</p>

<pre>
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 PRESENTATION LAYER (VIEWS)                             │
├────────────────────────────────────────────────────┬───────────────────────────────────┤
│          SUDO SPANDR TERMINAL TUI (app.py)         │   GHIDRA FORENSIC DESKTOP (gui_app)   │
│   • Python Rich ANSI / VT100 Terminal Engine       │   • PyQt6 (Qt6 C++ GUI Subsystem) │
│   • 8 Interactive Forensic Keyboard Panels         │   • Multi-Window Docking Layout   │
│   • Asynchronous Single-Character Event Loop       │   • Executive KPI Metric Deck     │
│   • High-Density ASCII Status Displays             │   • Interactive Pathology Cards   │
└─────────────────────────┬──────────────────────────┴─────────────────┬─────────────────┘
                          │                                            │
                          ▼                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                             CONTROLLER & DISPATCH INTERFACE                            │
│   • Evidence Ingestion & Cryptographic Hash Locking (SHA-256, MD5, SHA-512)            │
│   • Forensic Threat Matrix Orchestration & Multi-Vector Aggregator                     │
│   • Local LLM Worker Threading & Non-Blocking Asynchronous Event Dispatching           │
└──────────────────────────────────────────────────┬─────────────────────────────────────┘
                                                   │
                                                   ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                  CORE FORENSIC ENGINE                                  │
├──────────────────────────┬─────────────────────────────┬───────────────────────────────┤
│    core/parser.py        │      core/forensics.py      │       core/carver.py          │
│ • RFC 5322 State Machine │ • Sender Identity Pathology │ • MIME Part Decompiler        │
│ • Multi-Valued Unfolding │ • SPF / DKIM / DMARC Matrix │ • Magic Byte Header Matcher   │
│ • Base64 / QP Streaming  │ • Hop Transit Graph Math    │ • Shannon Entropy Speedometer │
│ • Header Tokenizer       │ • Homoglyph & Punycode      │ • Double-Extension Trapping   │
├──────────────────────────┼─────────────────────────────┼───────────────────────────────┤
│    core/ai_engine.py     │      core/rule_gen.py       │     core/bsa_cert.py          │
│ • Local Ollama REST API  │ • YARA Signature Compiler   │ • Section 63 BSA 2023 Model   │
│ • CatBERT NLP Heuristics │ • Snort / Suricata IDS Gen  │ • Cryptographic Hash Custody  │
│ • Police FIR Generator   │ • IOC Regular Expressions   │ • Legal Affirmation Template  │
│ • MITRE Kill-Chain Map   │ • Threat Rule Synthesis     │ • Forensic Auditor Telemetry  │
└──────────────────────────┴─────────────────────────────┴───────────────────────────────┘
</pre>

<h2>3.2 Technical Component Decomposition</h2>
<p>
To understand how SUDO SPANDR was engineered, we must examine the specific responsibilities of each constituent subsystem within the codebase:
</p>

<h3>1. <code>core/parser.py</code> — RFC 5322 MIME Grammar Parsing Engine</h3>
<p>
The foundation of electronic mail forensics begins with raw byte ingestion. <code>core/parser.py</code> implements a hardened RFC 5322 parsing engine that ingests raw <code>.eml</code>, <code>.msg</code>, and <code>.pst</code> streams. It immediately captures the raw bitstream, computes immutable cryptographic digests (SHA-256, MD5, SHA-512), and executes recursive MIME part extraction. It unfolds multi-line headers according to RFC 5322 Section 2.2.3, preserving original casing for byte-level integrity verification while normalizing values for forensic analysis.
</p>

<h3>2. <code>core/forensics.py</code> — Forensic Threat Matrix & Network Transit Engine</h3>
<p>
This module acts as the analytical brain of the forensic suite. It evaluates three critical threat vectors:
</p>
<ul>
    <li><strong>Envelope Masquerading Heuristics:</strong> Compares declared <code>From:</code> addresses, human-readable display names, <code>Return-Path:</code> bounce addresses, and <code>Reply-To:</code> targets to detect domain divergence and homograph spoofing.</li>
    <li><strong>Cryptographic Authentication Dissection:</strong> Parses <code>Authentication-Results</code>, <code>Received-SPF</code>, and <code>DKIM-Signature</code> headers to construct a multi-layer verification matrix.</li>
    <li><strong>Relay Transit Topology Graph:</strong> Reconstructs the chronological transit trajectory of the email by performing bottom-up topological sorting on all <code>Received:</code> headers, calculating transit latency ($\Delta t$) between MTA hops, isolating private RFC 1918 subnets, and identifying suspicious public transit nodes.</li>
</ul>

<h3>3. <code>core/carver.py</code> — Payload Dissector, True Magic Matcher & Shannon Entropy Gauge</h3>
<p>
Adversaries frequently employ file extension masquerading (such as appending benign extensions to malicious binaries, e.g., <code>Invoice.pdf.exe</code>) or packing payloads to evade basic signature filters. <code>core/carver.py</code> extracts every attachment into volatile memory, ignores the claimed filename extension, and inspects the initial 16 bytes against an embedded library of true file magic signatures (e.g., <code>4D 5A</code> for Windows PE binaries, <code>7F 45 4C 46</code> for Linux ELF, <code>25 50 44 46</code> for Adobe PDF, <code>50 4B 03 04</code> for ZIP archives). Furthermore, it computes the Shannon entropy score across the byte distribution to mathematically detect packed shellcode and encrypted droppers.
</p>

<h3>4. <code>core/ai_engine.py</code> — Local LLM Neural Copilot & Offline Cognitive NLP Engine</h3>
<p>
Engineered for zero-leakage, 100% air-gapped sovereign environments, <code>core/ai_engine.py</code> establishes an autonomous artificial intelligence layer. It implements a local REST client communicating with an offline <strong>Ollama</strong> server (defaulting to <code>http://localhost:11434</code>) or local OpenAI-compatible endpoints (e.g., Llama.cpp, vLLM, LM Studio) hosting models like <code>llama3:latest</code>, <code>mistral</code>, or <code>qwen2.5-coder</code>. If no local LLM daemon is active, it seamlessly fails over to an embedded deterministic cognitive NLP engine (<strong>CatBERT-Neural-CPU</strong>), performing sentiment scoring, urgency classification, and psychological coercion detection without external network dependencies.
</p>

<h3>5. <code>core/rule_gen.py</code> — Automated Threat Signature Synthesizer</h3>
<p>
Once an artifact has been forensically autopsied, <code>core/rule_gen.py</code> automatically translates extracted Indicators of Compromise (IOCs) into operational security rules. It compiles production-ready <strong>YARA rules</strong> containing file hashes, suspicious string patterns, and hex byte sequences, alongside <strong>Snort and Suricata IDS rules</strong> designed to block originating threat-actor IP addresses and phishing domains at enterprise perimeter firewalls.
</p>

<h3>6. <code>core/bsa_cert.py</code> & <code>core/pdf_gen.py</code> — Section 63 BSA 2023 Evidentiary Admissibility Engine</h3>
<p>
To ensure digital evidence is legally admissible in Indian courts, this module captures the complete chain of custody—including examiner identity, seizure case ID, workstation MAC address, operating system build, SHA-256/MD5 hashes, and system integrity affirmations. <code>core/pdf_gen.py</code> implements a zero-dependency, pure-Python PostScript PDF generation pipeline that compiles this telemetry into a court-ready <strong>Section 63 Bharatiya Sakshya Adhiniyam (BSA 2023) Electronic Evidence Certificate</strong>.
</p>

<h3>7. <code>core/batch.py</code> — High-Throughput Autonomous Triage Engine</h3>
<p>
In major security breaches or cybercrime operations, investigators often seize tens of thousands of email files. <code>core/batch.py</code> implements a multi-worker directory crawler that recursively ingests directory trees, applies automated triage heuristics, categorizes files by threat severity, and generates an aggregated forensic triage manifest in JSON and CSV formats.
</p>

<h2>3.3 Presentation Layer Technologies & UX Architecture</h2>
<p>
The user experience of SUDO SPANDR was deliberately designed to eliminate analytical fatigue caused by raw text walls:
</p>
<ul>
    <li><strong>PyQt6 GUI Subsystem:</strong> Built upon the industrial-strength Qt6 C++ graphics framework, providing a hardware-accelerated, dockable multi-window workspace. The layout features dark-mode styling inspired by modern cybersecurity IDEs (Tokyo Night color palette), with dedicated docks for the Evidence Program Tree, Forensic Autopsy Workspace, Hex Byte Carver, and Local LLM Copilot.</li>
    <li><strong>Top Executive KPI Deck:</strong> Situated prominently at the top of the GUI workspace, four glowing metric cards provide instantaneous situational awareness: Threat Score (0–100 with color verdict), Envelope Alignment Check, Cryptographic Authentication Status, and Carved Payload Entropy.</li>
    <li><strong>Rich Terminal TUI Subsystem:</strong> Developed using the Python <code>rich</code> library, the TUI provides a complete, keyboard-driven forensic command deck with split-pane layouts, live progress bars, syntax-highlighted tables, and synchronized hex dumps, operable inside standard terminal emulators over lightweight SSH connections.</li>
</ul>
"""
