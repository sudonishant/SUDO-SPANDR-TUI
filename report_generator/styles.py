"""CSS Styles for SUDO SPANDR Publication-Grade Technical Monograph PDF."""

PDF_CSS = """
@page {
    size: A4;
    margin: 22mm 18mm 22mm 18mm;
    @top-right {
        content: "SUDO SPANDR — Digital Forensic Technical Monograph";
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 7.5pt;
        color: #64748b;
        font-weight: 500;
        border-bottom: 0.5pt solid #cbd5e1;
        padding-bottom: 3mm;
    }
    @bottom-left {
        content: "AICTE Smart India Hackathon 2026 | Problem Statement #26106";
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 7.5pt;
        color: #94a3b8;
        border-top: 0.5pt solid #cbd5e1;
        padding-top: 3mm;
    }
    @bottom-right {
        content: "Page " counter(page) " of " counter(pages);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 7.5pt;
        color: #64748b;
        font-weight: 600;
        border-top: 0.5pt solid #cbd5e1;
        padding-top: 3mm;
    }
}

@page:first {
    margin: 0;
    @top-right { content: none; }
    @bottom-left { content: none; }
    @bottom-right { content: none; }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.55;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}

/* Cover Page */
.cover-page {
    page-break-after: always;
    background: linear-gradient(145deg, #090d16 0%, #0f172a 60%, #1e293b 100%);
    color: #f8fafc;
    padding: 40mm 24mm 30mm 24mm;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.cover-badge {
    display: inline-block;
    background: rgba(14, 165, 233, 0.15);
    border: 1px solid #0284c7;
    color: #38bdf8;
    padding: 4px 12px;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border-radius: 4px;
    margin-bottom: 25mm;
}

.cover-title {
    font-size: 26pt;
    font-weight: 800;
    line-height: 1.15;
    color: #ffffff;
    margin: 0 0 10mm 0;
    letter-spacing: -0.5px;
}

.cover-title span {
    color: #38bdf8;
}

.cover-subtitle {
    font-size: 13pt;
    font-weight: 400;
    line-height: 1.45;
    color: #94a3b8;
    margin: 0 0 20mm 0;
    border-left: 3px solid #38bdf8;
    padding-left: 5mm;
}

.cover-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8mm;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    padding-top: 10mm;
    margin-top: auto;
}

.cover-meta-item {
    font-size: 8.5pt;
    color: #94a3b8;
}

.cover-meta-item strong {
    display: block;
    color: #f1f5f9;
    font-size: 9.5pt;
    margin-bottom: 2px;
}

/* Headings */
h1 {
    font-size: 17pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 2.5mm;
    margin-top: 10mm;
    margin-bottom: 4mm;
    page-break-before: always;
    page-break-after: avoid;
    letter-spacing: -0.3px;
}

h2 {
    font-size: 13pt;
    font-weight: 700;
    color: #0369a1;
    margin-top: 7mm;
    margin-bottom: 3mm;
    page-break-after: avoid;
    border-left: 3px solid #0284c7;
    padding-left: 3mm;
}

h3 {
    font-size: 10.5pt;
    font-weight: 700;
    color: #334155;
    margin-top: 5mm;
    margin-bottom: 2mm;
    page-break-after: avoid;
}

p {
    margin-top: 0;
    margin-bottom: 3mm;
    text-align: justify;
}

/* Technical Callout Boxes */
.callout {
    background-color: #f8fafc;
    border-left: 4px solid #0284c7;
    padding: 3.5mm 4.5mm;
    margin: 4mm 0;
    border-radius: 0 4px 4px 0;
    font-size: 9pt;
    page-break-inside: avoid;
}

.callout.warning {
    background-color: #fffbeb;
    border-left-color: #f59e0b;
}

.callout.danger {
    background-color: #fef2f2;
    border-left-color: #ef4444;
}

.callout.success {
    background-color: #f0fdf4;
    border-left-color: #10b981;
}

.callout-title {
    font-weight: 700;
    font-size: 9pt;
    margin-bottom: 1.5mm;
    display: flex;
    align-items: center;
    color: #0f172a;
}

/* Code & Terminal Blocks */
pre, code {
    font-family: "DejaVu Sans Mono", "SFMono-Regular", Consolas, Menlo, monospace;
}

code {
    font-size: 8.5pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
}

pre {
    background-color: #0f172a;
    color: #e2e8f0;
    font-size: 8pt;
    line-height: 1.45;
    padding: 3.5mm 4.5mm;
    border-radius: 5px;
    border: 1px solid #334155;
    overflow-x: hidden;
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 3.5mm 0;
    page-break-inside: avoid;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 4mm 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}

th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 2.5mm 3mm;
    border: 1px solid #1e293b;
}

td {
    padding: 2mm 3mm;
    border: 1px solid #e2e8f0;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #f8fafc;
}

/* Figures & Images */
figure {
    margin: 5mm 0;
    padding: 0;
    text-align: center;
    page-break-inside: avoid;
}

figure img {
    max-width: 100%;
    height: auto;
    border-radius: 5px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

figcaption {
    font-size: 8pt;
    color: #64748b;
    margin-top: 2mm;
    font-style: italic;
}

/* Math block */
.math-equation {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 3mm;
    text-align: center;
    font-family: "DejaVu Sans Mono", monospace;
    font-weight: bold;
    color: #0369a1;
    margin: 3.5mm 0;
    page-break-inside: avoid;
}
"""
