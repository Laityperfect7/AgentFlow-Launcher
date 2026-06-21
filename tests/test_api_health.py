"""
Tests for the FastAPI server endpoints.

Uses FastAPI's TestClient — no need to start a real server.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_health_endpoint():
    """GET /health should return 200 and correct structure."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"


def test_root_endpoint():
    """GET / should return project info."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "AgentFlow-Launcher"


def test_list_agents():
    """GET /api/agents should list available agents."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.get("/api/agents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_list_workflows():
    """GET /api/workflows should list workflows."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.get("/api/workflows")
    assert response.status_code == 200


def test_list_skills():
    """GET /api/skills should list skills."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.get("/api/skills")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_run_agent_api():
    """POST /api/agents/{name}/run should run an agent."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.post(
        "/api/agents/demo_research_agent/run",
        json={"input": "Test research topic"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["type"] == "agent"


def test_run_workflow_api():
    """POST /api/workflows/{name}/run should run a workflow."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.post(
        "/api/workflows/content_pipeline/run",
        json={"input": "Test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_run_skill_api():
    """POST /api/skills/{name}/run should run a skill."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.post(
        "/api/skills/text_summarizer/run",
        json={"input": "Test text"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_404_for_missing_agent():
    """POST to a nonexistent agent should return 404."""
    from fastapi.testclient import TestClient
    from server.main import app

    client = TestClient(app)
    response = client.post(
        "/api/agents/nonexistent/run",
        json={"input": "test"},
    )
    assert response.status_code == 404
