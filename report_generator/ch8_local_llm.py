"""Chapter 8: Local LLM Neural Copilot Architecture & Indian Police FIR Generation"""

def get_chapter_8_html() -> str:
    return r"""
<h1>8. Local LLM Neural Copilot Architecture & Legal FIR Synthesis</h1>

<h2>8.1 The Sovereign AI Paradigm for Digital Forensics</h2>
<p>
The introduction of generative Large Language Models (LLMs) has revolutionized cyber threat analysis. However, in sensitive defense, intelligence, and police investigations, utilizing public commercial cloud AI services (e.g., OpenAI ChatGPT, Anthropic Claude, or Google Gemini) poses an unacceptable threat to <strong>national security, sovereign data privacy, and evidentiary chain-of-custody</strong>. Transmitting seized electronic evidence containing classified government communications, private corporate trade secrets, or unredacted personal identifiers to third-party cloud infrastructure constitutes an immediate data breach and contaminates the evidence docket under Indian jurisprudence.
</p>
<p>
To resolve this dilemma, <strong>SUDO SPANDR</strong> pioneers a <strong>100% Sovereign Local AI Architecture</strong>. All neural inference, cognitive reasoning, and legal text generation execute entirely on-device, within the physical workstation, requiring zero internet connectivity.
</p>

<h2>8.2 Dual-Tier Neural Engine Architecture</h2>
<p>
The intelligence subsystem within <code>core/ai_engine.py</code> is engineered as a robust dual-tier architecture featuring automatic service discovery and seamless fallback:
</p>

<pre>
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                     SUDO SPANDR LOCAL NEURAL COPILOT DISPATCH LAYER                    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   FORENSIC EVIDENCE ARTIFACT & THREAT TELEMETRY                                        │
│   └── Ingested Headers, Auth Status, URLs, Hops, Shannon Entropy, Carved Magic Bytes   │
│                                                                                        │
│   LOCAL INFERENCE PROBE (Non-blocking Discovery)                                       │
│   ├── Probe 1: Ollama Daemon via HTTP REST (http://localhost:11434/api/tags)           │
│   ├── Probe 2: Local OpenAI Endpoint (http://localhost:8080/v1/models or 1234)         │
│   └── Timeout: 1.5 seconds (Fail-Fast Circuit Breaker)                                 │
│                                                                                        │
│   TIER 1: HIGH-CAPACITY LOCAL LLM (Active if daemon detected)                          │
│   ├── Supported Models: LLaMA-3 (8B/70B), Mistral-7B, Qwen-2.5-Coder, DeepSeek-R1      │
│   ├── Execution: Quantized 4-bit / 8-bit GGUF via Vulkan / CUDA / CPU AVX-512          │
│   └── Interface: Parameterized System Prompting with Strict Zero-Hallucination Bounds   │
│                                                                                        │
│   TIER 2: DETERMINISTIC EMBEDDED ENGINE (CatBERT-Neural-CPU) (Always available)        │
│   ├── Zero Network Sockets: Pure-Python deterministic heuristic reasoning engine       │
│   ├── NLP Vectors: Linguistic urgency, coercive intimidation, cognitive sentiment      │
│   └── Templates: Statutory Indian Penal Code / BNS 2023 complaint synthesis            │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
</pre>

<h3>Tier 1: High-Capacity Local LLMs via Ollama & Local REST APIs</h3>
<p>
When an investigator operates on a workstation equipped with a modern CPU or dedicated GPU (e.g., NVIDIA RTX, Apple Silicon, or high-core AMD/Intel processors), SUDO SPANDR connects to local inference daemons such as <strong>Ollama</strong> or <strong>Llama.cpp</strong>. The system provides:
</p>
<ul>
    <li><strong>Model Auto-Discovery:</strong> The engine automatically queries <code>/api/tags</code> upon startup, populating the GUI dropdown with all locally installed weights (e.g., <code>llama3:latest</code>, <code>mistral:7b-instruct</code>, <code>phi3:mini</code>).</li>
    <li><strong>Asynchronous Non-Blocking Execution:</strong> AI inference runs inside a dedicated background thread (<code>QThread</code> in the GUI), preventing the main workstation user interface from freezing during multi-token text generation.</li>
    <li><strong>Strict Forensic Context Injection:</strong> Prompts are strictly bounded with extracted factual telemetry (SHA-256 hashes, true magic bytes, transit IPs). The model is instructed to act as an accredited digital forensics examiner and explicitly forbidden from hallucinating non-existent facts.</li>
</ul>

<h3>Tier 2: The Embedded CatBERT-Neural-CPU Fallback Engine</h3>
<p>
In austere deployment scenarios—such as field laptops in remote border areas, air-gapped forensic labs with strict USB/binary transfer policies, or systems lacking GPU acceleration—no local LLM daemon may be installed. SUDO SPANDR ensures that cognitive analysis never fails by providing an embedded, deterministic fallback engine: <strong>CatBERT-Neural-CPU</strong>.
</p>
<p>
Written in pure Python with zero external library dependencies, CatBERT implements rule-based Natural Language Processing heuristics:
</p>
<ul>
    <li><strong>Psychological Trigger Scoring:</strong> Scans the message body for urgency keywords (<code>"immediate suspension"</code>, <code>"24 hours"</code>, <code>"warrant issued"</code>), financial coercion (<code>"wire transfer"</code>, <code>"overdue invoice"</code>, <code>"bank details"</code>), and executive intimidation (<code>"confidential"</code>, <code>"CEO directive"</code>).</li>
    <li><strong>Linguistic Anomaly Evaluation:</strong> Computes the ratio of imperative commands to standard conversational sentences.</li>
    <li><strong>Deterministic Admissibility:</strong> Because CatBERT uses rule-based heuristic trees, its outputs are 100% deterministic and repeatable, satisfying the highest standards of scientific reproducibility required by judicial courts.</li>
</ul>

<h2>8.3 Automated Indian Police FIR Complaint Synthesis</h2>
<p>
A major operational bottleneck in cybercrime investigation is the time required by investigating officers (IOs) and corporate incident responders to draft formal police complaints. Improperly drafted complaints lacking specific penal statutory references or technical evidence summaries often lead to delayed FIR registration or evidentiary rejection.
</p>
<p>
SUDO SPANDR bridges this gap through its automated <strong>Police FIR Draft Synthesizer</strong>. With a single click (or pressing <code>[Space]</code> / <code>[F]</code>), the Local LLM Copilot compiles a comprehensive, ready-to-file First Information Report (FIR) complaint structured specifically for Indian Law Enforcement:
</p>

<h3>Statutory Legal Sections Cited in Generated FIRs</h3>
<ol>
    <li><strong>Section 66D of the Information Technology Act, 2000:</strong> <em>"Punishment for cheating by personation by using computer resource."</em> Applicable to domain masquerading, display-name spoofing, and forged Return-Path identities. Prescribes imprisonment up to three years and fines up to one lakh rupees.</li>
    <li><strong>Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 (BNS 2023):</strong> <em>"Cheating and dishonestly inducing delivery of property."</em> (Repealing and superseding Section 420 of the Indian Penal Code, 1860). Applicable when malicious emails solicit fraudulent wire transfers, credential harvesting, or financial disclosures.</li>
    <li><strong>Section 336(3) & Section 340(2) of the Bharatiya Nyaya Sanhita, 2023:</strong> <em>"Forgery of valuable security and electronic records."</em> (Repealing and superseding IPC Sections 468 and 471). Applicable when threat actors forge digital headers, fabricate brand logos, or falsify institutional domains.</li>
    <li><strong>Section 63 of the Bharatiya Sakshya Adhiniyam, 2023 (BSA 2023):</strong> The generated complaint explicitly incorporates the mandatory statutory certificate affirming the integrity, lawful custody, and cryptographic hash chain of the electronic evidence.</li>
</ol>

<div class="callout success">
    <div class="callout-title">📋 Sample Excerpt of Generated Police FIR Complaint</div>
    <pre>
TO:
THE STATION HOUSE OFFICER / INSPECTOR IN-CHARGE
CYBER CRIME POLICE STATION, CENTRAL POLICE DISTRICT

SUBJECT: FORMAL COMPLAINT UNDER SECTION 66D IT ACT, 2000 AND SECTION 318(4) & 
         336(3) BHARATIYA NYAYA SANHITA (BNS 2023) REGARDING SOPHISTICATED EMAIL 
         IMPERSONATION AND DIGITAL FORGERY CAMPAIGN

1. COMPLAINANT & CASE PARTICULARS:
   Case Reference ID : CS-CASE-20260907-72C614
   Date of Incident  : 2026-08-18 00:29:35 UTC
   Examining Agency  : Cyber Squad Forensic Lab (SUDO SPANDR Workstation v2.5)

2. TECHNICAL EVIDENCE & FORENSIC ARTIFACT SPECIFICATION:
   Seized File Name  : Security alert (1).eml
   SHA-256 Digest    : 72c61465cf2ac170881b54a61fe8a0bca50c319cf9657cc40dcfb50504970bb7
   MD5 Digest        : 24785ca8da5ee4f605a91438992c4228
   Bitstream Length  : 13,624 Bytes (Read-Only Forensic Duplicate)

3. PARTICULARS OF CYBER OFFENCE & MODUS OPERANDI:
   a. Deceptive Personation: The suspect sent an electronic mail purporting to originate 
      from "Google" (accounts.google.com), but underlying transport headers reveal 
      Return-Path routing to "gaia.bounces.google.com".
   b. Cognitive Coercion: Linguistic analysis revealed high-urgency security intimidation 
      designed to compel the recipient to click malicious credential-harvesting hyperlinks.

4. PRAYER & STATUTORY RELIEF:
   It is respectfully requested that an FIR be registered under Section 66D of the IT 
   Act, 2000 read with Sections 318(4) and 336(3) of the BNS 2023, that preserving 
   notices under Section 94 BNSS be served on originating MTAs, and that legal 
   proceedings be initiated against the perpetrators.
    </pre>
</div>

<h2>8.4 MITRE ATT&CK Enterprise Matrix Kill-Chain Mapping</h2>
<p>
To facilitate integration with national cyber defense centers and enterprise SOCs, the Local LLM Copilot maps all extracted indicators directly to the globally recognized <strong>MITRE ATT&CK Enterprise Matrix</strong>:
</p>

<table>
    <thead>
        <tr>
            <th>MITRE Tactic</th>
            <th>Technique ID & Name</th>
            <th>Observed Forensic Evidence & Indicator</th>
            <th>Automated Mitigation & Countermeasure</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Initial Access</strong></td>
            <td><code>T1566.001</code>: Spearphishing Attachment</td>
            <td>Attachment with anomalous magic bytes or Shannon entropy $H \ge 7.2$.</td>
            <td>Quarantine MIME part; deploy YARA rule to email gateway.</td>
        </tr>
        <tr>
            <td><strong>Initial Access</strong></td>
            <td><code>T1566.002</code>: Spearphishing Link</td>
            <td>Extracted URL with Punycode <code>xn--</code> or typo-squatted domain.</td>
            <td>Inject URL block into border firewall and DNS sinkhole.</td>
        </tr>
        <tr>
            <td><strong>Defense Evasion</strong></td>
            <td><code>T1036.005</code>: Masquerading (Double Extension)</td>
            <td>File named <code>document.pdf.exe</code> with PE32 magic <code>4D 5A</code>.</td>
            <td>Filter multi-extension filenames at edge MTA parser.</td>
        </tr>
        <tr>
            <td><strong>Defense Evasion</strong></td>
            <td><code>T1564.004</code>: Suspicious Header Obfuscation</td>
            <td>Folded multiline RFC 5322 headers with CRLF whitespace injections.</td>
            <td>Normalize and enforce strict RFC 5322 header grammar.</td>
        </tr>
        <tr>
            <td><strong>Execution</strong></td>
            <td><code>T1204.002</code>: Malicious File Execution</td>
            <td>Embedded macro scripts or compiled shellcode droppers.</td>
            <td>Block binary execution via endpoint application whitelisting.</td>
        </tr>
    </tbody>
</table>
"""
