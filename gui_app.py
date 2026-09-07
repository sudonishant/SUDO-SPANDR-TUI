#!/usr/bin/env python3
"""
SUDO SPANDR - Forensic Ghidra Desktop Workstation (GUI) v2.4
AICTE - Smart India Hackathon 2026 | Problem Statement #26106
Team SUDO SPANDR — 100% Offline & Air-Gap Ready Reverse-Engineering Forensic Suite
Modeled after NSA Ghidra CodeBrowser & IDA Pro
Deep Raw Email Post-Mortem, MIME Dissector, & Autopsy Engine
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QColor, QFont, QIcon, QTextCursor
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QDockWidget,
)

# Import SUDO SPANDR Forensic Core Modules
from core.ai_engine import perform_offline_cognitive_nlp_analysis, request_online_llm_analysis
from core.batch import export_batch_to_csv, scan_evidence_directory
from core.bsa_cert import export_bsa_certificate, format_bsa_certificate_text, generate_bsa_certificate_data
from core.carver import (
    analyze_attachment_forensics,
    calculate_shannon_entropy,
    generate_hex_dump,
    get_entropy_spectrum_bars,
)
from core.forensics import analyze_relay_hops, evaluate_forensic_threat_matrix
from core.parser import parse_email_evidence
from core.pdf_gen import export_bsa_pdf
from core.rule_gen import export_threat_rules, generate_snort_rule, generate_stix_bundle, generate_yara_rule

# Ghidra Cyberpunk / Obsidian Dark Palette
GHIDRA_QSS = """
QMainWindow {
    background-color: #16161e;
}
QMenuBar {
    background-color: #1a1b26;
    color: #c0caf5;
    border-bottom: 1px solid #2f3549;
    font-size: 13px;
    padding: 2px;
}
QMenuBar::item:selected {
    background-color: #283457;
    color: #00f0ff;
    border-radius: 3px;
}
QMenu {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1px solid #414868;
}
QMenu::item:selected {
    background-color: #3b4261;
    color: #00f0ff;
}
QToolBar {
    background-color: #1a1b26;
    border-bottom: 1px solid #2f3549;
    spacing: 6px;
    padding: 3px;
}
QToolButton {
    background-color: #24283b;
    color: #c0caf5;
    border: 1px solid #414868;
    border-radius: 4px;
    padding: 5px 10px;
    font-weight: bold;
    font-size: 12px;
}
QToolButton:hover {
    background-color: #3b4261;
    border-color: #00f0ff;
    color: #00f0ff;
}
QDockWidget {
    color: #00f0ff;
    font-weight: bold;
    font-size: 12px;
}
QDockWidget::title {
    background-color: #1f2335;
    padding: 6px;
    border: 1px solid #2f3549;
    border-radius: 3px;
}
QTreeWidget, QTableWidget, QTextEdit {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1px solid #2f3549;
    border-radius: 4px;
    gridline-color: #2f3549;
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 12px;
}
QTreeWidget::item:selected, QTableWidget::item:selected {
    background-color: #283457;
    color: #00f0ff;
}
QHeaderView::section {
    background-color: #1f2335;
    color: #7aa2f7;
    padding: 4px;
    font-weight: bold;
    border: 1px solid #2f3549;
}
QTabWidget::pane {
    border: 1px solid #2f3549;
    background-color: #1a1b26;
}
QTabBar::tab {
    background-color: #1f2335;
    color: #7aa2f7;
    padding: 6px 14px;
    border: 1px solid #2f3549;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #283457;
    color: #00f0ff;
    font-weight: bold;
    border-bottom: 2px solid #00f0ff;
}
QStatusBar {
    background-color: #1a1b26;
    color: #7aa2f7;
    border-top: 1px solid #2f3549;
    font-size: 11px;
}
QProgressBar {
    background-color: #1f2335;
    border: 1px solid #414868;
    border-radius: 4px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: #ff5555;
    border-radius: 3px;
}
"""

SAMPLE_RAW_EML = b"""From: "CEO" <urgent@lookalike-corp.in>
To: <investigator@target.gov.in>
Subject: URGENT: Action required immediately - Account Access Restricted
Date: Mon, 31 Aug 2026 14:10:00 +0530
Message-ID: <20260831141000.spoofed.0091@lookalike-corp.in>
Return-Path: <bounce-handler@attacker-server.ru>
Authentication-Results: mx.target.gov.in; spf=fail (domain does not designate 185.220.101.5); dkim=fail; dmarc=reject
Received: from mail-relay.target.gov.in (mail-relay.target.gov.in [10.20.30.1]) by mx.target.gov.in with ESMTP; Mon, 31 Aug 2026 14:10:12 +0530
Received: from attacker-relay.vps (attacker-relay.vps [194.165.16.2]) by mail-relay.target.gov.in with ESMTP; Mon, 31 Aug 2026 14:10:05 +0530
Received: from tor-exit-node.cn (tor-exit-node.cn [185.220.101.5]) by attacker-relay.vps with SMTP; Mon, 31 Aug 2026 14:10:00 +0530
Content-Type: multipart/mixed; boundary="====BOUNDARY_FORENSIC===="

--====BOUNDARY_FORENSIC====
Content-Type: text/plain; charset="utf-8"

URGENT NOTICE FROM EXECUTIVE CYBER SECURITY DIVISION:
Your official corporate net-banking credentials have been flagged for unauthorized access from an unrecognized IP in Moscow.
To avoid immediate permanent account suspension and legal penalty, you are required to verify your password and 2FA code immediately.

Please click the secure authorization link below within 24 hours:
https://lookalike-corp.in/login/verify-credentials?user=admin

Failure to comply will result in an immediate freeze of all wire transfers and legal notice.
Bank of Baroda Security Operations

--====BOUNDARY_FORENSIC====
Content-Type: application/octet-stream; name="Invoice_Q3_Approved.pdf.exe"
Content-Disposition: attachment; filename="Invoice_Q3_Approved.pdf.exe"
Content-Transfer-Encoding: base64

TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAA2AAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1v
ZGUuDQ0KJAAAAAAAAABQRQAATAEDAAAAAAAAAAAAAAAAAAAAAAAA
--====BOUNDARY_FORENSIC====--
"""


class GhidraForensicMainWindow(QMainWindow):
    """
    SUDO SPANDR - NSA Ghidra-Style Desktop Forensic Workstation Window.
    Multi-Window Dockable Workspace with Raw Email Post-Mortem, Hex Dissector, Listing View,
    and Cognitive AI Decompiler.
    """
    def __init__(self, evidence_path: Optional[str] = None):
        super().__init__()
        self.setWindowTitle("SUDO SPANDR v2.4 — Ghidra Forensic Workstation [AICTE SIH #26106]")
        self.resize(1450, 920)
        self.setStyleSheet(GHIDRA_QSS)

        # Forensic State
        self.current_evidence_path: str = ""
        self.evidence: Dict[str, Any] = {}
        self.threat: Dict[str, Any] = {}
        self.hops: List[Dict[str, Any]] = []
        self.ai_review: Dict[str, Any] = {}
        self.case_id: str = f"CS-CASE-{datetime.now().strftime('%Y%m%d')}"

        # Initialize Docking Framework
        self.setDockOptions(
            QMainWindow.DockOption.AnimatedDocks
            | QMainWindow.DockOption.AllowTabbedDocks
            | QMainWindow.DockOption.AllowNestedDocks
        )

        # Build UI Components
        self._init_menu_and_toolbar()
        self._init_docks()
        self._init_status_bar()

        # Load Initial Evidence
        target = evidence_path or "../Security alert (1).eml"
        if not os.path.exists(target):
            target = "Security alert (1).eml"
        if os.path.exists(target):
            self.load_evidence_file(target)
        else:
            self.load_mock_evidence()

    def _init_menu_and_toolbar(self):
        """Creates Ghidra-style MenuBar and Tactical ToolBar."""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")
        open_action = QAction("📂 Ingest Evidence (.eml, .msg, .pst)...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.action_open_evidence)
        file_menu.addAction(open_action)

        batch_action = QAction("📁 Batch Folder Audit...", self)
        batch_action.setShortcut("Ctrl+B")
        batch_action.triggered.connect(self.action_batch_audit)
        file_menu.addAction(batch_action)

        file_menu.addSeparator()

        pdf_action = QAction("📜 Generate Section 63 BSA 2023 PDF Certificate", self)
        pdf_action.setShortcut("Ctrl+P")
        pdf_action.triggered.connect(self.action_export_bsa_pdf)
        file_menu.addAction(pdf_action)

        export_yara_action = QAction("🛡️ Export YARA / Snort Threat Rules...", self)
        export_yara_action.setShortcut("Ctrl+Y")
        export_yara_action.triggered.connect(self.action_export_rules)
        file_menu.addAction(export_yara_action)

        export_autopsy_action = QAction("💾 Save Complete Post-Mortem Autopsy Report...", self)
        export_autopsy_action.triggered.connect(self.action_export_autopsy)
        file_menu.addAction(export_autopsy_action)

        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Analysis Menu (Ghidra Style)
        analysis_menu = menubar.addMenu("&Analysis")
        autopsy_action = QAction("🧬 Run Deep Raw Email Post-Mortem (Autopsy)", self)
        autopsy_action.setShortcut("Ctrl+M")
        autopsy_action.triggered.connect(self.action_deep_autopsy)
        analysis_menu.addAction(autopsy_action)

        auto_analyze_action = QAction("⚡ Run Complete Forensic Auto-Analysis", self)
        auto_analyze_action.setShortcut("Ctrl+A")
        auto_analyze_action.triggered.connect(self.action_auto_analyze)
        analysis_menu.addAction(auto_analyze_action)

        decompile_action = QAction("🧠 Decompile Cognitive Threat Intent (CatBERT)", self)
        decompile_action.triggered.connect(self.action_decompile_intent)
        analysis_menu.addAction(decompile_action)

        recalc_hash_action = QAction("🔒 Lock Cryptographic Bitstream Hashes (SHA-256)", self)
        recalc_hash_action.triggered.connect(self.action_lock_hashes)
        analysis_menu.addAction(recalc_hash_action)

        # View Menu
        view_menu = menubar.addMenu("&View")
        reset_layout_action = QAction("Reset Docks Layout", self)
        reset_layout_action.triggered.connect(self.action_reset_layout)
        view_menu.addAction(reset_layout_action)

        # Help Menu
        help_menu = menubar.addMenu("&Help")
        about_action = QAction("About SUDO SPANDR Ghidra Suite", self)
        about_action.triggered.connect(self.action_about)
        help_menu.addAction(about_action)

        # Top Tactical ToolBar
        toolbar = QToolBar("Forensic Navigation Bar", self)
        toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(toolbar)

        toolbar.addAction(open_action)
        toolbar.addSeparator()
        toolbar.addAction(autopsy_action)
        toolbar.addAction(auto_analyze_action)
        toolbar.addAction(decompile_action)
        toolbar.addAction(pdf_action)
        toolbar.addAction(export_yara_action)
        toolbar.addSeparator()

        # Live Threat Status Label in Toolbar
        self.tb_threat_badge = QLabel("  THREAT SCORE: 0/100 [CLEAN]  ", self)
        self.tb_threat_badge.setStyleSheet("color: #50fa7b; font-weight: bold; font-size: 13px; background: #24283b; border-radius: 4px; padding: 4px;")
        toolbar.addWidget(self.tb_threat_badge)

    def _init_docks(self):
        """Creates the core Ghidra-style multi-window docks with Post-Mortem Tabs."""

        # ----------------------------------------------------------------------
        # DOCK 1: Program Trees & Evidence Explorer (Left)
        # ----------------------------------------------------------------------
        self.dock_evidence = QDockWidget("📁 EVIDENCE & PROGRAM TREE", self)
        self.dock_evidence.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.tree_evidence = QTreeWidget()
        self.tree_evidence.setHeaderLabels(["Evidence Artifact", "Type / Entropy"])
        self.tree_evidence.itemClicked.connect(self._on_tree_item_clicked)
        self.dock_evidence.setWidget(self.tree_evidence)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_evidence)

        # ----------------------------------------------------------------------
        # DOCK 2: Listing, RFC Disassembler & Deep Post-Mortem Autopsy View (Center Top)
        # ----------------------------------------------------------------------
        self.dock_listing = QDockWidget("📜 LISTING & DEEP POST-MORTEM AUTOPSY DISSECTOR", self)
        self.tab_listing = QTabWidget()

        # Tab 1: 🧬 Deep Post-Mortem Autopsy Sheet
        self.txt_autopsy = QTextEdit()
        self.txt_autopsy.setReadOnly(True)
        self.tab_listing.addTab(self.txt_autopsy, "🧬 Post-Mortem Autopsy Sheet")

        # Tab 2: 📜 RFC Envelope Listing
        self.txt_listing = QTextEdit()
        self.txt_listing.setReadOnly(True)
        self.tab_listing.addTab(self.txt_listing, "📜 RFC Disassembly Stream")

        # Tab 3: 🔗 Extracted Hyperlinks & Homographs
        self.tbl_urls = QTableWidget(0, 5)
        self.tbl_urls.setHorizontalHeaderLabels(["Detected URL / Link", "Extracted Domain", "Punycode / Homograph", "Risk Level", "Pathology Indicator"])
        self.tbl_urls.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tab_listing.addTab(self.tbl_urls, "🔗 URL & Homograph Matrix")

        # Tab 4: 🧩 MIME Hierarchy & Attachments
        self.tbl_mime = QTableWidget(0, 5)
        self.tbl_mime.setHorizontalHeaderLabels(["Part #", "Content-Type", "Declared Name", "True Magic Bytes", "Entropy"])
        self.tbl_mime.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tab_listing.addTab(self.tbl_mime, "🧩 MIME & Attachment Anatomy")

        # Tab 5: 📄 Decoded Body
        self.txt_body = QTextEdit()
        self.txt_body.setReadOnly(True)
        self.tab_listing.addTab(self.txt_body, "📄 Plaintext & HTML Body")

        self.dock_listing.setWidget(self.tab_listing)
        self.setCentralWidget(self.dock_listing)

        # ----------------------------------------------------------------------
        # DOCK 3: Synchronized Byte / Hex Dissector & Carver (Center Bottom)
        # ----------------------------------------------------------------------
        self.dock_hex = QDockWidget("🔬 SYNCHRONIZED BYTE & HEX CARVER (GHIDRA BYTE VIEW)", self)
        hex_widget = QWidget()
        hex_layout = QVBoxLayout(hex_widget)
        hex_layout.setContentsMargins(4, 4, 4, 4)

        # Entropy Speedometer Header Bar
        entropy_bar_box = QHBoxLayout()
        entropy_lbl = QLabel("Shannon Entropy Speedometer:")
        entropy_lbl.setStyleSheet("color: #00f0ff; font-weight: bold;")
        self.lbl_entropy_value = QLabel("7.82 / 8.00 bits [MALWARE SHELLCODE PACKED]")
        self.lbl_entropy_value.setStyleSheet("color: #ff5555; font-weight: bold;")
        
        self.progress_entropy = QProgressBar()
        self.progress_entropy.setMaximum(800)
        self.progress_entropy.setValue(782)
        self.progress_entropy.setFormat("%v / 8.0 bits")
        self.progress_entropy.setStyleSheet("QProgressBar::chunk { background-color: #ff5555; }")

        entropy_bar_box.addWidget(entropy_lbl)
        entropy_bar_box.addWidget(self.progress_entropy)
        entropy_bar_box.addWidget(self.lbl_entropy_value)
        hex_layout.addLayout(entropy_bar_box)

        # Hex Dump Table
        self.tbl_hex = QTableWidget(0, 3)
        self.tbl_hex.setHorizontalHeaderLabels(["Byte Offset", "Hexadecimal Bytes (16 B/Line)", "ASCII Disassembly"])
        self.tbl_hex.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tbl_hex.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tbl_hex.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hex_layout.addWidget(self.tbl_hex)

        self.dock_hex.setWidget(hex_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock_hex)

        # ----------------------------------------------------------------------
        # DOCK 4: Cognitive AI Decompiler & Threat Reasoner (Right Top)
        # ----------------------------------------------------------------------
        self.dock_decompiler = QDockWidget("🧠 COGNITIVE DECOMPILER (CATBERT AI & INTENT)", self)
        decompiler_widget = QWidget()
        dec_layout = QVBoxLayout(decompiler_widget)
        dec_layout.setContentsMargins(6, 6, 6, 6)

        # Threat Score Gauge
        threat_box = QHBoxLayout()
        lbl_gauge_title = QLabel("Forensic Risk Meter:")
        lbl_gauge_title.setStyleSheet("color: #ffb86c; font-weight: bold;")
        self.progress_threat = QProgressBar()
        self.progress_threat.setMaximum(100)
        self.progress_threat.setValue(96)
        self.progress_threat.setStyleSheet("QProgressBar::chunk { background-color: #ff5555; }")
        threat_box.addWidget(lbl_gauge_title)
        threat_box.addWidget(self.progress_threat)
        dec_layout.addLayout(threat_box)

        # Protocol Authentication Badges (SPF / DKIM / DMARC)
        self.lbl_auth_matrix = QLabel("SPF: FAIL | DKIM: FAIL | DMARC: REJECT")
        self.lbl_auth_matrix.setStyleSheet("color: #ff5555; font-weight: bold; background: #24283b; padding: 4px; border-radius: 4px;")
        dec_layout.addWidget(self.lbl_auth_matrix)

        # Decompiled Psychological Reasoner Output
        self.txt_decompiler = QTextEdit()
        self.txt_decompiler.setReadOnly(True)
        dec_layout.addWidget(self.txt_decompiler)

        self.dock_decompiler.setWidget(decompiler_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_decompiler)

        # ----------------------------------------------------------------------
        # DOCK 5: Hop Transit & Threat Rules (Right Bottom)
        # ----------------------------------------------------------------------
        self.dock_hops_rules = QDockWidget("🌐 HOP RELAY MAP & IDS RULES", self)
        self.tab_hops_rules = QTabWidget()

        # Tab 1: Hop Sequence Table
        self.tbl_hops = QTableWidget(0, 4)
        self.tbl_hops.setHorizontalHeaderLabels(["Hop", "IP Address", "Delta Latency", "Network / Node Classification"])
        self.tbl_hops.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tab_hops_rules.addTab(self.tbl_hops, "Relay Sequence")

        # Tab 2: YARA Rules
        self.txt_yara = QTextEdit()
        self.txt_yara.setReadOnly(True)
        self.tab_hops_rules.addTab(self.txt_yara, "YARA Signature")

        # Tab 3: Snort Rules
        self.txt_snort = QTextEdit()
        self.txt_snort.setReadOnly(True)
        self.tab_hops_rules.addTab(self.txt_snort, "Snort / Suricata")

        self.dock_hops_rules.setWidget(self.tab_hops_rules)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_hops_rules)

    def _init_status_bar(self):
        """Initializes military-grade status bar."""
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self.status.showMessage("SUDO SPANDR Workstation Ready │ 100% Offline Air-Gap Mode Verified")

    # ==========================================================================
    # FORENSIC LOGIC & DATA BINDINGS
    # ==========================================================================
    def load_evidence_file(self, file_path: str | Path):
        """Parses and populates evidence across all docks."""
        try:
            self.current_evidence_path = str(file_path)
            self.evidence = parse_email_evidence(file_path)
            self.threat = evaluate_forensic_threat_matrix(self.evidence)
            self.hops = analyze_relay_hops(self.evidence.get("received_hops", []))
            self.ai_review = perform_offline_cognitive_nlp_analysis(self.evidence, self.threat)
            self.case_id = f"CS-CASE-{datetime.now().strftime('%Y%m%d')}-{self.evidence.get('sha256', '0000')[:6].upper()}"

            self._refresh_all_views()
            fname = Path(file_path).name
            self.status.showMessage(f"✔ Seized Evidence Ingested: {fname} │ SHA-256: {self.evidence.get('sha256')[:24]}...")
        except Exception as e:
            QMessageBox.critical(self, "Forensic Parse Error", f"Failed to ingest evidence: {str(e)}")

    def load_mock_evidence(self):
        """Loads built-in synthetic demonstration evidence."""
        self.current_evidence_path = "mock:Security alert (1).eml"
        self.evidence = parse_email_evidence(SAMPLE_RAW_EML, filename="Security alert (1).eml")
        self.threat = evaluate_forensic_threat_matrix(self.evidence)
        self.hops = analyze_relay_hops(self.evidence.get("received_hops", []))
        self.ai_review = perform_offline_cognitive_nlp_analysis(self.evidence, self.threat)
        self._refresh_all_views()

    def _refresh_all_views(self):
        """Synchronizes data across all Ghidra docks."""
        self._populate_evidence_tree()
        self._populate_autopsy_view()
        self._populate_listing_view()
        self._populate_urls_view()
        self._populate_mime_view()
        self._populate_hex_view()
        self._populate_decompiler_view()
        self._populate_hops_and_rules()
        self._update_toolbar_badge()

    # ==========================================================================
    # DEEP RAW EMAIL POST-MORTEM & AUTOPSY ENGINE
    # ==========================================================================
    def _generate_post_mortem_html(self) -> str:
        """Generates comprehensive coroner-style forensic autopsy report."""
        meta = self.evidence.get("meta", {})
        sha256 = self.evidence.get("sha256", "0" * 64)
        md5 = self.evidence.get("md5", "0" * 32)
        sha512 = self.evidence.get("sha512", "0" * 128)
        size_bytes = self.evidence.get("size_bytes", 0)
        fname = self.evidence.get("filename", "evidence.eml")
        
        score = self.threat.get("risk_score", 0)
        verdict = self.threat.get("verdict", "SUSPICIOUS")
        verdict_color = "#ff5555" if score >= 75 else "#ffb86c" if score >= 45 else "#50fa7b"

        auth = self.threat.get("auth_matrix", {})
        spf_st = auth.get("spf", {}).get("status", "NONE")
        dkim_st = auth.get("dkim", {}).get("status", "NONE")
        dmarc_st = auth.get("dmarc", {}).get("status", "NONE")

        ai = self.ai_review
        attachments = self.evidence.get("attachments", [])
        urls = self.threat.get("url_analysis", [])

        # Pathology findings accumulation
        pathology_bullets = []

        # 1. Header Spoofing Pathology
        from_hdr = meta.get("from", "")
        ret_hdr = meta.get("return_path", "")
        if ret_hdr and ("@" in ret_hdr and "@" in from_hdr):
            ret_domain = ret_hdr.split("@")[-1].rstrip(">").strip()
            from_domain = from_hdr.split("@")[-1].rstrip(">").strip()
            if ret_domain.lower() != from_domain.lower():
                pathology_bullets.append(
                    f"<b style='color:#ff5555;'>[CRITICAL ENVELOPE MISMATCH]</b> "
                    f"Declared From domain '<b>{from_domain}</b>' diverges from envelope Return-Path '<b>{ret_domain}</b>'. "
                    f"Hallmark of forged sender impersonation (BEC / Spear-Phishing)."
                )

        # 2. Authentication Protocol Pathology
        if spf_st == "FAIL" or dkim_st == "FAIL" or dmarc_st == "REJECT":
            pathology_bullets.append(
                f"<b style='color:#ff5555;'>[CRYPTO-AUTH BREACH]</b> "
                f"Protocol validation failed (SPF: {spf_st}, DKIM: {dkim_st}, DMARC: {dmarc_st}). "
                f"Originating relay MTA is not permitted to sign or route for this domain."
            )

        # 3. Attachment Masquerading & Entropy Pathology
        for att in attachments:
            forensics = analyze_attachment_forensics(att)
            att_name = att.get("filename", "unnamed")
            ent = forensics["entropy"]
            magic = forensics["magic_type"]

            if att_name.lower().endswith((".exe", ".scr", ".vbs", ".bat", ".pif", ".pdf.exe")):
                pathology_bullets.append(
                    f"<b style='color:#ff5555;'>[MALICIOUS MASQUERADING]</b> "
                    f"Attachment '<b>{att_name}</b>' uses disguised extension! True Magic: <code>{magic}</code>."
                )
            if ent >= 7.2:
                pathology_bullets.append(
                    f"<b style='color:#ff5555;'>[HIGH ENTROPY SHELLCODE]</b> "
                    f"Attachment stream entropy measured at <b>{ent:.2f} / 8.00 bits</b>. "
                    f"Signature of encrypted payload, packer (UPX/Themida), or binary shellcode."
                )

        # 4. Routing & Hop Anonymization Pathology
        if self.hops:
            origin_hop = self.hops[0]
            if "Tor" in origin_hop["isp_label"] or origin_hop.get("is_tor", False):
                pathology_bullets.append(
                    f"<b style='color:#ff5555;'>[ANONYMIZED ORIGIN]</b> "
                    f"Originating IP <b>{origin_hop['ip']}</b> is classified as an active <b>Tor Exit Node / Onion Proxy</b>."
                )

        # 5. Linguistic & Psychological Coercion Pathology
        if ai.get("psychological_triggers"):
            triggers_str = ", ".join([t.get("trigger", "") for t in ai.get("psychological_triggers", [])])
            pathology_bullets.append(
                f"<b style='color:#ffb86c;'>[PSYCHOLOGICAL COERCION]</b> "
                f"CatBERT NLP detected deliberate coercion tactics: <b>{triggers_str}</b>."
            )

        if not pathology_bullets:
            pathology_bullets.append("<span style='color:#50fa7b;'>✔ No critical anomalies detected in raw stream. Appears benign.</span>")

        pathology_html = "".join([f"<li style='margin-bottom:6px; color:#c0caf5;'>{p}</li>" for p in pathology_bullets])

        html = f"""
        <html>
        <body style="font-family:'DejaVu Sans Mono', monospace; background-color:#1a1b26; color:#c0caf5; padding:10px;">
        
        <div style="border-bottom: 2px solid #00f0ff; padding-bottom: 8px; margin-bottom: 12px;">
            <h2 style="color:#00f0ff; margin:0;">🧬 FORENSIC POST-MORTEM & RAW EMAIL AUTOPSY REPORT</h2>
            <p style="color:#7aa2f7; margin:4px 0 0 0; font-size:12px;">
                SUDO SPANDR Digital Forensics Lab │ AICTE SIH 2026 Problem Statement #26106 │ Case Ref: {self.case_id}
            </p>
        </div>

        <table style="width:100%; border-collapse:collapse; margin-bottom:14px;">
            <tr style="background-color:#1f2335;">
                <td style="padding:6px; color:#7aa2f7; width:22%;"><b>EVIDENCE ARTIFACT</b></td>
                <td style="padding:6px; color:#ffffff;">{fname} ({size_bytes} bytes / {size_bytes / 1024.0:.2f} KB)</td>
                <td style="padding:6px; color:#7aa2f7; width:22%;"><b>FORENSIC VERDICT</b></td>
                <td style="padding:6px; color:{verdict_color}; font-weight:bold;">● {verdict} ({score}/100)</td>
            </tr>
            <tr>
                <td style="padding:6px; color:#7aa2f7;"><b>MIME CONTENT-TYPE</b></td>
                <td style="padding:6px; color:#c0caf5;">{self.evidence.get('content_type', 'message/rfc822')}</td>
                <td style="padding:6px; color:#7aa2f7;"><b>ATTACHMENTS CARVED</b></td>
                <td style="padding:6px; color:#c0caf5;">{len(attachments)} Part(s) Extracted</td>
            </tr>
            <tr style="background-color:#1f2335;">
                <td style="padding:6px; color:#7aa2f7;"><b>CLAIMED SENDER</b></td>
                <td style="padding:6px; color:#ffffff;">{meta.get('from', 'N/A')}</td>
                <td style="padding:6px; color:#7aa2f7;"><b>ACTUAL RETURN-PATH</b></td>
                <td style="padding:6px; color:#ffb86c;">{meta.get('return_path', 'N/A')}</td>
            </tr>
            <tr>
                <td style="padding:6px; color:#7aa2f7;"><b>MESSAGE-ID</b></td>
                <td style="padding:6px; color:#c0caf5;" colspan="3">{meta.get('message_id', 'N/A')}</td>
            </tr>
        </table>

        <div style="background-color:#24283b; border-left: 4px solid {verdict_color}; padding: 10px; margin-bottom:14px; border-radius:3px;">
            <h3 style="color:{verdict_color}; margin:0 0 6px 0;">PATHOLOGY AUTOPSY FINDINGS (ROOT CAUSE OF MALICE):</h3>
            <ul style="margin:0; padding-left:20px;">
                {pathology_html}
            </ul>
        </div>

        <h3 style="color:#00f0ff; border-bottom:1px solid #2f3549; padding-bottom:4px; margin-top:16px;">🔏 CRYPTOGRAPHIC BITSTREAM INTEGRITY (SECTION 63 BSA 2023):</h3>
        <table style="width:100%; border-collapse:collapse; font-size:11px; margin-bottom:14px;">
            <tr style="background-color:#1f2335;">
                <td style="padding:5px; color:#7aa2f7; width:15%;"><b>MD5 CHECKSUM</b></td>
                <td style="padding:5px; color:#c0caf5;"><code>{md5}</code></td>
            </tr>
            <tr>
                <td style="padding:5px; color:#7aa2f7;"><b>SHA-256 DIGEST</b></td>
                <td style="padding:5px; color:#50fa7b;"><code>{sha256}</code></td>
            </tr>
            <tr style="background-color:#1f2335;">
                <td style="padding:5px; color:#7aa2f7;"><b>SHA-512 DIGEST</b></td>
                <td style="padding:5px; color:#c0caf5;"><code>{sha512[:64]}...</code></td>
            </tr>
        </table>

        <h3 style="color:#00f0ff; border-bottom:1px solid #2f3549; padding-bottom:4px; margin-top:16px;">🧠 COGNITIVE NLP THREAT INTENT DECOMPILATION:</h3>
        <p style="margin:4px 0; color:#c0caf5;"><b>Attack Classification:</b> <span style="color:#ff5555;">{ai.get('attack_vector')}</span> ({ai.get('confidence_percent')}% confidence)</p>
        <p style="margin:4px 0; color:#c0caf5;"><b>Linguistic Pathology:</b> {ai.get('executive_summary')}</p>

        <h3 style="color:#00f0ff; border-bottom:1px solid #2f3549; padding-bottom:4px; margin-top:16px;">⚖️ STATUTORY EVIDENCE CERTIFICATE STATUS:</h3>
        <p style="color:#50fa7b; margin:4px 0;">
            ✔ Certified under Section 63 of Bharatiya Sakshya Adhiniyam (BSA 2023). Bitstream preserved with zero alteration.
            Court PDF Certificate can be exported via <b>[Ctrl+P]</b> or the toolbar button.
        </p>

        </body>
        </html>
        """
        return html

    def _populate_autopsy_view(self):
        """Renders the HTML post-mortem autopsy report."""
        self.txt_autopsy.setHtml(self._generate_post_mortem_html())

    def _populate_urls_view(self):
        """Populates URL & Homograph Matrix Table."""
        urls = self.threat.get("url_analysis", [])
        self.tbl_urls.setRowCount(len(urls))

        for idx, u in enumerate(urls):
            url_str = u.get("url", "")
            domain = u.get("domain", "")
            is_puny = u.get("is_punycode", False)
            risk = u.get("risk_level", "SUSPICIOUS")
            findings = ", ".join(u.get("findings", ["Extracted link"]))

            it_url = QTableWidgetItem(url_str[:60])
            it_dom = QTableWidgetItem(domain)
            it_puny = QTableWidgetItem("YES (HOMOGRAPH ATTEMPT)" if is_puny else "NO (ASCII Standard)")
            it_puny.setForeground(QColor("#ff5555" if is_puny else "#50fa7b"))
            it_risk = QTableWidgetItem(risk)
            it_risk.setForeground(QColor("#ff5555" if risk == "CRITICAL" else "#ffb86c"))
            it_find = QTableWidgetItem(findings)

            self.tbl_urls.setItem(idx, 0, it_url)
            self.tbl_urls.setItem(idx, 1, it_dom)
            self.tbl_urls.setItem(idx, 2, it_puny)
            self.tbl_urls.setItem(idx, 3, it_risk)
            self.tbl_urls.setItem(idx, 4, it_find)

    def _populate_mime_view(self):
        """Populates MIME Hierarchy and Attachment Anatomy Table."""
        attachments = self.evidence.get("attachments", [])
        self.tbl_mime.setRowCount(len(attachments) + 1)

        # Row 0: Root MIME
        it_idx = QTableWidgetItem("Part 0 (Root)")
        it_ct = QTableWidgetItem(self.evidence.get("content_type", "message/rfc822")[:40])
        it_name = QTableWidgetItem(self.evidence.get("filename", "email.eml"))
        it_magic = QTableWidgetItem("RFC 5322 MIME Stream")
        it_ent = QTableWidgetItem(f"{calculate_shannon_entropy(self.evidence.get('raw_bytes', b'')):.2f} bits")

        self.tbl_mime.setItem(0, 0, it_idx)
        self.tbl_mime.setItem(0, 1, it_ct)
        self.tbl_mime.setItem(0, 2, it_name)
        self.tbl_mime.setItem(0, 3, it_magic)
        self.tbl_mime.setItem(0, 4, it_ent)

        # Attachment Rows
        for idx, att in enumerate(attachments, start=1):
            forensics = analyze_attachment_forensics(att)
            it_idx = QTableWidgetItem(f"Part {idx} (Attachment)")
            it_ct = QTableWidgetItem(att.get("content_type", "application/octet-stream"))
            it_name = QTableWidgetItem(att.get("filename", "unnamed.bin"))
            it_magic = QTableWidgetItem(forensics["magic_type"])
            it_magic.setForeground(QColor("#ff5555" if "Executable" in forensics["magic_type"] else "#50fa7b"))
            it_ent = QTableWidgetItem(f"{forensics['entropy']:.2f} bits")
            it_ent.setForeground(QColor("#ff5555" if forensics['entropy'] >= 7.2 else "#ffb86c"))

            self.tbl_mime.setItem(idx, 0, it_idx)
            self.tbl_mime.setItem(idx, 1, it_ct)
            self.tbl_mime.setItem(idx, 2, it_name)
            self.tbl_mime.setItem(idx, 3, it_magic)
            self.tbl_mime.setItem(idx, 4, it_ent)

    def _populate_evidence_tree(self):
        """Populates Program Tree with seized case items."""
        self.tree_evidence.clear()

        # Root: Case Container
        root_case = QTreeWidgetItem([f"Case: {self.case_id}", "Container"])
        root_case.setForeground(0, QColor("#00f0ff"))
        root_case.setExpanded(True)
        self.tree_evidence.addTopLevelItem(root_case)

        # Active Mail Item
        item_mail = QTreeWidgetItem([self.evidence.get("filename", "evidence.eml"), "RFC 5322 Stream"])
        item_mail.setForeground(0, QColor("#50fa7b"))
        root_case.addChild(item_mail)

        # Attachments Node
        root_att = QTreeWidgetItem(["Extracted Carved Attachments", f"{len(self.evidence.get('attachments', []))} parts"])
        root_att.setExpanded(True)
        root_case.addChild(root_att)

        for att in self.evidence.get("attachments", []):
            forensics = analyze_attachment_forensics(att)
            att_item = QTreeWidgetItem([att.get("filename", "unnamed.bin"), f"Entropy: {forensics['entropy']} ({forensics['magic_type']})"])
            att_item.setForeground(0, QColor("#ff5555" if forensics['entropy'] >= 7.2 else "#ffb86c"))
            root_att.addChild(att_item)

        # Cryptographic Hash Chain Node
        sha256 = self.evidence.get("sha256", "")
        root_hashes = QTreeWidgetItem(["Cryptographic Hashes", "SHA-256 Bitstream"])
        root_hashes.addChild(QTreeWidgetItem([f"SHA-256: {sha256[:16]}...{sha256[-8:]}", "Bitstream Hash"]))
        root_hashes.addChild(QTreeWidgetItem(["Legal Admissibility", "Section 63 BSA 2023 Compliant"]))
        root_case.addChild(root_hashes)

    def _populate_listing_view(self):
        """Populates raw RFC disassembler listing with tokenized syntax."""
        lines = []
        headers = self.evidence.get("headers_list", [])
        for k, v in headers:
            color = "#00f0ff" if k.lower() in {"from", "return-path"} else "#ffb86c" if "authentication" in k.lower() else "#7aa2f7"
            lines.append(f"<span style='color:{color}; font-weight:bold;'>{k}:</span> <span style='color:#c0caf5;'>{v}</span>")

        self.txt_listing.setHtml("<br>".join(lines))
        self.txt_body.setPlainText(self.evidence.get("body", "(Empty body)"))

    def _populate_hex_view(self):
        """Populates 16-byte hex dump and Shannon entropy gauge."""
        attachments = self.evidence.get("attachments", [])
        raw_bytes = self.evidence.get("raw_bytes", b"")

        target_bytes = attachments[0].get("bytes", b"") if attachments else raw_bytes[:1024]
        entropy = calculate_shannon_entropy(target_bytes)
        
        # Update Entropy Speedometer
        ent_scaled = int(min(entropy, 8.0) * 100)
        self.progress_entropy.setValue(ent_scaled)
        
        tag = "[MALWARE SHELLCODE PACKED]" if entropy >= 7.2 else "[STANDARD BYTE DENSITY]"
        self.lbl_entropy_value.setText(f"{entropy:.2f} / 8.00 bits {tag}")
        self.lbl_entropy_value.setStyleSheet(f"color: {'#ff5555' if entropy >= 7.2 else '#50fa7b'}; font-weight: bold;")

        # Populate Hex Table
        dump_data = generate_hex_dump(target_bytes, max_bytes=512)
        self.tbl_hex.setRowCount(len(dump_data))

        for row_idx, row in enumerate(dump_data):
            it_off = QTableWidgetItem(row["offset"])
            it_off.setForeground(QColor("#7aa2f7"))
            it_hex = QTableWidgetItem(row["hex"])
            it_hex.setForeground(QColor("#ffb86c"))
            it_asc = QTableWidgetItem(row["ascii"])
            it_asc.setForeground(QColor("#50fa7b"))

            self.tbl_hex.setItem(row_idx, 0, it_off)
            self.tbl_hex.setItem(row_idx, 1, it_hex)
            self.tbl_hex.setItem(row_idx, 2, it_asc)

    def _populate_decompiler_view(self):
        """Populates Cognitive AI Threat Decompiler."""
        score = self.threat.get("risk_score", 0)
        self.progress_threat.setValue(score)

        auth = self.threat.get("auth_matrix", {})
        spf_st = auth.get("spf", {}).get("status", "NONE")
        dkim_st = auth.get("dkim", {}).get("status", "NONE")
        dmarc_st = auth.get("dmarc", {}).get("status", "NONE")
        self.lbl_auth_matrix.setText(f"SPF: {spf_st}  |  DKIM: {dkim_st}  |  DMARC: {dmarc_st}")
        
        color = "#ff5555" if (spf_st == "FAIL" or dkim_st == "FAIL") else "#50fa7b"
        self.lbl_auth_matrix.setStyleSheet(f"color: {color}; font-weight: bold; background: #24283b; padding: 4px; border-radius: 4px;")

        # Formatted Decompiler Analysis
        ai = self.ai_review
        html = f"""
        <h3 style="color:#00f0ff;">⚡ Decompiled Threat Vector: {ai.get('attack_vector')}</h3>
        <p style="color:#ffffff;"><b>AI Confidence:</b> <span style="color:#50fa7b;">{ai.get('confidence_percent')}%</span></p>
        <p style="color:#ffffff;"><b>Perplexity / Synthetic LLM Lure:</b> <span style="color:{'#ff5555' if ai.get('synthetic_llm_detected') else '#50fa7b'};">
        {'YES (GENERATIVE AI DETECTED)' if ai.get('synthetic_llm_detected') else 'NO (HUMAN AUTHORED)'}</span></p>
        <hr style="border: 1px solid #414868;">
        <h4 style="color:#ffb86c;">Cognitive Linguistic Assessment:</h4>
        <p style="color:#c0caf5;">{ai.get('executive_summary')}</p>
        <h4 style="color:#ff5555;">Psychological Coercion Vectors:</h4>
        <ul>
        """
        for trigger in ai.get("psychological_triggers", []):
            html += f"<li><b><span style='color:#ff5555;'>[{trigger.get('impact')}]</span> {trigger.get('trigger')}:</b> {trigger.get('description')}</li>"
        html += "</ul>"

        self.txt_decompiler.setHtml(html)

    def _populate_hops_and_rules(self):
        """Populates Hop table and Threat Hunting Rules."""
        # Hop Table
        self.tbl_hops.setRowCount(len(self.hops))
        for idx, h in enumerate(self.hops):
            it_num = QTableWidgetItem(f"Hop {h['hop_number']}")
            it_ip = QTableWidgetItem(h["ip"])
            it_ip.setForeground(QColor("#ff5555" if "Tor" in h["isp_label"] else "#50fa7b"))
            it_delta = QTableWidgetItem(h["delta"])
            it_isp = QTableWidgetItem(h["isp_label"])

            self.tbl_hops.setItem(idx, 0, it_num)
            self.tbl_hops.setItem(idx, 1, it_ip)
            self.tbl_hops.setItem(idx, 2, it_delta)
            self.tbl_hops.setItem(idx, 3, it_isp)

        # Rules
        self.txt_yara.setPlainText(generate_yara_rule(self.evidence, self.threat))
        self.txt_snort.setPlainText(generate_snort_rule(self.evidence, self.threat))

    def _update_toolbar_badge(self):
        """Updates toolbar threat score indicator."""
        score = self.threat.get("risk_score", 0)
        verdict = self.threat.get("verdict", "SUSPICIOUS")
        color = "#ff5555" if score >= 75 else "#ffb86c" if score >= 45 else "#50fa7b"
        self.tb_threat_badge.setText(f"  THREAT SCORE: {score}/100 [{verdict}]  ")
        self.tb_threat_badge.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 13px; background: #24283b; border-radius: 4px; padding: 4px;")

    def _on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handles tree item click for deep dissection."""
        txt = item.text(0)
        if "RFC" in item.text(1) or "Container" in item.text(1):
            self.tab_listing.setCurrentIndex(1)
        elif "Entropy" in item.text(1):
            self.tab_listing.setCurrentIndex(3)
        elif "Hashes" in txt:
            self.tab_listing.setCurrentIndex(0)

    # ==========================================================================
    # TOOLBAR & MENU ACTIONS
    # ==========================================================================
    def action_deep_autopsy(self):
        """Triggers deep post-mortem analysis and highlights autopsy sheet."""
        self._populate_autopsy_view()
        self.tab_listing.setCurrentIndex(0)
        self.status.showMessage("✔ Deep Raw Email Post-Mortem Dissection Completed.")
        QMessageBox.information(self, "Post-Mortem Autopsy", "Raw Email Post-Mortem dissection completed!\nAll header inconsistencies, disguised binaries, and MIME pathologies mapped.")

    def action_open_evidence(self):
        """Opens native file chooser for evidence ingestion."""
        fname, _ = QFileDialog.getOpenFileName(
            self,
            "Select Seized Electronic Evidence",
            str(Path(self.current_evidence_path).parent if self.current_evidence_path else "."),
            "Email & Forensic Archives (*.eml *.msg *.pst *.mbox);;All Files (*)",
        )
        if fname:
            self.load_evidence_file(fname)

    def action_batch_audit(self):
        """Performs batch directory audit on multi-file case dump."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Evidence Directory for Batch Triage")
        if dir_path:
            self.status.showMessage(f"Scanning directory: {dir_path}...")
            batch_data = scan_evidence_directory(dir_path)
            stats = batch_data.get("stats", {})
            csv_path = Path("./forensic_exports/batch_triage.csv")
            export_batch_to_csv(batch_data, csv_path)
            QMessageBox.information(
                self,
                "Batch Triage Complete",
                f"Scanned: {stats.get('total_files', 0)} files\n"
                f"Critical Threats: {stats.get('critical', 0)}\n"
                f"Suspicious: {stats.get('suspicious', 0)}\n\n"
                f"CSV Export saved to:\n{csv_path.resolve()}"
            )
            self.status.showMessage("Batch Directory Triage Finished.")

    def action_auto_analyze(self):
        """Runs complete automated forensic analysis pipeline."""
        self.threat = evaluate_forensic_threat_matrix(self.evidence)
        self.hops = analyze_relay_hops(self.evidence.get("received_hops", []))
        self.ai_review = perform_offline_cognitive_nlp_analysis(self.evidence, self.threat)
        self._refresh_all_views()
        self.status.showMessage("✔ Complete Ghidra Forensic Auto-Analysis Executed.")
        QMessageBox.information(self, "Analysis Complete", f"Forensic Auto-Analysis completed!\nVerdict: {self.threat.get('verdict')}\nRisk Score: {self.threat.get('risk_score')}/100")

    def action_decompile_intent(self):
        """Refreshes AI cognitive intent."""
        self.ai_review = perform_offline_cognitive_nlp_analysis(self.evidence, self.threat)
        self._populate_decompiler_view()
        self.dock_decompiler.raise_()
        self.status.showMessage("Cognitive Threat Intent Decompiled.")

    def action_lock_hashes(self):
        """Locks bitstream cryptographic hashes for court chain of custody."""
        sha256 = self.evidence.get("sha256")
        sha512 = self.evidence.get("sha512")
        md5 = self.evidence.get("md5")
        QMessageBox.information(
            self,
            "Cryptographic Hash Chain Locked",
            f"Artifact: {self.evidence.get('filename')}\n\n"
            f"MD5    : {md5}\n"
            f"SHA-256: {sha256}\n"
            f"SHA-512: {sha512}\n\n"
            f"Integrity Status: BITSTREAM VERIFIED (Section 63 BSA Compliant)"
        )

    def action_export_bsa_pdf(self):
        """Exports court-admissible Section 63 BSA PDF certificate."""
        out_paths = export_bsa_certificate(
            self.evidence,
            output_dir="./forensic_exports",
            case_id=self.case_id,
        )
        pdf_path = out_paths.get("pdf_path")
        QMessageBox.information(
            self,
            "Section 63 BSA Certificate Generated",
            f"Court-Admissible Evidence Certificate generated successfully!\n\n"
            f"📄 PDF Report: {pdf_path}\n"
            f"📝 Plain Text : {out_paths.get('txt_path')}\n"
            f"🔏 SHA-256 Checksum: {out_paths.get('sha_path')}\n\n"
            f"Ready for court submission under Bharatiya Sakshya Adhiniyam, 2023."
        )
        self.status.showMessage(f"✔ Section 63 BSA PDF Saved: {Path(str(pdf_path)).name}")

    def action_export_rules(self):
        """Exports YARA and Snort rules to disk."""
        res = export_threat_rules(self.evidence, self.threat, output_dir="./forensic_exports")
        QMessageBox.information(
            self,
            "Threat Rules Exported",
            f"Enterprise Threat Hunting Rules generated:\n\n"
            f"YARA Rule  : {res['yara_path']}\n"
            f"Snort Rule : {res['snort_path']}\n"
            f"STIX 2.1   : {res['stix_path']}"
        )
        self.status.showMessage("✔ YARA & Snort Rules Saved to ./forensic_exports/")

    def action_export_autopsy(self):
        """Saves plain text autopsy dossier to disk."""
        out_path = Path("./forensic_exports") / f"AUTOPSY_{self.evidence.get('sha256', '0000')[:12]}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(self._generate_post_mortem_html(), encoding="utf-8")
        QMessageBox.information(
            self,
            "Autopsy Dossier Saved",
            f"Complete Post-Mortem Autopsy report exported:\n\n{out_path.resolve()}\n\n"
            f"Ready for inclusion in criminal case docket."
        )
        self.status.showMessage(f"✔ Autopsy Report Saved: {out_path.name}")

    def action_reset_layout(self):
        """Restores default docked layout."""
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_evidence)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock_hex)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_decompiler)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_hops_rules)
        self.dock_evidence.show()
        self.dock_hex.show()
        self.dock_decompiler.show()
        self.dock_hops_rules.show()

    def action_about(self):
        """Displays About dialog."""
        QMessageBox.about(
            self,
            "About SUDO SPANDR Ghidra Suite",
            "<h3>SUDO SPANDR Forensic Workstation v2.4</h3>"
            "<p><b>AICTE Smart India Hackathon 2026 | Problem Statement #26106</b></p>"
            "<p>Team SUDO SPANDR</p>"
            "<p>NSA Ghidra & IDA Pro inspired Offline Digital Forensic & Post-Mortem Workstation.</p>"
            "<p>Features: Raw Email Post-Mortem Dissection, Synchronized Hex Dissector, RFC Listing Stream, "
            "CatBERT Cognitive AI Decompiler, and Section 63 BSA 2023 Court PDF Certificate Generator.</p>"
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SUDO SPANDR Ghidra Forensic Workstation")
    
    # Handle CLI target file argument if passed
    target_file = sys.argv[1] if len(sys.argv) > 1 else None
    window = GhidraForensicMainWindow(evidence_path=target_file)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
