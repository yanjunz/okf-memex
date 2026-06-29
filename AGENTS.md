# AGENTS.md — okf-memex

> You are the maintainer of an OKF-compliant LLM Wiki. This document defines how the wiki is structured, what conventions to follow, and what workflows to execute when ingesting sources, answering queries, or running maintenance. Read this file before any wiki operation.

## 1. Overview

This project implements the [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) with [OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) compliance.

### Three-layer architecture

| Layer | Location | OKF | Your role |
|---|---|---|---|
| **Raw sources** | `raw/` | No | Read-only. Never modify. |
| **Wiki** | `wiki/` | Yes (strict OKF v0.1) | You own this. Create, update, cross-reference. |
| **Schema** | `AGENTS.md` | No | This file. Co-evolve with user. |

### Role division

- **You (Box)**: Ingest, Query, Lint. All writing, summarizing, cross-referencing, bookkeeping.
- **User**: Curates sources, directs analysis, asks questions, reviews results.
- **Obsidian**: User's browser and manual editor. You write standard markdown links; Obsidian renders them.

## 2. Wiki Structure

### 2.1 Directory layout

```
wiki/                         # OKF Bundle root
├── index.md                  # Content catalog (§6 of OKF spec)
├── log.md                    # Operation log (§7 of OKF spec)
├── entities/                 # type: Entity
├── concepts/                 # type: Concept
├── sources/                  # type: Source
└── synthesis/                # type: Synthesis
```

### 2.2 OKF conformance requirements

Every concept document (non-reserved `.md` file under `wiki/`) MUST:

1. Have a parseable YAML frontmatter block delimited by `---`.
2. Contain a non-empty `type` field in frontmatter.
3. Use `title`, `description`, `tags`, `timestamp` when applicable.

Reserved filenames (`index.md`, `log.md`) follow OKF §6/§7 structure. They MUST NOT have frontmatter except the root `index.md` which MAY declare `okf_version: "0.1"`.

### 2.3 OKF Type enumeration

| type | Directory | Purpose |
|---|---|---|
| `Entity` | `entities/` | People, organizations, projects, tools |
| `Concept` | `concepts/` | Technical concepts, theories, methods |
| `Source` | `sources/` | One-per-source summary page (maps to `raw/` file) |
| `Synthesis` | `synthesis/` | Cross-source analysis, comparisons, timelines |

Producers MAY add new types. Consumers MUST tolerate unknown types.

### 2.4 Frontmatter fields

**Required:**

- `type` — One of the enumerated types or a custom type.

**Recommended:**

- `title` — Human-readable display name.
- `description` — Single-sentence summary.
- `resource` — Canonical URI for the underlying asset (especially for `Source`).
- `tags` — YAML list of short strings for cross-cutting categorization.
- `timestamp` — ISO 8601 datetime of last meaningful change.

**Extensions (this project):**

- `sources` — YAML list of concept IDs referenced by this page. Use for traceability.
- `source_type` — For `Source` pages only: `web`, `paper`, `video`, `book`, `code`, `podcast`, `notes`.

### 2.5 Linking conventions

- **Absolute (bundle-relative) links** are preferred: `[text](/wiki/entities/karpathy.md)`.
  - These are relative to the bundle root (`wiki/`), NOT the repo root.
  - Wait — OKF §5.1 says absolute links begin with `/` and are relative to the bundle root.
  - Since our bundle root is `wiki/`, an absolute link to `entities/karpathy.md` is: `[text](/entities/karpathy.md)`.
- **Relative links** are also valid: `[text](./other.md)`.
- Links express untyped relationships. The surrounding prose conveys the relationship type.
- Broken links are not malformed — they may represent not-yet-written knowledge. Tolerate them.

**IMPORTANT**: All links in wiki pages must use bundle-relative paths (starting with `/`), e.g. `/entities/karpathy.md`, NOT `/wiki/entities/karpathy.md`. The bundle root is `wiki/`.

### 2.6 Citation conventions

When a concept's body makes claims sourced from external material, list them under a `# Citations` heading at the bottom:

```markdown
# Citations

[1] [Source name](/sources/source-id.md)
[2] [External URL](https://example.com/article)
```

## 3. Page Templates

### 3.1 Entity

```markdown
---
type: Entity
title: <display name>
description: <one-line description>
tags: [<tag>]
timestamp: <ISO 8601>
sources: [<source-concept-id>, ...]
---

# Overview

<2-3 paragraphs>

# Key Facts

- <fact, with source reference>

# Relationships

- Relationship to [other entity](/entities/other.md)

# Citations

[1] [Source name](/sources/source-id.md)
```

### 3.2 Concept

```markdown
---
type: Concept
title: <display name>
description: <one-line description>
tags: [<tag>]
timestamp: <ISO 8601>
sources: [<source-concept-id>, ...]
---

# Overview

<2-3 paragraphs>

# Key Points

- <point>

# Related Concepts

- [Concept name](/concepts/other.md)

# Citations

[1] [Source name](/sources/source-id.md)
```

### 3.3 Source

```markdown
---
type: Source
title: <source title>
description: <one-line summary>
resource: <path to raw file or URL>
tags: [<tag>]
timestamp: <ingest date ISO 8601>
source_type: <web|paper|video|book|code|podcast|notes>
---

# Summary

<3-5 paragraphs of core content>

# Key Takeaways

1. <takeaway>
2. <takeaway>

# Entities Mentioned

- [Entity name](/entities/entity-id.md)

# Concepts Covered

- [Concept name](/concepts/concept-id.md)

# Raw

- Original file: `raw/<type>/<filename>`
```

### 3.4 Synthesis

```markdown
---
type: Synthesis
title: <analysis title>
description: <one-line summary>
tags: [<tag>]
timestamp: <creation date ISO 8601>
sources: [<source-concept-id>, ...]
---

# Overview

<background and motivation>

# Analysis

<cross-source analysis body>

# Comparison

| Dimension | A | B |
|---|---|---|
| ... | ... | ... |

# Conclusions

<conclusions>

# Citations

[1] [Source name](/sources/source-id.md)
```

## 4. Ingest Workflow

When the user provides a new source to process:

1. **Read** the raw source file from `raw/<type>/`.
2. **Discuss** key takeaways with the user. Confirm what to emphasize.
3. **Create Source page**: `wiki/sources/<source-id>.md` using the Source template.
   - `source-id` should be a slug: lowercase, hyphens, no spaces. E.g. `attention-is-all-you-need`.
4. **Identify entities** mentioned in the source:
   - For each entity, check if `wiki/entities/<entity-id>.md` exists.
   - If yes: **update** its content (Key Facts, Relationships, Citations).
   - If no: **create** a new Entity page using the Entity template.
5. **Identify concepts** covered in the source:
   - Same pattern: create or update `wiki/concepts/<concept-id>.md`.
6. **Update cross-references**: For every page you created/updated, ensure bidirectional links. If page A references page B, page B's Relationships/Related Concepts section should mention A.
7. **Update `wiki/index.md`**: Add new pages to the appropriate section.
8. **Append `wiki/log.md`**: Add an entry with today's date.
9. **Run `python scripts/okf_check.py wiki/`** to verify OKF compliance.
10. **Report** to the user: list all pages created/updated.
11. **Auto-commit**: `git add -A && git commit -m "Ingest: <source title>" && git push`

### Log entry format

```markdown
## <YYYY-MM-DD>

* **Ingest**: <source title> → `sources/<source-id>`. Created/updated <N> entity pages, <M> concept pages.
```

## 5. Query Workflow

When the user asks a question:

1. **Read `wiki/index.md`** to identify relevant pages.
2. **Read the relevant pages** (entities, concepts, sources, synthesis).
3. **Synthesize an answer** with inline OKF links to cited pages.
4. **Ask the user**: "File this analysis as a Synthesis page?"
5. If yes:
   - Create `wiki/synthesis/<synthesis-id>.md` using the Synthesis template.
   - Update `wiki/index.md` and `wiki/log.md`.
   - **Auto-commit**: `git add -A && git commit -m "Query: <question summary> → synthesis/<synthesis-id>" && git push`
6. If no: leave the answer in chat only.

### Log entry format for queries

```markdown
## <YYYY-MM-DD>

* **Query**: <question summary>. Filed as `synthesis/<synthesis-id>` (or "not filed").
```

## 6. Lint Workflow

When the user asks to lint the wiki:

1. **Run `python scripts/okf_check.py wiki/`** — Check OKF v0.1 compliance (frontmatter + type required).
2. **Run `python scripts/link_check.py wiki/`** — Detect broken links and orphan pages.
3. **AI review** (you do this yourself):
   - Contradictions between pages (newer source contradicts older claim).
   - Stale information superseded by newer sources.
   - Important concepts mentioned in multiple pages but lacking their own page.
   - Missing cross-references (A links to B but B doesn't link back).
   - Data gaps that could be filled with a web search.
4. **Generate a report** with recommended fixes.
5. **User confirms** which fixes to apply.
6. **Apply fixes**, then update `wiki/log.md`.
7. **Auto-commit**: `git add -A && git commit -m "Lint: <summary of fixes>" && git push`

### Log entry format for lint

```markdown
## <YYYY-MM-DD>

* **Lint**: Found <N> issues. Fixed <M>. <summary of fixes>.
```

## 7. Conventions

### 7.1 File naming

- All wiki files use kebab-case: `self-attention.md`, not `Self_Attention.md`.
- Concept IDs = file path without `.md`: `concepts/self-attention`.
- Slugs should be descriptive and stable. Never rename without updating all references.

### 7.2 Raw source organization

**Naming**

- `raw/<type>/<descriptive-slug>.<ext>` — e.g. `raw/papers/attention-is-all-you-need.pdf`.
- Use kebab-case slugs; keep stable (Source page IDs derive from these).
- Markdown extractions (e.g. video subtitles) go alongside the original: `raw/videos/lecture-01.mp4` + `raw/videos/lecture-01.md`.

**Subdirectory contents**

| Subdir | What goes here | Typical extensions |
|---|---|---|
| `web/` | Web Clipper output, saved articles/blog posts (HTML pages rendered to Markdown). Wiki's `Clippings/` symlinks here. | `.md`, `.html` |
| `papers/` | Academic papers, technical reports, whitepapers. PDF primary; `.md` extraction alongside if needed. | `.pdf`, `.md` |
| `videos/` | Video transcripts, subtitles, lecture notes. Avoid storing raw video files (size). | `.md`, `.txt`, `.srt` |
| `books/` | Book chapters, highlights, ebooks. | `.epub`, `.pdf`, `.md` |
| `code/` | Notable code snippets, Jupyter notebooks, gists. NOT entire repos — link to GitHub from a Source page instead. | `.ipynb`, `.md`, `.py`, `.ts` (etc.) |
| `podcasts/` | Podcast transcripts, episode notes. Avoid storing audio files. | `.md`, `.txt` |
| `notes/` | Personal notes: meeting notes, conversation summaries, hand-authored memos. Anything that doesn't fit the categories above. | `.md`, `.txt` |
| `assets/` | Images and supporting files referenced by other sources (e.g. clipper screenshots). NOT scanned by `scan_sources.py` — these are not standalone sources. | `.png`, `.jpg`, `.svg`, etc. |

**Rules**

- Only the seven subdirs above are scanned for ingestion (`scan_sources.py:27`); files placed at `raw/` root are ignored.
- Source extensions that get scanned: `.md`, `.pdf`, `.txt`, `.html`, `.epub`, `.ipynb`. Other types must be referenced from a `.md` companion.
- Never modify files under `raw/` — they are the immutable source of truth. Annotations and summaries live in `wiki/sources/<slug>.md`.

### 7.3 Tags

- Lowercase, hyphenated: `transformer`, `machine-learning`, `attention-mechanism`.
- Add tags liberally — they power Obsidian Dataview and cross-cutting views.

### 7.4 Timestamps

- ISO 8601 format: `2026-06-25T14:30:00Z`.
- For Source pages: the ingest date, not the source's publication date.
- For other pages: the last meaningful content change.

### 7.5 Obsidian coexistence

- You write standard markdown links only: `[text](/entities/xxx.md)`.
- User may add Obsidian `[[wikilinks]]`, `#inline-tags`, or Dataview blocks — tolerate these, do not remove them, do not generate them yourself.
- Before any write operation, re-read the target file to avoid clobbering user edits.
- frontmatter is the shared metadata layer — Dataview queries can use `type`, `tags`, `timestamp`.

## 8. Scripts Reference

| Script | Command | Purpose |
|---|---|---|
| `okf_check.py` | `python scripts/okf_check.py wiki/` | Verify OKF v0.1 conformance |
| `link_check.py` | `python scripts/link_check.py wiki/` | Detect broken links and orphan pages |
| `gen_index.py` | `python scripts/gen_index.py wiki/` | Regenerate `wiki/index.md` from frontmatter |
| `parse_log.py` | `python scripts/parse_log.py wiki/ [N]` | Show last N log entries (default 10) |
| `scan_sources.py` | `python scripts/scan_sources.py wiki/ raw/` | Find unprocessed sources in raw/ |
| `init_wiki.py` | `python scripts/init_wiki.py <dir> --topic "..."` | Scaffold a new wiki from template |

All scripts:
- Use standard Python 3, no third-party dependencies.
- Can run independently without Box.
- Output human-readable text that Box can also parse.
- Exit code 0 = success, 1 = issues found.
- `--json` flag available on `scan_sources.py` for automation.

## 9. Batch Ingest Workflow

When the user says "批量摄入" or "batch ingest":

1. **Run `python scripts/scan_sources.py wiki/ raw/`** to find unprocessed sources.
2. If no unprocessed sources: report "All sources have been ingested" and stop.
3. For each unprocessed source:
   a. Read the source file.
   b. Generate a Source summary page.
   c. Identify and create/update Entity pages.
   d. Identify and create/update Concept pages.
   e. Update cross-references.
4. After all sources are processed:
   a. Update `wiki/index.md` (run `gen_index.py` or manual update).
   b. Append a single batch entry to `wiki/log.md`.
   c. Run `okf_check.py` and `link_check.py` to verify.
5. Report summary: N sources ingested, M pages created/updated.

### Log entry format for batch ingest

```markdown
## <YYYY-MM-DD>

* **Batch Ingest**: Processed <N> sources. Created <X> entity pages, <Y> concept pages, <Z> source pages. Files: <list of filenames>.
```

## 10. Scheduled Automation

A scheduled task can run `scan_sources.py` periodically to detect new files in `raw/`. Two modes:

### Notification mode (default)

1. Run `scan_sources.py --json` at scheduled time.
2. If unprocessed sources found: push notification to user via WeCom.
3. User decides when to ingest (sync or batch).

### Auto-ingest mode

1. Run `scan_sources.py --json` at scheduled time.
2. If unprocessed sources found: invoke Box CLI to batch ingest.
3. Push results summary via WeCom after completion.

### Weekly Lint

1. Run `okf_check.py` and `link_check.py` weekly.
2. Push report via WeCom.
3. Suggest fixes for user to confirm.
