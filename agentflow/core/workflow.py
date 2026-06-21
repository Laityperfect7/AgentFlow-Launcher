"""
Workflow runner — executes a sequence of steps defined in a workflow YAML.
"""

from __future__ import annotations

from typing import Any, Dict

from agentflow.core.loader import load_workflow
from agentflow.core.schemas import RunResponse, WorkflowDefinition
from agentflow.providers.base import BaseProvider
from agentflow.utils.logging import get_logger

logger = get_logger(__name__)


def _resolve_provider(provider_key: str, model_name: str) -> BaseProvider:
    """Resolve a provider key to a provider instance."""
    from agentflow.providers.mock_provider import MockProvider

    registry: Dict[str, type] = {"mock": MockProvider}
    cls = registry.get(provider_key, MockProvider)
    return cls(model_name=model_name)


def run_workflow(
    workflow_name: str,
    user_input: str,
    params: Dict[str, Any] | None = None,
    *,
    workflows_dir: Any = None,
) -> RunResponse:
    """
    Load a workflow by name and execute each step in order.

    Each step's prompt template is rendered with variables from the
    initial input and the accumulated outputs of previous steps.

    Args:
        workflow_name: Name of the workflow YAML file (without .yaml).
        user_input: The initial user input.
        params: Optional additional parameters.
        workflows_dir: Optional custom directory for workflow YAML files.

    Returns:
        RunResponse with the collected step outputs.
    """
    params = params or {}

    try:
        definition: WorkflowDefinition = load_workflow(workflow_name, workflows_dir)
    except FileNotFoundError as exc:
        return RunResponse(
            success=False,
            type="workflow",
            name=workflow_name,
            input=user_input,
            output=None,
            error=str(exc),
        )

    provider = _resolve_provider(definition.model_provider, definition.model_name)

    # Accumulated context shared across steps
    context: Dict[str, str] = {"user_input": user_input}
    step_outputs: list[Dict[str, Any]] = []

    for step in definition.steps:
        # Render the prompt template with available context
        try:
            rendered = step.prompt_template.format(**context, **params)
        except KeyError as missing:
            logger.warning("Step '%s' missing variable: %s", step.name, missing)
            rendered = step.prompt_template  # best-effort

        logger.info("Running workflow step: %s", step.name)

        try:
            result = provider.generate(prompt=rendered)
        except Exception as exc:
            step_outputs.append({"step": step.name, "error": str(exc)})
            continue

        # Store output under the step's output_key
        context[step.output_key] = result
        step_outputs.append({
            "step": step.name,
            "output_key": step.output_key,
            "result": result,
        })

    return RunResponse(
        success=True,
        type="workflow",
        name=workflow_name,
        input=user_input,
        output={
            "steps": step_outputs,
            "final_context_keys": list(context.keys()),
        },
        metadata={
            "model_provider": definition.model_provider,
            "model_name": definition.model_name,
            "steps_completed": len(step_outputs),
        },
    )
