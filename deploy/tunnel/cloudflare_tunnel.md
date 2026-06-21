# Cloudflare Tunnel (cloudflared)

Cloudflare Tunnel 可以将本地服务安全地暴露到公网，生成一个 `*.trycloudflare.com` 的临时域名。

## 优点
- **免费**：不需要注册账号即可使用快速隧道
- **HTTPS**：自动提供 SSL 证书
- **稳定**：Cloudflare 全球网络
- **无需注册**：`trycloudflare.com` 临时隧道无需 Cloudflare 账号

## 安装 cloudflared

### Windows (PowerShell)
```powershell
winget install --id Cloudflare.cloudflared
```

### macOS
```bash
brew install cloudflared
```

### Linux (Debian/Ubuntu)
```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb
```

## 使用方法

### 1. 确保 AgentFlow-Launcher 正在本地运行
```bash
python scripts/run_server.py
# 服务运行在 http://127.0.0.1:8000
```

### 2. 启动隧道
```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

### 3. 获取公网地址
启动后你会看到类似输出：
```
Your quick Tunnel has been created!
https://your-agent-demo.trycloudflare.com
```

### 4. 分享给他人
- Web Console: `https://your-agent-demo.trycloudflare.com/console`
- API Docs: `https://your-agent-demo.trycloudflare.com/docs`
- API Base: `https://your-agent-demo.trycloudflare.com`

## 停止隧道
按 `Ctrl+C` 即可。临时域名在隧道关闭后即失效。

## 注意事项
- 临时隧道每次启动域名会变化
- 如需固定域名，需要 Cloudflare 账号并配置 DNS
- 隧道关闭后公网地址立即失效
