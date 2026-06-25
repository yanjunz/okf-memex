---
type: Concept
title: LLM Wiki Pattern
description: A pattern where LLMs incrementally build and maintain a persistent, interlinked markdown wiki instead of retrieving from raw documents at query time.
tags: [llm, knowledge-management, wiki, pattern]
timestamp: 2026-06-25T20:50:00Z
sources: [karpathy-llm-wiki]
---

# Overview

The LLM Wiki Pattern, proposed by [Andrej Karpathy](/entities/andrej-karpathy.md), is a paradigm shift from RAG-style retrieval to **incremental knowledge compilation**. Instead of retrieving chunks from raw documents at query time, the LLM builds and maintains a persistent, interlinked wiki of markdown files. When a new source is added, the LLM reads it, extracts key information, and integrates it into the existing wiki — updating entity pages, revising summaries, flagging contradictions, and strengthening synthesis.

The wiki is a **persistent, compounding artifact**. Knowledge accumulates over time. Every source added and every question asked makes the wiki richer.

# Key Points

- **Not RAG**: Knowledge is compiled once and kept current, not re-derived on every query
- **Three-layer architecture**: Raw sources (immutable) → Wiki (LLM-owned) → Schema (configuration)
- **Three operations**: [Ingest](#), [Query](#), [Lint](#)
- **Human role**: Curate sources, direct analysis, ask questions
- **LLM role**: Everything else — summarizing, cross-referencing, filing, bookkeeping
- **Scales to ~100 sources / hundreds of pages** with just index.md, no embedding infrastructure needed
- **Maintenance burden is near-zero** with LLMs — humans abandon wikis because maintenance grows faster than value; LLMs don't get bored

# Related Concepts

- [RAG vs Knowledge Compilation](/concepts/rag-vs-knowledge-compilation.md)
- [Memex](/concepts/memex.md)

# Citations

[1] [LLM Wiki gist](/sources/karpathy-llm-wiki.md)
