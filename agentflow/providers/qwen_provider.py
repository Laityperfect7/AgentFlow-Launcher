"""
Qwen (Tongyi Qianwen / Alibaba Cloud) provider adapter.

Uses the Qwen API via DashScope (OpenAI-compatible endpoint).
Requires: pip install openai
API Key: Set QWEN_API_KEY in .env

Supported models: qwen-turbo, qwen-plus, qwen-max, qwen-max-longcontext, etc.

DashScope documentation: https://help.aliyun.com/document_detail/2712195.html
"""

from __future__ import annotations

import os
from typing import Any, Dict

from agentflow.providers.base import BaseProvider
from agentflow.utils.logging import get_logger

logger = get_logger(__name__)


class QwenProvider(BaseProvider):
    """
    Provider for Qwen (Tongyi Qianwen) models via Alibaba Cloud DashScope.

    Environment variables:
        QWEN_API_KEY: Your DashScope API key
        QWEN_BASE_URL: (Optional) Defaults to DashScope OpenAI-compatible endpoint
    """

    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    def __init__(self, model_name: str = "qwen-plus", **kwargs: Any) -> None:
        super().__init__(model_name=model_name, **kwargs)
        self.api_key = os.getenv("QWEN_API_KEY", "")
        self.base_url = os.getenv("QWEN_BASE_URL", self.BASE_URL)

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion using the Qwen DashScope API.

        The DashScope API is OpenAI-compatible, so we use the same client library.
        """
        if not self.api_key:
            raise ValueError(
                "QWEN_API_KEY is not set. "
                "Get your key at https://dashscope.console.aliyun.com/apiKey "
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
                "The 'openai' package is required for Qwen provider "
                "(DashScope uses an OpenAI-compatible API). "
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
            "provider": "QwenProvider",
            "model_name": self.model_name,
            "api_key_configured": bool(self.api_key),
            "available": bool(self.api_key),
        }
