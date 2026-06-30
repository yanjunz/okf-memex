# okf-memex

[English](README.md) | [中文](README.zh-CN.md)

> OKF 规范的 LLM Wiki 框架模板 —— 由 LLM 增量构建和维护的持久化、互链知识库。

受 [Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 启发，基于 [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 规范构建。以 Vannevar Bush 的 **Memex** 命名 —— 1945 年提出的个人策展知识库愿景，其"谁来维护"的未解之题终由 LLM 解决。

## 快速上手

### 创建你的 Wiki

```bash
# 克隆模板
git clone git@git.woa.com:yjzhuang/okf-memex.git

# 从模板创建新 wiki
python okf-memex/scripts/init_wiki.py create ~/Documents/my-wiki --topic "LLM技术"

# 初始化为你自己的仓库
cd ~/Documents/my-wiki
git init
git remote add origin <你的仓库地址>
git add -A && git commit -m "init: my wiki"
git push -u origin main

# 用 Obsidian 打开 wiki/ 目录作为 vault
```

### 更新脚手架文件

模板更新后，同步脚手架文件（scripts、AGENTS.md、.gitignore）到你的 wiki —— 不碰你的内容：

```bash
cd ~/okf-memex && git pull
python scripts/init_wiki.py update ~/Documents/my-wiki
cd ~/Documents/my-wiki
git diff                          # 查看变更
git add -A && git commit -m "Update scaffold from okf-memex template"
```

### 日常使用

1. **打开** `wiki/` 作为 Obsidian vault
2. **剪藏源文档** — 用 Obsidian Web Clipper，自动保存到 `Clippings/` → `raw/web/`
3. **摄入** — 告诉 Box：`"摄入 raw/web/xxx.md"` 或 `"批量摄入"`
4. **查询** — 随时提问，Box 从 wiki 综合回答
5. **Lint** — 定期让 Box 做健康检查

## 工作原理

```
你 (策划来源、提问)  →  Box AI (摄入/查询/Lint)  →  wiki/ (OKF Bundle)
                                ↕
                    Obsidian (浏览/手动编辑)
```

### 三层架构

| 层 | 位置 | 说明 |
|---|---|---|
| **原始资源** | `raw/` | 不可变源文档 —— 你的事实来源 |
| **Wiki** | `wiki/` | LLM 生成的知识页面 —— 一个 OKF Bundle |
| **Schema** | `AGENTS.md` | Box 操作手册 —— 工作流、模板、约定 |

### 三大操作

| 操作 | 流程 |
|---|---|
| **Ingest（摄入）** | Box 读源 → 与你讨论要点 → 创建 Source/Entity/Concept 页面 → 更新交叉引用、索引、日志 |
| **Query（查询）** | Box 读 wiki → 综合生成带引用的回答 → 询问是否存为 Synthesis 页面 |
| **Lint（检查）** | 脚本校验 OKF 合规 + 链接 → Box 审查矛盾/过时/孤儿页 → 建议修复 |

## CLI 工具

所有脚本仅依赖标准 Python 3，无第三方库。

```bash
# 脚手架管理
python scripts/init_wiki.py create <dir> --topic "..."   # 从模板创建新 wiki
python scripts/init_wiki.py update <dir>                  # 同步脚手架文件到已有 wiki

# Wiki 维护
python scripts/okf_check.py wiki/      # OKF v0.1 合规检查
python scripts/link_check.py wiki/     # 断链 + 孤儿页检测
python scripts/gen_index.py wiki/      # 从 frontmatter 重新生成 index.md
python scripts/parse_log.py wiki/ 10   # 显示最近 10 条日志

# 自动化
python scripts/scan_sources.py wiki/ raw/    # 扫描未处理的源文件
python scripts/scan_sources.py wiki/ raw/ --json  # JSON 输出（供定时任务用）
python scripts/auto_toggle.py <dir> ingest on     # 开启自动摄入
python scripts/auto_toggle.py <dir> ingest off    # 关闭自动摄入（仅通知）
python scripts/auto_toggle.py <dir> lint on       # 开启自动 Lint
python scripts/auto_toggle.py <dir> status        # 查看自动化状态
```

## 自动化

### 定时任务

通过 Box 创建每日定时任务，扫描 `raw/` 中的新源文件：

| 模式 | 行为 |
|---|---|
| **通知模式**（默认） | 扫描 → 企微推送待摄入列表 → 你手动让 Box 摄入 |
| **自动摄入模式** | 扫描 → Box 自动读文件、生成页面、更新索引/日志 → 推送结果摘要 |

切换模式：

```bash
python scripts/auto_toggle.py ~/my-wiki ingest on    # 开启自动摄入
python scripts/auto_toggle.py ~/my-wiki ingest off   # 仅通知（默认）
python scripts/auto_toggle.py ~/my-wiki status        # 查看当前状态
```

配置存储在 `.automation.json`（已 gitignore，按个人 wiki 独立配置）。

### 同步模板更新

```bash
cd ~/okf-memex && git pull
python scripts/init_wiki.py update ~/my-wiki
```

只同步 `scripts/`、`AGENTS.md`、`.gitignore` —— 你的 `wiki/`、`raw/`、`README.md` 不会被修改。

## 目录结构

```
okf-memex/                    # 模板仓库
├── AGENTS.md                 # Schema 层：Box 操作手册
├── scripts/                  # CLI 工具
│   ├── init_wiki.py          #   create / update wiki 脚手架
│   ├── okf_check.py          #   OKF v0.1 一致性校验
│   ├── link_check.py         #   断链 & 孤儿页检测
│   ├── gen_index.py          #   重新生成 index.md
│   ├── parse_log.py          #   显示最近日志条目
│   ├── scan_sources.py       #   扫描 raw/ 中未处理的源
│   └── auto_toggle.py        #   自动化开关控制
├── raw/                      # 不可变原始资源（模板目录，详见下文 "Raw 目录约定"）
│   ├── web/  papers/  videos/  books/  code/  podcasts/  notes/
│   └── assets/
├── wiki/                     # OKF Bundle（空模板）
│   ├── index.md              #   内容目录（OKF §6）
│   ├── log.md                #   操作日志（OKF §7）
│   ├── Clippings → ../raw/web  # 符号链接，供 Obsidian Web Clipper 使用
│   ├── entities/             #   type: Entity
│   ├── concepts/             #   type: Concept
│   ├── sources/              #   type: Source
│   └── synthesis/            #   type: Synthesis
└── .gitignore
```

## Raw 目录约定

`raw/` 是不可变的源文档层 —— Box 只读，所有摘要和分析都写入 `wiki/`。文件按内容类型分到固定子目录，`scan_sources.py` 仅扫描下表七个子目录。

| 子目录 | 存放内容 | 常用扩展名 |
|---|---|---|
| `web/` | Obsidian Web Clipper 剪藏的网页、博客文章（HTML 渲染为 Markdown）。`wiki/Clippings/` 通过符号链接指向此处。 | `.md`、`.html` |
| `papers/` | 学术论文、技术报告、白皮书。优先 PDF，必要时附带同名 `.md` 提取版。 | `.pdf`、`.md` |
| `videos/` | 视频字幕、文字稿、讲座笔记。**不要存原视频文件**（体积过大）。 | `.md`、`.txt`、`.srt` |
| `books/` | 电子书、章节高亮、阅读笔记。 | `.epub`、`.pdf`、`.md` |
| `code/` | 代码片段、notebook、gist，或需要锁版本的小项目源码。详见下方「代码存放模式」。 | `.ipynb`、`.md`、`.py`、`.ts` 等 |
| `podcasts/` | 播客文字稿、节目笔记。**不要存音频文件**。 | `.md`、`.txt` |
| `notes/` | 个人笔记：会议纪要、对话总结、手写备忘。不属于以上类别的内容。 | `.md`、`.txt` |
| `assets/` | 图片和被其他源引用的支撑文件（如剪藏截图）。**不会被 `scan_sources.py` 当作独立源扫描**。 | `.png`、`.jpg`、`.svg` 等 |

**命名约定**

- 路径格式：`raw/<类型>/<kebab-case-slug>.<扩展名>` —— 例如 `raw/papers/attention-is-all-you-need.pdf`
- Slug 用 kebab-case，且要稳定（Source 页面的 ID 由此派生，改名会破坏引用）
- 衍生文件与原文件同名放在一起，例如 `raw/videos/lecture-01.mp4` 配 `raw/videos/lecture-01.md`

**多级子目录**

- 任何子目录下都**支持嵌套**（`scan_sources.py` 用 `**/*` 递归扫描）。适合做自然分组：`raw/papers/<topic>/<slug>.pdf`、`raw/videos/<系列>/<集>.md`、`raw/code/<项目>/<文件>`
- 两层（`raw/<类型>/<分组>/<文件>`）是甜区，三层及以上就难记了
- `wiki/sources/` 本身保持平铺 —— 用 slug 前缀消歧（`wiki/sources/karpathy-micrograd.md`），不要用嵌套目录
- frontmatter 的 `resource:` 字段要写完整路径：`resource: raw/videos/karpathy/zero-to-hero/01-micrograd.md`

**代码存放模式**

`raw/code/` 三种 pattern，按意图选：

| 意图 | 放法 | 例子 |
|---|---|---|
| 单文件片段 / notebook / gist | 平铺单文件 | `raw/code/attention-impl.py`、`raw/code/rl-from-scratch.ipynb` |
| 锁定小项目某版本供深入研读 | 子目录 + 同名 `.md` 说明文件 | `raw/code/nanogpt/`（源码）+ `raw/code/nanogpt.md`（upstream URL、commit SHA、为什么锁这版） |
| 引用活跃维护的大仓库 | 不存本地 —— 只建 Source 页面 | `wiki/sources/transformers-lib.md` 里 `resource: https://github.com/huggingface/transformers` |

子目录方案中，**`.md` 说明文件是入口 Source** —— 建一个 `wiki/sources/<slug>.md`，`resource:` 指向目录（`resource: raw/code/nanogpt/`），在 Source 页面 body 里列出关键代码文件路径。目录里的 `.py`/`.ts` 文件会被扫到但视为伴随文件，不需要为它们各自建 Source。

**规则**

- 只有上表七个子目录会被扫描；放在 `raw/` 根下的文件会被忽略
- 可被摄入的扩展名：`.md`、`.pdf`、`.txt`、`.html`、`.epub`、`.ipynb` —— 其它类型需要配一个 `.md` 同名说明
- **永远不要修改 `raw/` 下的文件** —— 摘要、批注、标签全部写到 `wiki/sources/<slug>.md`

## Obsidian 集成

- **打开 `wiki/` 作为 vault**（不是仓库根目录）
- **Web Clipper**：保存到 `Clippings/` → 通过符号链接实际写入 `raw/web/`
- **图谱视图**：可视化 wiki 连接关系，发现枢纽页和孤儿页
- **Dataview**：查询 frontmatter（`type`、`tags`、`timestamp`）生成动态视图
- **Marp**：从 wiki 内容生成幻灯片
- Box 写入标准 markdown 链接 —— Obsidian 原生渲染
- 你可手动编辑任何页面 —— Box 在写入前重新读取，避免覆盖

## OKF 合规

- ✅ 每个概念文档有 YAML frontmatter 且包含非空 `type` 字段
- ✅ `index.md` 和 `log.md` 遵循 OKF §6/§7 结构
- ✅ Bundle 根声明 `okf_version: "0.1"`
- ✅ 交叉链接使用标准 markdown 语法（优先使用 bundle 相对绝对链接）
- ✅ 引用列于 `# Citations` 标题下

## 许可

个人使用。基于 Karpathy 的 LLM Wiki 模式和 Google 的 OKF 规范的开放理念构建。
