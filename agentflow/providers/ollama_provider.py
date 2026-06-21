"""
Ollama provider adapter — local LLM inference.

Uses the Ollama API for running models locally.
Requires: Ollama installed and running, pip install httpx
Base URL: Set OLLAMA_BASE_URL in .env (default: http://localhost:11434)

Supported models: any model pulled into your local Ollama instance
  (e.g., llama3, qwen2.5, mistral, phi3, gemma2, deepseek-r1, etc.)

Install Ollama: https://ollama.com
"""

from __future__ import annotations

import os
from typing import Any, Dict

from agentflow.providers.base import BaseProvider
from agentflow.utils.logging import get_logger

logger = get_logger(__name__)


class OllamaProvider(BaseProvider):
    """
    Provider for local Ollama models.

    Environment variables:
        OLLAMA_BASE_URL: Ollama server URL (default: http://localhost:11434)

    No API key required — Ollama runs locally.
    """

    DEFAULT_BASE_URL = "http://localhost:11434"

    def __init__(self, model_name: str = "llama3", **kwargs: Any) -> None:
        super().__init__(model_name=model_name, **kwargs)
        self.base_url = os.getenv("OLLAMA_BASE_URL", self.DEFAULT_BASE_URL)

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion using the local Ollama API.

        Requires Ollama to be installed and running locally.
        The requested model must be pulled first: ollama pull <model_name>
        """
        try:
            import httpx
        except ImportError:
            raise ImportError(
                "The 'httpx' package is required for Ollama provider. "
                "Install it with: pip install httpx"
            )

        api_url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        try:
            with httpx.Client(timeout=120.0) as client:
                response = client.post(api_url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
        except httpx.ConnectError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Make sure Ollama is installed and running. "
                "Download from: https://ollama.com"
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise ValueError(
                    f"Model '{self.model_name}' not found in Ollama. "
                    f"Pull it first: ollama pull {self.model_name}"
                )
            raise

    def health_check(self) -> Dict[str, Any]:
        try:
            import httpx
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(f"{self.base_url}/api/tags")
                available = resp.is_success
        except Exception:
            available = False

        return {
            "provider": "OllamaProvider",
            "model_name": self.model_name,
            "base_url": self.base_url,
            "available": available,
            "local": True,
        }
