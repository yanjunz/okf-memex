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
python okf-memex/scripts/init_wiki.py ~/Documents/my-wiki --topic "LLM技术"

# 初始化为你自己的仓库
cd ~/Documents/my-wiki
git init
git remote add origin <你的仓库地址>
git add -A && git commit -m "init: my wiki"
git push -u origin main
```

### 日常使用

1. **打开** wiki 目录作为 Obsidian vault
2. **添加源** 到 `raw/` 子目录（Web Clipper 剪藏、PDF、字幕、笔记）
3. **摄入** — 告诉 Box：`"摄入 raw/web/xxx.md"`
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
python scripts/okf_check.py wiki/      # OKF v0.1 合规检查
python scripts/link_check.py wiki/     # 断链 + 孤儿页检测
python scripts/gen_index.py wiki/      # 从 frontmatter 重新生成 index.md
python scripts/parse_log.py wiki/ 10   # 显示最近 10 条日志
python scripts/init_wiki.py <dir>      # 从模板创建新 wiki
```

## 目录结构

```
okf-memex/                    # 模板仓库
├── AGENTS.md                 # Schema 层：Box 操作手册
├── scripts/                  # CLI 工具（含 init_wiki.py）
│   ├── init_wiki.py          #   从模板创建新 wiki
│   ├── okf_check.py          #   OKF v0.1 一致性校验
│   ├── link_check.py         #   断链 & 孤儿页检测
│   ├── gen_index.py          #   重新生成 index.md
│   └── parse_log.py          #   显示最近日志条目
├── raw/                      # 不可变原始资源（模板目录）
│   ├── web/  papers/  videos/  books/  code/  podcasts/  notes/
│   └── assets/
├── wiki/                     # OKF Bundle（空模板）
│   ├── index.md              #   内容目录（OKF §6）
│   ├── log.md                #   操作日志（OKF §7）
│   ├── entities/             #   type: Entity
│   ├── concepts/             #   type: Concept
│   ├── sources/              #   type: Source
│   └── synthesis/            #   type: Synthesis
└── .gitignore
```

## OKF 合规

- ✅ 每个概念文档有 YAML frontmatter 且包含非空 `type` 字段
- ✅ `index.md` 和 `log.md` 遵循 OKF §6/§7 结构
- ✅ Bundle 根声明 `okf_version: "0.1"`
- ✅ 交叉链接使用标准 markdown 语法（优先使用 bundle 相对绝对链接）
- ✅ 引用列于 `# Citations` 标题下

## Obsidian 集成

- **Web Clipper**：浏览器扩展 → `raw/web/`，快速获取来源
- **图谱视图**：可视化 wiki 连接关系，发现枢纽页和孤儿页
- **Dataview**：查询 frontmatter（`type`、`tags`、`timestamp`）生成动态视图
- **Marp**：从 wiki 内容生成幻灯片
- Box 写入标准 markdown 链接 —— Obsidian 原生渲染
- 你可手动编辑任何页面 —— Box 在写入前重新读取，避免覆盖

## 许可

个人使用。基于 Karpathy 的 LLM Wiki 模式和 Google 的 OKF 规范的开放理念构建。
