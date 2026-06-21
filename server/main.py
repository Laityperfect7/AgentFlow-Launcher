"""
AgentFlow-Launcher FastAPI Server
==================================

Provides REST API endpoints for running agents, workflows, and skills.
Also serves the web console and auto-generated API documentation.

Usage:
    python scripts/run_server.py
    uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload

Endpoints:
    GET  /                              Project info
    GET  /health                        Health check
    GET  /api/agents                    List available agents
    POST /api/agents/{name}/run         Run an agent
    GET  /api/workflows                 List available workflows
    POST /api/workflows/{name}/run      Run a workflow
    GET  /api/skills                    List available skills
    POST /api/skills/{name}/run         Run a skill
    GET  /docs                          Swagger UI
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

# Ensure project root is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from agentflow.core.agent import run_agent
from agentflow.core.loader import (
    list_agent_names,
    list_skill_names,
    list_workflow_names,
    load_all_agents,
    load_all_skills,
    load_all_workflows,
)
from agentflow.core.schemas import HealthResponse, RunRequest, RunResponse
from agentflow.core.skill import run_skill
from agentflow.core.workflow import run_workflow
from agentflow.utils.config import is_mock_mode

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AgentFlow-Launcher API",
    description=(
        "A cross-platform toolkit for building, running, and deploying "
        "LLM-powered agents, workflows, and skills."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Static files — serve the web console
# ---------------------------------------------------------------------------

_web_dir = _PROJECT_ROOT / "web"
if _web_dir.exists():
    app.mount("/console", StaticFiles(directory=str(_web_dir), html=True), name="console")


# ---------------------------------------------------------------------------
# Root & Health
# ---------------------------------------------------------------------------

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Return project status and available endpoints."""
    return {
        "project": "AgentFlow-Launcher",
        "version": "1.0.0",
        "description": "LLM Agent / Workflow / Skill build & deploy platform",
        "mock_mode": is_mock_mode(),
        "agents": list_agent_names(),
        "workflows": list_workflow_names(),
        "skills": list_skill_names(),
        "docs": "/docs",
        "console": "/console",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        version="1.0.0",
        mock_mode=is_mock_mode(),
    )


# ---------------------------------------------------------------------------
# Agent endpoints
# ---------------------------------------------------------------------------

@app.get("/api/agents", response_model=List[Dict[str, Any]])
async def list_agents():
    """List all available agents with their descriptions."""
    agents = load_all_agents()
    return [
        {
            "name": a.name,
            "description": a.description,
            "model_provider": a.model_provider,
            "model_name": a.model_name,
        }
        for a in agents.values()
    ]


@app.post("/api/agents/{agent_name}/run", response_model=RunResponse)
async def api_run_agent(agent_name: str, request: RunRequest):
    """Run a specific agent with user input."""
    if agent_name not in list_agent_names():
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' not found. Available: {list_agent_names()}",
        )
    return run_agent(agent_name, request.input, request.params)


# ---------------------------------------------------------------------------
# Workflow endpoints
# ---------------------------------------------------------------------------

@app.get("/api/workflows", response_model=List[Dict[str, Any]])
async def list_workflows():
    """List all available workflows with their descriptions."""
    workflows = load_all_workflows()
    return [
        {
            "name": w.name,
            "description": w.description,
            "steps_count": len(w.steps),
            "model_provider": w.model_provider,
        }
        for w in workflows.values()
    ]


@app.post("/api/workflows/{workflow_name}/run", response_model=RunResponse)
async def api_run_workflow(workflow_name: str, request: RunRequest):
    """Run a specific workflow with user input."""
    if workflow_name not in list_workflow_names():
        raise HTTPException(
            status_code=404,
            detail=f"Workflow '{workflow_name}' not found. Available: {list_workflow_names()}",
        )
    return run_workflow(workflow_name, request.input, request.params)


# ---------------------------------------------------------------------------
# Skill endpoints
# ---------------------------------------------------------------------------

@app.get("/api/skills", response_model=List[Dict[str, Any]])
async def list_skills():
    """List all available skills with their descriptions."""
    skills = load_all_skills()
    return [
        {
            "name": s.name,
            "description": s.description,
            "category": s.category,
            "model_provider": s.model_provider,
        }
        for s in skills.values()
    ]


@app.post("/api/skills/{skill_name}/run", response_model=RunResponse)
async def api_run_skill(skill_name: str, request: RunRequest):
    """Run a specific skill with user input."""
    if skill_name not in list_skill_names():
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found. Available: {list_skill_names()}",
        )
    return run_skill(skill_name, request.input, request.params)


# ---------------------------------------------------------------------------
# Main entry point (for `python server/main.py`)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )
