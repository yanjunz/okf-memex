---
type: Entity
title: Obsidian
description: A local-first knowledge management app based on markdown files with bidirectional linking, graph view, and plugin ecosystem.
tags: [knowledge-management, markdown, tools]
timestamp: 2026-06-25T20:50:00Z
sources: [karpathy-llm-wiki]
---

# Overview

Obsidian is a local-first knowledge management application that stores notes as plain markdown files. It provides bidirectional linking, graph visualization, and a rich plugin ecosystem. In the [LLM Wiki Pattern](/concepts/llm-wiki-pattern.md), Obsidian serves as the human's browser and IDE for the wiki — "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

# Key Facts

- Stores notes as plain markdown files on local disk
- Supports bidirectional links and graph view for navigating connections
- Web Clipper browser extension converts web articles to markdown for sourcing
- Dataview plugin runs queries over page frontmatter (tags, dates, metadata)
- Marp plugin enables slide deck generation from markdown
- Compatible with git for version control

# Relationships

- Used as the browsing/editing layer in the [LLM Wiki Pattern](/concepts/llm-wiki-pattern.md)
- Dataview queries can operate on OKF frontmatter (`type`, `tags`, `timestamp`)

# Citations

[1] [LLM Wiki gist](/sources/karpathy-llm-wiki.md)
