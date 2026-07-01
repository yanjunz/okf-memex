# okf-memex

[English](README.md) | [中文](README.zh-CN.md)

> An OKF-compliant LLM Wiki framework template — scaffold a personal knowledge base where LLMs incrementally build and maintain a persistent, interlinked wiki.

Inspired by [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and built on the [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) specification. Named after Vannevar Bush's **Memex** — the 1945 vision of a personal, curated knowledge store, where the unsolved problem of "who does the maintenance" is finally solved by LLMs.

## Quick Start

### Create Your Wiki

```bash
# Clone the template
git clone git@git.woa.com:yjzhuang/okf-memex.git

# Scaffold a new wiki (bundle dir defaults to wiki/)
python okf-memex/scripts/init_wiki.py create ~/Documents/my-wiki --topic "LLM技术"

# For multi-wiki Obsidian setups, give the bundle a distinctive name:
python okf-memex/scripts/init_wiki.py create ~/yjzhuang-wiki --topic "..." --bundle-name yjzhuang

# Initialize as your own repo
cd ~/Documents/my-wiki
git init
git remote add origin <your-repo-url>
git add -A && git commit -m "init: my wiki"
git push -u origin main

# Open the bundle dir (wiki/ by default, or your --bundle-name) as Obsidian vault
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

**All maintenance scripts accept an optional path argument** — when omitted, they walk up from CWD looking for `.okf-config.json` to resolve the bundle directory (falls back to `wiki/`).

```bash
# Scaffold & update (target dir required)
python scripts/init_wiki.py create <dir> --topic "..." [--bundle-name yjzhuang]
python scripts/init_wiki.py update <dir>
python scripts/rename_bundle.py <new_name>            # Rename bundle dir (auto-resolve from CWD)

# Wiki maintenance (run from inside the repo, no path needed)
python scripts/okf_check.py       # OKF v0.1 conformance
python scripts/link_check.py      # broken links + orphans
python scripts/gen_index.py       # regenerate index.md
python scripts/parse_log.py 10    # show last 10 log entries

# Automation
python scripts/scan_sources.py            # scan raw/ for unprocessed sources
python scripts/scan_sources.py --json     # JSON output (for cron)
python scripts/auto_toggle.py ingest on   # enable auto-ingest
python scripts/auto_toggle.py ingest off  # notification only
python scripts/auto_toggle.py lint on     # enable weekly lint
python scripts/auto_toggle.py status      # show automation status

# Explicit paths still work for running from outside the repo:
python scripts/okf_check.py ~/yjzhuang-wiki/yjzhuang/
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
│   ├── rename_bundle.py      #   Rename the bundle dir (updates .okf-config.json)
│   ├── okf_paths.py          #   bundle path resolver (shared by other scripts)
│   ├── okf_check.py          #   OKF v0.1 conformance checker
│   ├── link_check.py         #   Broken link & orphan detector
│   ├── gen_index.py          #   Regenerate index.md
│   ├── parse_log.py          #   Display recent log entries
│   ├── scan_sources.py       #   Scan raw/ for unprocessed sources
│   └── auto_toggle.py        #   Toggle automation switches
├── raw/                      # Immutable source documents (see "Raw Directory Conventions" below)
│   ├── web/  papers/  videos/  books/  code/  podcasts/  notes/
│   └── assets/
├── wiki/                     # OKF Bundle (empty template; can be renamed via --bundle-name)
│   ├── index.md              #   Content catalog (OKF §6)
│   ├── log.md                #   Operation log (OKF §7)
│   ├── Clippings → ../raw/web  # Symlink for Obsidian Web Clipper
│   ├── entities/             #   type: Entity
│   ├── concepts/             #   type: Concept
│   ├── sources/              #   type: Source
│   └── synthesis/            #   type: Synthesis
├── .okf-config.json          # Optional: written by init_wiki.py when --bundle-name is custom
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
| `code/` | Code snippets, notebooks, gists, or small project trees worth version-locking. See **Code patterns** below. | `.ipynb`, `.md`, `.py`, `.ts`, etc. |
| `podcasts/` | Podcast transcripts, episode notes. **Don't store audio files**. | `.md`, `.txt` |
| `notes/` | Personal notes: meeting notes, conversation summaries, hand-authored memos. Anything that doesn't fit above. | `.md`, `.txt` |
| `assets/` | Images and supporting files referenced by other sources (e.g. clipper screenshots). **Not scanned by `scan_sources.py`** — these are not standalone sources. | `.png`, `.jpg`, `.svg`, etc. |

**Naming**

- Path format: `raw/<type>/<kebab-case-slug>.<ext>` — e.g. `raw/papers/attention-is-all-you-need.pdf`
- Use kebab-case slugs and keep them stable (Source page IDs derive from these; renaming breaks references)
- Companion files share the base name: `raw/videos/lecture-01.mp4` + `raw/videos/lecture-01.md`

**Nested subdirectories**

- Multi-level paths under any subdir are supported (`scan_sources.py` recursively globs `**/*`). Use for natural grouping: `raw/papers/<topic>/<slug>.pdf`, `raw/videos/<series>/<ep>.md`, `raw/code/<project>/<file>`
- Two levels (`raw/<type>/<group>/<file>`) is the sweet spot. Three+ levels become hard to remember
- `wiki/sources/` itself stays flat — disambiguate with slug prefixes (`wiki/sources/karpathy-micrograd.md`), not nested directories
- The `resource:` frontmatter field must record the full path: `resource: raw/videos/karpathy/zero-to-hero/01-micrograd.md`

**Code patterns**

Three patterns for `raw/code/`, pick by intent:

| Intent | Pattern | Example |
|---|---|---|
| Single snippet / notebook / gist | Flat file | `raw/code/attention-impl.py`, `raw/code/rl-from-scratch.ipynb` |
| Version-lock a small project for study | Subdirectory + companion `.md` entry | `raw/code/nanogpt/` (source files) + `raw/code/nanogpt.md` (upstream URL, commit SHA, why pinned) |
| Reference a live large repo | No raw file — Source page only | `wiki/sources/transformers-lib.md` with `resource: https://github.com/huggingface/transformers` |

For the subdirectory pattern: the **`.md` entry file is the canonical Source**. Create one `wiki/sources/<slug>.md` whose `resource:` points to the directory (`resource: raw/code/nanogpt/`); list key code files inside that Source page's body. The scanner will see `.py`/`.ts` files inside the dir but they are companion files, not standalone sources.

**Rules**

- Only the seven subdirs above are scanned; files placed at `raw/` root are ignored
- Scannable extensions: `.md`, `.pdf`, `.txt`, `.html`, `.epub`, `.ipynb` — other types need a `.md` companion
- **Never modify files under `raw/`** — annotations and summaries live in `wiki/sources/<slug>.md`

## Multi-Wiki Coexistence

If you maintain multiple independent wikis (e.g. `~/yjzhuang-wiki/` and `~/home-wiki/`), opening each one's `wiki/` subdirectory in Obsidian shows **"wiki" for both vaults** — indistinguishable. Obsidian locks the vault name to the folder name; renaming changes the disk folder; symlinks get resolved via realpath. There's no display-only workaround.

The fix: **give each wiki's bundle a distinctive name**.

```bash
# Specify at creation time
python scripts/init_wiki.py create ~/yjzhuang-wiki --topic "..." --bundle-name yjzhuang
python scripts/init_wiki.py create ~/home-wiki --topic "..." --bundle-name home

# Resulting structure:
#   ~/yjzhuang-wiki/yjzhuang/   ← Obsidian shows "yjzhuang"
#   ~/home-wiki/home/           ← Obsidian shows "home"
```

The bundle name is recorded in `.okf-config.json` at the repo root, and all scripts read it automatically:

```json
{"bundle": "yjzhuang"}
```

**Migrating an existing `wiki/` repo**:

Use the rename helper — one command does the rename + writes `.okf-config.json`:

```bash
cd ~/yjzhuang-wiki
python scripts/rename_bundle.py yjzhuang
git add -A && git commit -m "Rename bundle: wiki/ → yjzhuang/"
git push
```

`raw/`, `scripts/`, `AGENTS.md` are untouched. Bundle-relative links inside the wiki (`/entities/xxx.md` etc.) keep working — they're relative to the bundle root, so renaming the directory doesn't change their semantics. The Clippings symlink is relative, so it follows the rename automatically.

Reverting to the default `wiki/`? `python scripts/rename_bundle.py wiki` removes `.okf-config.json` at the same time (the default name is implicit — no config needed).

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
