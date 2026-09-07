"""Main Compilation Script: Assembles all chapters and generates publication-grade PDF."""
import os
import sys
import weasyprint
from pathlib import Path

from report_generator.styles import PDF_CSS
import report_generator.ch1_executive as c1
import report_generator.ch2_philosophy as c2
import report_generator.ch3_architecture as c3
import report_generator.ch4_pipeline as c4
import report_generator.ch5_math as c5
import report_generator.ch6_legal_bsa as c6
import report_generator.ch7_screenshots as c7
import report_generator.ch8_local_llm as c8
import report_generator.ch9_operations as c9
import report_generator.ch10_benchmarks as c10

def build_cover_page() -> str:
    return """
<div class="cover-page">
    <div>
        <div class="cover-badge">AICTE Smart India Hackathon 2026 • Problem Statement #26106</div>
        <div class="cover-title">
            SUDO <span>SPANDR</span>
        </div>
        <div class="cover-subtitle">
            The Definitive Technical Architecture & Reverse-Engineering Monograph:<br>
            100% Offline Electronic Mail Autopsy Engine, Local LLM Intelligence, and Section 63 BSA 2023 Evidentiary Admissibility
        </div>
    </div>

    <div class="cover-meta-grid">
        <div class="cover-meta-item">
            <strong>PROJECT INITIATIVE</strong>
            Smart India Hackathon (SIH 2026)<br>
            Problem Statement #26106
        </div>
        <div class="cover-meta-item">
            <strong>DEVELOPMENT TEAM</strong>
            Team SUDO SPANDR<br>
            Sovereign Cyber Defense Research
        </div>
        <div class="cover-meta-item">
            <strong>DOCUMENT CLASSIFICATION</strong>
            Technical Specification & Reverse-Engineering Reference Manual
        </div>
        <div class="cover-meta-item">
            <strong>RELEASE VERSION & BUILD</strong>
            Version 2.5 (Gold Master Edition)<br>
            September 2026
        </div>
    </div>
</div>
"""

def build_table_of_contents() -> str:
    return """
<h1>Table of Contents</h1>
<table style="margin-top: 6mm;">
    <thead>
        <tr>
            <th style="width: 15%;">Chapter</th>
            <th style="width: 65%;">Title & Core Forensic Subject Matter</th>
            <th style="width: 20%;">Coverage</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Chapter 1</strong></td>
            <td><strong>Executive Summary & Problem Statement #26106</strong><br>
            Threat Landscape 2026, Cloud Failure Risks, Sovereign Air-Gap Mandate</td>
            <td>Strategic Overview</td>
        </tr>
        <tr>
            <td><strong>Chapter 2</strong></td>
            <td><strong>The Reverse-Engineering Forensic Philosophy</strong><br>
            Ghidra/IDA Pro Paradigm, Treating Mail as Compiled Binary, Post-Mortem Dissection</td>
            <td>Methodology</td>
        </tr>
        <tr>
            <td><strong>Chapter 3</strong></td>
            <td><strong>System Architecture & Tech Stack ("Kaise Bana Hai")</strong><br>
            MVC Architecture, PyQt6 GUI, Rich TUI, Parser/Forensics/Carver Modular Decomposition</td>
            <td>Engineering Design</td>
        </tr>
        <tr>
            <td><strong>Chapter 4</strong></td>
            <td><strong>The Deep Raw Email Post-Mortem Pipeline ("Kaise Kaam Karta Hai")</strong><br>
            12-Stage Execution Pipeline from Bitstream Locking to Rule Generation</td>
            <td>Pipeline Anatomy</td>
        </tr>
        <tr>
            <td><strong>Chapter 5</strong></td>
            <td><strong>Mathematical & Algorithmic Foundations</strong><br>
            Shannon Entropy $H(X)$, Levenshtein Edit Distance, IDN Homoglyphs, Transit Graph DAG</td>
            <td>Mathematics</td>
        </tr>
        <tr>
            <td><strong>Chapter 6</strong></td>
            <td><strong>Legal Admissibility & Section 63 BSA 2023 Implementation</strong><br>
            Transition from Sec 65B IEA, Statutory Mandates, Tamper-Evident PDF Certification</td>
            <td>Legal Framework</td>
        </tr>
        <tr>
            <td><strong>Chapter 7</strong></td>
            <td><strong>UI/UX Workstation Walkthrough & Operational Telemetry</strong><br>
            Figures 1-7: Full Screenshot Tour of TUI, Ghidra GUI, Header Inspector, URLs, MIME, Copilot</td>
            <td>Visual Interfaces</td>
        </tr>
        <tr>
            <td><strong>Chapter 8</strong></td>
            <td><strong>Local LLM Neural Copilot Architecture & Legal FIR Synthesis</strong><br>
            Ollama REST Client, CatBERT Embedded Fallback, Police FIR Draft (IT Act / BNS 2023)</td>
            <td>Artificial Intelligence</td>
        </tr>
        <tr>
            <td><strong>Chapter 9</strong></td>
            <td><strong>Deployment, Installation & Operational Reference Guide</strong><br>
            Kali Linux Setup, Virtualenv, Execution Flags, Complete Keyboard Shortcut Matrix</td>
            <td>User Operations</td>
        </tr>
        <tr>
            <td><strong>Chapter 10</strong></td>
            <td><strong>Empirical Benchmarks, Comparative Analysis & Future Roadmap</strong><br>
            Latency & Memory Profiling, Industry Benchmark Matrix, HSM & GNN Roadmap</td>
            <td>Empirical Evaluation</td>
        </tr>
    </tbody>
</table>
"""

def generate_full_pdf(output_pdf_path: str = "SUDO_SPANDR_Comprehensive_Technical_Architecture_Report.pdf"):
    print("Assembling all chapters...")
    cover = build_cover_page()
    toc = build_table_of_contents()
    ch1 = c1.get_chapter_1_html()
    ch2 = c2.get_chapter_2_html()
    ch3 = c3.get_chapter_3_html()
    ch4 = c4.get_chapter_4_html()
    ch5 = c5.get_chapter_5_html()
    ch6 = c6.get_chapter_6_html()
    ch7 = c7.get_chapter_7_html()
    ch8 = c8.get_chapter_8_html()
    ch9 = c9.get_chapter_9_html()
    ch10 = c10.get_chapter_10_html()

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SUDO SPANDR: Definitive Technical Monograph</title>
    <style>
        {PDF_CSS}
    </style>
</head>
<body>
    {cover}
    {toc}
    {ch1}
    {ch2}
    {ch3}
    {ch4}
    {ch5}
    {ch6}
    {ch7}
    {ch8}
    {ch9}
    {ch10}
</body>
</html>
"""

    print("Writing temporary monograph HTML...")
    html_path = Path("monograph.html")
    html_path.write_text(full_html, encoding="utf-8")

    print(f"Compiling PDF via WeasyPrint to '{output_pdf_path}'...")
    html_doc = weasyprint.HTML(filename=str(html_path))
    html_doc.write_pdf(target=output_pdf_path)
    print(f"✔ Successfully generated publication-grade PDF: {output_pdf_path}")

    # Check generated PDF size
    pdf_file = Path(output_pdf_path)
    size_mb = pdf_file.stat().st_size / (1024 * 1024)
    print(f"PDF File Size: {size_mb:.2f} MB")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "SUDO_SPANDR_Comprehensive_Technical_Architecture_Report.pdf"
    generate_full_pdf(out)
