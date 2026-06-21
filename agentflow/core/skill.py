"""
Skill runner — loads a Skill definition and executes it against a provider.
"""

from __future__ import annotations

from typing import Any, Dict

from agentflow.core.loader import load_skill
from agentflow.core.schemas import RunResponse, SkillDefinition
from agentflow.providers.base import BaseProvider
from agentflow.utils.logging import get_logger

logger = get_logger(__name__)


def _resolve_provider(provider_key: str, model_name: str) -> BaseProvider:
    """Resolve a provider key to a provider instance."""
    from agentflow.providers.mock_provider import MockProvider

    registry: Dict[str, type] = {"mock": MockProvider}
    cls = registry.get(provider_key, MockProvider)
    return cls(model_name=model_name)


def run_skill(
    skill_name: str,
    user_input: str,
    params: Dict[str, Any] | None = None,
    *,
    skills_dir: Any = None,
) -> RunResponse:
    """
    Load a skill by name, render its prompt template, and run it.

    Skills are reusable prompt templates with defined input/output schemas.

    Args:
        skill_name: Name of the skill YAML file (without .yaml).
        user_input: The user's input text.
        params: Optional additional parameters.
        skills_dir: Optional custom directory for skill YAML files.

    Returns:
        RunResponse with the skill output.
    """
    params = params or {}

    try:
        definition: SkillDefinition = load_skill(skill_name, skills_dir)
    except FileNotFoundError as exc:
        return RunResponse(
            success=False,
            type="skill",
            name=skill_name,
            input=user_input,
            output=None,
            error=str(exc),
        )

    provider = _resolve_provider(definition.model_provider, definition.model_name)

    # Build template variables
    template_vars: Dict[str, str] = {"input": user_input, **params}

    # Render prompt template
    try:
        rendered = definition.prompt_template.format(**template_vars)
    except KeyError as missing:
        logger.warning("Skill '%s' missing variable: %s", skill_name, missing)
        rendered = definition.prompt_template

    try:
        result = provider.generate(prompt=rendered)
        return RunResponse(
            success=True,
            type="skill",
            name=skill_name,
            input=user_input,
            output=result,
            metadata={
                "category": definition.category,
                "model_provider": definition.model_provider,
                "model_name": definition.model_name,
            },
        )
    except Exception as exc:
        logger.error("Skill run failed: %s", exc)
        return RunResponse(
            success=False,
            type="skill",
            name=skill_name,
            input=user_input,
            output=None,
            error=str(exc),
        )
