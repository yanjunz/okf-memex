# okf-memex

[English](README.md) | [中文](README.zh-CN.md)

> An OKF-compliant LLM Wiki framework template — scaffold a personal knowledge base where LLMs incrementally build and maintain a persistent, interlinked wiki.

Inspired by [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and built on the [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) specification. Named after Vannevar Bush's **Memex** — the 1945 vision of a personal, curated knowledge store, where the unsolved problem of "who does the maintenance" is finally solved by LLMs.

## Quick Start

### Create Your Wiki

```bash
# Clone the template
git clone git@git.woa.com:yjzhuang/okf-memex.git

# Scaffold a new wiki
python okf-memex/scripts/init_wiki.py ~/Documents/my-wiki --topic "LLM技术"

# Initialize as your own repo
cd ~/Documents/my-wiki
git init
git remote add origin <your-repo-url>
git add -A && git commit -m "init: my wiki"
git push -u origin main
```

### Daily Usage

1. **Open** the wiki directory as an Obsidian vault
2. **Add sources** to `raw/` subdirectories (Web Clipper, PDFs, subtitles, notes)
3. **Ingest** — tell Box: `"摄入 raw/web/xxx.md"`
4. **Query** — ask questions, Box reads the wiki and synthesizes answers
5. **Lint** — periodically ask Box to health-check the wiki

## How It Works

```
你 (策划来源、提问)  →  Box AI (摄入/查询/Lint)  →  wiki/ (OKF Bundle)
                                ↕
                    Obsidian (浏览/手动编辑)
```

### Three-Layer Architecture

| Layer | Location | Description |
|---|---|---|
| **Raw sources** | `raw/` | Immutable source documents — your source of truth |
| **Wiki** | `wiki/` | LLM-generated knowledge pages — an OKF Bundle |
| **Schema** | `AGENTS.md` | Box's operation manual — workflows, templates, conventions |

### Three Operations

| Operation | What happens |
|---|---|
| **Ingest** | Box reads source → discusses with you → creates Source/Entity/Concept pages → updates cross-refs, index, log |
| **Query** | Box reads wiki → synthesizes answer with citations → offers to file as Synthesis page |
| **Lint** | Scripts check OKF compliance + links → Box reviews contradictions/staleness/orphans → suggests fixes |

## CLI Tools

All scripts use standard Python 3 — no dependencies.

```bash
python scripts/okf_check.py wiki/      # OKF v0.1 合规检查
python scripts/link_check.py wiki/     # 断链 + 孤儿页检测
python scripts/gen_index.py wiki/      # 从 frontmatter 重新生成 index.md
python scripts/parse_log.py wiki/ 10   # 显示最近 10 条日志
python scripts/init_wiki.py <dir>      # 从模板创建新 wiki
```

## Directory Structure

```
okf-memex/                    # Template repository
├── AGENTS.md                 # Schema: Box's operation manual
├── scripts/                  # CLI tools (including init_wiki.py)
│   ├── init_wiki.py          #   Scaffold new wiki from template
│   ├── okf_check.py          #   OKF v0.1 conformance checker
│   ├── link_check.py         #   Broken link & orphan detector
│   ├── gen_index.py          #   Regenerate index.md
│   └── parse_log.py          #   Display recent log entries
├── raw/                      # Immutable source documents (template dirs)
│   ├── web/  papers/  videos/  books/  code/  podcasts/  notes/
│   └── assets/
├── wiki/                     # OKF Bundle (empty template)
│   ├── index.md              #   Content catalog (OKF §6)
│   ├── log.md                #   Operation log (OKF §7)
│   ├── entities/             #   type: Entity
│   ├── concepts/             #   type: Concept
│   ├── sources/              #   type: Source
│   └── synthesis/            #   type: Synthesis
└── .gitignore
```

## OKF Compliance

- ✅ Every concept document has YAML frontmatter with non-empty `type` field
- ✅ `index.md` and `log.md` follow OKF §6/§7 structure
- ✅ Bundle root declares `okf_version: "0.1"`
- ✅ Cross-links use standard markdown (bundle-relative absolute links preferred)
- ✅ Citations under `# Citations` heading

## Obsidian Integration

- **Web Clipper**: browser extension → `raw/web/` for quick sourcing
- **Graph view**: visualize wiki connections, find hubs and orphans
- **Dataview**: query frontmatter (`type`, `tags`, `timestamp`) for dynamic views
- **Marp**: generate slide decks from wiki content
- Box writes standard markdown links — Obsidian renders natively
- You can manually edit any page — Box re-reads before writing

## License

Personal use. Based on open ideas from Karpathy's LLM Wiki pattern and Google's OKF specification.
