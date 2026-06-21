#!/usr/bin/env python3
"""
Release packager — creates a clean zip archive for distribution.

Excludes:
    - .git directory
    - venv / .venv
    - node_modules
    - __pycache__
    - .env (secrets)
    - outputs/ (generated files)
    - dist/ build/ *.egg-info/
    - IDE files (.vscode, .idea)

Usage:
    python scripts/package_release.py
    python scripts/package_release.py --output ../releases/agentflow-v1.0.0.zip
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# Ensure the project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Patterns to exclude from the release archive
EXCLUDE_PATTERNS = [
    ".git",
    ".gitignore",
    "venv",
    ".venv",
    "node_modules",
    "__pycache__",
    ".env",
    "outputs",
    "dist",
    "build",
    "*.egg-info",
    ".vscode",
    ".idea",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
]


def should_exclude(path: Path, root: Path) -> bool:
    """Check if a path should be excluded from the release."""
    rel = path.relative_to(root)
    parts = rel.parts

    for part in parts:
        for pattern in EXCLUDE_PATTERNS:
            if Path(part).match(pattern):
                return True
    return False


def create_release(output_path: Path) -> None:
    """Create a release zip archive."""
    root = PROJECT_ROOT

    output_path.parent.mkdir(parents=True, exist_ok=True)

    file_count = 0
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_dir():
                continue
            if should_exclude(path, root):
                continue

            rel_path = path.relative_to(root)
            zf.write(path, rel_path)
            file_count += 1

    size_mb = output_path.stat().st_size / (1024 * 1024)

    print(f"✓ Release created: {output_path}")
    print(f"  Files included: {file_count}")
    print(f"  Size: {size_mb:.2f} MB")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Package AgentFlow-Launcher for release",
    )
    default_name = f"AgentFlow-Launcher-{datetime.now(timezone.utc).strftime('%Y%m%d')}.zip"
    default_path = PROJECT_ROOT.parent / "releases" / default_name

    parser.add_argument(
        "--output", "-o",
        default=str(default_path),
        help=f"Output zip path (default: {default_path})",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  AgentFlow-Launcher — Release Packager")
    print("=" * 60)
    print(f"  Project root: {PROJECT_ROOT}")
    print(f"  Output: {args.output}")
    print()

    create_release(Path(args.output))


if __name__ == "__main__":
    main()
