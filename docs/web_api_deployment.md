# Web API 部署与公网暴露指南

## 本地 API 服务

启动 API 服务：
```bash
python scripts/run_server.py
```

服务地址：
- API 根路径：`http://127.0.0.1:8000`
- Swagger 文档：`http://127.0.0.1:8000/docs`
- ReDoc 文档：`http://127.0.0.1:8000/redoc`
- Web 控制台：`http://127.0.0.1:8000/console`

## API 接口速览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 项目信息 |
| GET | `/health` | 健康检查 |
| GET | `/api/agents` | Agent 列表 |
| POST | `/api/agents/{name}/run` | 运行 Agent |
| GET | `/api/workflows` | Workflow 列表 |
| POST | `/api/workflows/{name}/run` | 运行 Workflow |
| GET | `/api/skills` | Skill 列表 |
| POST | `/api/skills/{name}/run` | 运行 Skill |

## curl 使用示例

### 运行 Agent
```bash
curl -X POST http://127.0.0.1:8000/api/agents/demo_research_agent/run \
  -H "Content-Type: application/json" \
  -d '{"input": "大模型 Agent 开发"}'
```

### 运行 Workflow
```bash
curl -X POST http://127.0.0.1:8000/api/workflows/content_pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"input": "AI技术写作指南"}'
```

### 运行 Skill
```bash
curl -X POST http://127.0.0.1:8000/api/skills/text_summarizer/run \
  -H "Content-Type: application/json" \
  -d '{"input": "这是一段需要被总结的长文本..."}'
```

## 公网暴露

将本地 API 临时暴露到公网，方便远程演示和测试：

| 方案 | 工具 | 文档 |
|------|------|------|
| 方案 A | Cloudflare Tunnel | [cloudflare_tunnel.md](../deploy/tunnel/cloudflare_tunnel.md) |
| 方案 B | Ngrok | [ngrok.md](../deploy/tunnel/ngrok.md) |
| 方案 C | LocalTunnel | [localtunnel.md](../deploy/tunnel/localtunnel.md) |

### 快速示例（Cloudflare Tunnel）
```bash
# 1. 启动服务
python scripts/run_server.py

# 2. 另开终端，启动隧道
cloudflared tunnel --url http://127.0.0.1:8000

# 3. 获得公网地址（形如）
# https://your-demo.trycloudflare.com
```

### 公网暴露后
- Web Console: `https://<your-url>/console`
- API Docs: `https://<your-url>/docs`
- Health Check: `https://<your-url>/health`

## 注意事项
- 公网暴露仅用于开发和演示，生产环境请使用正式部署方案
- 临时域名在隧道关闭后立即失效
- 不要在公网暴露未加保护的 API 服务
- 生产环境建议使用反向代理（Nginx）+ HTTPS + 认证
