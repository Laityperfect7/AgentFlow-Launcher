#!/usr/bin/env python3
"""
Project validator — checks that all required files and configurations
are present and correctly structured.

Usage:
    python scripts/validate_project.py
    python scripts/validate_project.py --verbose
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def check(condition: bool, message: str, verbose: bool = False) -> int:
    """Check a condition and return 1 if it fails, 0 otherwise."""
    if condition:
        if verbose:
            print(f"  [OK] {message}")
        return 0
    else:
        print(f"  [FAIL] {message}")
        return 1


def validate(verbose: bool = False) -> int:
    """Run all validation checks. Returns count of failures."""
    root = PROJECT_ROOT
    failures = 0

    print("=" * 60)
    print("  AgentFlow-Launcher — Project Validator")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Root files
    # ------------------------------------------------------------------
    print("\n[1] Root files")
    failures += check((root / "README.md").exists(), "README.md exists", verbose)
    failures += check((root / "LICENSE").exists(), "LICENSE exists", verbose)
    failures += check((root / ".gitignore").exists(), ".gitignore exists", verbose)
    failures += check((root / ".env.example").exists(), ".env.example exists", verbose)
    failures += check((root / "requirements.txt").exists(), "requirements.txt exists", verbose)
    failures += check((root / "pyproject.toml").exists(), "pyproject.toml exists", verbose)

    # ------------------------------------------------------------------
    # .env should NOT be tracked
    # ------------------------------------------------------------------
    print("\n[2] Security checks")
    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text(encoding="utf-8")
        failures += check(".env" in gitignore_content, ".env is in .gitignore", verbose)
    else:
        failures += check(False, ".gitignore not found")

    env_path = root / ".env"
    if env_path.exists():
        print(f"  [WARN] .env file exists. Make sure it is NOT committed to git.")
    else:
        if verbose:
            print(f"  [WARN] .env not found (OK if using mock mode)")

    # ------------------------------------------------------------------
    # Package structure
    # ------------------------------------------------------------------
    print("\n[3] Python package")
    failures += check((root / "agentflow/__init__.py").exists(), "agentflow/__init__.py", verbose)
    failures += check((root / "agentflow/core/__init__.py").exists(), "agentflow/core/", verbose)
    failures += check((root / "agentflow/core/agent.py").exists(), "agentflow/core/agent.py", verbose)
    failures += check((root / "agentflow/core/workflow.py").exists(), "agentflow/core/workflow.py", verbose)
    failures += check((root / "agentflow/core/skill.py").exists(), "agentflow/core/skill.py", verbose)
    failures += check((root / "agentflow/core/loader.py").exists(), "agentflow/core/loader.py", verbose)
    failures += check((root / "agentflow/core/schemas.py").exists(), "agentflow/core/schemas.py", verbose)
    failures += check((root / "agentflow/providers/base.py").exists(), "agentflow/providers/base.py", verbose)
    failures += check((root / "agentflow/providers/mock_provider.py").exists(), "agentflow/providers/mock_provider.py", verbose)

    # ------------------------------------------------------------------
    # Configurations
    # ------------------------------------------------------------------
    print("\n[4] YAML configurations")
    failures += check((root / "agents/demo_research_agent.yaml").exists(), "agents/demo_research_agent.yaml", verbose)
    failures += check((root / "workflows/content_pipeline.yaml").exists(), "workflows/content_pipeline.yaml", verbose)
    failures += check((root / "skills/text_summarizer.yaml").exists(), "skills/text_summarizer.yaml", verbose)
    failures += check((root / "skills/code_explainer.yaml").exists(), "skills/code_explainer.yaml", verbose)
    failures += check((root / "skills/prompt_optimizer.yaml").exists(), "skills/prompt_optimizer.yaml", verbose)

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------
    print("\n[5] API server")
    failures += check((root / "server/__init__.py").exists(), "server/__init__.py", verbose)
    failures += check((root / "server/main.py").exists(), "server/main.py", verbose)

    # ------------------------------------------------------------------
    # Web console
    # ------------------------------------------------------------------
    print("\n[6] Web console")
    failures += check((root / "web/index.html").exists(), "web/index.html", verbose)
    failures += check((root / "web/styles.css").exists(), "web/styles.css", verbose)
    failures += check((root / "web/app.js").exists(), "web/app.js", verbose)

    # ------------------------------------------------------------------
    # Desktop scripts
    # ------------------------------------------------------------------
    print("\n[7] Desktop deployment")
    failures += check((root / "desktop/windows/start_agentflow.bat").exists(), "desktop/windows/start_agentflow.bat", verbose)
    failures += check((root / "desktop/windows/create_shortcut.ps1").exists(), "desktop/windows/create_shortcut.ps1", verbose)
    failures += check((root / "desktop/macos/start_agentflow.command").exists(), "desktop/macos/start_agentflow.command", verbose)
    failures += check((root / "desktop/linux/start_agentflow.sh").exists(), "desktop/linux/start_agentflow.sh", verbose)
    failures += check((root / "desktop/linux/agentflow-launcher.desktop").exists(), "desktop/linux/agentflow-launcher.desktop", verbose)

    # ------------------------------------------------------------------
    # Deploy docs
    # ------------------------------------------------------------------
    print("\n[8] Deploy documentation")
    failures += check((root / "deploy/README.md").exists(), "deploy/README.md", verbose)
    failures += check((root / "deploy/tunnel/cloudflare_tunnel.md").exists(), "deploy/tunnel/cloudflare_tunnel.md", verbose)
    failures += check((root / "deploy/tunnel/ngrok.md").exists(), "deploy/tunnel/ngrok.md", verbose)
    failures += check((root / "deploy/tunnel/localtunnel.md").exists(), "deploy/tunnel/localtunnel.md", verbose)

    # ------------------------------------------------------------------
    # Scripts
    # ------------------------------------------------------------------
    print("\n[9] Utility scripts")
    failures += check((root / "scripts/setup_windows.ps1").exists(), "scripts/setup_windows.ps1", verbose)
    failures += check((root / "scripts/setup_unix.sh").exists(), "scripts/setup_unix.sh", verbose)
    failures += check((root / "scripts/run_server.py").exists(), "scripts/run_server.py", verbose)
    failures += check((root / "scripts/run_demo.py").exists(), "scripts/run_demo.py", verbose)
    failures += check((root / "scripts/validate_project.py").exists(), "scripts/validate_project.py", verbose)
    failures += check((root / "scripts/package_release.py").exists(), "scripts/package_release.py", verbose)

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------
    print("\n[10] Tests")
    failures += check((root / "tests/test_agent_loader.py").exists(), "tests/test_agent_loader.py", verbose)
    failures += check((root / "tests/test_workflow_runner.py").exists(), "tests/test_workflow_runner.py", verbose)
    failures += check((root / "tests/test_skill_runner.py").exists(), "tests/test_skill_runner.py", verbose)
    failures += check((root / "tests/test_api_health.py").exists(), "tests/test_api_health.py", verbose)

    # ------------------------------------------------------------------
    # Docs images directory
    # ------------------------------------------------------------------
    print("\n[11] Documentation images")
    failures += check((root / "docs/images/README.md").exists(), "docs/images/ directory", verbose)

    # ------------------------------------------------------------------
    # Mock provider import test
    # ------------------------------------------------------------------
    print("\n[12] Mock provider import")
    try:
        from agentflow.providers.mock_provider import MockProvider
        provider = MockProvider()
        result = provider.generate("Hello")
        failures += check(len(result) > 0, "MockProvider.generate() works", verbose)
    except Exception as exc:
        failures += check(False, f"MockProvider failed: {exc}", verbose)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    if failures == 0:
        print("  [OK] All checks passed!")
    else:
        print(f"  [FAIL] {failures} check(s) failed.")
    print("=" * 60)

    return failures


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate AgentFlow-Launcher project structure")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show passing checks too")
    args = parser.parse_args()
    sys.exit(validate(verbose=args.verbose))
