#!/usr/bin/env python3
"""
AgentFlow-Launcher Demo Runner
===============================
Runs one agent, one workflow, and one skill using the mock provider,
saving all results to outputs/demo_result.json.

No API keys required — works fully offline.

Usage:
    python scripts/run_demo.py
    python scripts/run_demo.py --output outputs/my_result.json
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Ensure the project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agentflow.core.agent import run_agent
from agentflow.core.skill import run_skill
from agentflow.core.workflow import run_workflow
from agentflow.utils.config import get_output_dir, is_mock_mode
from agentflow.utils.logging import setup_logging

logger = setup_logging()


def demo_agent() -> Dict[str, Any]:
    """Run the demo research agent."""
    print("\n" + "=" * 60)
    print("  [1/3] Running Agent: demo_research_agent")
    print("=" * 60)

    result = run_agent(
        agent_name="demo_research_agent",
        user_input="Large Language Model Agent Development",
    )
    _print_result(result)
    return result.model_dump()


def demo_workflow() -> Dict[str, Any]:
    """Run the content pipeline workflow."""
    print("\n" + "=" * 60)
    print("  [2/3] Running Workflow: content_pipeline")
    print("=" * 60)

    result = run_workflow(
        workflow_name="content_pipeline",
        user_input="AI Agent Development Best Practices",
    )
    _print_result(result)
    return result.model_dump()


def demo_skill() -> Dict[str, Any]:
    """Run the text summarizer skill."""
    print("\n" + "=" * 60)
    print("  [3/3] Running Skill: text_summarizer")
    print("=" * 60)

    sample_text = (
        "Large Language Models (LLMs) have revolutionized the field of "
        "artificial intelligence by enabling machines to understand and "
        "generate human-like text. These models, trained on vast amounts "
        "of data, can perform a wide range of tasks including translation, "
        "summarization, code generation, and creative writing. The development "
        "of agent-based systems that leverage LLMs has opened new possibilities "
        "for autonomous task completion, workflow automation, and intelligent "
        "assistance across industries."
    )

    result = run_skill(
        skill_name="text_summarizer",
        user_input=sample_text,
    )
    _print_result(result)
    return result.model_dump()


def _print_result(result: Any) -> None:
    """Print a concise summary of a run result."""
    if result.success:
        print(f"  [OK] Success (type={result.type}, name={result.name})")
        output_preview = str(result.output)[:150]
        print(f"  Output preview: {output_preview}...")
    else:
        print(f"  [FAIL] Failed: {result.error}")


def save_results(results: List[Dict[str, Any]], output_path: Path) -> None:
    """Save demo results to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "project": "AgentFlow-Launcher",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mock_mode": is_mock_mode(),
        "results": results,
        "summary": {
            "total": len(results),
            "success": sum(1 for r in results if r.get("success")),
            "failed": sum(1 for r in results if not r.get("success")),
        },
    }

    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    print(f"\n[OK] Results saved to: {output_path}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="AgentFlow-Launcher Demo")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON file path (default: outputs/demo_result.json)",
    )
    args = parser.parse_args()

    output_path = Path(args.output) if args.output else get_output_dir() / "demo_result.json"

    print("=" * 60)
    print("  AgentFlow-Launcher — Demo Runner")
    print("  Mode:", "MOCK (offline)" if is_mock_mode() else "LIVE (API keys detected)")
    print("=" * 60)

    results: List[Dict[str, Any]] = []

    try:
        results.append(demo_agent())
    except Exception as exc:
        print(f"  [FAIL] Agent demo failed: {exc}")
        results.append({"success": False, "type": "agent", "error": str(exc)})

    try:
        results.append(demo_workflow())
    except Exception as exc:
        print(f"  [FAIL] Workflow demo failed: {exc}")
        results.append({"success": False, "type": "workflow", "error": str(exc)})

    try:
        results.append(demo_skill())
    except Exception as exc:
        print(f"  [FAIL] Skill demo failed: {exc}")
        results.append({"success": False, "type": "skill", "error": str(exc)})

    save_results(results, output_path)

    # Summary
    success_count = sum(1 for r in results if r.get("success"))
    print("\n" + "=" * 60)
    print(f"  Demo Complete: {success_count}/{len(results)} successful")
    print("=" * 60)


if __name__ == "__main__":
    main()
