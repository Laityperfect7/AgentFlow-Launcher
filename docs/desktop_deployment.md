# 桌面端部署指南

AgentFlow-Launcher 支持 Windows、macOS、Linux 三大桌面平台的一键启动和快捷方式创建。

## Windows

### 一键启动
双击 `desktop/windows/start_agentflow.bat`

该脚本会：
1. 自动激活虚拟环境
2. 启动 FastAPI 服务器
3. 自动打开浏览器访问 Web 控制台

### 创建桌面快捷方式
在 PowerShell 中运行：
```powershell
powershell -ExecutionPolicy Bypass -File desktop/windows/create_shortcut.ps1
```

桌面会出现「AgentFlow Launcher」快捷方式，双击即可启动。

## macOS

### 一键启动
双击 `desktop/macos/start_agentflow.command`

首次使用需要赋予执行权限：
```bash
chmod +x desktop/macos/start_agentflow.command
```

### 放入 Dock
将 `.command` 文件直接拖入 Dock 右侧即可。

### 创建应用程序
详见 `desktop/macos/create_app_shortcut.md`

## Linux

### 一键启动
```bash
bash desktop/linux/start_agentflow.sh
```

### 创建应用程序菜单快捷方式
1. 编辑 `desktop/linux/agentflow-launcher.desktop`
2. 将路径替换为你的实际项目路径
3. 复制到应用目录：
   ```bash
   cp desktop/linux/agentflow-launcher.desktop ~/.local/share/applications/
   ```
4. 程序菜单中搜索「AgentFlow Launcher」即可找到

## 通用说明

- 所有桌面脚本启动的服务默认地址：`http://127.0.0.1:8000`
- 浏览器会自动打开 Web 控制台：`http://127.0.0.1:8000/console`
- API 文档：`http://127.0.0.1:8000/docs`
- 关闭终端窗口即停止服务
