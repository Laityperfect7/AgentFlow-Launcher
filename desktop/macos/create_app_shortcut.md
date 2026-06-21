# macOS 桌面快捷方式 / Dock 快捷方式创建指南

## 方法一：将 .command 文件放入 Dock（推荐，最简单）

1. 在 Finder 中找到 `desktop/macos/start_agentflow.command`
2. 将文件拖入 Dock 的右侧（回收站旁边）
3. 以后点击 Dock 上的图标即可启动

## 方法二：使用 Automator 创建独立 App

如果你想拥有一个独立的 `.app` 应用程序：

1. 打开 **Automator**（在 Applications 中）
2. 选择 **Application** 类型
3. 在左侧搜索栏搜索 **Run Shell Script**，拖入右侧
4. Shell 选择 `/bin/bash`
5. 输入以下脚本：

```bash
cd /path/to/AgentFlow-Launcher
source venv/bin/activate
python scripts/run_server.py &
sleep 2
open http://127.0.0.1:8000/console
```

6. File → Save，命名为 `AgentFlow-Launcher.app`，保存到 Applications 文件夹
7. 将 `.app` 拖入 Dock

## 方法三：创建桌面 Alias

1. 右键 `desktop/macos/start_agentflow.command`
2. 选择 **Make Alias**（创建替身）
3. 将 Alias 拖到桌面

## 自定义图标

1. 准备一张 512×512 的 PNG 图标
2. 使用 Preview 打开，Cmd+A 全选，Cmd+C 复制
3. 右键 .command 或 .app → Get Info
4. 点击左上角的小图标，Cmd+V 粘贴

## 注意事项

- 首次使用需要给 .command 文件执行权限：
  ```bash
  chmod +x desktop/macos/start_agentflow.command
  ```
- 如果遇到「无法打开，因为它来自身份不明的开发者」：
  System Preferences → Security & Privacy → 点击 Open Anyway
