"""
Configuration helpers — load .env and provide typed config access.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

# Try to load .env at import time
try:
    from dotenv import load_dotenv

    _ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"
    if _ENV_FILE.exists():
        load_dotenv(_ENV_FILE)
except ImportError:
    pass


def get_env(key: str, default: str = "") -> str:
    """Get an environment variable with an optional default."""
    return os.getenv(key, default)


def get_project_root() -> Path:
    """Return the absolute path to the project root directory."""
    return Path(__file__).resolve().parent.parent.parent


def get_output_dir() -> Path:
    """Return the outputs directory, creating it if necessary."""
    out = get_project_root() / "outputs"
    out.mkdir(exist_ok=True)
    return out


def is_mock_mode() -> bool:
    """Return True if no real API keys are configured (mock mode)."""
    real_keys = ["OPENAI_API_KEY", "DEEPSEEK_API_KEY", "QWEN_API_KEY"]
    return not any(os.getenv(k) for k in real_keys)
