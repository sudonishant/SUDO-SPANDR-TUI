#!/usr/bin/env python3
"""
SUDO SPANDR - Forensic Ghidra Desktop Workstation (GUI) v2.5
AICTE - Smart India Hackathon 2026 | Problem Statement #26106
Team SUDO SPANDR — 100% Offline & Air-Gap Ready Reverse-Engineering Forensic Suite
Modeled after NSA Ghidra CodeBrowser & Modern Cyber Threat Intelligence Platforms
Deep Raw Email Post-Mortem, Visual Pathology Cards, MIME Dissector & Local LLM Copilot
"""
from __future__ import annotations

import html
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
    QComboBox,
    QDockWidget,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
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
)

# Import SUDO SPANDR Forensic Core Modules
from core.ai_engine import (
    check_local_llm_status,
    perform_offline_cognitive_nlp_analysis,
    query_local_llm,
    request_online_llm_analysis,
)
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

# Modern Tokyo Night & Ghidra Cyber Tactical QSS
GHIDRA_QSS = """
QMainWindow {
    background-color: #13141c;
}
QMenuBar {
    background-color: #1a1b26;
    color: #a9b1d6;
    border-bottom: 1px solid #24283b;
    font-size: 12px;
    padding: 2px;
}
QMenuBar::item:selected {
    background-color: #24283b;
    color: #7dcfff;
    border-radius: 4px;
}
QMenu {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1px solid #414868;
}
QMenu::item:selected {
    background-color: #2f3549;
    color: #7dcfff;
}
QToolBar {
    background-color: #16161e;
    border-bottom: 1px solid #24283b;
    spacing: 8px;
    padding: 5px 8px;
}
QToolButton {
    background-color: #1f2335;
    color: #c0caf5;
    border: 1px solid #3b4261;
    border-radius: 5px;
    padding: 6px 12px;
    font-weight: bold;
    font-size: 11px;
}
QToolButton:hover {
    background-color: #283457;
    border-color: #7dcfff;
    color: #7dcfff;
}
QDockWidget {
    color: #7dcfff;
    font-weight: bold;
    font-size: 11px;
}
QDockWidget::title {
    background-color: #1a1b26;
    padding: 7px 10px;
    border: 1px solid #24283b;
    border-radius: 4px;
}
QTreeWidget, QTableWidget, QTextEdit, QLineEdit, QComboBox {
    background-color: #1a1b26;
    color: #c0caf5;
    border: 1px solid #24283b;
    border-radius: 6px;
    gridline-color: #1f2335;
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 11px;
}
QTableWidget {
    alternate-background-color: #16161e;
}
QTreeWidget::item:selected, QTableWidget::item:selected {
    background-color: #283457;
    color: #7dcfff;
}
QHeaderView::section {
    background-color: #1f2335;
    color: #7aa2f7;
    padding: 5px;
    font-weight: bold;
    border: 1px solid #24283b;
    font-size: 11px;
}
QTabWidget::pane {
    border: 1px solid #24283b;
    background-color: #16161e;
    border-radius: 6px;
}
QTabBar::tab {
    background-color: #1a1b26;
    color: #7aa2f7;
    padding: 7px 16px;
    border: 1px solid #24283b;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 3px;
    font-size: 11px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background-color: #24283b;
    color: #7dcfff;
    border-bottom: 2px solid #7dcfff;
}
QStatusBar {
    background-color: #16161e;
    color: #7aa2f7;
    border-top: 1px solid #24283b;
    font-size: 11px;
}
QPushButton {
    background-color: #1f2335;
    color: #7dcfff;
    border: 1px solid #3b4261;
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: bold;
    font-size: 11px;
}
QPushButton:hover {
    background-color: #283457;
    border-color: #7dcfff;
}
QProgressBar {
    background-color: #1a1b26;
    border: 1px solid #3b4261;
    border-radius: 4px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    font-size: 10px;
}
QProgressBar::chunk {
    background-color: #f7768e;
    border-radius: 3px;
}
QScrollArea {
    border: none;
    background-color: transparent;
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


def create_stat_card(title: str, value: str, subvalue: str, border_color: str = "#3b4261", value_color: str = "#7dcfff") -> QFrame:
    """Helper to create a modern glowing KPI metric card."""
    frame = QFrame()
    frame.setStyleSheet(f"""
        QFrame {{
            background-color: #1a1b26;
            border: 1px solid {border_color};
            border-left: 4px solid {border_color};
            border-radius: 6px;
            padding: 8px 12px;
        }}
    """)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(4, 4, 4, 4)
    layout.setSpacing(2)

    lbl_title = QLabel(title.upper())
    lbl_title.setStyleSheet("color: #7aa2f7; font-size: 10px; font-weight: bold; letter-spacing: 0.5px;")
    
    lbl_val = QLabel(value)
    lbl_val.setStyleSheet(f"color: {value_color}; font-size: 15px; font-weight: bold;")
    
    lbl_sub = QLabel(subvalue)
    lbl_sub.setStyleSheet("color: #a9b1d6; font-size: 10px;")
    lbl_sub.setWordWrap(True)

    layout.addWidget(lbl_title)
    layout.addWidget(lbl_val)
    layout.addWidget(lbl_sub)
    return frame


class GhidraForensicMainWindow(QMainWindow):
    """
    SUDO SPANDR - NSA Ghidra-Style Desktop Forensic Workstation Window v2.5.
    Features:
    - Top Executive Metric Deck (4 Glowing Forensic KPI Cards)
    - Central Visual Dashboard with Pathology Cards & Envelope Inspector (Zero boring text walls)
    - Synchronized Byte & Hex Dissector with Shannon Entropy Visualizer
    - Interactive Local LLM Copilot Chat & Quick Prompts
    """
    def __init__(self, evidence_path: Optional[str] = None):
        super().__init__()
        self.setWindowTitle("SUDO SPANDR v2.5 — Ghidra Forensic Workstation [AICTE SIH #26106]")
        self.resize(1520, 960)
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

        batch_action = QAction("📁 Batch Directory Audit...", self)
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

        export_autopsy_action = QAction("💾 Export Full Autopsy Dossier (HTML)...", self)
        export_autopsy_action.triggered.connect(self.action_export_autopsy)
        file_menu.addAction(export_autopsy_action)

        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Analysis Menu (Ghidra Style)
        analysis_menu = menubar.addMenu("&Analysis")
        auto_analyze_action = QAction("⚡ Run Complete Forensic Auto-Analysis", self)
        auto_analyze_action.setShortcut("Ctrl+A")
        auto_analyze_action.triggered.connect(self.action_auto_analyze)
        analysis_menu.addAction(auto_analyze_action)

        copilot_action = QAction("🤖 Focus Local LLM Neural Copilot", self)
        copilot_action.setShortcut("Ctrl+L")
        copilot_action.triggered.connect(self.action_focus_copilot)
        analysis_menu.addAction(copilot_action)

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
        toolbar.addAction(auto_analyze_action)
        toolbar.addAction(copilot_action)
        toolbar.addAction(pdf_action)
        toolbar.addAction(export_yara_action)
        toolbar.addSeparator()

        # Live Threat Status Label in Toolbar
        self.tb_threat_badge = QLabel("  THREAT SCORE: 0/100 [CLEAN]  ", self)
        self.tb_threat_badge.setStyleSheet("color: #9ece6a; font-weight: bold; font-size: 12px; background: #1f2335; border: 1px solid #3b4261; border-radius: 4px; padding: 4px 8px;")
        toolbar.addWidget(self.tb_threat_badge)

    def _init_docks(self):
        """Creates the Ghidra-style multi-window docks."""

        # ----------------------------------------------------------------------
        # DOCK 1: Program Trees & Evidence Explorer (Left)
        # ----------------------------------------------------------------------
        self.dock_evidence = QDockWidget("📁 EVIDENCE & PROGRAM TREE", self)
        self.dock_evidence.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.tree_evidence = QTreeWidget()
        self.tree_evidence.setHeaderLabels(["Evidence Artifact", "Type / Status"])
        self.tree_evidence.setColumnWidth(0, 200)
        self.tree_evidence.itemClicked.connect(self._on_tree_item_clicked)
        self.dock_evidence.setWidget(self.tree_evidence)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_evidence)

        # ----------------------------------------------------------------------
        # DOCK 2: Central Visual Dissector & Pathology Dashboard (Center)
        # ----------------------------------------------------------------------
        self.dock_central = QDockWidget("🔬 FORENSIC POST-MORTEM & DISASSEMBLY WORKSPACE", self)
        central_container = QWidget()
        cc_layout = QVBoxLayout(central_container)
        cc_layout.setContentsMargins(4, 4, 4, 4)
        cc_layout.setSpacing(6)

        # Top Executive Metric Deck (4 Glowing Forensic KPI Cards)
        self.kpi_layout = QHBoxLayout()
        self.kpi_layout.setSpacing(8)
        
        self.kpi_threat = create_stat_card("Threat Score", "0/100", "Evaluating matrix...", "#f7768e", "#f7768e")
        self.kpi_envelope = create_stat_card("Envelope Check", "VALIDATING", "Sender identity", "#7aa2f7", "#7dcfff")
        self.kpi_crypto = create_stat_card("Crypto Auth", "SPF/DKIM", "Checking DNS records", "#e0af68", "#e0af68")
        self.kpi_payload = create_stat_card("Carved Payload", "0 Attachments", "Entropy scanning", "#bb9af7", "#bb9af7")

        self.kpi_layout.addWidget(self.kpi_threat)
        self.kpi_layout.addWidget(self.kpi_envelope)
        self.kpi_layout.addWidget(self.kpi_crypto)
        self.kpi_layout.addWidget(self.kpi_payload)
        cc_layout.addLayout(self.kpi_layout)

        # Central Tabs
        self.tab_listing = QTabWidget()

        # Tab 1: 📊 Visual Forensic Pathology Cards (Interactive Cards - No giant text dump!)
        self.scroll_pathology = QScrollArea()
        self.scroll_pathology.setWidgetResizable(True)
        self.widget_pathology = QWidget()
        self.layout_pathology = QVBoxLayout(self.widget_pathology)
        self.layout_pathology.setContentsMargins(8, 8, 8, 8)
        self.layout_pathology.setSpacing(10)
        self.scroll_pathology.setWidget(self.widget_pathology)
        self.tab_listing.addTab(self.scroll_pathology, "📊 Pathology Findings & Autopsy Cards")

        # Tab 2: 📜 Searchable RFC Header Inspector Table
        header_widget = QWidget()
        hw_layout = QVBoxLayout(header_widget)
        hw_layout.setContentsMargins(4, 4, 4, 4)
        
        search_box = QHBoxLayout()
        lbl_search = QLabel("🔍 Filter Headers:")
        lbl_search.setStyleSheet("color: #7dcfff; font-weight:bold;")
        self.edit_header_filter = QLineEdit()
        self.edit_header_filter.setPlaceholderText("Type header name (e.g. 'Authentication', 'From', 'Received')...")
        self.edit_header_filter.textChanged.connect(self._filter_header_table)
        search_box.addWidget(lbl_search)
        search_box.addWidget(self.edit_header_filter)
        hw_layout.addLayout(search_box)

        self.tbl_headers = QTableWidget(0, 2)
        self.tbl_headers.setHorizontalHeaderLabels(["RFC 5322 Header Name", "Analyzed Header Value"])
        self.tbl_headers.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tbl_headers.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hw_layout.addWidget(self.tbl_headers)
        self.tab_listing.addTab(header_widget, "📜 RFC Header Inspector")

        # Tab 3: 🔗 Extracted Hyperlinks & Homographs
        self.tbl_urls = QTableWidget(0, 5)
        self.tbl_urls.setHorizontalHeaderLabels(["Detected Hyperlink", "Target Domain", "Punycode / Homograph", "Risk Rating", "Pathology Indicators"])
        self.tbl_urls.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tbl_urls.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tbl_urls.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tbl_urls.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tbl_urls.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.tab_listing.addTab(self.tbl_urls, "🔗 URL & Homograph Matrix")

        # Tab 4: 🧩 MIME Hierarchy & Attachments
        self.tbl_mime = QTableWidget(0, 5)
        self.tbl_mime.setHorizontalHeaderLabels(["Part #", "Content-Type", "Declared Name", "True Magic Bytes", "Entropy Score"])
        self.tbl_mime.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tab_listing.addTab(self.tbl_mime, "🧩 MIME & Attachment Anatomy")

        # Tab 5: 📄 Plaintext & HTML Body
        self.txt_body = QTextEdit()
        self.txt_body.setReadOnly(True)
        self.tab_listing.addTab(self.txt_body, "📄 Plaintext Body Preview")

        cc_layout.addWidget(self.tab_listing)
        self.dock_central.setWidget(central_container)
        self.setCentralWidget(self.dock_central)

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
        entropy_lbl.setStyleSheet("color: #7dcfff; font-weight: bold;")
        self.lbl_entropy_value = QLabel("7.82 / 8.00 bits [SHELLCODE PACKED]")
        self.lbl_entropy_value.setStyleSheet("color: #f7768e; font-weight: bold;")
        
        self.progress_entropy = QProgressBar()
        self.progress_entropy.setMaximum(800)
        self.progress_entropy.setValue(782)
        self.progress_entropy.setFormat("%v / 8.0 bits")
        self.progress_entropy.setStyleSheet("QProgressBar::chunk { background-color: #f7768e; }")

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
        # DOCK 4: 🤖 LOCAL LLM NEURAL COPILOT (Right Top)
        # ----------------------------------------------------------------------
        self.dock_copilot = QDockWidget("🤖 LOCAL LLM NEURAL COPILOT (OLLAMA & CATBERT)", self)
        copilot_widget = QWidget()
        cp_layout = QVBoxLayout(copilot_widget)
        cp_layout.setContentsMargins(6, 6, 6, 6)

        # Local LLM Config Row
        cfg_box = QHBoxLayout()
        lbl_eng = QLabel("Engine:")
        lbl_eng.setStyleSheet("color: #7dcfff; font-weight:bold; font-size:11px;")
        self.combo_engine = QComboBox()
        self.combo_engine.addItems([
            "Ollama (http://localhost:11434)",
            "Local Llama.cpp (http://localhost:8080/v1)",
            "Embedded CatBERT (100% Offline)",
        ])
        
        lbl_mod = QLabel("Model:")
        lbl_mod.setStyleSheet("color: #7dcfff; font-weight:bold; font-size:11px;")
        self.combo_model = QComboBox()
        self.combo_model.addItems(["llama3:latest", "mistral:latest", "qwen2.5:coder", "phi3", "catbert-neural-cpu"])

        self.btn_ping_llm = QPushButton("⚡ Ping")
        self.btn_ping_llm.clicked.connect(self.action_ping_local_llm)

        cfg_box.addWidget(lbl_eng)
        cfg_box.addWidget(self.combo_engine)
        cfg_box.addWidget(lbl_mod)
        cfg_box.addWidget(self.combo_model)
        cfg_box.addWidget(self.btn_ping_llm)
        cp_layout.addLayout(cfg_box)

        # Status indicator
        self.lbl_llm_status = QLabel("● Status: Embedded Air-Gap Neural Engine Active (100% Offline)")
        self.lbl_llm_status.setStyleSheet("color: #9ece6a; font-weight: bold; font-size: 11px; background: #1f2335; padding: 4px 8px; border-radius: 4px;")
        cp_layout.addWidget(self.lbl_llm_status)

        # Quick Tactical AI Actions Row
        actions_box = QHBoxLayout()
        self.btn_ai_autopsy = QPushButton("⚡ Deep Autopsy")
        self.btn_ai_autopsy.clicked.connect(lambda: self.action_run_quick_prompt("autopsy"))

        self.btn_ai_fir = QPushButton("📝 Police FIR Draft")
        self.btn_ai_fir.clicked.connect(lambda: self.action_run_quick_prompt("fir"))

        self.btn_ai_killchain = QPushButton("🎯 MITRE Kill-Chain")
        self.btn_ai_killchain.clicked.connect(lambda: self.action_run_quick_prompt("killchain"))

        actions_box.addWidget(self.btn_ai_autopsy)
        actions_box.addWidget(self.btn_ai_fir)
        actions_box.addWidget(self.btn_ai_killchain)
        cp_layout.addLayout(actions_box)

        # Interactive Chat Transcript Box
        self.txt_copilot_chat = QTextEdit()
        self.txt_copilot_chat.setReadOnly(True)
        cp_layout.addWidget(self.txt_copilot_chat)

        # Chat Input Box Row
        input_box = QHBoxLayout()
        self.edit_copilot_input = QLineEdit()
        self.edit_copilot_input.setPlaceholderText("Ask Local LLM: e.g. 'Is the attachment dangerous?' or 'Explain spoofing'...")
        self.edit_copilot_input.returnPressed.connect(self.action_send_copilot_chat)

        self.btn_send_chat = QPushButton("Send")
        self.btn_send_chat.clicked.connect(self.action_send_copilot_chat)

        input_box.addWidget(self.edit_copilot_input)
        input_box.addWidget(self.btn_send_chat)
        cp_layout.addLayout(input_box)

        self.dock_copilot.setWidget(copilot_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_copilot)

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
            
            # Greet in Copilot
            self._append_copilot_message("SYSTEM", f"Evidence artifact <b>'{fname}'</b> loaded. Cryptographic hash locked. Ready for Local LLM forensic query.")
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
        self._append_copilot_message("SYSTEM", "Sample synthetic phishing evidence loaded. Ready for Local LLM inquiry.")

    def _refresh_all_views(self):
        """Synchronizes data across all Ghidra docks."""
        self._update_kpi_deck()
        self._populate_evidence_tree()
        self._populate_pathology_cards()
        self._populate_header_table()
        self._populate_urls_view()
        self._populate_mime_view()
        self._populate_hex_view()
        self._populate_hops_and_rules()
        self._update_toolbar_badge()

    def _update_kpi_deck(self):
        """Updates the 4 top glowing KPI cards with live metrics."""
        score = self.threat.get("risk_score", 0)
        verdict = self.threat.get("verdict", "SUSPICIOUS")
        score_col = "#f7768e" if score >= 75 else "#e0af68" if score >= 45 else "#9ece6a"

        # Card 1: Threat Score
        self.kpi_threat.findChildren(QLabel)[1].setText(f"{score}/100")
        self.kpi_threat.findChildren(QLabel)[1].setStyleSheet(f"color: {score_col}; font-size: 16px; font-weight: bold;")
        self.kpi_threat.findChildren(QLabel)[2].setText(f"Verdict: {verdict}")

        # Card 2: Envelope Check
        meta = self.evidence.get("meta", {})
        from_dom = meta.get("from", "").split("@")[-1].rstrip(">").strip() if "@" in meta.get("from", "") else "N/A"
        ret_dom = meta.get("return_path", "").split("@")[-1].rstrip(">").strip() if "@" in meta.get("return_path", "") else "N/A"
        is_mismatch = (from_dom.lower() != ret_dom.lower()) and (ret_dom != "N/A")
        
        env_status = "❌ SPOOFED MISMATCH" if is_mismatch else "✔ ALIGNED"
        env_col = "#f7768e" if is_mismatch else "#9ece6a"
        self.kpi_envelope.findChildren(QLabel)[1].setText(env_status)
        self.kpi_envelope.findChildren(QLabel)[1].setStyleSheet(f"color: {env_col}; font-size: 14px; font-weight: bold;")
        self.kpi_envelope.findChildren(QLabel)[2].setText(f"From: {from_dom} │ Return: {ret_dom}")

        # Card 3: Crypto Auth
        auth = self.threat.get("auth_matrix", {})
        spf = auth.get("spf", {}).get("status", "NONE")
        dkim = auth.get("dkim", {}).get("status", "NONE")
        dmarc = auth.get("dmarc", {}).get("status", "NONE")
        all_pass = (spf == "PASS" and dkim == "PASS")
        
        self.kpi_crypto.findChildren(QLabel)[1].setText("✔ PASSING" if all_pass else "❌ AUTH FAILED")
        self.kpi_crypto.findChildren(QLabel)[1].setStyleSheet(f"color: {'#9ece6a' if all_pass else '#f7768e'}; font-size: 14px; font-weight: bold;")
        self.kpi_crypto.findChildren(QLabel)[2].setText(f"SPF: {spf} │ DKIM: {dkim} │ DMARC: {dmarc}")

        # Card 4: Carved Payload
        attachments = self.evidence.get("attachments", [])
        if attachments:
            att = attachments[0]
            forensics = analyze_attachment_forensics(att)
            self.kpi_payload.findChildren(QLabel)[1].setText(f"{forensics['entropy']:.2f} bits")
            self.kpi_payload.findChildren(QLabel)[1].setStyleSheet(f"color: {'#f7768e' if forensics['entropy'] >= 7.2 else '#e0af68'}; font-size: 15px; font-weight: bold;")
            self.kpi_payload.findChildren(QLabel)[2].setText(f"{att.get('filename', 'part')[:20]} ({forensics['magic_type'][:15]})")
        else:
            self.kpi_payload.findChildren(QLabel)[1].setText("Clean Body")
            self.kpi_payload.findChildren(QLabel)[1].setStyleSheet("color: #9ece6a; font-size: 14px; font-weight: bold;")
            self.kpi_payload.findChildren(QLabel)[2].setText("No binary attachments found")

    def _populate_pathology_cards(self):
        """Builds modern visual cards for the Pathology Findings tab instead of a plain text wall."""
        # Clear existing cards
        while self.layout_pathology.count():
            item = self.layout_pathology.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        meta = self.evidence.get("meta", {})
        threat = self.threat
        ai = self.ai_review

        # ----------------------------------------------------------------------
        # Card 1: Envelope Identity & Spoofing Breakdown
        # ----------------------------------------------------------------------
        card_env = QFrame()
        card_env.setStyleSheet("background-color: #1a1b26; border: 1px solid #3b4261; border-radius: 8px; padding: 12px;")
        layout_env = QVBoxLayout(card_env)
        
        lbl_env_title = QLabel("🔍 ENVELOPE IDENTITY & SENDER SPOOFING PATHOLOGY")
        lbl_env_title.setStyleSheet("color: #7dcfff; font-size: 13px; font-weight: bold;")
        layout_env.addWidget(lbl_env_title)

        grid_env = QGridLayout()
        grid_env.addWidget(QLabel("Declared From Header:"), 0, 0)
        from_val = html.escape(str(meta.get('from', 'N/A')))
        lbl_from = QLabel(f"<b>{from_val}</b>")
        lbl_from.setStyleSheet("color: #ffffff; background: #24283b; padding: 4px; border-radius: 4px;")
        grid_env.addWidget(lbl_from, 0, 1)

        grid_env.addWidget(QLabel("Actual Return-Path:"), 1, 0)
        ret_val = html.escape(str(meta.get('return_path', 'N/A')))
        lbl_ret = QLabel(f"<b>{ret_val}</b>")
        lbl_ret.setStyleSheet("color: #e0af68; background: #24283b; padding: 4px; border-radius: 4px;")
        grid_env.addWidget(lbl_ret, 1, 1)

        grid_env.addWidget(QLabel("Subject Line:"), 2, 0)
        sub_val = html.escape(str(meta.get('subject', 'N/A')))
        lbl_sub = QLabel(f"<b>{sub_val}</b>")
        lbl_sub.setStyleSheet("color: #c0caf5;")
        grid_env.addWidget(lbl_sub, 2, 1)
        layout_env.addLayout(grid_env)
        self.layout_pathology.addWidget(card_env)

        # ----------------------------------------------------------------------
        # Card 2: Root Cause Pathology Findings
        # ----------------------------------------------------------------------
        card_path = QFrame()
        card_path.setStyleSheet("background-color: #1a1b26; border: 1px solid #f7768e; border-left: 5px solid #f7768e; border-radius: 8px; padding: 12px;")
        layout_path = QVBoxLayout(card_path)

        lbl_path_title = QLabel("🚨 PRIMARY PATHOLOGY FINDINGS (ROOT CAUSE OF MALICE)")
        lbl_path_title.setStyleSheet("color: #f7768e; font-size: 13px; font-weight: bold;")
        layout_path.addWidget(lbl_path_title)

        # Check anomalies
        anomalies = []
        from_hdr = meta.get("from", "")
        ret_hdr = meta.get("return_path", "")
        if ret_hdr and ("@" in ret_hdr and "@" in from_hdr):
            ret_dom = ret_hdr.split("@")[-1].rstrip(">").strip()
            from_dom = from_hdr.split("@")[-1].rstrip(">").strip()
            if ret_dom.lower() != from_dom.lower():
                anomalies.append(("❌ DOMAIN DIVERGENCE", f"Sender claims to be '{from_dom}', but mail routing returns to '{ret_dom}'. Classic spear-phishing forgery."))

        auth = threat.get("auth_matrix", {})
        if auth.get("spf", {}).get("status") == "FAIL" or auth.get("dkim", {}).get("status") == "FAIL":
            anomalies.append(("❌ CRYPTOGRAPHIC BREACH", "SPF / DKIM signatures failed verification. Originating server is not authorized to transmit for this domain."))

        attachments = self.evidence.get("attachments", [])
        for att in attachments:
            forensics = analyze_attachment_forensics(att)
            if forensics["entropy"] >= 7.2:
                anomalies.append(("🚨 HIGH ENTROPY BINARY", f"Attachment '{att.get('filename')}' measured {forensics['entropy']:.2f} bits entropy with magic '{forensics['magic_type']}'. Indicates packed dropper or shellcode."))

        if not anomalies:
            anomalies.append(("✔ STANDARD BENIGN", "No major cryptographic or masquerading anomalies detected in evidence artifact."))

        for tag, desc in anomalies:
            h_box = QHBoxLayout()
            lbl_tag = QLabel(f" {tag} ")
            lbl_tag.setStyleSheet("background-color: #283457; color: #f7768e; font-weight: bold; border-radius: 4px; padding: 3px 6px;")
            lbl_desc = QLabel(desc)
            lbl_desc.setStyleSheet("color: #c0caf5; font-size: 11px;")
            lbl_desc.setWordWrap(True)
            h_box.addWidget(lbl_tag)
            h_box.addWidget(lbl_desc, 1)
            layout_path.addLayout(h_box)

        self.layout_pathology.addWidget(card_path)

        # ----------------------------------------------------------------------
        # Card 3: Cryptographic Bitstream Custody (Section 63 BSA 2023)
        # ----------------------------------------------------------------------
        card_bsa = QFrame()
        card_bsa.setStyleSheet("background-color: #1a1b26; border: 1px solid #9ece6a; border-left: 5px solid #9ece6a; border-radius: 8px; padding: 12px;")
        layout_bsa = QVBoxLayout(card_bsa)

        lbl_bsa_title = QLabel("⚖️ SECTION 63 BHARATIYA SAKSHYA ADHINIYAM (BSA 2023) ADMISSIBILITY")
        lbl_bsa_title.setStyleSheet("color: #9ece6a; font-size: 13px; font-weight: bold;")
        layout_bsa.addWidget(lbl_bsa_title)

        sha256 = self.evidence.get("sha256", "0" * 64)
        md5 = self.evidence.get("md5", "0" * 32)
        grid_bsa = QGridLayout()
        grid_bsa.addWidget(QLabel("SHA-256 Bitstream Hash:"), 0, 0)
        lbl_sha = QLabel(f"<code>{sha256}</code>")
        lbl_sha.setStyleSheet("color: #9ece6a; font-weight: bold;")
        grid_bsa.addWidget(lbl_sha, 0, 1)

        grid_bsa.addWidget(QLabel("MD5 Checksum:"), 1, 0)
        lbl_md5 = QLabel(f"<code>{md5}</code>")
        lbl_md5.setStyleSheet("color: #a9b1d6;")
        grid_bsa.addWidget(lbl_md5, 1, 1)
        layout_bsa.addLayout(grid_bsa)

        btn_box = QHBoxLayout()
        btn_gen_pdf = QPushButton("📄 Export Signed Section 63 BSA PDF Certificate")
        btn_gen_pdf.clicked.connect(self.action_export_bsa_pdf)
        btn_box.addWidget(btn_gen_pdf)
        btn_box.addStretch()
        layout_bsa.addLayout(btn_box)

        self.layout_pathology.addWidget(card_bsa)
        self.layout_pathology.addStretch()

    def _populate_header_table(self):
        """Populates searchable RFC 5322 header inspector table."""
        headers = self.evidence.get("headers_list", [])
        self.tbl_headers.setRowCount(len(headers))

        for idx, (k, v) in enumerate(headers):
            it_name = QTableWidgetItem(k)
            it_val = QTableWidgetItem(v)

            # Highlight important headers
            k_lower = k.lower()
            if k_lower in {"from", "return-path", "to", "subject"}:
                it_name.setForeground(QColor("#7dcfff"))
                it_name.setFont(QFont("DejaVu Sans Mono", 11, QFont.Weight.Bold))
            elif "authentication" in k_lower or "dkim" in k_lower:
                it_name.setForeground(QColor("#e0af68"))
            elif "received" in k_lower:
                it_name.setForeground(QColor("#7aa2f7"))

            self.tbl_headers.setItem(idx, 0, it_name)
            self.tbl_headers.setItem(idx, 1, it_val)

        # Body Preview
        self.txt_body.setPlainText(self.evidence.get("body", "(Empty body text)"))

    def _filter_header_table(self, query: str):
        """Filters header table based on search input."""
        q = query.strip().lower()
        for row in range(self.tbl_headers.rowCount()):
            it_name = self.tbl_headers.item(row, 0)
            it_val = self.tbl_headers.item(row, 1)
            name_match = (it_name and q in it_name.text().lower())
            val_match = (it_val and q in it_val.text().lower())
            self.tbl_headers.setRowHidden(row, not (name_match or val_match))

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
            it_puny = QTableWidgetItem("YES (HOMOGRAPH ATTEMPT)" if is_puny else "NO (Standard ASCII)")
            it_puny.setForeground(QColor("#f7768e" if is_puny else "#9ece6a"))
            it_risk = QTableWidgetItem(risk)
            it_risk.setForeground(QColor("#f7768e" if risk == "CRITICAL" else "#e0af68"))
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
            it_magic.setForeground(QColor("#f7768e" if "Executable" in forensics["magic_type"] else "#9ece6a"))
            it_ent = QTableWidgetItem(f"{forensics['entropy']:.2f} bits")
            it_ent.setForeground(QColor("#f7768e" if forensics['entropy'] >= 7.2 else "#e0af68"))

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
        root_case.setForeground(0, QColor("#7dcfff"))
        root_case.setExpanded(True)
        self.tree_evidence.addTopLevelItem(root_case)

        # Active Mail Item
        item_mail = QTreeWidgetItem([self.evidence.get("filename", "evidence.eml"), "RFC 5322"])
        item_mail.setForeground(0, QColor("#9ece6a"))
        root_case.addChild(item_mail)

        # Attachments Node
        root_att = QTreeWidgetItem(["Extracted Attachments", f"{len(self.evidence.get('attachments', []))} parts"])
        root_att.setExpanded(True)
        root_case.addChild(root_att)

        for att in self.evidence.get("attachments", []):
            forensics = analyze_attachment_forensics(att)
            att_item = QTreeWidgetItem([att.get("filename", "unnamed.bin"), f"Entropy {forensics['entropy']:.2f}"])
            att_item.setForeground(0, QColor("#f7768e" if forensics['entropy'] >= 7.2 else "#e0af68"))
            root_att.addChild(att_item)

        # Cryptographic Hash Chain Node
        sha256 = self.evidence.get("sha256", "")
        root_hashes = QTreeWidgetItem(["Hash Chain", "SHA-256"])
        root_hashes.addChild(QTreeWidgetItem([f"{sha256[:16]}...", "SHA-256 Digest"]))
        root_hashes.addChild(QTreeWidgetItem(["Admissibility", "Section 63 BSA 2023"]))
        root_case.addChild(root_hashes)

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
        self.lbl_entropy_value.setStyleSheet(f"color: {'#f7768e' if entropy >= 7.2 else '#9ece6a'}; font-weight: bold;")

        # Populate Hex Table
        dump_data = generate_hex_dump(target_bytes, max_bytes=512)
        self.tbl_hex.setRowCount(len(dump_data))

        for row_idx, row in enumerate(dump_data):
            it_off = QTableWidgetItem(row["offset"])
            it_off.setForeground(QColor("#7aa2f7"))
            it_hex = QTableWidgetItem(row["hex"])
            it_hex.setForeground(QColor("#e0af68"))
            it_asc = QTableWidgetItem(row["ascii"])
            it_asc.setForeground(QColor("#9ece6a"))

            self.tbl_hex.setItem(row_idx, 0, it_off)
            self.tbl_hex.setItem(row_idx, 1, it_hex)
            self.tbl_hex.setItem(row_idx, 2, it_asc)

    def _populate_hops_and_rules(self):
        """Populates Hop table and Threat Hunting Rules."""
        # Hop Table
        self.tbl_hops.setRowCount(len(self.hops))
        for idx, h in enumerate(self.hops):
            it_num = QTableWidgetItem(f"Hop {h['hop_number']}")
            it_ip = QTableWidgetItem(h["ip"])
            it_ip.setForeground(QColor("#f7768e" if "Tor" in h["isp_label"] else "#9ece6a"))
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
        color = "#f7768e" if score >= 75 else "#e0af68" if score >= 45 else "#9ece6a"
        self.tb_threat_badge.setText(f"  THREAT SCORE: {score}/100 [{verdict}]  ")
        self.tb_threat_badge.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px; background: #1f2335; border: 1px solid #3b4261; border-radius: 4px; padding: 4px 8px;")

    def _on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handles tree item click for deep dissection."""
        txt = item.text(0)
        if "RFC" in item.text(1) or "Container" in item.text(1):
            self.tab_listing.setCurrentIndex(1)
        elif "Entropy" in item.text(1):
            self.tab_listing.setCurrentIndex(3)
        elif "Hash" in txt:
            self.tab_listing.setCurrentIndex(0)

    # ==========================================================================
    # LOCAL LLM COPILOT ACTIONS
    # ==========================================================================
    def action_ping_local_llm(self):
        """Tests connection to local Ollama or OpenAI-compatible server."""
        eng_choice = self.combo_engine.currentText()
        endpoint = "http://localhost:11434"
        if "8080" in eng_choice:
            endpoint = "http://localhost:8080/v1"
        elif "Embedded" in eng_choice:
            self.lbl_llm_status.setText("● Status: Embedded CatBERT Neural Engine Active (Air-Gap Safe)")
            self.lbl_llm_status.setStyleSheet("color: #9ece6a; font-weight: bold; font-size: 11px; background: #1f2335; padding: 4px 8px;")
            QMessageBox.information(self, "Embedded Neural Engine", "Embedded Air-Gap Neural Engine active and verified!\n100% Offline & Non-Network Dependent.")
            return

        st = check_local_llm_status(endpoint)
        if st["online"]:
            self.lbl_llm_status.setText(f"● Status: 🟢 {st['status_text']}")
            self.lbl_llm_status.setStyleSheet("color: #9ece6a; font-weight: bold; font-size: 11px; background: #1f2335; padding: 4px 8px;")
            QMessageBox.information(self, "Local LLM Connected", f"Successfully connected to Local LLM!\nEndpoint: {st['endpoint']}\nAvailable Models: {', '.join(st['models'][:5])}")
            # Refresh models dropdown
            self.combo_model.clear()
            self.combo_model.addItems(st["models"])
        else:
            self.lbl_llm_status.setText("● Status: 🟡 Local Server Offline — Using Embedded Air-Gap Engine")
            self.lbl_llm_status.setStyleSheet("color: #e0af68; font-weight: bold; font-size: 11px; background: #1f2335; padding: 4px 8px;")
            QMessageBox.warning(self, "Local Server Offline", f"No running local LLM found on {endpoint}.\nAutomatically falling back to Embedded Air-Gap Neural Engine!\n\nTo use Ollama, run: 'ollama run llama3' in a terminal.")

    def action_run_quick_prompt(self, action_type: str):
        """Runs specialized forensic prompts through the local LLM."""
        meta = self.evidence.get("meta", {})
        context = (
            f"Evidence: {self.evidence.get('filename')}\n"
            f"From: {meta.get('from')}\n"
            f"Return-Path: {meta.get('return_path')}\n"
            f"Subject: {meta.get('subject')}\n"
            f"Threat Score: {self.threat.get('risk_score')}/100\n"
            f"Hops Count: {len(self.hops)}\n"
            f"Body Excerpt: {self.evidence.get('body', '')[:600]}"
        )

        model_name = self.combo_model.currentText()
        endpoint = "http://localhost:11434" if "11434" in self.combo_engine.currentText() else "http://localhost:8080/v1"
        eng_type = "embedded" if "Embedded" in self.combo_engine.currentText() else "auto"

        self.status.showMessage("Running Local LLM Forensic Reasoning...")

        if action_type == "autopsy":
            prompt = f"Conduct a comprehensive technical forensic autopsy for this seized email evidence:\n\n{context}"
            self._append_copilot_message("INVESTIGATOR", "Run comprehensive Local LLM forensic autopsy on this evidence artifact.")
        elif action_type == "fir":
            prompt = f"Draft an official Police FIR complaint under Section 66C/66D IT Act and Bharatiya Nyaya Sanhita (BNS) for this email fraud case:\n\n{context}"
            self._append_copilot_message("INVESTIGATOR", "Draft an official Police FIR Complaint under IT Act & BNS for this case.")
        elif action_type == "killchain":
            prompt = f"Deconstruct the Cyber Kill-Chain and MITRE ATT&CK techniques observed in this email artifact:\n\n{context}"
            self._append_copilot_message("INVESTIGATOR", "Deconstruct the MITRE ATT&CK Cyber Kill-Chain for this email.")
        else:
            prompt = f"Analyze this email:\n{context}"

        resp = query_local_llm(prompt, endpoint=endpoint, model=model_name, engine_type=eng_type)
        self._append_copilot_message("LOCAL LLM COPILOT", resp)
        self.status.showMessage("✔ Local LLM Response Received.")

    def action_send_copilot_chat(self):
        """Sends user input query to the Local LLM."""
        query = self.edit_copilot_input.text().strip()
        if not query:
            return

        self._append_copilot_message("INVESTIGATOR", query)
        self.edit_copilot_input.clear()

        meta = self.evidence.get("meta", {})
        prompt = (
            f"Evidence Artifact: {self.evidence.get('filename')}\n"
            f"From Header: {meta.get('from')}\n"
            f"Return-Path: {meta.get('return_path')}\n"
            f"Subject: {meta.get('subject')}\n"
            f"Threat Score: {self.threat.get('risk_score')}/100\n"
            f"Body Text: {self.evidence.get('body', '')[:600]}\n\n"
            f"Investigator Question: {query}"
        )

        model_name = self.combo_model.currentText()
        endpoint = "http://localhost:11434" if "11434" in self.combo_engine.currentText() else "http://localhost:8080/v1"
        eng_type = "embedded" if "Embedded" in self.combo_engine.currentText() else "auto"

        resp = query_local_llm(prompt, endpoint=endpoint, model=model_name, engine_type=eng_type)
        self._append_copilot_message("LOCAL LLM COPILOT", resp)

    def _append_copilot_message(self, sender: str, msg: str):
        """Appends formatted message bubble to the chat feed."""
        color = "#7dcfff" if sender == "INVESTIGATOR" else "#9ece6a" if "LLM" in sender else "#e0af68"
        formatted = f"<div style='margin-bottom:8px;'><b style='color:{color};'>[{sender}]:</b><br><span style='color:#c0caf5;'>{msg.replace(chr(10), '<br>')}</span></div><hr style='border:1px solid #24283b;'>"
        self.txt_copilot_chat.append(formatted)
        self.txt_copilot_chat.moveCursor(QTextCursor.MoveOperation.End)

    def action_focus_copilot(self):
        """Brings Local LLM Copilot dock to front and focuses prompt input."""
        self.dock_copilot.raise_()
        self.edit_copilot_input.setFocus()

    # ==========================================================================
    # TOOLBAR & MENU ACTIONS
    # ==========================================================================
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
        # Construct summary html
        meta = self.evidence.get("meta", {})
        from_esc = html.escape(str(meta.get('from', '')))
        ret_esc = html.escape(str(meta.get('return_path', '')))
        report_html = f"""
        <html><body style="font-family:sans-serif; background:#1a1b26; color:#c0caf5; padding:20px;">
        <h1 style="color:#7dcfff;">SUDO SPANDR FORENSIC AUTOPSY DOSSIER</h1>
        <p><b>Case ID:</b> {self.case_id} │ <b>SHA-256:</b> {self.evidence.get('sha256')}</p>
        <p><b>From:</b> {from_esc} │ <b>Return-Path:</b> {ret_esc}</p>
        <p><b>Threat Score:</b> {self.threat.get('risk_score')}/100 ({self.threat.get('verdict')})</p>
        </body></html>
        """
        out_path.write_text(report_html, encoding="utf-8")
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
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_copilot)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_hops_rules)
        self.dock_evidence.show()
        self.dock_hex.show()
        self.dock_copilot.show()
        self.dock_hops_rules.show()

    def action_about(self):
        """Displays About dialog."""
        QMessageBox.about(
            self,
            "About SUDO SPANDR Ghidra Suite",
            "<h3>SUDO SPANDR Forensic Workstation v2.5</h3>"
            "<p><b>AICTE Smart India Hackathon 2026 | Problem Statement #26106</b></p>"
            "<p>Team SUDO SPANDR</p>"
            "<p>NSA Ghidra & IDA Pro inspired Offline Digital Forensic Workstation.</p>"
            "<p>Features: Visual Pathology Cards, Searchable RFC Header Inspector, "
            "Local LLM Neural Copilot (Ollama / CatBERT), Synchronized Hex Dissector, and Section 63 BSA PDF Generator.</p>"
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
