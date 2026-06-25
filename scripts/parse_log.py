#!/usr/bin/env python3
"""Parse and display recent entries from wiki/log.md.

Extracts date-grouped entries from the OKF log file and displays
the most recent N entries (default 10).

Log format (per OKF §7):
    ## YYYY-MM-DD
    * **Action**: Description.

Usage:
    python parse_log.py <wiki_dir> [N]

Exit codes:
    0 — success
    1 — error
"""

import sys
import os
import re
import glob
from datetime import datetime


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
    if len(sys.argv) < 2:
        print("Usage: python parse_log.py <wiki_dir> [N]")
        sys.exit(1)

    wiki_dir = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    if not os.path.isdir(wiki_dir):
        print(f"Error: {wiki_dir} is not a directory")
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
