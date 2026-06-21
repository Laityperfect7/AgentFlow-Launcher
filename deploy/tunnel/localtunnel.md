# LocalTunnel

LocalTunnel 是一个基于 Node.js 的免费内网穿透工具，无需注册即可使用。

## 优点
- **完全免费**：无需注册账号
- **开源**：代码在 GitHub 上
- **轻量**：只需要 Node.js
- **支持自定义子域名**：`lt --subdomain myagent`

## 安装

### 前提条件
需要安装 Node.js (v12+)：https://nodejs.org

### 安装 localtunnel
```bash
npm install -g localtunnel
```

## 使用方法

### 1. 启动 AgentFlow-Launcher
```bash
python scripts/run_server.py
# 服务运行在 http://127.0.0.1:8000
```

### 2. 启动 LocalTunnel
```bash
lt --port 8000
```

### 3. 获取公网地址
你会看到：
```
your url is: https://xxxx.loca.lt
```

### 4. 访问
- Web Console: `https://xxxx.loca.lt/console`
- API Docs: `https://xxxx.loca.lt/docs`

## 自定义子域名（可能与其他用户冲突）
```bash
lt --port 8000 --subdomain my-agentflow-demo
# 地址: https://my-agentflow-demo.loca.lt
```

## 首次访问需要密码
LocalTunnel 默认要求输入你的外网 IP 作为密码：
- 访问 https://xxxx.loca.lt
- 页面会显示 "Click to Continue"
- 输入你的公网 IP（页面会提示）

或者查看 https://ipv4.icanhazip.com 获取你的公网 IP。

## 停止
按 `Ctrl+C` 即可。

## 注意事项
- 免费服务可能不如 Cloudflare/ngrok 稳定
- 自定义子域名可能已被他人占用
- 建议偶尔用于临时演示，不适合生产环境
