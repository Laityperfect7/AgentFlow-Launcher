"""
Abstract base class for LLM providers.

All providers must implement the `generate` method.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseProvider(ABC):
    """
    Abstract provider interface.

    Subclass this to add a new LLM backend. The only required method
    is ``generate``, which takes a prompt string and returns a text
    completion.
    """

    def __init__(self, model_name: str = "default", **kwargs: Any) -> None:
        self.model_name = model_name
        self.kwargs = kwargs

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion for the given prompt.

        Args:
            prompt: The full prompt string.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            The generated text.
        """
        ...

    def health_check(self) -> Dict[str, Any]:
        """Return provider status information."""
        return {
            "provider": self.__class__.__name__,
            "model_name": self.model_name,
            "available": True,
        }
