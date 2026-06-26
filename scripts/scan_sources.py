#!/usr/bin/env python3
"""Scan raw/ for source files not yet ingested into the wiki.

Compares files in raw/ against Source pages in wiki/sources/ to find
unprocessed sources. Outputs a structured report.

Usage:
    python scan_sources.py <wiki_dir> <raw_dir> [--json]

Exit codes:
    0 — no unprocessed sources found
    1 — unprocessed sources found (or error)

JSON output mode (--json) emits machine-readable output for automation.
"""

import sys
import os
import re
import glob
import json
import argparse
from datetime import datetime


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
RAW_SUBDIRS = ["web", "papers", "videos", "books", "code", "podcasts", "notes"]
IGNORED_EXTS = {".gitkeep", ".ds_store", ".pyc"}
SOURCE_EXTENSIONS = {".md", ".pdf", ".txt", ".html", ".epub", ".ipynb"}


def parse_frontmatter(content):
    """Extract frontmatter dict from markdown content."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None
    fm_text = match.group(1)
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            fm[key] = value
    return fm


def get_ingested_sources(wiki_dir):
    """Return set of raw file paths mentioned in Source pages."""
    ingested = set()
    sources_dir = os.path.join(wiki_dir, "sources")
    if not os.path.isdir(sources_dir):
        return ingested

    for filepath in glob.glob(os.path.join(sources_dir, "**/*.md"), recursive=True):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue

        # Look for "Original file:" or "raw/" references in body
        for match in re.finditer(r"(?:raw/|Original file:\s*`)([^\s`)]+)", content):
            raw_path = match.group(1).strip()
            ingested.add(raw_path)

        # Also check frontmatter resource field
        fm = parse_frontmatter(content)
        if fm and "resource" in fm:
            resource = fm["resource"]
            if resource.startswith("raw/"):
                ingested.add(resource)

    return ingested


def scan_raw_dir(raw_dir):
    """Scan raw/ directory for source files. Returns list of dicts."""
    sources = []

    for subdir in RAW_SUBDIRS:
        subdir_path = os.path.join(raw_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        for filepath in sorted(glob.glob(os.path.join(subdir_path, "**/*"), recursive=True)):
            if os.path.isdir(filepath):
                continue

            filename = os.path.basename(filepath)
            ext = os.path.splitext(filename)[1].lower()

            # Skip ignored files
            if filename.lower() in IGNORED_EXTS:
                continue
            if ext not in SOURCE_EXTENSIONS and filename != ".gitkeep":
                # Include unknown types too, but skip clearly non-source files
                if ext in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
                    continue

            rel_path = os.path.relpath(filepath, raw_dir)

            # Get file stats
            stat = os.stat(filepath)
            size = stat.st_size
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")

            # Format file size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.1f} MB"

            sources.append({
                "type": subdir,
                "filename": filename,
                "rel_path": rel_path,
                "size": size_str,
                "size_bytes": size,
                "modified": mtime,
            })

    return sources


def main():
    parser = argparse.ArgumentParser(
        description="Scan raw/ for unprocessed source files."
    )
    parser.add_argument("wiki_dir", help="Wiki bundle directory (e.g. wiki/)")
    parser.add_argument("raw_dir", help="Raw sources directory (e.g. raw/)")
    parser.add_argument("--json", action="store_true", help="Output JSON for automation")
    args = parser.parse_args()

    wiki_dir = os.path.abspath(args.wiki_dir)
    raw_dir = os.path.abspath(args.raw_dir)

    if not os.path.isdir(wiki_dir):
        print(f"Error: {wiki_dir} is not a directory")
        sys.exit(1)
    if not os.path.isdir(raw_dir):
        print(f"Error: {raw_dir} is not a directory")
        sys.exit(1)

    # Get already-ingested sources
    ingested = get_ingested_sources(wiki_dir)

    # Scan raw/ for all source files
    all_sources = scan_raw_dir(raw_dir)

    # Find unprocessed
    unprocessed = []
    for src in all_sources:
        # Check various path formats that might appear in Source pages
        rel_path = src["rel_path"]
        possible_refs = [
            rel_path,
            f"raw/{rel_path}",
            os.path.basename(rel_path),
        ]
        if not any(ref in ingested for ref in possible_refs):
            unprocessed.append(src)

    # Output
    if args.json:
        print(json.dumps({
            "total_raw": len(all_sources),
            "total_ingested": len(all_sources) - len(unprocessed),
            "total_unprocessed": len(unprocessed),
            "unprocessed": unprocessed,
        }, indent=2, ensure_ascii=False))
    else:
        total_ingested = len(all_sources) - len(unprocessed)
        print(f"Source Scan — {raw_dir}")
        print(f"Total files: {len(all_sources)} | Ingested: {total_ingested} | Unprocessed: {len(unprocessed)}")
        print()

        if unprocessed:
            print(f"Found {len(unprocessed)} unprocessed source(s):\n")
            for src in unprocessed:
                print(f"  [{src['type']}] {src['filename']}")
                print(f"       path: raw/{src['rel_path']}")
                print(f"       size: {src['size']}, added: {src['modified']}")
                print()

            print("To ingest:")
            print('  Tell Box: "批量摄入 raw/ 下未处理的源"')
            print("  Or run:   python scripts/okf_check.py wiki/  (after manual ingest)")
        else:
            print("✓ All sources have been ingested.")

    sys.exit(1 if unprocessed else 0)


if __name__ == "__main__":
    main()
