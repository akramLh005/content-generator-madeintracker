#!/bin/bash
# ============================================================
#  MadeInTracker - macOS/Linux Setup Script
#  Requires Python 3.10 or newer
# ============================================================

set -e  # Stop on first error

echo "[1/4] Checking Python version..."
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
  echo "ERROR: Python not found. Please install Python 3.10+ from https://python.org"
  exit 1
fi
$PYTHON --version

echo "[2/4] Creating virtual environment..."
$PYTHON -m venv .venv

echo "[3/4] Activating virtual environment..."
source .venv/bin/activate

echo "[4/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "============================================================"
echo " Setup complete! To start the project:"
echo "   1. Activate the venv:   source .venv/bin/activate"
echo "   2. Copy .env.example to .env and fill in your API keys"
echo "   3. Run:                  python main.py"
echo "============================================================"
