# 用 skillshare 管理和备份当前技能

2026-11-12 快照：423 个顶层技能、444 个可识别技能（含嵌套引用），6,930 个技能及配套文件。使用 skillshare 0.30.6。

旧的 2026-10-14 Windows 迁移包、Release 与说明继续保留。本目录的 skills/ 是新的技能文件源，不包含 Codex 登录信息、聊天记录或 MCP 凭据。

## 本机

仓库：~/CodexTool；skillshare 的 sources.skills 已设为 ~/CodexTool/skills（配置文件内为绝对路径）。

```bash
skillshare list
skillshare ui start
skillshare push --dry-run
skillshare push -m "Update research skills"
```

push 需要本机 Git 的 GitHub 登录；Codex 的 GitHub 连接器授权不会自动登录终端 Git。GitHub CLI 登录后可运行 gh auth setup-git。

后续编辑以仓库 skills/ 内的文件为准。原 ~/.codex/skills 保留独立副本，当前尚未改为符号链接；修改它不会自动写回仓库。迁移前先运行 skillshare collect codex --dry-run 检查差异，再按实际差异收集；同步前运行 skillshare sync --dry-run，检查同名技能冲突。不要直接强制覆盖尚未核对的本地修改。

## 其他电脑首次使用

先安装 skillshare 并登录 GitHub。在尚未初始化 skillshare 的电脑上执行：

```bash
skillshare init --remote https://github.com/xiepm/CodexTool.git --subdir skills --no-copy --no-skill
skillshare list
skillshare sync --dry-run
skillshare sync
```

初始化时选择该电脑实际安装的智能体。已有 skillshare 配置的电脑应先备份配置和技能，再调整 sources.skills 指向该仓库的 skills/；不要照搬本机绝对路径。

日常从其他电脑取回更新：skillshare pull --dry-run，然后 skillshare pull。pull 还会同步配置的目标目录，先检查目标中的独立修改。同一时间尽量只在一台电脑修改，先 pull 再改，改完 push。

## 核验和恢复

inventory/skillshare-2026-11-12.json 是初始快照的逐文件 SHA256；inventory/skillshare-sources-2026-11-12.json 记录原仓库和来源提交。这些是初始快照记录，后续改动后校验值会变化。

```bash
python3 scripts/verify-skills-backup.py
```

本机另有 ~/.local/share/skillshare/backups/ 下的 tar.gz、SHA256SUMS 和切换前的 config.before.yaml。压缩包包含 skills/ 与 manifest.json，可解压到空目录核验后使用。原 ~/.config/skillshare/skills 也保留作切换前副本。

技能文件备份不等于依赖环境备份。PaperSpine 的 references/installed-suite.json 指向原电脑的运行时，新电脑需重新安装其平台运行时；API Key、Python/R/Node、数据库与商业软件须分别配置。不要将个人凭据提交到这个公开仓库。
