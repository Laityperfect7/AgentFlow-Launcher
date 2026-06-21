"""
OpenAI provider adapter.

Uses the OpenAI-compatible chat completions API.
Requires: pip install openai
API Key: Set OPENAI_API_KEY in .env

Supported models: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo, etc.
"""

from __future__ import annotations

import os
from typing import Any, Dict

from agentflow.providers.base import BaseProvider
from agentflow.utils.logging import get_logger

logger = get_logger(__name__)


class OpenAIProvider(BaseProvider):
    """
    Provider for OpenAI models (GPT-4o, GPT-4, GPT-3.5, etc.).

    Environment variables:
        OPENAI_API_KEY: Your OpenAI API key
        OPENAI_BASE_URL: (Optional) Custom base URL for proxies
    """

    def __init__(self, model_name: str = "gpt-4o-mini", **kwargs: Any) -> None:
        super().__init__(model_name=model_name, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion using the OpenAI Chat Completions API.

        Note: This implementation requires the 'openai' Python package.
        Install with: pip install openai
        """
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. "
                "Please set it in your .env file or environment variables. "
                "See .env.example for reference."
            )

        try:
            from openai import OpenAI  # type: ignore[import-untyped]

            client = OpenAI(api_key=self.api_key, base_url=self.base_url)

            # Separate system and user messages from the prompt if possible
            messages = self._parse_messages(prompt)

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            content = response.choices[0].message.content
            return content or ""

        except ImportError:
            raise ImportError(
                "The 'openai' package is required for OpenAI provider. "
                "Install it with: pip install openai"
            )

    @staticmethod
    def _parse_messages(prompt: str) -> list[Dict[str, str]]:
        """
        Try to split a combined prompt into system + user messages.

        If the prompt contains 'User:' marker, everything before it
        is treated as the system message.
        """
        if "User:" in prompt:
            parts = prompt.split("User:", 1)
            system = parts[0].strip()
            user = parts[1].strip() if len(parts) > 1 else ""
            return [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
        return [{"role": "user", "content": prompt}]

    def health_check(self) -> Dict[str, Any]:
        return {
            "provider": "OpenAIProvider",
            "model_name": self.model_name,
            "api_key_configured": bool(self.api_key),
            "available": bool(self.api_key),
        }
