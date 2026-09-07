#!/usr/bin/env bash
# SUDO SPANDR - Forensic Ghidra Desktop Workstation (GUI) Launcher
set -e

# Resolve directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure X11 display is available
if [ -z "$DISPLAY" ]; then
    export DISPLAY=":0.0"
fi

# Launch Ghidra-Style Forensic GUI
echo "[*] Launching SUDO SPANDR Ghidra Forensic Workstation..."
python3 "$SCRIPT_DIR/gui_app.py" "$@"
