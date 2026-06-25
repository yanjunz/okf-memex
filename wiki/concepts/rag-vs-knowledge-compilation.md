---
type: Concept
title: RAG vs Knowledge Compilation
description: Contrast between retrieving from raw documents at query time (RAG) vs. incrementally compiling knowledge into a persistent wiki.
tags: [rag, llm, knowledge-management]
timestamp: 2026-06-25T20:50:00Z
sources: [karpathy-llm-wiki]
---

# Overview

Most people's experience with LLMs and documents follows the RAG pattern: upload files, retrieve relevant chunks at query time, generate an answer. This works, but the LLM **rediscovers knowledge from scratch on every question**. There's no accumulation. Ask a subtle question requiring synthesis of five documents, and the LLM must find and piece together fragments every time.

The [LLM Wiki Pattern](/concepts/llm-wiki-pattern.md) proposes the opposite: **knowledge compilation**. The LLM reads each source, extracts key information, and integrates it into a persistent wiki. The knowledge is compiled once and kept current.

# Key Points

| Dimension | RAG | LLM Wiki (Knowledge Compilation) |
|---|---|---|
| Knowledge state | Ephemeral — rediscovered each query | Persistent — compiled once, kept current |
| Accumulation | None | Compounds with every source and question |
| Cross-references | Must be discovered at query time | Already present in wiki structure |
| Contradiction detection | Ad hoc, per query | Flagged during ingest, tracked over time |
| Infrastructure | Embedding DB, vector search | Markdown files + index.md |
| Scale | Works at any scale with infrastructure | Works at moderate scale (~100 sources) without infrastructure |
| Best for | Large document corpora, one-off Q&A | Personal/team knowledge building over time |

# Related Concepts

- [LLM Wiki Pattern](/concepts/llm-wiki-pattern.md)
- [Memex](/concepts/memex.md)

# Citations

[1] [LLM Wiki gist](/sources/karpathy-llm-wiki.md)
