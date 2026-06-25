# okf-memex

> An OKF-compliant LLM Wiki framework — where LLMs incrementally build and maintain a persistent, interlinked knowledge base.

Inspired by [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and built on the [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) specification. Named after Vannevar Bush's **Memex** — the 1945 vision of a personal, curated knowledge store with associative trails, where the unsolved problem of "who does the maintenance" is finally solved by LLMs.

## What is this?

A framework for building personal knowledge bases where:

- **You** curate sources, direct analysis, and ask questions
- **Box AI** ingests sources, writes wiki pages, cross-references, and maintains consistency
- **Obsidian** serves as your browser and manual editor — bidirectional coexistence with Box
- **OKF v0.1** ensures the wiki is portable, diffable, and interoperable

The wiki is a **persistent, compounding artifact**. Knowledge is compiled once and kept current, not re-derived on every query like RAG.

## Quick Start

### 1. Open in Obsidian

Open the `okf-memex/` directory as a vault in Obsidian. You'll see the full structure in the file explorer and the graph view.

### 2. Add a source

Drop a source file into the appropriate `raw/` subdirectory:

```bash
# e.g. clip a web article with Obsidian Web Clipper → raw/web/
# e.g. download a paper → raw/papers/
# e.g. save video subtitles → raw/videos/
```

### 3. Ingest with Box

Tell Box:

> "Ingest raw/web/my-article.md"

Box will:
1. Read the source and discuss key takeaways with you
2. Create a Source summary page in `wiki/sources/`
3. Create/update Entity and Concept pages
4. Update cross-references, `index.md`, and `log.md`
5. Run OKF conformance check

### 4. Query

Ask Box:

> "What's the difference between RAG and the LLM Wiki pattern?"

Box reads the wiki, synthesizes an answer with citations, and offers to file it as a Synthesis page.

### 5. Lint

Periodically ask Box:

> "Lint the wiki"

Box runs all checks, reviews for contradictions/staleness/orphans, and suggests fixes.

## Directory Structure

```
okf-memex/
├── AGENTS.md              # Schema: Box's operation manual
├── raw/                   # Immutable source documents
│   ├── web/               #   Web articles (Obsidian Web Clipper)
│   ├── papers/            #   Academic papers (PDF)
│   ├── videos/            #   Video subtitles/notes
│   ├── books/             #   Book chapters
│   ├── code/              #   GitHub repos / code snippets
│   ├── podcasts/          #   Podcast transcripts
│   └── notes/             #   Personal notes / meeting records
├── wiki/                  # OKF Bundle (Box maintains this)
│   ├── index.md           #   Content catalog (OKF §6)
│   ├── log.md             #   Operation log (OKF §7)
│   ├── entities/          #   type: Entity
│   ├── concepts/          #   type: Concept
│   ├── sources/           #   type: Source
│   └── synthesis/         #   type: Synthesis
├── scripts/               # Lightweight CLI tools
│   ├── okf_check.py       #   OKF v0.1 conformance checker
│   ├── link_check.py      #   Broken link & orphan page detector
│   ├── gen_index.py       #   Regenerate index.md from frontmatter
│   └── parse_log.py       #   Display recent log entries
└── .gitignore
```

## CLI Tools

All scripts use standard Python 3 — no dependencies.

```bash
# Check OKF v0.1 compliance
python scripts/okf_check.py wiki/

# Detect broken links and orphan pages
python scripts/link_check.py wiki/

# Regenerate index.md from page frontmatter
python scripts/gen_index.py wiki/

# Show last 10 log entries
python scripts/parse_log.py wiki/ 10
```

## OKF Compliance

This wiki bundle strictly conforms to [OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md):

- ✅ Every concept document has YAML frontmatter with a non-empty `type` field
- ✅ `index.md` and `log.md` follow OKF §6/§7 structure
- ✅ Bundle root (`wiki/`) declares `okf_version: "0.1"` in root `index.md`
- ✅ Cross-links use standard markdown syntax (bundle-relative absolute links preferred)
- ✅ Citations listed under `# Citations` heading

## Three-Layer Architecture

| Layer | Location | Description |
|---|---|---|
| **Raw sources** | `raw/` | Immutable source documents — your source of truth |
| **Wiki** | `wiki/` | LLM-generated knowledge pages — an OKF Bundle |
| **Schema** | `AGENTS.md` | Box's operation manual — workflows, templates, conventions |

## Obsidian Integration

- Open `okf-memex/` as an Obsidian vault
- Box writes standard markdown links — Obsidian renders them natively
- **Web Clipper**: browser extension → `raw/web/` for quick sourcing
- **Graph view**: visualize wiki connections, find hubs and orphans
- **Dataview**: query frontmatter (`type`, `tags`, `timestamp`) for dynamic views
- **Marp**: generate slide decks from wiki content
- You can manually edit any page — Box re-reads before writing to avoid clobbering

## Creating New Wikis

To start a new wiki on a different topic, copy this structure:

```bash
cp -r okf-memex/ my-new-wiki/
cd my-new-wiki/

# Clear demo content
rm -rf wiki/entities/* wiki/concepts/* wiki/sources/* wiki/synthesis/*
rm -rf raw/web/*

# Reset index and log
# (Edit wiki/index.md and wiki/log.md to start fresh)

# Update AGENTS.md if your domain needs different conventions
```

## License

Personal use. Based on open ideas from Karpathy's LLM Wiki pattern and Google's OKF specification.
