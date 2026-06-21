"""
Tests for workflow loading and execution.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_list_workflow_names():
    """Workflow names should be discoverable."""
    from agentflow.core.loader import list_workflow_names

    names = list_workflow_names()
    assert "content_pipeline" in names


def test_load_workflow():
    """Should load workflow definition."""
    from agentflow.core.loader import load_workflow

    wf = load_workflow("content_pipeline")
    assert wf.name == "content_pipeline"
    assert len(wf.steps) >= 2


def test_run_workflow_mock():
    """Should run workflow with mock provider."""
    from agentflow.core.workflow import run_workflow

    result = run_workflow("content_pipeline", "Test topic")
    assert result.success, f"Workflow failed: {result.error}"
    assert result.type == "workflow"
    assert result.output is not None
    assert "steps" in result.output


def test_run_nonexistent_workflow():
    """Should return error for missing workflow."""
    from agentflow.core.workflow import run_workflow

    result = run_workflow("nonexistent", "test")
    assert not result.success
