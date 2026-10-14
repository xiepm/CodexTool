# Codex 技能、插件与 MCP 迁移包

打包日期：2026-10-14。按另一台 **Windows 电脑**编写恢复流程，恢复工具需要 **Python 3.11+**。

## 1. 新电脑的最快恢复方法

1. 安装 Codex，登录同一账号与工作区；安装 Python 3.11+ 并加入 PATH。
2. 完整解压 ZIP 到较短目录，如 C:/CodexMigration。不要直接在压缩文件内运行。
3. 退出目标电脑的 Codex，避免同时修改配置。进入解压后的包目录，打开 PowerShell。
4. 执行校验、预览与恢复：

~~~powershell
python .\restore.py --verify
python .\restore.py
python .\restore.py --apply
~~~

也可运行 Restore.ps1、Restore.ps1 -Verify、Restore.ps1 -Apply。若脚本执行策略阻止 PowerShell，直接用上述 Python 命令即可。

默认恢复行为：
- 自定义技能分别恢复到目标用户的 .codex/skills 和 .agents/skills；完整保留脚本、模板、参考资料与资产。
- 目标电脑已有同目录技能时，整个技能跳过，避免混合新旧版本。报告列出所有跳过项。
- 桥接代码与支持文件放到目标 .codex/migration-support/codex-migration-2026-10-14。
- 只新增目标 config.toml 中不存在的 MCP 名称；新加入服务全部 enabled=false，完成配置后再启用。
- 目标电脑同名 MCP、其他配置原样保留；配置变更前备份目标 config.toml。
- 系统技能与官方插件缓存保存在 archive 供核对，由新 Codex 提供或重新安装，恢复脚本不覆盖应用运行时。
- 应用自管的 node_repl 不导入；旧进程管道、内部路径不能在新电脑复用。
- 恢复不会安装软件、发起账号登录或启动 CAD 程序。依赖安装脚本按组件另行执行。
- 每次实际恢复会输出支持目录位置与 restore-report JSON。

可以指定用户或自定义 Codex 主目录：

~~~powershell
python .\restore.py --target-home "C:\Users\NewUser"
python .\restore.py --apply --target-home "C:\Users\NewUser"
python .\restore.py --apply --target-codex-dir "D:\MyCodex"
~~~

--skip-mcp 可只恢复文件。需要更改旧安装路径时，将 path-map.example.json 复制到包外，编辑副本，再使用：

~~~powershell
Copy-Item .\path-map.example.json ..\path-map.local.json
# 编辑包外的 ..\path-map.local.json 后：
python .\restore.py --path-map ..\path-map.local.json
python .\restore.py --apply --path-map ..\path-map.local.json
~~~

自动路径映射涵盖旧用户目录、旧 .codex 根目录、D:/NXTEST 及 Scientific Illustrator 市场目录。其他绝对路径见 PATHS_TO_REVIEW.csv。该表由文本提取，包含示例路径，需结合实际用途判断。

## 2. 安装可选依赖

支持目录默认如下；如果指定了 --target-codex-dir，请使用恢复报告给出的 support_dir：

~~~powershell
$support = Join-Path $env:USERPROFILE ".codex\migration-support\codex-migration-2026-10-14"

# 仅预览 CAD Python 环境安装命令
& "$support\Setup-Dependencies.ps1" -Cad

# 实际安装所选组件；按需要选择
& "$support\Setup-Dependencies.ps1" -Cad -Apply
& "$support\Setup-Dependencies.ps1" -InstSci -Apply
& "$support\Setup-Dependencies.ps1" -Markmap -Apply
~~~

这些步骤会联网。-Cad 建立独立虚拟环境并安装本机已用版本 mcp==1.26.0、pywin32==312 和包内 SOLIDWORKS 源码。
-InstSci 安装 instsci==0.2.0a2；-Markmap 需要先安装 Node.js/npm，再安装 @jinzcdev/markmap-mcp-server@0.2.0。
完整旧 CAD Python 包版本记录在 inventory/cad-python-installed.json，便于排查，未直接复制虚拟环境。

若当前软件源无法取得记录的版本，请根据 inventory 中的版本和来源定位同版本安装包；不要把安装失败当作服务已恢复。

## 3. 每个 MCP 需要重新配置什么

| MCP | 已打包 | 新电脑的安装和配置 |
|---|---|---|
| node_repl | 管理说明 | 由新 Codex 安装/更新生成，不搬运旧内部进程与管道 |
| OpenAI Docs | 公共 HTTP 地址 | 在 MCP 设置中启用并检查联网 |
| MATLAB | 启动配置记录 | 安装并授权 MATLAB；重新安装 MATLAB MCP server；设置实际 EXE 与工作目录 |
| InstSci | 模块代码快照、版本和入口元数据 | 安装 Python 包；浏览器组件与机构登录重新配置 |
| Siemens NX | Python 桥接、.NET 源码、构建/启动脚本 | 安装 NX 与许可；设置 NX 根目录；针对目标 NX 编译并加载桥接 |
| SOLIDWORKS | solidworks-agent-mcp 0.4.0 本地源码 | 安装软件、许可和 CAD Python 依赖；设置零件、装配模板真实路径 |
| Mastercam | server.py、ipc_client.py 等源代码 | 安装 Mastercam；启用 NET-Script IPCServer；确认启动路径，先只读探测 |
| SOLIDWORKS CAM | server.py、worker.py | 安装 CAM 插件与许可；更新 worker.py 中 cwaddinu.dll 路径 |
| Memory | dsh-memory-eternal 0.7.0 代码快照与版本 | 安装 DSH Desktop 和对应插件；重设命令路径；记忆数据库未复制 |
| Markmap | 0.2.0 代码快照与版本 | 安装 Node.js/npm 并运行 Markmap 依赖安装步骤 |

目标 config.toml 和支持目录 mcp.generated.toml 中的 __SET_...__ 是需要手工填写的值。
先填路径与模板、装好依赖，再在 Codex 设置 → MCP servers 中逐项启用、重启并检查连接。

同名服务已存在时，恢复脚本保留目标配置；可与 mcp.generated.toml 比较，不要重复整体追加。
源配置记录保存在 inventory/mcp-config.sanitized.json，可查看原电脑的非敏感环境变量和执行选项。

### NX 桥接

本机使用 NX 2412 / .NET Remoting。新电脑须按实际 NX 编译：

~~~powershell
$support = Join-Path $env:USERPROFILE ".codex\migration-support\codex-migration-2026-10-14"
$ug = Join-Path $support "NXTEST\CAD-Agent-Hub\MCP\UG"
& "$ug\dotnet_bridge\build_bridge.ps1" -NXRoot "C:\Program Files\Siemens\NX2412"
~~~

构建依赖 Windows .NET Framework C# 编译器与目标 NX 的 NXOpen 程序集；商业软件 DLL/EXE 未打包。
如需 NX 启动时自动加载，手工执行 $ug/install_nx_autostart.ps1 -NXRoot <实际路径>。
该脚本遇到已经设置的不同 UGII_USER_DIR 会停止，需要保留并合并原自定义配置。
详细说明在包内 NX README.current.zh-CN.md；不要默认沿用示例 NX 安装位置。

### Mastercam 与 SOLIDWORKS CAM

桥接按自身目录限制允许访问的工作区。恢复后的根目录为支持目录中的 NXTEST；验证时使用该目录内的测试副本。
Mastercam 的启动 EXE、SOLIDWORKS CAM 的插件 DLL 等源码路径需按实际安装修改。
旧 archive/CAD-CONNECTIONS.original.md 仅作历史安装参考，其中的“通过”描述不代表新电脑已通过验证。

刀具库、机床库、后处理器、历史工件和生产 NC 未迁移；恢复连接不代表完成加工或生产放行。

## 4. 插件恢复

全部包的来源、缓存版本和恢复方式见 PLUGINS.md / inventory/plugins.json。

- Codex 自带/官方运行时插件：安装新 Codex 后检查，在 Plugins 中补装缺少项；不要覆盖其版本化运行时缓存。
- 账号云端插件：登录同一账号和工作区后检查 Installed；Gmail、Drive、GitHub 等按需要重新授权。
- Scientific Illustrator：已附完整本地市场源码；按以下命令注册，再从插件目录安装。
- 自建 Codex Harness/tunnel：重新部署本地服务并建立隧道/账号连接；包内插件声明不能恢复服务端实例。
- 其他缓存包保留在 archive/plugin-cache，供版本核对或必要时从原来源重装。

~~~powershell
$support = Join-Path $env:USERPROFILE ".codex\migration-support\codex-migration-2026-10-14"
& "$support\Register-ScientificIllustrator.ps1" -Apply
~~~

注册要求 Codex CLI 在 PATH 中。完成后进入 Plugins，选择 scientific-illustrator-tools，安装 scientific-illustrator，启动新聊天。
另需 Node.js、draw.io 桌面版、Microsoft PowerPoint 或 WPS，并按插件自带说明检查连接。浏览器扩展与桌面控制权限需在新电脑重新授予。

## 5. Skills 的外部依赖

- Zotero / Obsidian：另装程序，并单独迁移文献库、附件、笔记库，配置 API/CLI。
- Asta / BGPT / 学术 API：另接服务或配置 API Key。技能文件存在不代表服务可调用。
- Python/R/Node/LaTeX 绘图与文档流程：按对应技能安装依赖，或使用目标 Codex 提供的官方运行时。
- D:/deepscientist 等外部研究工程、数据与模型权重未打包；按 PATHS_TO_REVIEW.csv 更新或迁移。
- 同名但不同来源的技能保留原目录布局，恢复脚本不去重。包内另有 shared 共用资源目录，因此恢复报告的目录数可能比 SKILL.md 数多 1。
- .system 技能只归档，由目标 Codex 安装提供，以匹配目标版本。

## 6. 包含与排除

包含：用户技能及参考资源、全部已发现插件包快照、本地市场源码、CAD/CAM 桥接源码、MCP 非敏感配置、版本清单、恢复脚本和校验文件。

未包含：账号 auth.json、密钥和 OAuth 会话、浏览器状态、聊天/记忆数据库、虚拟环境与 node_modules 依赖树、商业软件及 DLL/EXE、旧工件和运行输出。
文件筛选明细见 inventory/exclusions.json。高置信密钥模式替换记录见 inventory/redactions.json；该检测是启发式，不能覆盖所有可能的秘密格式。

包内有个人工作流与参考资源，适合迁移到自己的电脑。源电脑配置未被恢复脚本修改。

## 7. 校验与测试边界

manifest.json 和 SHA256SUMS.txt 记录所有交付文件的哈希；restore.py --verify 会在恢复前校验。
ZIP 外的 .sha256 文件用于检查整个压缩包。
VALIDATION.md 记录独立临时目录模拟恢复、配置保留、重复运行、损坏拒绝和脚本语法检查结果。
这些检查不替代另一台电脑上的软件许可、插件授权和原生应用测试。

## 8. 官方参考

- [Skills](https://learn.chatgpt.com/docs/build-skills)
- [MCP](https://learn.chatgpt.com/docs/extend/mcp)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [本地插件市场](https://developers.openai.com/plugins/build/plugins)
