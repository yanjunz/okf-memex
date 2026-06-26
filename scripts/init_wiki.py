#!/usr/bin/env python3
"""Scaffold a new OKF-compliant LLM Wiki from the okf-memex template.

Creates a fresh wiki directory with clean structure, ready for content.

Usage:
    python init_wiki.py <target_dir> [--topic "主题名称"] [--author "作者"]

Examples:
    python init_wiki.py ~/Documents/my-llm-wiki --topic "LLM技术"
    python init_wiki.py ./team-wiki --topic "团队知识库" --author "团队名"

Exit codes:
    0 — wiki scaffolded successfully
    1 — error
"""

import sys
import os
import shutil
import argparse


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ROOT = os.path.dirname(SCRIPT_DIR)  # okf-memex/ root


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new OKF LLM Wiki from okf-memex template."
    )
    parser.add_argument("target", help="Target directory path for the new wiki")
    parser.add_argument("--topic", default="My Wiki", help="Wiki topic/name (default: My Wiki)")
    parser.add_argument("--author", default="", help="Author name (default: git config user.name)")
    args = parser.parse_args()

    target = os.path.abspath(args.target)
    topic = args.topic
    author = args.author or "wiki author"

    if os.path.exists(target):
        print(f"Error: {target} already exists. Choose a new directory.")
        sys.exit(1)

    print(f"Scaffolding wiki: {topic}")
    print(f"Target: {target}")
    print()

    # Copy template structure
    shutil.copytree(TEMPLATE_ROOT, target, ignore=shutil.ignore_patterns(
        ".git", ".thumbs", "__pycache__", ".DS_Store", "*.pyc"
    ))

    # Clean demo content from wiki/
    wiki_dirs = ["entities", "concepts", "sources", "synthesis"]
    for d in wiki_dirs:
        dir_path = os.path.join(target, "wiki", d)
        # Remove everything except .gitkeep
        for item in os.listdir(dir_path):
            if item != ".gitkeep":
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

    # Clean demo content from raw/
    raw_dirs = ["web", "papers", "videos", "books", "code", "podcasts", "notes"]
    for d in raw_dirs:
        dir_path = os.path.join(target, "raw", d)
        if os.path.exists(dir_path):
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path) and item != "assets":
                    shutil.rmtree(item_path)

    # Write fresh index.md
    index_path = os.path.join(target, "wiki", "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"""---
okf_version: "0.1"
---

# Wiki Index

## Entities

*No entity pages yet.*

## Concepts

*No concept pages yet.*

## Sources

*No source pages yet.*

## Synthesis

*No synthesis pages yet.*
""")

    # Write fresh log.md
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    log_path = os.path.join(target, "wiki", "log.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"""# Wiki Update Log

## {now}

* **Initialization**: Created wiki "{topic}" from okf-memex template.
""")

    # Update AGENTS.md — no changes needed, it's generic

    # Write fresh README
    readme_path = os.path.join(target, "README.md")
    slug = os.path.basename(target)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"""# {topic}

> Based on [okf-memex](https://git.woa.com/yjzhuang/okf-memex) — an OKF-compliant LLM Wiki framework.

## Quick Start

1. Open this directory as an Obsidian vault
2. Drop source files into `raw/` subdirectories
3. Tell Box: "摄入 raw/web/xxx.md"
4. Query: ask questions against the wiki
5. Lint: periodically ask Box to health-check the wiki

## CLI Tools

```bash
python scripts/okf_check.py wiki/     # OKF 合规检查
python scripts/link_check.py wiki/    # 断链 + 孤儿页检测
python scripts/gen_index.py wiki/     # 重新生成 index.md
python scripts/parse_log.py wiki/ 10  # 查看最近日志
```

## Structure

See [okf-memex](https://git.woa.com/yjzhuang/okf-memex) for framework documentation.
""")

    # Remove the Chinese README and design spec from personal wiki
    zh_readme = os.path.join(target, "README.zh-CN.md")
    if os.path.exists(zh_readme):
        os.remove(zh_readme)

    # Remove init_wiki.py from personal copy (it's a template tool)
    init_script = os.path.join(target, "scripts", "init_wiki.py")
    if os.path.exists(init_script):
        os.remove(init_script)

    print("✓ Directory structure created")
    print("✓ Demo content cleared")
    print("✓ Fresh index.md and log.md generated")
    print("✓ README.md written")
    print()
    print("Next steps:")
    print(f"  1. cd {target}")
    print(f"  2. git init && git add -A && git commit -m 'init: {topic}'")
    print(f"  3. git remote add origin <your-repo-url>")
    print(f"  4. git push -u origin main")
    print(f"  5. Open {target} as Obsidian vault")
    print(f"  6. Add sources to raw/ and tell Box to ingest")
    sys.exit(0)


if __name__ == "__main__":
    main()
