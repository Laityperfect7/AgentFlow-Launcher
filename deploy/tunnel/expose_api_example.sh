#!/bin/bash
# =============================================================================
# AgentFlow-Launcher — Public Tunnel Example (macOS / Linux)
# =============================================================================
# This script shows how to expose the local API server to the public internet
# using different tunnel tools.
#
# Usage:
#   bash deploy/tunnel/expose_api_example.sh [cloudflare|ngrok|localtunnel]
# =============================================================================

METHOD="${1:-cloudflare}"
PORT="${2:-8000}"

echo "============================================"
echo "  AgentFlow-Launcher — Public Tunnel"
echo "============================================"
echo "  Method: $METHOD"
echo "  Local Port: $PORT"
echo "============================================"
echo ""

# Check if server is already running
if ! curl -s "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then
    echo "[INFO] Starting AgentFlow-Launcher server..."
    cd "$(dirname "$0")/../.."
    source venv/bin/activate 2>/dev/null
    python scripts/run_server.py &
    sleep 3
fi

case "$METHOD" in
    cloudflare|cf)
        echo "[INFO] Starting Cloudflare Tunnel..."
        echo "  Public URL will be a *.trycloudflare.com address"
        echo ""
        cloudflared tunnel --url "http://127.0.0.1:$PORT"
        ;;
    ngrok)
        echo "[INFO] Starting Ngrok Tunnel..."
        echo "  Public URL will be a *.ngrok-free.app address"
        echo "  Local inspector: http://127.0.0.1:4040"
        echo ""
        ngrok http "$PORT"
        ;;
    localtunnel|lt)
        echo "[INFO] Starting LocalTunnel..."
        echo "  Public URL will be a *.loca.lt address"
        echo ""
        lt --port "$PORT"
        ;;
    *)
        echo "[ERROR] Unknown method: $METHOD"
        echo "Usage: bash $0 [cloudflare|ngrok|localtunnel] [port]"
        exit 1
        ;;
esac
