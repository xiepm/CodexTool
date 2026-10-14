# CodexTool

本机 Codex Skills、插件和 MCP 的迁移快照与 Windows 恢复指南。

## 下载完整迁移包

- **[下载迁移 ZIP（约 81 MiB）](https://github.com/xiepm/CodexTool/releases/download/migration-2026-10-14/codex-migration-2026-10-14.zip)**
- [下载 SHA-256 校验文件](https://github.com/xiepm/CodexTool/releases/download/migration-2026-10-14/codex-migration-2026-10-14.zip.sha256)
- [查看 Release](https://github.com/xiepm/CodexTool/releases/tag/migration-2026-10-14)

请下载上面的迁移 ZIP。GitHub 的 **Code → Download ZIP** 和 Release 自动生成的 **Source code** 只包含本仓库说明与目录，不包含完整迁移载荷。

## 新电脑恢复

1. 安装 Codex，登录所需账号与工作区；安装 Python 3.11+。
2. 下载并完整解压迁移 ZIP 到较短目录，例如 `C:\CodexMigration`。
3. 退出目标电脑的 Codex。在包含 `restore.py` 的解压目录打开 PowerShell，依次运行：

```powershell
python .\restore.py --verify
python .\restore.py
python .\restore.py --apply
```

第二条命令仅预览。恢复时保留目标电脑已有的同名技能和 MCP；修改 MCP 配置前备份。新导入的 MCP 默认禁用，填好路径、装好依赖后逐项启用。

**[完整中文恢复说明](README.zh-CN.md)** · [插件重装清单](PLUGINS.md) · [验证记录](VALIDATION.md)

## 快照范围

| 内容 | 数量 / 说明 |
|---|---|
| 可恢复的自定义技能 | 128 项，另有 shared 公共资源目录 |
| 全部 SKILL.md 快照 | 206 份，包含系统与插件技能 |
| 插件版本包 | 26 个 |
| MCP 配置记录 | 10 项；9 项作为禁用配置迁移，node_repl 由新 Codex 管理 |
| 本地桥接 | NX、SOLIDWORKS、Mastercam、SOLIDWORKS CAM 源码 |
| 其他支持 | Scientific Illustrator 本地市场、恢复脚本、依赖版本及哈希清单 |

[技能目录](inventory/skills.json) · [插件目录](inventory/plugins.json) · [数量汇总](inventory/summary.json)

## 需要重新安装或配置

- **Codex 官方插件与系统运行时**：由目标 Codex 提供或从插件目录补装；缓存快照仅供核对。
- **云端连接**：检查同账号、同工作区的连接状态，按需重新授权 GitHub、Google Drive、Gmail 等服务。
- **本地 MCP**：重新安装 Python/Node.js 依赖，调整 EXE、模板、工作目录等路径；API Key、登录和隧道连接需重新配置。
- **商业与桌面软件**：另装并授权 NX、Mastercam、SOLIDWORKS/CAM、MATLAB；draw.io、PowerPoint/WPS、Zotero、Obsidian 按需安装。
- **数据与工程**：文献库、笔记库、研究工程、模型权重、刀具库、机床库、后处理器及生产工件需另行迁移。

详细命令和每项 MCP 的配置要求见[恢复说明](README.zh-CN.md)。

## 完整性与边界

快照日期：2026-10-14。ZIP SHA-256：

```text
582f607d4ab46335e72f152178886dd45e961e52611d64d4768d37d3d878bf5d
```

下载后可使用 `Get-FileHash .\codex-migration-2026-10-14.zip -Algorithm SHA256` 核对。解压后的 `restore.py --verify` 会校验包内文件。

已通过隔离目录下的恢复、配置保留、重复运行、损坏拒绝及 ZIP 完整性检查；尚未在另一台真实电脑完成软件安装与原生 CAD/CAM 验证。

包内排除了账号登录凭据、OAuth 会话、浏览器状态、聊天/记忆数据库、虚拟环境、node_modules、商业软件二进制及生产数据。密钥模式检测为启发式，详情见包内排除与替换记录。

包内包含第三方技能、插件及源码快照；各组件继续适用其原有许可。本仓库不为第三方内容额外授予许可。
