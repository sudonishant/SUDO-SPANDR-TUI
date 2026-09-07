"""Chapter 7: UI/UX Workstation Walkthrough with High-Resolution Screenshots"""
from pathlib import Path

def get_chapter_7_html() -> str:
    pwd = Path(".").resolve()
    img_tui = (pwd / "report_assets/00_tui_terminal.svg").as_uri()
    img_main = (pwd / "report_assets/01_gui_main_autopsy.png").as_uri()
    img_headers = (pwd / "report_assets/02_gui_headers.png").as_uri()
    img_urls = (pwd / "report_assets/03_gui_urls.png").as_uri()
    img_mime = (pwd / "report_assets/04_gui_mime.png").as_uri()
    img_yara = (pwd / "report_assets/05_gui_yara_rules.png").as_uri()
    img_copilot = (pwd / "report_assets/06_gui_copilot_active.png").as_uri()

    return f"""
<h1>7. UI/UX Workstation Walkthrough & Operational Telemetry</h1>

<h2>7.1 Visual Interface Design Rationale</h2>
<p>
A core design directive of <strong>SUDO SPANDR</strong> was the complete eradication of unformatted text walls. Forensic analysts investigating critical cyber intrusions cannot afford to sift through tens of thousands of lines of raw ASCII headers, unindexed Base64 dumps, or unparsed SMTP logs. Human cognitive overload inevitably causes missed indicators of compromise.
</p>
<p>
To resolve this, SUDO SPANDR introduces a multi-tier visual hierarchy:
</p>
<ul>
    <li><strong>Executive KPI Metric Tiles:</strong> Prominent glowing status blocks providing immediate situational awareness (Threat Score, Envelope Integrity, Cryptographic Authentication, Payload Density).</li>
    <li><strong>Discrete Pathology Finding Cards:</strong> Every forensic observation is rendered as a standalone visual card with colored pill badges, high-contrast monospace comparison boxes, and clear technical explanations.</li>
    <li><strong>Searchable Data Tables:</strong> Headers, extracted URLs, MIME attachments, and relay hops are presented in interactive tables supporting live substring filtering and syntax color-coding.</li>
    <li><strong>Synchronized Byte & Hex Disassembly:</strong> A 16-byte Ghidra byte view coupled with a Shannon entropy speedometer for deep payload inspection.</li>
    <li><strong>Integrated Neural Copilot:</strong> An interactive AI reasoning pane operable via one-click tactical buttons or conversational queries.</li>
</ul>

<h2>7.2 Walkthrough of the Forensic Workstation Interfaces</h2>

<h3>Figure 1: The Tactical Terminal User Interface (TUI)</h3>
<figure>
    <img src="{img_tui}" alt="SUDO SPANDR Terminal TUI Dashboard" style="width: 100%; border: 1px solid #334155;" />
    <figcaption>Figure 7.1: SUDO SPANDR Terminal User Interface (TUI) displaying the 4-panel tactical forensic deck, evidence file browser, cryptographic hashing, and Shannon entropy speedometer.</figcaption>
</figure>
<p>
The Terminal User Interface (shown in Figure 7.1) is designed for immediate incident response in austere environments, SSH jump boxes, and headless servers. It features:
</p>
<ul>
    <li><strong>Top Navigation Deck:</strong> Eight dedicated forensic panels accessible via keyboard shortcuts: <code>[1] 4-Panel Deck</code>, <code>[2] Hop Map</code>, <code>[3] CatBERT AI</code>, <code>[4] Hex Carver</code>, <code>[5] BSA-63 PDF</code>, <code>[6] Batch Queue</code>, <code>[7] YARA Rules</code>, <code>[8] Summary Card</code>.</li>
    <li><strong>Evidence Browser (Top-Left):</strong> Real-time directory navigation showing discovered evidence files with file sizes and active loaded status.</li>
    <li><strong>Forensic Inspection Panel (Top-Right):</strong> Displays Case SHA-256 digest, declared From header, actual Return-Path, SPF/DKIM/DMARC status, and CatBERT cognitive classification.</li>
    <li><strong>Hop Relay Chain (Bottom-Left):</strong> Chronological MTA relay sequence with transmitting IP addresses, transit latency deltas, and node classifications.</li>
    <li><strong>Attachment Carver & Entropy Speedometer (Bottom-Right):</strong> True magic byte identification (detecting disguised <code>.exe</code> files), Shannon entropy score, and ASCII spectrum bar.</li>
</ul>

<h3>Figure 2: Ghidra Forensic Desktop Workstation — Main Autopsy Workspace</h3>
<figure>
    <img src="{img_main}" alt="SUDO SPANDR Ghidra Forensic Desktop Workstation" style="width: 100%;" />
    <figcaption>Figure 7.2: SUDO SPANDR Ghidra Desktop Workstation showing the 4-tile Executive KPI Deck, Envelope Identity Pathology Card, Domain Divergence Alert, Local LLM Copilot, and Shannon Entropy Hex Carver.</figcaption>
</figure>
<p>
Figure 7.2 captures the main window of the PyQt6 desktop workstation after ingesting evidence file <code>Security alert (1).eml</code>:
</p>
<ul>
    <li><strong>Top Global Toolbar:</strong> Ingest Evidence button, Run Complete Auto-Analysis button, Focus Local LLM Copilot button, Generate Section 63 BSA 2023 PDF Certificate button, Export Threat Rules button, and the glowing Threat Score badge (<code>THREAT SCORE: 30/100 [ELEVATED RISK / REVIEW]</code>).</li>
    <li><strong>Executive KPI Metric Deck (Top Center):</strong> Four glowing tiles:
        <ol>
            <li><em>Threat Score Tile:</em> <code>30/100 (ELEVATED RISK / REVIEW)</code> with amber warning styling.</li>
            <li><em>Envelope Check Tile:</em> <code>❌ SPOOFED MISMATCH</code> with crimson alert styling, explicitly highlighting that the declared sender domain is <code>accounts.google.com</code> while mail routing returns to <code>gaia.bounces.google.com</code>.</li>
            <li><em>Crypto Auth Tile:</em> <code>✔ PASSING</code> showing SPF, DKIM, and DMARC verification.</li>
            <li><em>Carved Payload Tile:</em> <code>Clean Body</code> indicating no executable attachment was present in this message part.</li>
        </ol>
    </li>
    <li><strong>Pathology Findings / Autopsy Cards (Center):</strong>
        <ol>
            <li><em>Card 1 (Envelope Identity & Sender Spoofing Pathology):</em> Monospace pill boxes contrasting the Declared From Header (<code>Google &lt;no-reply@accounts.google.com&gt;</code>), the Actual Return-Path (<code>&lt;3cKeDaggTCykST...gaia.bounces.google.com&gt;</code>), and Subject Line.</li>
            <li><em>Card 2 (Primary Pathology Findings):</em> Dynamic root cause card displaying badge <code>❌ DOMAIN DIVERGENCE</code> with an explicit forensic explanation of the masquerading tactic.</li>
        </ol>
    </li>
    <li><strong>Synchronized Byte & Hex Carver (Bottom):</strong> 16-byte Ghidra byte view with byte offsets, hexadecimal bytes, ASCII disassembly, and a live Shannon Entropy Speedometer measuring <code>5.67 / 8.00 bits [STANDARD BYTE DENSITY]</code>.</li>
</ul>

<h3>Figure 3: Searchable RFC 5322 Header Inspector Table</h3>
<figure>
    <img src="{img_headers}" alt="Searchable RFC Header Inspector" style="width: 100%;" />
    <figcaption>Figure 7.3: Interactive RFC Header Inspector table featuring live search filtering and color-coded forensic taxonomy.</figcaption>
</figure>
<p>
Shown in Figure 7.3, the Header Inspector replaces raw text dumps with an interactive two-column table. Analysts can type keywords (e.g., <code>"Return-Path"</code>, <code>"Authentication"</code>, <code>"Received"</code>) into the live search bar, instantly isolating matching headers across hundreds of lines. High-priority headers are rendered in distinct syntax colors: bold cyan for identity routing, amber for cryptographic signatures, and blue for network transit hops.
</p>

<h3>Figure 4: Hyperlink & Homograph Threat Matrix</h3>
<figure>
    <img src="{img_urls}" alt="URL and Homograph Matrix" style="width: 100%;" />
    <figcaption>Figure 7.4: URL & Homograph Matrix table dissecting extracted hyperlinks, target domains, Punycode encoding, and risk ratings.</figcaption>
</figure>
<p>
Figure 7.4 illustrates the URL analysis engine. Extracted hyperlinks are parsed into target domains, screened for Punycode homograph spoofs (<code>NO (Standard ASCII)</code> or <code>YES (HOMOGRAPH ATTEMPT)</code>), evaluated for threat risk (<code>HIGH</code>, <code>CLEAN</code>), and annotated with specific pathology indicators.
</p>

<h3>Figure 5: MIME & Attachment Anatomy Decomposition</h3>
<figure>
    <img src="{img_mime}" alt="MIME Hierarchy and Attachment Table" style="width: 100%;" />
    <figcaption>Figure 7.5: MIME Hierarchy and Attachment Anatomy table detailing part structures, true magic bytes, and Shannon entropy scores.</figcaption>
</figure>
<p>
In Figure 7.5, the MIME part tree is laid out in a clear tabular grid displaying Part Number (Root vs. Attachment Parts), Content-Type, Declared Filename, True Magic Bytes, and individual byte entropy scores. Any discrepancy between declared file extensions and underlying magic bytes is highlighted in bright red.
</p>

<h3>Figure 6: Threat Rule Generator & Hop Transit Topology</h3>
<figure>
    <img src="{img_yara}" alt="Threat Rules and Hop Map Dock" style="width: 100%;" />
    <figcaption>Figure 7.6: Threat Rule Generator displaying automated YARA and Snort/Suricata rules alongside the multi-hop relay sequence.</figcaption>
</figure>
<p>
Figure 7.6 showcases the Right-Bottom dock, which toggles between the chronological Hop Relay Map (with IP addresses, delta latency, and ASN classifications) and automated threat signature tabs for <strong>YARA Signatures</strong> and <strong>Snort/Suricata Rules</strong> ready for deployment across enterprise security perimeters.
</p>

<h3>Figure 7: Local LLM Neural Copilot in Active Forensic Reasoning</h3>
<figure>
    <img src="{img_copilot}" alt="Local LLM Neural Copilot Active Chat" style="width: 100%;" />
    <figcaption>Figure 7.7: Local LLM Neural Copilot performing an automated deep autopsy using local Ollama / CatBERT intelligence.</figcaption>
</figure>
<p>
Figure 7.7 demonstrates the Local LLM Neural Copilot dock in action. Connected to a local Ollama server (or running on the embedded fallback engine), the Copilot accepts conversational queries or one-click tactical prompts (<code>⚡ Deep Autopsy</code>, <code>📝 Police FIR Draft</code>, <code>🎯 MITRE Kill-Chain</code>). The chat transcript displays a structured forensic explanation of the evidence artifact, highlighting envelope discrepancies, cryptographic alignment, and recommended investigative actions.
</p>
"""
