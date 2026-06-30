#!/usr/bin/env python3
"""Broken link and orphan page detector for OKF wiki bundles.

Scans all markdown links in the wiki and reports:
1. Broken links — link targets that don't exist in the bundle.
2. Orphan pages — pages with no inbound links from other pages.

Usage:
    python link_check.py [wiki_dir]

    wiki_dir is optional — if omitted, the bundle is resolved from
    .okf-config.json or the default wiki/ directory by walking up from CWD.

Exit codes:
    0 — no issues found
    1 — broken links or orphan pages found
"""

import sys
import os
import re
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okf_paths import resolve_bundle  # noqa: E402


RESERVED_FILES = {"index.md", "log.md"}

# Match markdown links: [text](url)
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def get_all_md_files(wiki_dir):
    """Return dict of rel_path -> filepath for all .md files in bundle."""
    files = {}
    for filepath in sorted(glob.glob(os.path.join(wiki_dir, "**/*.md"), recursive=True)):
        rel_path = os.path.relpath(filepath, wiki_dir)
        files[rel_path] = filepath
    return files


def extract_links(content, source_rel_path, wiki_dir):
    """Extract all markdown links from content. Returns list of (link_text, target_rel_path)."""
    links = []
    for match in LINK_RE.finditer(content):
        text = match.group(1)
        url = match.group(2).strip()

        # Skip external URLs
        if url.startswith(("http://", "https://", "mailto:", "#")):
            continue

        # Skip non-md links (images, etc.)
        if not url.endswith(".md"):
            # Could be a directory link (e.g. "subdir/")
            continue

        # Resolve bundle-relative absolute links (starting with /)
        if url.startswith("/"):
            target_rel = url.lstrip("/")
        else:
            # Relative link — resolve relative to source file's directory
            source_dir = os.path.dirname(source_rel_path)
            target_rel = os.path.normpath(os.path.join(source_dir, url))

        links.append((text, target_rel))
    return links


def main():
    explicit = sys.argv[1] if len(sys.argv) > 1 else None
    _, wiki_dir = resolve_bundle(explicit)
    if wiki_dir is None:
        print("Error: could not locate bundle directory.")
        print("Pass it explicitly: python link_check.py <wiki_dir>")
        print("Or run from inside an OKF repo (contains .okf-config.json or wiki/).")
        sys.exit(1)

    all_files = get_all_md_files(wiki_dir)

    # Build link graph: source -> set of targets
    link_graph = {}  # source_rel -> set of target_rel
    all_targets = set()

    for rel_path, filepath in all_files.items():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue

        links = extract_links(content, rel_path, wiki_dir)
        link_graph[rel_path] = set()
        for text, target in links:
            link_graph[rel_path].add(target)
            all_targets.add(target)

    # Find broken links: targets not in all_files
    broken_links = []
    for source, targets in sorted(link_graph.items()):
        for target in sorted(targets):
            if target not in all_files:
                broken_links.append((source, target))

    # Find orphan pages: non-reserved .md files with no inbound links
    inbound_links = {rel: 0 for rel in all_files}
    for source, targets in link_graph.items():
        for target in targets:
            if target in inbound_links:
                inbound_links[target] += 1

    orphans = []
    for rel_path in sorted(all_files.keys()):
        filename = os.path.basename(rel_path)
        if filename in RESERVED_FILES:
            continue
        if inbound_links[rel_path] == 0:
            orphans.append(rel_path)

    # Report
    print(f"Link Check — {wiki_dir}")
    print(f"Scanned {len(all_files)} markdown file(s), found {sum(len(t) for t in link_graph.values())} internal link(s).\n")

    if broken_links:
        print(f"BROKEN LINKS ({len(broken_links)}):")
        for source, target in broken_links:
            print(f"  ✗ {source} → {target} (target not found)")
        print()
    else:
        print("✓ No broken links found.\n")

    if orphans:
        print(f"ORPHAN PAGES ({len(orphans)}):")
        for path in orphans:
            print(f"  ⚠ {path} (no inbound links)")
        print()
    else:
        print("✓ No orphan pages found.\n")

    has_issues = bool(broken_links or orphans)
    if has_issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
