"""
Tests for skill loading and execution.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_list_skill_names():
    """Skill names should be discoverable."""
    from agentflow.core.loader import list_skill_names

    names = list_skill_names()
    assert "text_summarizer" in names
    assert "code_explainer" in names
    assert "prompt_optimizer" in names


def test_load_skill():
    """Should load skill definition."""
    from agentflow.core.loader import load_skill

    skill = load_skill("text_summarizer")
    assert skill.name == "text_summarizer"
    assert skill.prompt_template is not None


def test_run_skill_mock():
    """Should run skill with mock provider."""
    from agentflow.core.skill import run_skill

    result = run_skill("text_summarizer", "This is a test text to summarize.")
    assert result.success, f"Skill failed: {result.error}"
    assert result.type == "skill"


def test_run_all_skills():
    """All skills should be runnable."""
    from agentflow.core.loader import list_skill_names
    from agentflow.core.skill import run_skill

    for name in list_skill_names():
        result = run_skill(name, "test input")
        assert result.success, f"Skill '{name}' failed: {result.error}"
