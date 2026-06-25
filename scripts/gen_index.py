#!/usr/bin/env python3
"""Regenerate wiki/index.md from frontmatter of all concept documents.

Scans all non-reserved .md files in the wiki bundle, reads their frontmatter,
and generates an index.md organized by type and directory.

Preserves root index.md frontmatter (okf_version declaration).

Usage:
    python gen_index.py <wiki_dir>

Exit codes:
    0 — index generated successfully
    1 — error
"""

import sys
import os
import re
import glob


RESERVED_FILES = {"index.md", "log.md"}
TYPE_ORDER = ["Entity", "Concept", "Source", "Synthesis"]
TYPE_DIRS = {
    "Entity": "entities",
    "Concept": "concepts",
    "Source": "sources",
    "Synthesis": "synthesis",
}
TYPE_PLURALS = {
    "Entity": "Entities",
    "Concept": "Concepts",
    "Source": "Sources",
    "Synthesis": "Synthesis",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(content):
    """Extract and parse YAML frontmatter. Returns dict or None."""
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python gen_index.py <wiki_dir>")
        sys.exit(1)

    wiki_dir = sys.argv[1]
    if not os.path.isdir(wiki_dir):
        print(f"Error: {wiki_dir} is not a directory")
        sys.exit(1)

    # Preserve root index.md frontmatter if it has okf_version
    index_path = os.path.join(wiki_dir, "index.md")
    index_fm = ""
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        fm = parse_frontmatter(content)
        if fm and "okf_version" in fm:
            index_fm = f'---\nokf_version: "{fm["okf_version"]}"\n---\n\n'

    # Collect all concept documents grouped by type
    by_type = {}  # type -> list of (rel_path, title, description)

    for filepath in sorted(glob.glob(os.path.join(wiki_dir, "**/*.md"), recursive=True)):
        rel_path = os.path.relpath(filepath, wiki_dir)
        filename = os.path.basename(filepath)

        if filename in RESERVED_FILES:
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm = parse_frontmatter(content)
        if fm is None:
            continue

        doc_type = fm.get("type", "Unknown")
        title = fm.get("title", filename.replace(".md", "").replace("-", " ").title())
        description = fm.get("description", "")

        if doc_type not in by_type:
            by_type[doc_type] = []
        by_type[doc_type].append((rel_path, title, description))

    # Generate index content
    lines = [index_fm + "# Wiki Index\n"]

    # Track total for summary
    total = 0
    known_types = set()

    # Known types in defined order
    for doc_type in TYPE_ORDER:
        type_dir = TYPE_DIRS.get(doc_type, doc_type.lower() + "s")
        section_name = TYPE_PLURALS.get(doc_type, doc_type + "s")
        entries = by_type.pop(doc_type, [])
        total += len(entries)
        known_types.add(doc_type)

        lines.append(f"## {section_name}\n")
        if entries:
            for rel_path, title, desc in entries:
                # Convert rel_path to bundle-relative absolute link
                link = f"/{rel_path}"
                if desc:
                    lines.append(f"* [{title}]({link}) — {desc}")
                else:
                    lines.append(f"* [{title}]({link})")
                lines.append("")
        else:
            lines.append(f"*No {section_name.lower()} pages yet.*\n")

    # Unknown types
    for doc_type, entries in sorted(by_type.items()):
        section_name = doc_type + "s"
        lines.append(f"## {section_name}\n")
        total += len(entries)
        for rel_path, title, desc in entries:
            link = f"/{rel_path}"
            if desc:
                lines.append(f"* [{title}]({link}) — {desc}")
            else:
                lines.append(f"* [{title}]({link})")
            lines.append("")

    # Write index.md
    output = "\n".join(lines)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(output)

    num_types = len(known_types) + len(by_type)
    print(f"Generated {index_path}")
    print(f"Indexed {total} concept document(s) across {num_types} type(s).")
    sys.exit(0)


if __name__ == "__main__":
    main()
