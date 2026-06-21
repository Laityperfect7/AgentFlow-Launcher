"""
DeepSeek provider adapter.

Uses the DeepSeek API (OpenAI-compatible endpoint).
Requires: pip install openai (DeepSeek API is OpenAI-compatible)
API Key: Set DEEPSEEK_API_KEY in .env

Supported models: deepseek-chat, deepseek-reasoner, etc.
"""

from __future__ import annotations

import os
from typing import Any, Dict

from agentflow.providers.base import BaseProvider
from agentflow.utils.logging import get_logger

logger = get_logger(__name__)


class DeepSeekProvider(BaseProvider):
    """
    Provider for DeepSeek models.

    DeepSeek provides an OpenAI-compatible API endpoint, so we can
    reuse the same client library.

    Environment variables:
        DEEPSEEK_API_KEY: Your DeepSeek API key
        DEEPSEEK_BASE_URL: (Optional) Defaults to https://api.deepseek.com/v1
    """

    BASE_URL = "https://api.deepseek.com/v1"

    def __init__(self, model_name: str = "deepseek-chat", **kwargs: Any) -> None:
        super().__init__(model_name=model_name, **kwargs)
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL", self.BASE_URL)

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion using the DeepSeek API.

        DeepSeek uses an OpenAI-compatible endpoint, making integration simple.
        """
        if not self.api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY is not set. "
                "Get your key at https://platform.deepseek.com/api_keys "
                "and set it in your .env file."
            )

        try:
            from openai import OpenAI  # type: ignore[import-untyped]

            client = OpenAI(api_key=self.api_key, base_url=self.base_url)

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
                "The 'openai' package is required for DeepSeek provider "
                "(DeepSeek uses an OpenAI-compatible API). "
                "Install it with: pip install openai"
            )

    @staticmethod
    def _parse_messages(prompt: str) -> list[Dict[str, str]]:
        """Split prompt into system + user messages if possible."""
        if "User:" in prompt:
            parts = prompt.split("User:", 1)
            return [
                {"role": "system", "content": parts[0].strip()},
                {"role": "user", "content": parts[1].strip() if len(parts) > 1 else ""},
            ]
        return [{"role": "user", "content": prompt}]

    def health_check(self) -> Dict[str, Any]:
        return {
            "provider": "DeepSeekProvider",
            "model_name": self.model_name,
            "api_key_configured": bool(self.api_key),
            "available": bool(self.api_key),
        }
