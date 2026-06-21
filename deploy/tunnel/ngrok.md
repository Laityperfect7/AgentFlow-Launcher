# Ngrok

Ngrok 是最流行的内网穿透工具之一，提供稳定的公网隧道服务。

## 优点
- **成熟稳定**：广泛使用，社区活跃
- **Web 界面**：提供本地 Web 检查器 (http://127.0.0.1:4040)
- **静态域名**：付费版支持固定域名
- **多种协议**：支持 HTTP、TCP、TLS

## 安装 Ngrok

### 所有平台
1. 访问 https://ngrok.com/download
2. 下载对应系统的版本
3. 解压到合适的位置（建议加入 PATH）

### 或使用包管理器
```bash
# macOS
brew install ngrok

# Windows (winget)
winget install ngrok

# Linux (snap)
sudo snap install ngrok
```

## 注册与认证
1. 在 https://dashboard.ngrok.com/signup 注册免费账号
2. 获取 Authtoken: https://dashboard.ngrok.com/get-started/your-authtoken
3. 配置：
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

## 使用方法

### 1. 启动 AgentFlow-Launcher
```bash
python scripts/run_server.py
```

### 2. 启动 Ngrok 隧道
```bash
ngrok http 8000
```

### 3. 获取公网地址
你会看到：
```
Forwarding  https://xxxx-xx-xxx-xxx-xxx.ngrok-free.app -> http://127.0.0.1:8000
```

### 4. 访问
- Web Console: `https://xxxx.ngrok-free.app/console`
- API Docs: `https://xxxx.ngrok-free.app/docs`

## 使用 Web 检查器
Ngrok 提供了一个本地 Web 界面来查看请求日志：
- http://127.0.0.1:4040

在这里你可以：
- 查看所有请求/响应
- 重放请求
- 查看流量统计

## 停止
按 `Ctrl+C` 或在 Web 检查器中停止。

## 免费版限制
- 带宽有限
- 每次启动域名随机
- 每分钟请求数有限
