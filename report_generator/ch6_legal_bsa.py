"""Chapter 6: Legal Admissibility & Section 63 BSA 2023 Implementation"""

def get_chapter_6_html() -> str:
    return r"""
<h1>6. Legal Admissibility & Section 63 BSA 2023 Implementation</h1>

<h2>6.1 The Statutory Transition in Indian Evidence Jurisprudence</h2>
<p>
For over two decades, the admissibility of electronic evidence in Indian courts was governed by <strong>Section 65B of the Indian Evidence Act, 1872 (IEA)</strong>, introduced by the Information Technology Act, 2000. In landmark rulings such as <em>Anvar P.V. v. P.K. Basheer (2014) 10 SCC 473</em> and <em>Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) 7 SCC 1</em>, the Supreme Court of India established that electronic records are inadmissible as secondary evidence unless accompanied by a mandatory certificate under Section 65B(4).
</p>
<p>
With the historic enactment of the <strong>Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023)</strong>, which came into full legal force on <strong>July 1, 2024</strong>, the Indian Evidence Act, 1872 was formally repealed and superseded. Electronic evidence admissibility is now governed exclusively by <strong>Section 63 of the Bharatiya Sakshya Adhiniyam, 2023 (BSA 2023)</strong>.
</p>

<div class="callout success">
    <div class="callout-title">⚖️ Statutory Alignment with Bharatiya Sakshya Adhiniyam, 2023</div>
    <p>
    <strong>SUDO SPANDR</strong> is the first open-architecture forensic email suite in India engineered specifically to comply with the statutory provisions and procedural requirements of <strong>Section 63 of the Bharatiya Sakshya Adhiniyam, 2023</strong>. Every examination session automatically establishes cryptographic chain-of-custody, recording device telemetry, examiner identity, and cryptographic bitstream hashes necessary to withstand rigorous judicial examination in Indian criminal and civil courts.
    </p>
</div>

<h2>6.2 Core Provisions of Section 63 BSA 2023</h2>
<p>
Section 63 of the BSA 2023 establishes four fundamental statutory mandates that any forensic software must satisfy to render electronic records admissible as primary or secondary evidence:
</p>

<h3>1. Section 63(1) — Legal Status of Electronic Records</h3>
<p>
Any information contained in an electronic record which is printed on paper, stored, recorded, or copied in optical, magnetic, or electronic media produced by a computer shall be deemed to be also a document, and shall be admissible in any proceedings, without further proof or production of the original, as evidence of any contents of the original or of any fact stated therein of which direct evidence would be admissible.
</p>

<h3>2. Section 63(2) — Conditions Precedent to Admissibility</h3>
<p>
The computer system utilized to extract, process, or store the electronic record must satisfy four cumulative statutory conditions:
</p>
<ul>
    <li><strong>Lawful Control & Continuous Use:</strong> The computer was produced by the computer during the period over which the computer was used regularly to store or process information for the purposes of any activities regularly carried on over that period by the person having lawful control over the use of the computer.</li>
    <li><strong>Regular Supply of Information:</strong> During the said period, information of the kind contained in the electronic record or from which the information so contained is derived was regularly fed into the computer in the ordinary course of the said activities.</li>
    <li><strong>Operational Integrity:</strong> Throughout the material part of the said period, the computer was operating properly or, if not, that in respect of any period in which it was not operating properly or was out of operation for that part of the period, was not such as to affect the electronic record or the accuracy of its contents.</li>
    <li><strong>Reproduction Fidelity:</strong> The information contained in the electronic record reproduces or is derived from such information fed into the computer in the ordinary course of the said activities.</li>
</ul>

<h3>3. Section 63(4) — Mandatory Evidentiary Certificate</h3>
<p>
To satisfy Section 63(4), a formal certificate must be presented to the court, fulfilling three requirements:
</p>
<ol>
    <li>Identifying the electronic record containing the statement and describing the manner in which it was produced;</li>
    <li>Giving such particulars of any device involved in the production of that electronic record as may be appropriate for the purpose of showing that the electronic record was produced by a computer;</li>
    <li>Purporting to be signed by a person in charge of the computer or device, or by a person occupying a responsible official position in relation to the operation of the relevant device or the management of the relevant activities.</li>
</ol>

<h2>6.3 The Cryptographic Chain-of-Custody Architecture</h2>
<p>
To eliminate human error and prevent allegations of evidence tampering during police investigations or court proceedings, <strong>SUDO SPANDR</strong> automates the entire Section 63 certification workflow through <code>core/bsa_cert.py</code> and <code>core/pdf_gen.py</code>.
</p>

<pre>
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               SUDO SPANDR CRYPTOGRAPHIC BITSTREAM CUSTODY PIPELINE                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   SEIZED EVIDENCE FILE (.eml / .msg / .pst)                                            │
│   └── Physical Storage: Read-Only POSIX File Descriptor Locked                         │
│                                                                                        │
│   CRYPTOGRAPHIC BITSTREAM IMMUTABILITY LAYER                                           │
│   ├── SHA-256 Digest : 72c61465cf2ac170881b54a61fe8a0bca50c319cf9657cc40dcfb505...   │
│   ├── MD5 Digest     : 24785ca8da5ee4f605a91438992c4228                               │
│   └── File Size      : 13,624 Bytes (Exact bitstream byte count)                       │
│                                                                                        │
│   EXAMINER & SYSTEM ENVIRONMENT BINDING                                                │
│   ├── Workstation Hostname : kali-forensic-lab-01                                      │
│   ├── Operating System     : Linux 6.1.0-kali-amd64 #1 SMP PREEMPT_DYNAMIC             │
│   ├── Forensic Software    : SUDO SPANDR Workstation v2.5 (Core Build: 2026.09.07)     │
│   ├── Primary MAC Address  : 08:00:27:C4:B9:71                                         │
│   └── Forensic Case ID     : CS-CASE-20260907-72C614                                   │
│                                                                                        │
│   LEGAL ATTESTATION COMPILATION (Section 63 BSA 2023)                                  │
│   ├── Timestamp (UTC)      : 2026-09-07 17:30:00 UTC                                   │
│   ├── Statutory Statement  : "All examinations conducted on bitstream duplicates..."   │
│   └── Legal Status         : Admissible in Indian Criminal Courts & Tribunals          │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
</pre>

<h2>6.4 Structure of the Generated Court Certificate PDF</h2>
<p>
When an analyst clicks <strong>[Generate Section 63 BSA 2023 PDF Certificate]</strong> in the GUI toolbar or presses <code>[E]</code> in the TUI, the system compiles a multi-page, high-resolution PDF document formatted specifically for submission to Indian criminal trial courts (Magistrate Courts, Sessions Courts, and Special CBI/Cyber Courts). The certificate contains:
</p>
<ul>
    <li><strong>Court & Case Docket Header:</strong> Case Title, Seizure Memo Number, Police Station / Investigating Agency, and Investigating Officer Name.</li>
    <li><strong>Hardware & Software Telemetry:</strong> Machine hostname, CPU architecture, operating system kernel release, and MAC address.</li>
    <li><strong>Bitstream Cryptographic Profile:</strong> Full 64-character SHA-256 hash and 32-character MD5 hash of the electronic evidence, establishing that the seized artifact has not undergone bit-level alteration.</li>
    <li><strong>RFC 5322 Envelope Metadata:</strong> From, To, Subject, Date, Message-ID, hop count, and carved attachment inventory.</li>
    <li><strong>Statutory Declaration:</strong> Formal legal statement affirming that the computer system was operating properly, that no unauthorized intervention occurred, and that the report represents a true reproduction of the digital evidence.</li>
    <li><strong>Signature Block:</strong> Reserved section for digital signatures (DSC Token / e-Sign) or physical attestation by the Forensic Examiner under Section 63(4).</li>
</ul>
"""
