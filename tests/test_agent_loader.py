"""
Tests for agent loading and execution.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_list_agent_names():
    """Agent names should be discoverable."""
    from agentflow.core.loader import list_agent_names

    names = list_agent_names()
    assert "demo_research_agent" in names, f"Expected demo_research_agent in {names}"


def test_load_agent():
    """Should load agent definition without error."""
    from agentflow.core.loader import load_agent

    agent = load_agent("demo_research_agent")
    assert agent.name == "demo_research_agent"
    assert agent.model_provider is not None


def test_load_all_agents():
    """Should load all agents."""
    from agentflow.core.loader import load_all_agents

    agents = load_all_agents()
    assert len(agents) >= 1


def test_run_agent_mock():
    """Should run agent with mock provider."""
    from agentflow.core.agent import run_agent

    result = run_agent("demo_research_agent", "AI Development")
    assert result.success, f"Agent failed: {result.error}"
    assert result.type == "agent"
    assert result.output is not None


def test_run_nonexistent_agent():
    """Should return error for missing agent."""
    from agentflow.core.agent import run_agent

    result = run_agent("nonexistent_agent", "test")
    assert not result.success
    assert result.error is not None
