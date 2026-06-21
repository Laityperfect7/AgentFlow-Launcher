# Provider 适配器使用指南

## 支持的 Provider

| Provider | 类名 | 默认模型 | 需要 API Key | 需要网络 |
|----------|------|----------|-------------|----------|
| Mock | `MockProvider` | mock-model | 否 | 否 |
| OpenAI | `OpenAIProvider` | gpt-4o-mini | `OPENAI_API_KEY` | 是 |
| DeepSeek | `DeepSeekProvider` | deepseek-chat | `DEEPSEEK_API_KEY` | 是 |
| Qwen | `QwenProvider` | qwen-plus | `QWEN_API_KEY` | 是 |
| Ollama | `OllamaProvider` | llama3 | 否 | 本地 |

## 配置方式

### 1. 环境变量

在 `.env` 文件中设置对应的 API Key：

```bash
# 复制 .env.example
cp .env.example .env

# 编辑 .env，填入你的 Key
OPENAI_API_KEY=sk-your-key-here
DEEPSEEK_API_KEY=sk-your-key-here
QWEN_API_KEY=sk-your-key-here
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. YAML 配置

在 Agent / Workflow / Skill 的 YAML 文件中指定 provider：

```yaml
# 使用 OpenAI
model_provider: openai
model_name: gpt-4o-mini

# 使用 DeepSeek
model_provider: deepseek
model_name: deepseek-chat

# 使用 Qwen
model_provider: qwen
model_name: qwen-plus

# 使用本地 Ollama
model_provider: ollama
model_name: llama3

# 使用 Mock（离线）
model_provider: mock
model_name: mock-model
```

## 添加新 Provider

1. 在 `agentflow/providers/` 创建新文件，如 `my_provider.py`
2. 继承 `BaseProvider`
3. 实现 `generate()` 方法
4. 在 `agentflow/core/agent.py` 的 `_resolve_provider()` 中注册

示例：

```python
from agentflow.providers.base import BaseProvider

class MyProvider(BaseProvider):
    def generate(self, prompt, *, temperature=0.7, max_tokens=2048, **kwargs):
        # 调用你的 API
        response = your_api_call(prompt)
        return response
```

## Provider 自动降级

如果指定的 Provider 不可用（如缺少依赖包），系统会自动降级到 MockProvider，确保项目始终可运行。
