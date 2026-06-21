"""
Mock provider — runs entirely offline with no API key required.

Used for development, testing, and demo purposes. Returns structured,
predictable responses based on the prompt content.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from typing import Any, Dict

from agentflow.providers.base import BaseProvider
from agentflow.utils.logging import get_logger

logger = get_logger(__name__)

# Seed the RNG for reproducible demos
MOCK_SEED = 42


class MockProvider(BaseProvider):
    """
    Offline mock LLM provider.

    Generates realistic-looking responses without any network calls.
    Perfect for:
    - Running the demo without API keys
    - Writing tests
    - CI/CD pipelines
    - Offline development
    """

    def __init__(self, model_name: str = "mock-model", **kwargs: Any) -> None:
        super().__init__(model_name=model_name, **kwargs)
        self._rng = random.Random(MOCK_SEED)

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> str:
        """Generate a mock response based on the prompt content."""
        logger.info("MockProvider generating response (model=%s)", self.model_name)

        # Simulate a small delay for realism
        time.sleep(0.2)

        # Detect the type of request from the prompt
        prompt_lower = prompt.lower()

        if "background introduction" in prompt_lower or "背景介绍" in prompt_lower:
            return self._research_response(prompt)
        elif "summarize" in prompt_lower or "summar" in prompt_lower or "摘要" in prompt_lower or "总结" in prompt_lower:
            return self._summarize_response(prompt)
        elif "explain" in prompt_lower or "code" in prompt_lower or "解释" in prompt_lower or "代码" in prompt_lower:
            return self._explain_response(prompt)
        elif "optimize" in prompt_lower or "优化" in prompt_lower or "improve" in prompt_lower:
            return self._optimize_response(prompt)
        elif "step" in prompt_lower and ("collect" in prompt_lower or "draft" in prompt_lower or "generate" in prompt_lower):
            return self._workflow_step_response(prompt)
        else:
            return self._generic_response(prompt)

    # ------------------------------------------------------------------
    # Response generators
    # ------------------------------------------------------------------

    def _research_response(self, prompt: str) -> str:
        """Generate a structured research report."""
        topic = self._extract_topic(prompt)
        return json.dumps({
            "background": f"## Background\n\n{topic} is an emerging field that has gained significant attention in recent years. "
                          f"The rapid advancement of large language models has transformed how we approach {topic}.",
            "key_points": [
                f"Core concept of {topic} and its fundamental principles",
                f"Latest technological breakthroughs in {topic}",
                "Industry adoption trends and real-world use cases",
                "Common challenges and known limitations",
                "Future research directions and opportunities",
            ],
            "action_steps": [
                f"Step 1: Understand the fundamentals of {topic}",
                f"Step 2: Set up a development environment for experimentation",
                f"Step 3: Run baseline experiments to establish benchmarks",
                f"Step 4: Iterate and optimize based on empirical results",
                f"Step 5: Document findings and share with the community",
            ],
            "risks": [
                "Rapid technology evolution may outdate current approaches",
                "API costs can escalate quickly without proper monitoring",
                "Model hallucinations may produce unreliable outputs",
                "Data privacy concerns when sending sensitive information to cloud APIs",
            ],
            "next_steps": [
                "Review the latest papers on arXiv related to this topic",
                "Join relevant Discord/Slack communities for discussions",
                "Start a small proof-of-concept project",
                "Evaluate different model providers for cost-performance trade-offs",
            ],
        }, ensure_ascii=False, indent=2)

    def _summarize_response(self, prompt: str) -> str:
        """Generate a structured summary."""
        source = self._extract_topic(prompt)
        return json.dumps({
            "summary": f"A concise overview of the content related to '{source}', capturing the main thesis and supporting arguments.",
            "key_takeaways": [
                "Primary argument: The content presents a clear central thesis",
                "Supporting evidence: Multiple data points are provided to back the claims",
                "Practical implications: The ideas have direct applicability to real-world scenarios",
            ],
            "word_count_original": 1250,
            "word_count_summary": 180,
            "compression_ratio": "6.94x",
        }, ensure_ascii=False, indent=2)

    def _explain_response(self, prompt: str) -> str:
        """Generate a code explanation."""
        snippet = self._extract_topic(prompt)
        return json.dumps({
            "overview": f"This code implements a solution for {snippet}. It follows common design patterns and best practices.",
            "line_by_line": [
                {"line": 1, "code": "import something", "explanation": "Imports required dependencies"},
                {"line": 2, "code": "def main():", "explanation": "Entry point function definition"},
                {"line": 3, "code": "    result = process(data)", "explanation": "Core processing logic call"},
                {"line": 4, "code": "    return result", "explanation": "Returns the processed result"},
            ],
            "suggestions": [
                "Consider adding error handling for edge cases",
                "Add type hints for better code documentation",
                "The function could benefit from async support for I/O operations",
            ],
        }, ensure_ascii=False, indent=2)

    def _optimize_response(self, prompt: str) -> str:
        """Generate prompt optimization suggestions."""
        return json.dumps({
            "original_prompt_length": len(prompt),
            "optimized_prompt": prompt.strip() + "\n\nPlease be specific, structured, and provide actionable output.",
            "improvements": [
                "Added specificity directive for clearer output",
                "Requested structured format for easier parsing",
                "Added actionable output requirement",
            ],
            "estimated_quality_improvement": "+35%",
        }, ensure_ascii=False, indent=2)

    def _workflow_step_response(self, prompt: str) -> str:
        """Generate a workflow step result."""
        return json.dumps({
            "step_result": f"Step completed successfully. Analysis based on input: {prompt[:100]}...",
            "confidence": 0.92,
            "tokens_used": self._rng.randint(100, 500),
        }, ensure_ascii=False, indent=2)

    def _generic_response(self, prompt: str) -> str:
        """Fallback generic response."""
        topic = self._extract_topic(prompt)
        resp_id = hashlib.md5(prompt.encode()).hexdigest()[:8]
        return json.dumps({
            "response": f"Mock response for: '{topic}'. This is a simulated LLM output generated by MockProvider.",
            "request_id": resp_id,
            "model": self.model_name,
            "note": "This response was generated offline by the mock provider. "
                    "Configure a real provider (OpenAI, DeepSeek, etc.) for production use.",
        }, ensure_ascii=False, indent=2)

    def _extract_topic(self, prompt: str) -> str:
        """Heuristic to extract the likely topic from a prompt."""
        # Try to find the user input portion
        markers = ["User:", "user:", "input:", "Input:", "text:", "Text:"]
        for marker in markers:
            if marker in prompt:
                parts = prompt.split(marker, 1)
                if len(parts) > 1:
                    return parts[1].strip()[:100]
        # Fallback: use the last line
        lines = [l for l in prompt.strip().split("\n") if l.strip()]
        if lines:
            return lines[-1].strip()[:100]
        return "general query"

    def health_check(self) -> Dict[str, Any]:
        return {
            "provider": "MockProvider",
            "model_name": self.model_name,
            "available": True,
            "mock": True,
            "offline": True,
        }
