#!/usr/bin/env python3
"""Scaffold and update OKF-compliant LLM Wikis from the okf-memex template.

Usage:
    # Create a new wiki
    python init_wiki.py create <target_dir> --topic "主题名称"

    # Update an existing wiki's scaffold files from template
    python init_wiki.py update <target_dir>

Examples:
    python init_wiki.py create ~/Documents/my-llm-wiki --topic "LLM技术"
    python init_wiki.py update ~/Documents/my-llm-wiki

Exit codes:
    0 — success
    1 — error
"""

import sys
import os
import shutil
import argparse
import hashlib
from datetime import datetime, timezone, timedelta


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ROOT = os.path.dirname(SCRIPT_DIR)  # okf-memex/ root

# Files synced by `update` — scaffold only, never touch content
SCAFFOLD_FILES = [
    "AGENTS.md",
    ".gitignore",
    "scripts/okf_check.py",
    "scripts/link_check.py",
    "scripts/gen_index.py",
    "scripts/parse_log.py",
    "scripts/scan_sources.py",
]


def file_hash(filepath):
    """Return MD5 hash of file content, or None if unreadable."""
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def cmd_create(args):
    """Create a new wiki from template."""
    target = os.path.abspath(args.target)
    topic = args.topic

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
                if item == ".gitkeep":
                    continue
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path) and item != "assets":
                    shutil.rmtree(item_path)

    # Write fresh index.md
    index_path = os.path.join(target, "wiki", "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("""---
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
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    log_path = os.path.join(target, "wiki", "log.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"""# Wiki Update Log

## {now}

* **Initialization**: Created wiki "{topic}" from okf-memex template.
""")

    # Write fresh README
    readme_path = os.path.join(target, "README.md")
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
python scripts/scan_sources.py wiki/ raw/  # 扫描未处理源
```

## Structure

See [okf-memex](https://git.woa.com/yjzhuang/okf-memex) for framework documentation.
""")

    # Remove the Chinese README from personal wiki
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


def cmd_update(args):
    """Update scaffold files in an existing wiki from template."""
    target = os.path.abspath(args.target)

    if not os.path.isdir(target):
        print(f"Error: {target} is not a directory.")
        sys.exit(1)

    # Verify it looks like a wiki (has wiki/ and scripts/)
    if not os.path.isdir(os.path.join(target, "wiki")):
        print(f"Error: {target} does not appear to be a wiki (no wiki/ directory).")
        sys.exit(1)

    print(f"Updating scaffold files in: {target}")
    print(f"Template source: {TEMPLATE_ROOT}")
    print()

    updated = []
    skipped = []
    missing = []

    for rel_path in SCAFFOLD_FILES:
        src = os.path.join(TEMPLATE_ROOT, rel_path)
        dst = os.path.join(target, rel_path)

        if not os.path.exists(src):
            missing.append(rel_path)
            continue

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        # Compare hashes
        src_hash = file_hash(src)
        dst_hash = file_hash(dst)

        if src_hash == dst_hash:
            skipped.append(rel_path)
        else:
            shutil.copy2(src, dst)
            updated.append(rel_path)

    # Also copy init_wiki.py itself (so update can be run again from the wiki)
    init_src = os.path.join(TEMPLATE_ROOT, "scripts", "init_wiki.py")
    init_dst = os.path.join(target, "scripts", "init_wiki.py")
    if os.path.exists(init_src) and file_hash(init_src) != file_hash(init_dst):
        shutil.copy2(init_src, init_dst)
        updated.append("scripts/init_wiki.py")

    # Report
    if updated:
        print(f"Updated ({len(updated)}):")
        for f in updated:
            print(f"  ✓ {f}")
        print()

    if skipped:
        print(f"Already up to date ({len(skipped)}):")
        for f in skipped:
            print(f"  = {f}")
        print()

    if missing:
        print(f"Not in template ({len(missing)}):")
        for f in missing:
            print(f"  ? {f}")
        print()

    if not updated:
        print("✓ All scaffold files are already up to date.")
        sys.exit(0)
    else:
        print(f"✓ {len(updated)} file(s) updated. Review changes and commit.")
        print()
        print("Next steps:")
        print(f"  cd {target}")
        print(f"  git diff                          # review changes")
        print(f"  git add -A && git commit -m 'Update scaffold from okf-memex template'")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold and update OKF LLM Wikis from okf-memex template."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create subcommand
    create_parser = subparsers.add_parser("create", help="Create a new wiki from template")
    create_parser.add_argument("target", help="Target directory path for the new wiki")
    create_parser.add_argument("--topic", default="My Wiki", help="Wiki topic/name (default: My Wiki)")
    create_parser.add_argument("--author", default="", help="Author name (deprecated, kept for compat)")

    # update subcommand
    update_parser = subparsers.add_parser("update", help="Update scaffold files in an existing wiki")
    update_parser.add_argument("target", help="Target wiki directory to update")

    args = parser.parse_args()

    if args.command == "create":
        cmd_create(args)
    elif args.command == "update":
        cmd_update(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
