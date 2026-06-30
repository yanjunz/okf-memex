#!/usr/bin/env python3
"""Parse and display recent entries from wiki/log.md.

Extracts date-grouped entries from the OKF log file and displays
the most recent N entries (default 10).

Log format (per OKF §7):
    ## YYYY-MM-DD
    * **Action**: Description.

Usage:
    python parse_log.py [wiki_dir] [N]

    wiki_dir is optional — if omitted, the bundle is resolved from
    .okf-config.json or the default wiki/ directory by walking up from CWD.
    `python parse_log.py 5` is treated as N=5 (auto-resolve wiki_dir).

Exit codes:
    0 — success
    1 — error
"""

import sys
import os
import re
import glob
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okf_paths import resolve_bundle  # noqa: E402


DATE_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})")


def parse_log(content):
    """Parse log.md content into list of (date, entries) tuples, newest first."""
    entries = []
    current_date = None
    current_entries = []

    for line in content.split("\n"):
        match = DATE_RE.match(line)
        if match:
            if current_date:
                entries.append((current_date, current_entries))
            current_date = match.group(1)
            current_entries = []
        elif current_date and line.strip():
            current_entries.append(line.strip())

    if current_date:
        entries.append((current_date, current_entries))

    # Sort by date descending
    entries.sort(key=lambda x: x[0], reverse=True)
    return entries


def main():
    args = sys.argv[1:]
    explicit = None
    n = 10

    # Treat a bare integer as N (auto-resolve wiki_dir); otherwise first arg is wiki_dir
    if args and not args[0].isdigit():
        explicit = args[0]
        args = args[1:]
    if args:
        try:
            n = int(args[0])
        except ValueError:
            print(f"Error: '{args[0]}' is not a valid integer for N")
            sys.exit(1)

    _, wiki_dir = resolve_bundle(explicit)
    if wiki_dir is None:
        print("Error: could not locate bundle directory.")
        print("Pass it explicitly: python parse_log.py <wiki_dir> [N]")
        print("Or run from inside an OKF repo (contains .okf-config.json or wiki/).")
        sys.exit(1)

    # Find all log.md files in the bundle
    log_files = []
    for filepath in glob.glob(os.path.join(wiki_dir, "**/log.md"), recursive=True):
        log_files.append(filepath)

    if not log_files:
        print(f"No log.md found in {wiki_dir}")
        sys.exit(1)

    all_entries = []

    for log_path in sorted(log_files):
        rel_path = os.path.relpath(log_path, wiki_dir)
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()

        entries = parse_log(content)
        for date, day_entries in entries:
            for entry in day_entries:
                all_entries.append((date, rel_path, entry))

    # Sort by date descending
    all_entries.sort(key=lambda x: x[0], reverse=True)

    # Take last N
    recent = all_entries[:n]

    print(f"Wiki Log — last {len(recent)} entr{'y' if len(recent) == 1 else 'ies'} (of {len(all_entries)} total)\n")

    if not recent:
        print("No log entries found.")
        sys.exit(0)

    current_date = None
    for date, source, entry in recent:
        if date != current_date:
            current_date = date
            # Format date nicely
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                weekday = dt.strftime("%A")
                print(f"## {date} ({weekday})")
            except ValueError:
                print(f"## {date}")
        # Indicate which log file if multiple
        if len(log_files) > 1:
            print(f"  [{source}] {entry}")
        else:
            print(f"  {entry}")

    sys.exit(0)


if __name__ == "__main__":
    main()
