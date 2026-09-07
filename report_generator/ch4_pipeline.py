"""Chapter 4: The Deep Raw Email Post-Mortem Pipeline ("Kaise Kaam Karta Hai")"""

def get_chapter_4_html() -> str:
    return r"""
<h1>4. The Deep Raw Email Post-Mortem Pipeline ("Kaise Kaam Karta Hai")</h1>

<h2>4.1 Overview of the End-to-End Forensic Dissection Pipeline</h2>
<p>
To perform a mathematically rigorous and legally defensible forensic examination, <strong>SUDO SPANDR</strong> executes a disciplined, multi-stage <strong>Post-Mortem Autopsy Pipeline</strong>. Every seized electronic mail file undergoes twelve sequential processing phases, transitioning from raw bitstream hashing through structural grammar parsing, cryptographic verification, transit graph reconstruction, byte-level payload carving, and cognitive artificial intelligence evaluation, culminating in automated court-admissible certificate generation.
</p>

<pre>
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                     THE 12-STAGE SUDO SPANDR FORENSIC AUTOPSY PIPELINE                 │
├─────────┬──────────────────────────────────────────────────────────────────────────────┤
│ Stage 1 │ EVIDENCE INGESTION & CRYPTOGRAPHIC BITSTREAM LOCKING (SHA-256 / MD5)         │
│ Stage 2 │ RFC 5322 LEXICAL ANALYSIS, HEADER UNFOLDING & STATE MACHINE TOKENIZATION    │
│ Stage 3 │ ENVELOPE IDENTITY & DISPLAY-NAME SPOOFING PATHOLOGY                          │
│ Stage 4 │ CRYPTOGRAPHIC AUTHENTICATION MATRIX EVALUATION (SPF, DKIM, DMARC, ARC)       │
│ Stage 5 │ RELAY TRANSIT TOPOLOGY RECONSTRUCTION & DELTA LATENCY MATHEMATICS            │
│ Stage 6 │ HYPERLINK HARVESTING, IDN PUNYCODE DECODING & HOMOGLYPH MATRIX DISSECTION    │
│ Stage 7 │ MIME MULTI-PART BODY CARVING & RECURSIVE ATTACHMENT EXTRACTION              │
│ Stage 8 │ TRUE FILE MAGIC BYTE IDENTIFICATION & DOUBLE-EXTENSION DETECTION            │
│ Stage 9 │ SHANNON ENTROPY BITSTREAM CARVING (PACKED SHELLCODE & DROPPER IDENTIFICATION)│
│ Stage 10│ COGNITIVE NLP & CATBERT PSYCHOLOGICAL THREAT PROFILING                       │
│ Stage 11│ LOCAL LLM NEURAL COPILOT REASONING & POLICE FIR COMPLAINT SYNTHESIS         │
│ Stage 12│ RULE COMPILATION (YARA / SNORT) & SECTION 63 BSA 2023 CERTIFICATE EXPORT    │
└─────────┴──────────────────────────────────────────────────────────────────────────────┘
</pre>

<h2>4.2 Step-by-Step Deep Forensic Breakdown</h2>

<h3>Stage 1: Evidence Ingestion & Cryptographic Bitstream Locking</h3>
<p>
When an investigator selects an evidence file (e.g., <code>Security alert (1).eml</code>), the system immediately reads the file into an isolated in-memory byte buffer in binary mode (<code>'rb'</code>). The file descriptor on disk is set to read-only. Before any parsing begins, the engine computes three distinct cryptographic digests across the raw byte array:
</p>
<ul>
    <li><strong>SHA-256 (FIPS 180-4):</strong> The primary 256-bit hash serving as the global unique identifier and legal anchor for the forensic case docket.</li>
    <li><strong>MD5 (RFC 1321):</strong> Computed for legacy cross-referencing with historical forensic databases and National Software Reference Library (NSRL) records.</li>
    <li><strong>SHA-512 (FIPS 180-4):</strong> Computed for high-security defense cases requiring 512-bit collision resistance.</li>
</ul>
<p>
These hashes are permanently locked into the runtime state object. If even a single bit of the file is modified downstream, the hash verification check fails immediately, aborting the investigation and preserving evidentiary integrity.
</p>

<h3>Stage 2: RFC 5322 Lexical Analysis & Header Unfolding</h3>
<p>
Electronic mail headers conform to RFC 5322 grammar, which permits "folding" (splitting long header values across multiple lines by indenting subsequent lines with space or horizontal tab characters). Malicious threat actors frequently exploit parser differences by inserting folding characters into sensitive headers like <code>From:</code> or <code>Subject:</code> to cause email security gateways to skip inspection while client MUAs unfold and execute the string.
</p>
<p>
SUDO SPANDR executes a lexical tokenizer that scans for CRLF sequences followed by whitespace (<code>\r\n[ \t]</code>). It unfolds the multiline values into normalized strings while simultaneously retaining the raw, folded byte offsets in a secondary audit table for forensic review.
</p>

<h3>Stage 3: Envelope Identity & Display-Name Spoofing Pathology</h3>
<p>
The engine performs a critical comparative analysis between three distinct identity parameters defined in the SMTP protocol suite:
</p>
<ol>
    <li><strong>RFC 5321 Mail From (Envelope Return-Path):</strong> The physical routing address used by Mail Transfer Agents to route non-delivery reports (NDRs) and bounce notices.</li>
    <li><strong>RFC 5322 From (Header From):</strong> The email address displayed in the user interface of the recipient's mail client.</li>
    <li><strong>RFC 5322 Display Name (Friendly-From):</strong> The human-readable string associated with the From address (e.g., <code>"Google Security Team"</code>).</li>
</ol>
<p>
Adversaries routinely execute "Display-Name Masquerading"—setting the display name to a legitimate entity (e.g., <code>"Google &lt;no-reply@accounts.google.com&gt;"</code>) while setting the actual transmitting mailbox to an attacker-controlled address. SUDO SPANDR separates the display string from the RFC angle brackets, isolates the top-level domain (TLD) and second-level domain (SLD) of each, and flags domain divergence with a high-priority forensic warning.
</p>

<h3>Stage 4: Cryptographic Authentication Matrix Evaluation (SPF, DKIM, DMARC)</h3>
<p>
Modern email authentication relies on a triad of cryptographic and DNS protocols:
</p>
<ul>
    <li><strong>Sender Policy Framework (SPF, RFC 7208):</strong> Validates whether the IP address of the transmitting MTA is authorized to transmit email on behalf of the domain listed in the envelope <code>Return-Path</code>. SUDO SPANDR parses <code>Received-SPF</code> headers, identifying <code>PASS</code>, <code>FAIL</code>, <code>SOFTFAIL</code>, <code>NEUTRAL</code>, and <code>NONE</code> dispositions.</li>
    <li><strong>DomainKeys Identified Mail (DKIM, RFC 6376):</strong> Verifies an asymmetric cryptographic signature generated by the sender using a private RSA key. The signature covers specified email headers and the message body hash (<code>bh=</code>). SUDO SPANDR evaluates the signature tag-value list (<code>v=1; a=rsa-sha256; d=example.com; s=selector; bh=...; b=...</code>) to confirm cryptographic integrity.</li>
    <li><strong>Domain-based Message Authentication, Reporting, and Conformance (DMARC, RFC 7489):</strong> Enforces domain alignment. Even if SPF and DKIM pass individually, DMARC mandates that the domain validated by SPF and/or DKIM must match the domain displayed to the end-user in the RFC 5322 <code>From:</code> header. If domain alignment is broken, SUDO SPANDR flags the artifact for DMARC violation.</li>
</ul>

<h3>Stage 5: Relay Transit Topology Reconstruction & Delta Latency Mathematics</h3>
<p>
Every intermediate MTA that relays an email prepends a <code>Received:</code> header to the message stream. SUDO SPANDR parses these headers in bottom-up chronological order (from the originating client up to the final recipient's MX server), extracting timestamps, transmitting IP addresses, and EHLO/HELO hostnames.
</p>
<p>
The engine computes the transit latency delta ($\Delta t$) between consecutive hops:
</p>
<div class="math-equation">
    \Delta t_{hop} = \text{Timestamp}(Hop_{i+1}) - \text{Timestamp}(Hop_{i})
</div>
<p>
Anomalous latency signatures are instantly flagged:
</p>
<ul>
    <li><strong>Negative Delta Latency ($\Delta t < 0$):</strong> Indicates either clock synchronization failure (NTP desynchronization) or intentional header forgery injected by an adversary attempting to spoof intermediate routing hops.</li>
    <li><strong>Excessive Transit Latency ($\Delta t > 3600\text{s}$):</strong> Suggests that the email was held in an intermediate graylisting queue, intercepted by a man-in-the-middle (MITM) proxy, or subjected to offline weaponization before final delivery.</li>
    <li><strong>Anomalous IP Classification:</strong> Transmitting IPs are classified as RFC 1918 private addresses, major corporate cloud infrastructure (Google Workspace, Microsoft 365, Amazon SES), or suspicious foreign autonomous systems (ASNs).</li>
</ul>

<h3>Stage 6: Hyperlink Harvesting, IDN Punycode Decoding & Homoglyph Matrix</h3>
<p>
Phishing attacks overwhelmingly rely on deceptive hyperlinks. SUDO SPANDR extracts all URLs from both plaintext and HTML MIME parts using regular expression pattern matching. Each URL is dissected into its constituent scheme, host, port, path, and query parameters.
</p>
<p>
The engine specifically hunts for <strong>Internationalized Domain Name (IDN) Homograph Attacks</strong>. Threat actors register domains containing non-Latin characters (e.g., Cyrillic <code>'а'</code> (U+0430) instead of Latin <code>'a'</code> (U+0061)) which look visually identical in client mail applications but resolve to malicious servers. When decoded by web browsers, these domains are represented via Punycode (prefixed with <code>xn--</code>). SUDO SPANDR decodes all Punycode strings, detects mixed-script Unicode anomalies, and computes Levenshtein edit distances against a dictionary of high-value financial and technology domains.
</p>

<h3>Stage 7: MIME Multi-Part Body Carving & Recursive Extraction</h3>
<p>
Emails containing formatting and attachments utilize the Multipurpose Internet Mail Extensions (MIME, RFC 2045) standard. SUDO SPANDR traverses the MIME part tree recursively, identifying content types (e.g., <code>multipart/mixed</code>, <code>multipart/alternative</code>, <code>text/html</code>, <code>application/octet-stream</code>). It handles base64 and quoted-printable decoding streams, safely carving encapsulated binary payloads into memory buffers without writing them to disk as executable files.
</p>

<h3>Stage 8: True File Magic Byte Identification & Double-Extension Trapping</h3>
<p>
Relying on file extensions is fatal in malware analysis. Threat actors routinely disguise executable droppers as benign documents (e.g., naming a file <code>Quarterly_Earnings.pdf.exe</code> or setting the MIME header to <code>Content-Type: application/pdf</code> while the underlying byte stream contains a Windows PE binary).
</p>
<p>
SUDO SPANDR reads the magic byte signatures from the first 16 bytes of each carved payload and matches them against its internal signature database:
</p>
<table>
    <thead>
        <tr>
            <th>File Type</th>
            <th>True Magic Bytes (Hex)</th>
            <th>MIME / Declared Extension</th>
            <th>Threat Indication If Mismatched</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Windows Portable Executable</strong></td>
            <td><code>4D 5A</code> (<code>MZ</code>)</td>
            <td><code>.exe</code>, <code>.dll</code>, <code>.scr</code></td>
            <td>CRITICAL: Executable binary disguised as document</td>
        </tr>
        <tr>
            <td><strong>Linux ELF Executable</strong></td>
            <td><code>7F 45 4C 46</code> (<code>.ELF</code>)</td>
            <td><code>.bin</code>, <code>.sh</code></td>
            <td>HIGH: Compiled Linux binary dropper</td>
        </tr>
        <tr>
            <td><strong>Adobe PDF Document</strong></td>
            <td><code>25 50 44 46</code> (<code>%PDF</code>)</td>
            <td><code>.pdf</code></td>
            <td>NORMAL: Standard PDF document structure</td>
        </tr>
        <tr>
            <td><strong>ZIP Archive / Office XML</strong></td>
            <td><code>50 4B 03 04</code> (<code>PK..</code>)</td>
            <td><code>.zip</code>, <code>.docx</code>, <code>.xlsx</code></td>
            <td>ELEVATED: Compressed container; inspect inner files</td>
        </tr>
        <tr>
            <td><strong>Microsoft Compound OLE</strong></td>
            <td><code>D0 CF 11 E0 A1 B1 1A E1</code></td>
            <td><code>.doc</code>, <code>.xls</code></td>
            <td>HIGH: Legacy Office document with potential VBA macros</td>
        </tr>
    </tbody>
</table>

<h3>Stage 9: Shannon Entropy Bitstream Carving</h3>
<p>
To detect packed malware, encrypted shellcode droppers, and encrypted C2 configuration blocks, SUDO SPANDR calculates the Shannon entropy across the byte distribution of carved attachments and raw message bodies. A score greater than 7.2 bits per byte indicates dense encryption or packing, triggering an immediate alert.
</p>

<h3>Stage 10: Cognitive NLP & CatBERT Psychological Threat Profiling</h3>
<p>
The linguistic text of the email is parsed to detect psychological manipulation techniques. The engine scores urgency, authority impersonation, and financial coercion, generating an objective cognitive threat rating.
</p>

<h3>Stage 11: Local LLM Neural Copilot Reasoning & Police FIR Synthesis</h3>
<p>
The complete forensic dossier is handed off to the Local LLM Copilot (running via local Ollama or the embedded offline engine). Analysts can execute automated one-click actions:
</p>
<ul>
    <li><code>⚡ Deep Autopsy:</code> Synthesizes a structured intelligence breakdown of all discovered anomalies.</li>
    <li><code>📝 Police FIR Draft:</code> Automatically generates a formal First Information Report (FIR) complaint compliant with Indian penal statutes (Section 66D of the Information Technology Act, 2000 and Section 318(4) of the Bharatiya Nyaya Sanhita, 2023).</li>
    <li><code>🎯 MITRE Kill-Chain:</code> Maps the observed indicators directly to MITRE ATT&CK techniques (T1566.001 Spearphishing Attachment, T1566.002 Spearphishing Link, T1036 Masquerading).</li>
</ul>

<h3>Stage 12: Threat Rule Compilation & Section 63 BSA 2023 Certification</h3>
<p>
Finally, the system compiles automated YARA and Snort/Suricata rules for enterprise defense and exports an immutable Section 63 BSA 2023 court-admissible certificate PDF.
</p>
"""
