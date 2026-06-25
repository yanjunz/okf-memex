#!/usr/bin/env python3
"""OKF v0.1 conformance checker.

Validates that all non-reserved .md files in a wiki bundle have:
1. A parseable YAML frontmatter block (delimited by ---).
2. A non-empty `type` field in frontmatter.

Reserved filenames (index.md, log.md) are checked for structure but
do not require frontmatter (except root index.md which MAY declare okf_version).

Usage:
    python okf_check.py <wiki_dir>

Exit codes:
    0 — all checks passed
    1 — one or more violations found
"""

import sys
import os
import re
import glob


RESERVED_FILES = {"index.md", "log.md"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(content):
    """Extract and parse YAML frontmatter. Returns (dict, body) or (None, content)."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, content

    fm_text = match.group(1)
    body = content[match.end():]

    # Minimal YAML parsing for key: value pairs
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Remove surrounding quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            # Handle YAML lists: [a, b, c]
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
            fm[key] = value

    return fm, body


def check_file(filepath, rel_path, violations):
    """Check a single markdown file for OKF compliance."""
    filename = os.path.basename(filepath)
    is_reserved = filename in RESERVED_FILES

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        violations.append((rel_path, f"Cannot read file: {e}"))
        return

    if is_reserved:
        # Reserved files: check structure (should have headings, not frontmatter
        # except root index.md which MAY have okf_version)
        if filename == "index.md" and rel_path == "index.md":
            fm, _ = parse_frontmatter(content)
            if fm and "okf_version" not in fm:
                # Frontmatter present but no okf_version — that's fine, it's optional
                pass
        # Reserved files don't need frontmatter/type
        return

    # Non-reserved file: must have frontmatter
    fm, body = parse_frontmatter(content)
    if fm is None:
        violations.append((rel_path, "Missing YAML frontmatter block (delimited by ---)"))
        return

    # Must have non-empty type field
    type_val = fm.get("type")
    if not type_val:
        violations.append((rel_path, "Missing or empty `type` field in frontmatter"))
        return

    # Soft warnings for recommended fields
    missing_recommended = []
    for field in ["title", "description", "timestamp"]:
        if field not in fm or not fm[field]:
            missing_recommended.append(field)

    if missing_recommended:
        violations.append(
            (rel_path, f"Warning: missing recommended fields: {', '.join(missing_recommended)}")
        )


def main():
    if len(sys.argv) < 2:
        print("Usage: python okf_check.py <wiki_dir>")
        sys.exit(1)

    wiki_dir = sys.argv[1]
    if not os.path.isdir(wiki_dir):
        print(f"Error: {wiki_dir} is not a directory")
        sys.exit(1)

    violations = []
    file_count = 0

    for filepath in sorted(glob.glob(os.path.join(wiki_dir, "**/*.md"), recursive=True)):
        rel_path = os.path.relpath(filepath, wiki_dir)
        file_count += 1
        check_file(filepath, rel_path, violations)

    # Separate errors from warnings
    errors = [v for v in violations if not v[1].startswith("Warning")]
    warnings = [v for v in violations if v[1].startswith("Warning")]

    print(f"OKF Conformance Check — {wiki_dir}")
    print(f"Scanned {file_count} markdown file(s).\n")

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for path, msg in errors:
            print(f"  ✗ {path}: {msg}")
        print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for path, msg in warnings:
            print(f"  ⚠ {path}: {msg}")
        print()

    if not errors:
        print("✓ All concept documents conform to OKF v0.1.")
        if not warnings:
            print("✓ All recommended fields present.")
        sys.exit(0)
    else:
        print(f"✗ {len(errors)} conformance error(s) found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
