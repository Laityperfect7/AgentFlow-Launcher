"""
Agent runner — loads an Agent definition and executes it against a provider.
"""

from __future__ import annotations

from typing import Any, Dict

from agentflow.core.loader import load_agent
from agentflow.core.schemas import AgentDefinition, RunResponse
from agentflow.providers.base import BaseProvider
from agentflow.utils.logging import get_logger

logger = get_logger(__name__)


def _resolve_provider(provider_key: str, model_name: str) -> BaseProvider:
    """Resolve a provider key to a provider instance."""
    from agentflow.providers.mock_provider import MockProvider

    # Map provider keys to classes
    registry: Dict[str, type] = {
        "mock": MockProvider,
    }

    # Try to import real providers if their key is requested
    if provider_key == "openai":
        try:
            from agentflow.providers.openai_provider import OpenAIProvider
            registry["openai"] = OpenAIProvider
        except ImportError:
            logger.warning("OpenAI provider not available, falling back to mock")
    elif provider_key == "deepseek":
        try:
            from agentflow.providers.deepseek_provider import DeepSeekProvider
            registry["deepseek"] = DeepSeekProvider
        except ImportError:
            logger.warning("DeepSeek provider not available, falling back to mock")
    elif provider_key == "qwen":
        try:
            from agentflow.providers.qwen_provider import QwenProvider
            registry["qwen"] = QwenProvider
        except ImportError:
            logger.warning("Qwen provider not available, falling back to mock")
    elif provider_key == "ollama":
        try:
            from agentflow.providers.ollama_provider import OllamaProvider
            registry["ollama"] = OllamaProvider
        except ImportError:
            logger.warning("Ollama provider not available, falling back to mock")

    cls = registry.get(provider_key, MockProvider)
    return cls(model_name=model_name)


def run_agent(
    agent_name: str,
    user_input: str,
    params: Dict[str, Any] | None = None,
    *,
    agents_dir: Any = None,
) -> RunResponse:
    """
    Load an agent by name, resolve its provider, and run it.

    Args:
        agent_name: Name of the agent YAML file (without .yaml).
        user_input: The user's input text.
        params: Optional additional parameters.
        agents_dir: Optional custom directory for agent YAML files.

    Returns:
        RunResponse with the agent output.
    """
    params = params or {}

    try:
        definition: AgentDefinition = load_agent(agent_name, agents_dir)
    except FileNotFoundError as exc:
        return RunResponse(
            success=False,
            type="agent",
            name=agent_name,
            input=user_input,
            output=None,
            error=str(exc),
        )

    provider = _resolve_provider(definition.model_provider, definition.model_name)

    # Build the full prompt
    system = definition.system_prompt
    temperature = params.get("temperature", definition.temperature)
    max_tokens = params.get("max_tokens", definition.max_tokens)

    # Include tool descriptions in the prompt if any
    tools_text = ""
    if definition.tools:
        tools_text = "\n\nAvailable tools:\n" + "\n".join(
            f"- {t.name}: {t.description}" for t in definition.tools
        )

    full_prompt = f"{system}{tools_text}\n\nUser: {user_input}\n\nAssistant:"

    try:
        result = provider.generate(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return RunResponse(
            success=True,
            type="agent",
            name=agent_name,
            input=user_input,
            output=result,
            metadata={
                "model_provider": definition.model_provider,
                "model_name": definition.model_name,
                "tools_count": len(definition.tools),
            },
        )
    except Exception as exc:
        logger.error("Agent run failed: %s", exc)
        return RunResponse(
            success=False,
            type="agent",
            name=agent_name,
            input=user_input,
            output=None,
            error=str(exc),
        )
