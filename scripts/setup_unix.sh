#!/bin/bash
# =============================================================================
# AgentFlow-Launcher — One-click Setup (macOS / Linux)
# =============================================================================
# Usage:
#   bash scripts/setup_unix.sh
# =============================================================================

set -e

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "============================================================"
echo "  AgentFlow-Launcher — Unix Setup (macOS / Linux)"
echo "============================================================"
echo ""

# Check Python
echo "[1/4] Checking Python..."
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "  [ERROR] Python not found. Please install Python 3.10+"
    exit 1
fi
PY_VERSION=$($PYTHON --version 2>&1)
echo "  $PY_VERSION"

# Create virtual environment
echo "[2/4] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "  Virtual environment already exists, skipping."
else
    $PYTHON -m venv venv
    echo "  Virtual environment created."
fi

# Activate and install dependencies
echo "[3/4] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "  Dependencies installed."

# Configure .env
echo "[4/4] Configuring environment..."
if [ -f ".env" ]; then
    echo "  .env file already exists, skipping."
else
    cp .env.example .env
    echo "  .env file created from .env.example."
    echo ""
    echo "  ========================================"
    echo "  IMPORTANT: Edit .env to add your API keys"
    echo "  (Optional: Mock mode works without keys)"
    echo "  ========================================"
fi

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x scripts/*.py 2>/dev/null || true
chmod +x desktop/linux/start_agentflow.sh 2>/dev/null || true
chmod +x desktop/macos/start_agentflow.command 2>/dev/null || true

echo ""
echo "============================================================"
echo "  Setup complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env to add your API keys (optional)"
echo "  2. Run demo:   python scripts/run_demo.py"
echo "  3. Run server:  python scripts/run_server.py"
echo "  4. Open:        http://127.0.0.1:8000/console"
echo "  5. API docs:    http://127.0.0.1:8000/docs"
echo ""
