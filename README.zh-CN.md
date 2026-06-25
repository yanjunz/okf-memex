# okf-memex

[English](README.md) | [中文](README.zh-CN.md)

> OKF 规范的 LLM Wiki 框架 —— 由 LLM 增量构建和维护的持久化、互链知识库。

受 [Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 启发，基于 [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 规范构建。以 Vannevar Bush 的 **Memex** 命名 —— 1945 年提出的个人策展知识库愿景，其"谁来维护"的未解之题终由 LLM 解决。

## 这是什么？

一个构建个人知识库的框架：

- **你**：策划来源、引导分析、提出问题
- **Box AI**：摄入源文档、撰写 wiki 页面、交叉引用、维护一致性
- **Obsidian**：作为浏览器和手动编辑器 —— 与 Box 双向共存
- **OKF v0.1**：确保 wiki 可移植、可 diff、可互操作

Wiki 是一个**持久化、复利增长的产物**。知识编译一次后持续更新，而非像 RAG 那样每次查询重新推导。

## 快速上手

### 1. 在 Obsidian 中打开

将 `okf-memex/` 目录作为 Obsidian vault 打开。你可以在文件管理器和图谱视图中看到完整结构。

### 2. 添加源文档

将源文件放入 `raw/` 对应子目录：

```bash
# 用 Obsidian Web Clipper 剪藏网页 → raw/web/
# 下载论文 → raw/papers/
# 保存视频字幕 → raw/videos/
```

### 3. 用 Box 摄入

告诉 Box：

> "摄入 raw/web/my-article.md"

Box 将：
1. 阅读源文档并与你讨论核心要点
2. 在 `wiki/sources/` 创建 Source 摘要页
3. 创建/更新 Entity 和 Concept 页面
4. 更新交叉引用、`index.md` 和 `log.md`
5. 运行 OKF 一致性校验

### 4. 查询

问 Box：

> "RAG 和 LLM Wiki 模式的区别是什么？"

Box 读取 wiki、综合生成带引用的回答，并询问是否存为 Synthesis 页面。

### 5. 健康检查

定期让 Box：

> "Lint 一下 wiki"

Box 运行所有检查，审查矛盾/过时/孤儿页面，并建议修复。

## 目录结构

```
okf-memex/
├── AGENTS.md              # Schema 层：Box 操作手册
├── raw/                   # 不可变原始资源
│   ├── web/               #   网页文章（Obsidian Web Clipper）
│   ├── papers/            #   学术论文（PDF）
│   ├── videos/            #   视频字幕/笔记
│   ├── books/             #   书籍章节
│   ├── code/              #   GitHub 仓库 / 代码片段
│   ├── podcasts/          #   播客转写文本
│   └── notes/             #   个人笔记 / 会议记录
├── wiki/                  # OKF Bundle（Box 维护此层）
│   ├── index.md           #   内容目录（OKF §6）
│   ├── log.md             #   操作日志（OKF §7）
│   ├── entities/          #   type: Entity
│   ├── concepts/          #   type: Concept
│   ├── sources/           #   type: Source
│   └── synthesis/         #   type: Synthesis
├── scripts/               # 轻量 CLI 工具
│   ├── okf_check.py       #   OKF v0.1 一致性校验
│   ├── link_check.py      #   断链 & 孤儿页检测
│   ├── gen_index.py       #   从 frontmatter 重新生成 index.md
│   └── parse_log.py       #   显示最近日志条目
└── .gitignore
```

## CLI 工具

所有脚本仅依赖标准 Python 3，无第三方库。

```bash
# 检查 OKF v0.1 合规性
python scripts/okf_check.py wiki/

# 检测断链和孤儿页面
python scripts/link_check.py wiki/

# 从页面 frontmatter 重新生成 index.md
python scripts/gen_index.py wiki/

# 显示最近 10 条日志
python scripts/parse_log.py wiki/ 10
```

## OKF 合规

本 wiki bundle 严格遵从 [OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)：

- ✅ 每个概念文档有 YAML frontmatter 且包含非空 `type` 字段
- ✅ `index.md` 和 `log.md` 遵循 OKF §6/§7 结构
- ✅ Bundle 根（`wiki/`）在根 `index.md` 中声明 `okf_version: "0.1"`
- ✅ 交叉链接使用标准 markdown 语法（优先使用 bundle 相对绝对链接）
- ✅ 引用列于 `# Citations` 标题下

## 三层架构

| 层 | 位置 | 说明 |
|---|---|---|
| **原始资源** | `raw/` | 不可变源文档 —— 你的事实来源 |
| **Wiki** | `wiki/` | LLM 生成的知识页面 —— 一个 OKF Bundle |
| **Schema** | `AGENTS.md` | Box 操作手册 —— 工作流、模板、约定 |

## Obsidian 集成

- 将 `okf-memex/` 作为 Obsidian vault 打开
- Box 写入标准 markdown 链接 —— Obsidian 原生渲染
- **Web Clipper**：浏览器扩展 → `raw/web/`，快速获取来源
- **图谱视图**：可视化 wiki 连接关系，发现枢纽页和孤儿页
- **Dataview**：查询 frontmatter（`type`、`tags`、`timestamp`）生成动态视图
- **Marp**：从 wiki 内容生成幻灯片
- 你可手动编辑任何页面 —— Box 在写入前重新读取，避免覆盖你的编辑

## 创建新 Wiki

要创建不同主题的新 wiki，复制此结构：

```bash
cp -r okf-memex/ my-new-wiki/
cd my-new-wiki/

# 清空 demo 内容
rm -rf wiki/entities/* wiki/concepts/* wiki/sources/* wiki/synthesis/*
rm -rf raw/web/*

# 重置 index 和 log
# （编辑 wiki/index.md 和 wiki/log.md 重新开始）

# 如需调整领域约定，更新 AGENTS.md
```

## 许可

个人使用。基于 Karpathy 的 LLM Wiki 模式和 Google 的 OKF 规范的开放理念构建。
