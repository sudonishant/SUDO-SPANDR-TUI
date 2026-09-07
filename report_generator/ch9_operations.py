"""Chapter 9: Deployment, Installation & Operational Reference Guide"""

def get_chapter_9_html() -> str:
    return r"""
<h1>9. Deployment, Installation & Operational Reference Guide</h1>

<h2>9.1 Hardware & Operating System Prerequisites</h2>
<p>
<strong>SUDO SPANDR</strong> was engineered to maintain exceptional operational versatility, running efficiently on everything from constrained field laptops and single-board computers (e.g., Raspberry Pi 5) to multi-GPU forensic analysis servers in centralized defense laboratories.
</p>

<table>
    <thead>
        <tr>
            <th>Hardware Component</th>
            <th>Minimum Specification (TUI / Field Mode)</th>
            <th>Recommended Specification (Ghidra GUI & Local LLM)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Processor (CPU)</strong></td>
            <td>Dual-Core x86_64 or ARM64 (1.5 GHz)</td>
            <td>8-Core x86_64 (Intel Core i7/i9, AMD Ryzen 7/9) or Apple M-Series</td>
        </tr>
        <tr>
            <td><strong>Memory (RAM)</strong></td>
            <td>2 GB RAM (Embedded CatBERT Mode)</td>
            <td>16 GB to 32 GB RAM (for 8B/70B Quantized Local LLMs)</td>
        </tr>
        <tr>
            <td><strong>Dedicated GPU</strong></td>
            <td>Not Required (Pure CPU Fallback Engine)</td>
            <td>NVIDIA RTX 3060+ (6GB+ VRAM) or Apple Unified Memory</td>
        </tr>
        <tr>
            <td><strong>Disk Storage</strong></td>
            <td>150 MB for core software and runtime</td>
            <td>10 GB (to accommodate local GGUF/Ollama model weights)</td>
        </tr>
        <tr>
            <td><strong>Operating System</strong></td>
            <td>Kali Linux 2024+, Ubuntu 22.04/24.04 LTS, Debian 12, Arch Linux, Fedora 40, macOS 13+, Windows WSL2</td>
            <td>Kali Linux 2024.x (Active X11 / Wayland Desktop Session)</td>
        </tr>
    </tbody>
</table>

<h2>9.2 Step-by-Step Installation & Environment Setup</h2>

<h3>Step 1: Clone the Official Repository</h3>
<pre>
# Clone the repository from GitHub
git clone https://github.com/sudonishant/SUDO-SPANDR-TUI.git
cd SUDO-SPANDR-TUI
</pre>

<h3>Step 2: Configure Python Isolated Virtual Environment</h3>
<pre>
# Ensure Python 3.10 or higher is installed
python3 --version

# Create and activate an isolated virtual environment
python3 -m venv .venv
source .venv/bin/activate
</pre>

<h3>Step 3: Install Core Dependencies</h3>
<pre>
# Install all required Python libraries
pip install --upgrade pip
pip install -r requirements.txt

# For the Ghidra Desktop GUI and Publication Engine:
pip install PyQt6 weasyprint pypdf rich
</pre>

<h3>Step 4: Optional Local LLM Setup (Ollama)</h3>
<p>
For advanced conversational intelligence, install and start the open-source <strong>Ollama</strong> engine:
</p>
<pre>
# Install Ollama on Linux / macOS
curl -fsSL https://ollama.com/install.sh | sh

# Pull desired sovereign model (e.g., LLaMA-3 8B or Mistral 7B)
ollama pull llama3:latest

# Verify daemon is running locally
curl http://localhost:11434/api/tags
</pre>
<p>
<em>Note: If Ollama is not installed or the system is air-gapped, SUDO SPANDR automatically defaults to its built-in CatBERT-Neural-CPU engine without throwing errors.</em>
</p>

<h2>9.3 Execution & Operational Modes</h2>

<h3>Mode A: Launching the Ghidra Desktop Workstation (GUI)</h3>
<p>
To launch the primary visual reverse-engineering workstation with multi-window docking, glowing KPI cards, and interactive tables:
</p>
<pre>
# Use the automated launcher script (handles X11 display export)
./run_gui.sh

# Or invoke directly with Python, optionally loading a seized case file:
python3 gui_app.py "/path/to/evidence/suspect_email.eml"
</pre>

<h3>Mode B: Launching the Tactical Terminal User Interface (TUI)</h3>
<p>
For lightweight operations over SSH connections or headless terminal consoles:
</p>
<pre>
# Launch the terminal forensic deck
./run_tui.sh

# Or invoke directly with a target file:
python3 app.py "/path/to/evidence/suspect_email.eml"
</pre>

<h3>Mode C: High-Volume Autonomous Batch Directory Triage</h3>
<p>
When executing large-scale incident response involving thousands of seized mailboxes:
</p>
<pre>
# Recursively crawl a directory, triage all .eml/.msg files, and export manifest
python3 app.py --batch "/var/spool/seized_mailboxes/" --workers 8 --output triage_report.json
</pre>

<h2>9.4 Comprehensive Keyboard Shortcuts Reference Table</h2>
<p>
Both interfaces feature rapid keyboard shortcuts designed for high-efficiency forensic examination:
</p>

<table>
    <thead>
        <tr>
            <th>Shortcut Key</th>
            <th>Desktop GUI Workstation Action</th>
            <th>Terminal TUI Forensic Action</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>[Ctrl+O]</code> / <code>[Enter]</code></td>
            <td>Open File Dialog to Ingest Evidence File</td>
            <td>Load Highlighted File from Evidence Browser</td>
        </tr>
        <tr>
            <td><code>[Ctrl+A]</code> / <code>[Space]</code></td>
            <td>Execute 1-Click Complete Auto-Analysis</td>
            <td>Run 1-Click Complete Forensic Auto-Audit</td>
        </tr>
        <tr>
            <td><code>[Ctrl+M]</code></td>
            <td>Switch Focus to Main Post-Mortem Autopsy Dock</td>
            <td>N/A (Tab [1] 4-Panel Deck)</td>
        </tr>
        <tr>
            <td><code>[Ctrl+P]</code> / <code>[E]</code></td>
            <td>Generate Section 63 BSA 2023 PDF Certificate</td>
            <td>Export Signed Section 63 BSA Court PDF</td>
        </tr>
        <tr>
            <td><code>[Ctrl+Y]</code> / <code>[7]</code></td>
            <td>Focus Threat Rules Dock (YARA / Snort)</td>
            <td>Switch to Panel 7 (YARA / Snort Compiler)</td>
        </tr>
        <tr>
            <td><code>[Ctrl+B]</code> / <code>[6]</code></td>
            <td>Open Batch Directory Triage Tool</td>
            <td>Switch to Panel 6 (Batch Queue Manifest)</td>
        </tr>
        <tr>
            <td><code>[Ctrl+F]</code></td>
            <td>Focus Search Bar in RFC Header Inspector Table</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td><code>[Ctrl+L]</code></td>
            <td>Focus Local LLM Copilot Chat Input Bar</td>
            <td>Switch to Panel 3 (CatBERT NLP Intelligence)</td>
        </tr>
        <tr>
            <td><code>[Ctrl+S]</code></td>
            <td>Export Complete Forensic Autopsy Dossier (HTML)</td>
            <td>Save ASCII Autopsy Dossier to Disk</td>
        </tr>
        <tr>
            <td><code>[Ctrl+Q]</code> / <code>[Q]</code></td>
            <td>Safely Terminate Application</td>
            <td>Safely Exit TUI Session</td>
        </tr>
        <tr>
            <td><code>[1] - [8]</code></td>
            <td>N/A</td>
            <td>Direct Panel Switching across all 8 TUI Docks</td>
        </tr>
        <tr>
            <td><code>[↑] / [↓]</code></td>
            <td>Navigate Table Rows & Tree Nodes</td>
            <td>Navigate Evidence File List & Hex Offsets</td>
        </tr>
    </tbody>
</table>

<h2>9.5 Air-Gap Verification & System Hardening</h2>
<p>
To demonstrate compliance with sovereign air-gap mandates during forensic audits, administrators can verify that SUDO SPANDR operates without transmitting network packets. On Linux, execute the tool within an isolated network namespace using the POSIX <code>unshare</code> command:
</p>
<pre>
# Launch SUDO SPANDR with completely disabled network loopback and interfaces
unshare -n python3 gui_app.py "evidence.eml"
</pre>
<p>
The application will execute flawlessly, confirming that 100% of parsing, rendering, entropy calculation, and neural cognitive heuristics function with zero network access.
</p>
"""
