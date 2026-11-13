# GitHub Star 分类索引（laoshuterry）

FatMouse 的 GitHub Star 分类索引数据。共 **736** 个仓库、**22** 个分类，每个仓库都有一句中文简介和 2–5 个中文标签。

- 数据：[`data/stars.json`](data/stars.json)（主数据）、[`data/stars.csv`](data/stars.csv)（平铺表格，UTF-8 BOM，可直接用 Excel 打开）
- 页面：`docs/` 目录发布到 GitHub Pages → https://laoshuterry.github.io/github-stars/ （当前为占位测试页，正式页面待设计稿确认后由 RD 团队实现）
- `docs/stars.json` 是 `data/stars.json` 的副本，供页面同源加载。

## 数据结构（stars.json）

```jsonc
{
  "generated_at": "ISO 8601 时间",
  "user": "laoshuterry",
  "total": 736,
  "stats": { "archived": 42, "stale": 275, "summary_from_readme": 27, "summary_name_only": 5, "stale_cutoff": "2025-11-13" },
  "categories": [ { "id": "ai-agent-skills", "name_zh": "AI Agent 与编程 Skills", "description_zh": "…", "count": 46 } ],
  "repos": [ { …见下表… } ]
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `full_name` | string | `owner/repo`，唯一键 |
| `name` / `owner` | string | 仓库名 / 所有者 |
| `html_url` | string | GitHub 链接 |
| `description` | string | 原始英文/中文描述（可能为空） |
| `summary_zh` | string | 一句中文简介（≤60 字） |
| `category` | string | 分类 id，对应 `categories[].id` |
| `tags` | string[] | 2–5 个中文标签 |
| `language` | string\|null | 主语言 |
| `stargazers_count` / `forks_count` | number | Star 数 / Fork 数（抓取时） |
| `topics` | string[] | GitHub topics |
| `homepage` | string | 项目主页（可能为空） |
| `license` | string\|null | SPDX 许可证 id |
| `archived` | bool | 仓库已归档 |
| `stale` | bool | 最近推送早于 2025-11-13（超过 12 个月未更新） |
| `fork` | bool | 是否为 fork 仓库 |
| `pushed_at` / `created_at` / `updated_at` | string | ISO 8601（UTC） |
| `starred_at` | string | 用户点 Star 的时间（UTC） |
| `owner_avatar_url` | string | 所有者头像 |
| `summary_source` | string | `description` / `readme` / `name_only`（无描述也无 README，仅凭名称概述） |

stars.csv 字段同上，数组用 `|` 连接，另含 `category_name_zh`。

## 分类与数量

| id | 分类 | 数量 | 说明 |
|---|---|---|---|
| `ai-agent-skills` | AI Agent 与编程 Skills | 46 | Claude Code / Codex 等编程 Agent、Agent 框架、通用工程类 Skills 与 Agent 学习资料 |
| `design-slides` | 设计、PPT 与图表 | 23 | 设计工具、设计规范、AI 设计/前端审美 Skills、PPT 与图表生成 |
| `content-creation` | 自媒体与内容创作 | 17 | 小红书/公众号/X 等内容生产、排版、发布与运营工具和 Skills |
| `aigc-video` | AI 图像、视频与多媒体创作 | 33 | AI 生图/生视频模型、ComfyUI、提示词库、视频剪辑与动画生成 |
| `llm-ml` | 大模型与机器学习 | 48 | 大模型训练推理、机器学习框架、模型与 AI/深度学习教程书籍 |
| `cs-learning` | 计算机学习与面试 | 59 | CS 课程、编程教程、算法刷题、面试题、技术书籍与速查手册 |
| `life-growth` | 生活指南、成长与阅读 | 18 | 生活建议、健康、理财入门、人际、移民、一人公司与阅读资源 |
| `finance-blockchain` | 金融、量化与区块链 | 11 | 个人财务、量化投资、行情工具、比特币/以太坊 |
| `proxy` | 网络代理与科学上网 | 50 | 代理协议、客户端、面板、规则与相关教程 |
| `network-telecom` | 网络与通信协议 | 16 | 网络仿真、协议编解码、LTE/5G/3GPP、高性能网络 |
| `self-hosted` | 自托管服务与网盘 | 19 | 可自建的相册、影音、密码、通讯、文件与 WebDAV 服务 |
| `media` | 影音播放、下载与 BT | 33 | 视频/音乐播放器、下载器、直播录制、IPTV、BT 工具 |
| `audio-music` | 音频与音乐制作 | 33 | 合成器、音频插件、DAW、音频框架与 DSP 资源 |
| `devtools` | 开发工具、编辑器与终端 | 70 | IDE/编辑器配置、终端、字体、调试分析、构建与自动化工具 |
| `lang-lib` | 编程语言、框架与库 | 42 | 编程语言实现、通用框架、各语言库与 SDK |
| `web-frontend` | Web 前端、可视化与建站 | 23 | 前端框架/组件、图表可视化、图标字体、静态站点生成 |
| `os-hardware` | 操作系统、固件与硬件 | 41 | 内核、BIOS/UEFI、路由器固件、RISC-V/FPGA、开发板、飞控 |
| `security` | 安全与逆向工程 | 15 | 渗透测试、逆向/反编译、调试器、安全书籍与工具 |
| `games-graphics` | 游戏、图形与仿真 | 58 | 游戏源码/引擎、模拟器、渲染与图形学、物理/航天/机器人仿真、棋类 AI |
| `utilities` | 桌面与效率工具 | 29 | Windows/macOS 实用工具、文件传输清理、笔记与日常效率软件 |
| `awesome-lists` | Awesome 资源合集 | 31 | 各类 awesome 列表与资源导航 |
| `misc` | 其他 | 21 | 个人博客、杂项或难以归类的仓库 |

状态统计：已归档 42 个，超过 12 个月未更新（stale）275 个。

## 页面需求（给 RD 团队）

单个静态页面（`docs/index.html`，纯前端，无构建依赖亦可），中文界面：

1. 加载同目录下 `stars.json`（相对路径 `./stars.json`，不要依赖站点根目录）。
2. 左侧分类侧边栏：全部 + 各分类，显示数量；移动端折叠。
3. 顶部搜索框：匹配 `full_name`、`summary_zh`、`description`、`tags`、`topics`、`language`。
4. 排序：Star 数、最近更新（`pushed_at`）、点 Star 时间（`starred_at`），升/降序。
5. 筛选：语言、隐藏已归档/长期未更新。
6. 卡片：头像、仓库名（链接 GitHub）、`summary_zh`、标签、Star 数、语言、最近更新时间；`archived` / `stale` 徽章。
7. 美观现代、支持深色模式、响应式。正式实现需先出设计稿经用户确认。

## 自动更新流程

- **人工/AI 整理内容的唯一来源**：`data/curation.json`（`{full_name: {category, summary_zh, tags}}`），分类体系在 `data/categories.json`。
- `scripts/build_data.py`：通过公开 API 抓取 laoshuterry 的全部 Star（有 `GITHUB_TOKEN` 时带上），与 curation 合并，计算 `archived` / `stale`（以运行时间往前 365 天为界），写出 `docs/stars.json`；不在 curation 中的新 Star 归入 `uncategorized`（待整理）、`summary_zh` 为空，并列入 `data/uncurated.json`；已取消 Star 的仓库自动移除。内容未变时不更新 `generated_at`，避免空提交。
- `.github/workflows/update-stars.yml`：每天 02:00 UTC（巴基斯坦时间 07:00）、手动触发、或 `data/**` / `scripts/**` 有推送时运行；`docs/stars.json` 有变化就提交，并请求 Pages 重新构建。
- 整理新仓库：把 `data/uncurated.json` 中的条目补进 `data/curation.json` 并推送，工作流会自动重建页面数据。
- `data/stars.json` / `data/stars.csv` 是首次整理时的快照（含 `summary_source` 字段）；线上页面以 `docs/stars.json` 为准。

本地运行：`GITHUB_TOKEN=... python3 scripts/build_data.py`

旧的一次性脚本（`fetch_stars.sh`、`assign.py`、`build_dataset.py`）仅为首次整理留档。
