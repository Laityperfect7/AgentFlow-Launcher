"""
Pydantic schemas for Agent, Workflow, and Skill definitions.

These schemas provide runtime validation and serialization for all
configuration-driven components in AgentFlow-Launcher.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Agent schemas
# ---------------------------------------------------------------------------

class AgentTool(BaseModel):
    """A tool available to an agent."""
    name: str = Field(..., description="Tool identifier")
    description: str = Field(default="", description="What the tool does")
    parameters: Dict[str, Any] = Field(default_factory=dict)


class AgentMemory(BaseModel):
    """Memory configuration for an agent."""
    type: str = Field(default="buffer", description="Memory type: buffer, summary, vector")
    max_tokens: int = Field(default=4096, description="Maximum tokens to retain")


class AgentInputSchema(BaseModel):
    """Expected input shape for an agent run."""
    fields: Dict[str, str] = Field(default_factory=dict, description="Field name -> type mapping")


class AgentOutputSchema(BaseModel):
    """Expected output shape for an agent run."""
    fields: Dict[str, str] = Field(default_factory=dict)


class AgentDefinition(BaseModel):
    """Full agent definition loaded from YAML."""
    name: str = Field(..., description="Unique agent name")
    description: str = Field(default="")
    model_provider: str = Field(default="mock", description="Provider key: openai, deepseek, qwen, ollama, mock")
    model_name: str = Field(default="mock-model", description="Model identifier for the provider")
    system_prompt: str = Field(default="You are a helpful assistant.")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=2048)
    tools: List[AgentTool] = Field(default_factory=list)
    memory: AgentMemory = Field(default_factory=AgentMemory)
    input_schema: AgentInputSchema = Field(default_factory=AgentInputSchema)
    output_schema: AgentOutputSchema = Field(default_factory=AgentOutputSchema)


# ---------------------------------------------------------------------------
# Workflow schemas
# ---------------------------------------------------------------------------

class WorkflowStep(BaseModel):
    """A single step within a workflow."""
    name: str = Field(..., description="Step identifier")
    description: str = Field(default="")
    prompt_template: str = Field(..., description="Prompt with {variable} placeholders")
    input_variables: List[str] = Field(default_factory=list)
    output_key: str = Field(default="output", description="Key to store step result under")


class WorkflowDefinition(BaseModel):
    """Full workflow definition loaded from YAML."""
    name: str = Field(..., description="Unique workflow name")
    description: str = Field(default="")
    model_provider: str = Field(default="mock")
    model_name: str = Field(default="mock-model")
    steps: List[WorkflowStep] = Field(..., min_length=1)
    max_steps: int = Field(default=20, description="Safety cap on step count")


# ---------------------------------------------------------------------------
# Skill schemas
# ---------------------------------------------------------------------------

class SkillField(BaseModel):
    """An input or output field for a skill."""
    name: str
    type: str = "string"
    description: str = ""


class SkillDefinition(BaseModel):
    """Full skill definition loaded from YAML."""
    name: str = Field(..., description="Unique skill name")
    description: str = Field(default="")
    category: str = Field(default="general", description="Skill category for grouping")
    model_provider: str = Field(default="mock")
    model_name: str = Field(default="mock-model")
    input_fields: List[SkillField] = Field(default_factory=list)
    output_format: Dict[str, str] = Field(default_factory=dict)
    prompt_template: str = Field(..., description="Prompt with {variable} placeholders")
    examples: List[Dict[str, str]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# API request / response schemas
# ---------------------------------------------------------------------------

class RunRequest(BaseModel):
    """Request body for running an agent, workflow, or skill."""
    input: str = Field(..., description="User input text")
    params: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters")


class RunResponse(BaseModel):
    """Standard response from a run."""
    success: bool
    type: str = Field(..., description="agent | workflow | skill")
    name: str
    input: str
    output: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    version: str = "1.0.0"
    mock_mode: bool = True
