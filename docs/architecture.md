# AgentFlow-Launcher 系统架构

## 概述

AgentFlow-Launcher 采用分层架构设计，从上到下分为：

```
┌─────────────────────────────────────────────┐
│              前端层 (Web Console)             │
│         HTML + CSS + JavaScript              │
├─────────────────────────────────────────────┤
│              API 层 (FastAPI)                │
│    REST Endpoints + Swagger Docs             │
├─────────────────────────────────────────────┤
│           核心引擎层 (Core Engine)            │
│   Agent Runner │ Workflow Runner │ Skill Runner │
├─────────────────────────────────────────────┤
│          Provider 适配层 (Providers)          │
│  OpenAI │ DeepSeek │ Qwen │ Ollama │ Mock    │
├─────────────────────────────────────────────┤
│           配置层 (YAML Configs)               │
│   agents/ │ workflows/ │ skills/              │
└─────────────────────────────────────────────┘
```

## 核心组件

### 1. Provider 层 (`agentflow/providers/`)

负责与大模型 API 通信。所有 Provider 继承自 `BaseProvider`，实现统一的 `generate(prompt, ...)` 接口。

- **BaseProvider**: 抽象基类，定义接口契约
- **MockProvider**: 离线 mock，无需 API Key
- **OpenAIProvider**: OpenAI GPT 系列
- **DeepSeekProvider**: DeepSeek 系列
- **QwenProvider**: 通义千问系列
- **OllamaProvider**: 本地 Ollama 模型

### 2. 核心引擎层 (`agentflow/core/`)

- **Loader**: YAML 配置加载器，将配置文件解析为 Pydantic 模型
- **Agent Runner**: 单个 Agent 的执行引擎
- **Workflow Runner**: 多步骤 Workflow 的编排引擎
- **Skill Runner**: 可复用 Skill 的执行引擎
- **Schemas**: Pydantic 数据模型定义

### 3. API 层 (`server/`)

基于 FastAPI 的 REST API 服务：

- `GET /` — 项目信息
- `GET /health` — 健康检查
- `GET /api/agents` — Agent 列表
- `POST /api/agents/{name}/run` — 运行 Agent
- `GET /api/workflows` — Workflow 列表
- `POST /api/workflows/{name}/run` — 运行 Workflow
- `GET /api/skills` — Skill 列表
- `POST /api/skills/{name}/run` — 运行 Skill
- `GET /docs` — Swagger UI 自动文档

### 4. Web 控制台 (`web/`)

纯前端 SPA，通过 AJAX 调用本地 API：

- 深色科技风 UI
- 类型选择（Agent / Workflow / Skill）
- 模块下拉选择
- 输入区域 + Run 按钮
- JSON 结果展示
- API 状态指示

## 数据流

```
用户输入 → Web Console / curl
    ↓
FastAPI Endpoint 接收请求
    ↓
核心引擎加载 YAML 配置
    ↓
Provider 调用 LLM API（或 Mock）
    ↓
结果封装为 RunResponse
    ↓
返回 JSON → 前端展示
```
