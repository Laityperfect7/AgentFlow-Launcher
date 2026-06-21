"""
YAML configuration loader for agents, workflows, and skills.

Scans the project directories and parses YAML definitions into
Pydantic models for runtime use.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from agentflow.core.schemas import (
    AgentDefinition,
    SkillDefinition,
    WorkflowDefinition,
)

# Resolve project root (parent of agentflow package)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def _read_yaml(path: Path) -> dict:
    """Read a YAML file and return its contents as a dict."""
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


# ---------------------------------------------------------------------------
# Agent loading
# ---------------------------------------------------------------------------

def list_agent_names(agents_dir: Optional[Path] = None) -> List[str]:
    """Return the names of all available agents."""
    if agents_dir is None:
        agents_dir = _PROJECT_ROOT / "agents"
    if not agents_dir.exists():
        return []
    return sorted(
        p.stem for p in agents_dir.glob("*.yaml")
    )


def load_agent(name: str, agents_dir: Optional[Path] = None) -> AgentDefinition:
    """Load a single agent definition by name."""
    if agents_dir is None:
        agents_dir = _PROJECT_ROOT / "agents"
    path = agents_dir / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Agent definition not found: {path}")
    data = _read_yaml(path)
    return AgentDefinition(**data)


def load_all_agents(agents_dir: Optional[Path] = None) -> Dict[str, AgentDefinition]:
    """Load all agent definitions."""
    if agents_dir is None:
        agents_dir = _PROJECT_ROOT / "agents"
    result: Dict[str, AgentDefinition] = {}
    for name in list_agent_names(agents_dir):
        result[name] = load_agent(name, agents_dir)
    return result


# ---------------------------------------------------------------------------
# Workflow loading
# ---------------------------------------------------------------------------

def list_workflow_names(workflows_dir: Optional[Path] = None) -> List[str]:
    """Return the names of all available workflows."""
    if workflows_dir is None:
        workflows_dir = _PROJECT_ROOT / "workflows"
    if not workflows_dir.exists():
        return []
    return sorted(
        p.stem for p in workflows_dir.glob("*.yaml")
    )


def load_workflow(name: str, workflows_dir: Optional[Path] = None) -> WorkflowDefinition:
    """Load a single workflow definition by name."""
    if workflows_dir is None:
        workflows_dir = _PROJECT_ROOT / "workflows"
    path = workflows_dir / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Workflow definition not found: {path}")
    data = _read_yaml(path)
    return WorkflowDefinition(**data)


def load_all_workflows(workflows_dir: Optional[Path] = None) -> Dict[str, WorkflowDefinition]:
    """Load all workflow definitions."""
    if workflows_dir is None:
        workflows_dir = _PROJECT_ROOT / "workflows"
    result: Dict[str, WorkflowDefinition] = {}
    for name in list_workflow_names(workflows_dir):
        result[name] = load_workflow(name, workflows_dir)
    return result


# ---------------------------------------------------------------------------
# Skill loading
# ---------------------------------------------------------------------------

def list_skill_names(skills_dir: Optional[Path] = None) -> List[str]:
    """Return the names of all available skills."""
    if skills_dir is None:
        skills_dir = _PROJECT_ROOT / "skills"
    if not skills_dir.exists():
        return []
    return sorted(
        p.stem for p in skills_dir.glob("*.yaml")
    )


def load_skill(name: str, skills_dir: Optional[Path] = None) -> SkillDefinition:
    """Load a single skill definition by name."""
    if skills_dir is None:
        skills_dir = _PROJECT_ROOT / "skills"
    path = skills_dir / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Skill definition not found: {path}")
    data = _read_yaml(path)
    return SkillDefinition(**data)


def load_all_skills(skills_dir: Optional[Path] = None) -> Dict[str, SkillDefinition]:
    """Load all skill definitions."""
    if skills_dir is None:
        skills_dir = _PROJECT_ROOT / "skills"
    result: Dict[str, SkillDefinition] = {}
    for name in list_skill_names(skills_dir):
        result[name] = load_skill(name, skills_dir)
    return result
