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
python okf-memex/scripts/init_wiki.py create ~/Documents/my-wiki --topic "LLM技术"

# Initialize as your own repo
cd ~/Documents/my-wiki
git init
git remote add origin <your-repo-url>
git add -A && git commit -m "init: my wiki"
git push -u origin main

# Open wiki/ as Obsidian vault
```

### Update Scaffold Files

When the template is updated, sync scaffold files (scripts, AGENTS.md, .gitignore) to your wiki — never touches your content:

```bash
cd ~/okf-memex && git pull
python scripts/init_wiki.py update ~/Documents/my-wiki
cd ~/Documents/my-wiki
git diff                          # review changes
git add -A && git commit -m "Update scaffold from okf-memex template"
```

### Daily Usage

1. **Open** `wiki/` as an Obsidian vault
2. **Clip sources** — use Obsidian Web Clipper, saves to `Clippings/` → `raw/web/` automatically
3. **Ingest** — tell Box: `"摄入 raw/web/xxx.md"` or `"批量摄入"`
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
# Scaffold & update
python scripts/init_wiki.py create <dir> --topic "..."   # Create new wiki from template
python scripts/init_wiki.py update <dir>                  # Sync scaffold files to existing wiki

# Wiki maintenance
python scripts/okf_check.py wiki/      # OKF v0.1 合规检查
python scripts/link_check.py wiki/     # 断链 + 孤儿页检测
python scripts/gen_index.py wiki/      # 从 frontmatter 重新生成 index.md
python scripts/parse_log.py wiki/ 10   # 显示最近 10 条日志

# Automation
python scripts/scan_sources.py wiki/ raw/    # 扫描未处理的源文件
python scripts/scan_sources.py wiki/ raw/ --json  # JSON 输出（供定时任务用）
python scripts/auto_toggle.py <dir> ingest on     # 开启自动摄入
python scripts/auto_toggle.py <dir> ingest off    # 关闭自动摄入（仅通知）
python scripts/auto_toggle.py <dir> lint on       # 开启自动 Lint
python scripts/auto_toggle.py <dir> status        # 查看自动化状态
```

## Automation

### Scheduled Task

Set up a daily scheduled task (via Box) to scan `raw/` for new sources:

| Mode | Behavior |
|---|---|
| **Notification** (default) | Scan → push WeCom notification with pending source list → you ingest manually |
| **Auto-ingest** | Scan → Box automatically reads, generates pages, updates index/log → push result summary |

Toggle modes:

```bash
python scripts/auto_toggle.py ~/my-wiki ingest on    # Enable auto-ingest
python scripts/auto_toggle.py ~/my-wiki ingest off   # Notification only (default)
python scripts/auto_toggle.py ~/my-wiki status        # Check current status
```

Config is stored in `.automation.json` (gitignored, per-wiki preference).

### Sync Template Updates

```bash
cd ~/okf-memex && git pull
python scripts/init_wiki.py update ~/my-wiki
```

Only touches `scripts/`, `AGENTS.md`, `.gitignore` — your `wiki/`, `raw/`, `README.md` are never modified.

## Directory Structure

```
okf-memex/                    # Template repository
├── AGENTS.md                 # Schema: Box's operation manual
├── scripts/                  # CLI tools
│   ├── init_wiki.py          #   create / update wiki scaffold
│   ├── okf_check.py          #   OKF v0.1 conformance checker
│   ├── link_check.py         #   Broken link & orphan detector
│   ├── gen_index.py          #   Regenerate index.md
│   ├── parse_log.py          #   Display recent log entries
│   ├── scan_sources.py       #   Scan raw/ for unprocessed sources
│   └── auto_toggle.py        #   Toggle automation switches
├── raw/                      # Immutable source documents (see "Raw Directory Conventions" below)
│   ├── web/  papers/  videos/  books/  code/  podcasts/  notes/
│   └── assets/
├── wiki/                     # OKF Bundle (empty template)
│   ├── index.md              #   Content catalog (OKF §6)
│   ├── log.md                #   Operation log (OKF §7)
│   ├── Clippings → ../raw/web  # Symlink for Obsidian Web Clipper
│   ├── entities/             #   type: Entity
│   ├── concepts/             #   type: Concept
│   ├── sources/              #   type: Source
│   └── synthesis/            #   type: Synthesis
└── .gitignore
```

## Raw Directory Conventions

`raw/` is the immutable source layer — Box reads but never writes. Files are sorted into fixed subdirectories by content type; `scan_sources.py` only scans the seven subdirs below.

| Subdir | What goes here | Typical extensions |
|---|---|---|
| `web/` | Web Clipper output, saved articles/blog posts (HTML rendered to Markdown). `wiki/Clippings/` symlinks here. | `.md`, `.html` |
| `papers/` | Academic papers, technical reports, whitepapers. PDF primary; `.md` extraction alongside if needed. | `.pdf`, `.md` |
| `videos/` | Video transcripts, subtitles, lecture notes. **Don't store raw video files** (size). | `.md`, `.txt`, `.srt` |
| `books/` | Book chapters, highlights, ebooks. | `.epub`, `.pdf`, `.md` |
| `code/` | Notable code snippets, Jupyter notebooks, gists. **NOT entire repos** — link to GitHub from a Source page instead. | `.ipynb`, `.md`, `.py`, `.ts`, etc. |
| `podcasts/` | Podcast transcripts, episode notes. **Don't store audio files**. | `.md`, `.txt` |
| `notes/` | Personal notes: meeting notes, conversation summaries, hand-authored memos. Anything that doesn't fit above. | `.md`, `.txt` |
| `assets/` | Images and supporting files referenced by other sources (e.g. clipper screenshots). **Not scanned by `scan_sources.py`** — these are not standalone sources. | `.png`, `.jpg`, `.svg`, etc. |

**Naming**

- Path format: `raw/<type>/<kebab-case-slug>.<ext>` — e.g. `raw/papers/attention-is-all-you-need.pdf`
- Use kebab-case slugs and keep them stable (Source page IDs derive from these; renaming breaks references)
- Companion files share the base name: `raw/videos/lecture-01.mp4` + `raw/videos/lecture-01.md`

**Rules**

- Only the seven subdirs above are scanned; files placed at `raw/` root are ignored
- Scannable extensions: `.md`, `.pdf`, `.txt`, `.html`, `.epub`, `.ipynb` — other types need a `.md` companion
- **Never modify files under `raw/`** — annotations and summaries live in `wiki/sources/<slug>.md`

## Obsidian Integration

- **Open `wiki/` as vault** — not the repo root
- **Web Clipper**: saves to `Clippings/` → actually writes to `raw/web/` via symlink
- **Graph view**: visualize wiki connections, find hubs and orphans
- **Dataview**: query frontmatter (`type`, `tags`, `timestamp`) for dynamic views
- **Marp**: generate slide decks from wiki content
- Box writes standard markdown links — Obsidian renders natively
- You can manually edit any page — Box re-reads before writing

## OKF Compliance

- ✅ Every concept document has YAML frontmatter with non-empty `type` field
- ✅ `index.md` and `log.md` follow OKF §6/§7 structure
- ✅ Bundle root declares `okf_version: "0.1"`
- ✅ Cross-links use standard markdown (bundle-relative absolute links preferred)
- ✅ Citations under `# Citations` heading

## License

Personal use. Based on open ideas from Karpathy's LLM Wiki pattern and Google's OKF specification.
