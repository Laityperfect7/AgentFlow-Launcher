#!/usr/bin/env python3
"""
AgentFlow-Launcher Server Starter
===================================
Starts the FastAPI server on http://127.0.0.1:8000

Usage:
    python scripts/run_server.py
    python scripts/run_server.py --port 9000
    python scripts/run_server.py --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure the project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agentflow.utils.logging import setup_logging


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AgentFlow-Launcher Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_server.py
  python scripts/run_server.py --port 9000
  python scripts/run_server.py --host 0.0.0.0 --port 8000
        """,
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--log-level", default="info", help="Log level")
    args = parser.parse_args()

    setup_logging()

    print("=" * 60)
    print("  AgentFlow-Launcher Server")
    print("=" * 60)
    print(f"  Host:   http://{args.host}:{args.port}")
    print(f"  Docs:   http://{args.host}:{args.port}/docs")
    print(f"  Console: http://{args.host}:{args.port}/console")
    print("=" * 60)
    print()

    import uvicorn

    uvicorn.run(
        "server.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
    )


if __name__ == "__main__":
    main()
