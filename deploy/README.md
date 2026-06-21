# AgentFlow-Launcher 部署指南

本目录包含将 AgentFlow-Launcher 部署到不同环境的文档和脚本。

## 目录结构

```
deploy/
├── README.md              # 本文件
└── tunnel/                # 公网隧道暴露方案
    ├── cloudflare_tunnel.md
    ├── ngrok.md
    ├── localtunnel.md
    ├── expose_api_example.sh
    └── expose_api_example.ps1
```

## 快速导航

| 部署方式 | 适用场景 | 文档 |
|----------|----------|------|
| 本地运行 | 开发、测试、Demo | 项目 README |
| 桌面快捷方式 | 一键启动 | [desktop/](../desktop/) |
| 公网临时暴露 | 远程演示、API 测试 | [tunnel/](tunnel/) |
| 生产环境部署 | 正式上线 | 后续 Roadmap |

## 部署前检查

- [ ] `.env` 文件已配置（参考 `.env.example`）
- [ ] 虚拟环境已创建并安装依赖
- [ ] Mock 模式可正常运行
- [ ] 如使用真实 API，Key 已配置且有效
