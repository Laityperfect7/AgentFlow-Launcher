#!/bin/bash
# =============================================================================
# AgentFlow-Launcher — macOS Desktop Launcher
# =============================================================================
# Double-click this .command file to start the AgentFlow-Launcher server
# and open the web console in your default browser.
#
# Prerequisites:
#   1. Run: bash scripts/setup_unix.sh
#   2. Copy .env.example to .env and configure your API keys (optional)
#   3. Make this file executable: chmod +x desktop/macos/start_agentflow.command
# =============================================================================

# Navigate to the project directory (relative to this script's location)
cd "$(dirname "$0")/../.." || exit 1

PROJECT_DIR="$(pwd)"

# Check if venv exists
if [ ! -f "venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found."
    echo "Please run: bash scripts/setup_unix.sh"
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Print banner
echo "============================================================"
echo "  AgentFlow-Launcher"
echo "  Agent / Workflow / Skill 一体化构建与部署平台"
echo "============================================================"
echo ""
echo "  Local API:     http://127.0.0.1:8000"
echo "  Swagger Docs:  http://127.0.0.1:8000/docs"
echo "  Web Console:   http://127.0.0.1:8000/console"
echo "============================================================"
echo ""

# Open browser
sleep 1
open "http://127.0.0.1:8000/console" 2>/dev/null || true

# Start the server
python scripts/run_server.py

# Keep terminal open on error
read -p "Press Enter to exit..."
