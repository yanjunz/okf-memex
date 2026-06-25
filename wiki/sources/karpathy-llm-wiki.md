---
type: Source
title: "LLM Wiki — A Pattern for Building Personal Knowledge Bases Using LLMs"
description: Karpathy's gist describing a pattern where LLMs incrementally build and maintain a persistent wiki instead of RAG-style retrieval.
resource: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
tags: [llm, knowledge-management, wiki, rag]
timestamp: 2026-06-25T20:50:00Z
source_type: web
---

# Summary

Karpathy proposes a fundamental shift from RAG (Retrieval-Augmented Generation) to **incremental knowledge compilation**. In RAG, the LLM rediscovers knowledge from scratch on every query — there's no accumulation. In the LLM Wiki pattern, the LLM reads each source, extracts key information, and integrates it into a persistent, interlinked markdown wiki. The knowledge is compiled once and kept current, not re-derived on every query.

The wiki is a **persistent, compounding artifact**. Cross-references are already there. Contradictions are already flagged. Synthesis reflects everything you've read. The wiki gets richer with every source added and every question asked.

The human never (or rarely) writes the wiki — the LLM writes and maintains all of it. The human's job is sourcing, exploration, and asking questions. The LLM does all the grunt work: summarizing, cross-referencing, filing, and bookkeeping.

# Key Takeaways

1. **RAG's limitation**: No knowledge accumulation. Each query rediscovers from scratch. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.
2. **Wiki as persistent artifact**: LLM incrementally builds and maintains a structured markdown wiki. Knowledge is compiled once, kept current.
3. **Three-layer architecture**: Raw sources (immutable) → Wiki (LLM-owned) → Schema (configuration file like CLAUDE.md/AGENTS.md).
4. **Three operations**: Ingest (process new source), Query (answer from wiki), Lint (health-check).
5. **index.md + log.md**: Content-oriented catalog + chronological operation log. Works at moderate scale (~100 sources, hundreds of pages) without embedding-based RAG.
6. **Human-LLM division**: Human curates sources, directs analysis, asks questions. LLM does everything else — the maintenance burden that makes humans abandon wikis is near-zero for LLMs.
7. **Memex connection**: Related to Vannevar Bush's 1945 Memex vision — personal, curated knowledge store with associative trails. The part Bush couldn't solve (who does the maintenance) is solved by LLMs.
8. **Obsidian integration**: Obsidian is the IDE, LLM is the programmer, wiki is the codebase. Web Clipper for sourcing, graph view for navigation, Dataview for dynamic views, Marp for presentations.

# Entities Mentioned

- [Andrej Karpathy](/entities/andrej-karpathy.md)
- [Vannevar Bush](/entities/vannevar-bush.md)
- [Obsidian](/entities/obsidian.md)

# Concepts Covered

- [LLM Wiki Pattern](/concepts/llm-wiki-pattern.md)
- [RAG vs Knowledge Compilation](/concepts/rag-vs-knowledge-compilation.md)
- [Memex](/concepts/memex.md)

# Raw

- Original file: `raw/web/karpathy-llm-wiki.md`
- Source URL: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
