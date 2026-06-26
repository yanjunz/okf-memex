#!/usr/bin/env python3
"""Toggle automation switches for the wiki.

Usage:
    python auto_toggle.py <wiki_root> ingest on     # Enable auto-ingest
    python auto_toggle.py <wiki_root> ingest off    # Disable auto-ingest
    python auto_toggle.py <wiki_root> lint on       # Enable auto-lint
    python auto_toggle.py <wiki_root> lint off      # Disable auto-lint
    python auto_toggle.py <wiki_root> status        # Show current status

Exit codes:
    0 — success
    1 — error
"""

import sys
import os
import json


CONFIG_FILENAME = ".automation.json"
DEFAULT_CONFIG = {
    "auto_ingest": False,
    "auto_lint": False,
    "lint_schedule": "weekly",
}

VALID_KEYS = {
    "ingest": "auto_ingest",
    "lint": "auto_lint",
}


def load_config(wiki_root):
    path = os.path.join(wiki_root, CONFIG_FILENAME)
    if not os.path.exists(path):
        return DEFAULT_CONFIG.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        # Merge with defaults
        merged = DEFAULT_CONFIG.copy()
        merged.update(config)
        return merged
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(wiki_root, config):
    path = os.path.join(wiki_root, CONFIG_FILENAME)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    if len(sys.argv) < 3:
        print("Usage: python auto_toggle.py <wiki_root> <ingest|lint|status> [on|off]")
        print()
        print("Commands:")
        print("  ingest on   — Enable automatic source ingestion")
        print("  ingest off  — Disable (notification only)")
        print("  lint on     — Enable automatic weekly lint")
        print("  lint off    — Disable automatic lint")
        print("  status      — Show current automation status")
        sys.exit(1)

    wiki_root = os.path.abspath(sys.argv[1])
    action = sys.argv[2]

    if not os.path.isdir(wiki_root):
        print(f"Error: {wiki_root} is not a directory")
        sys.exit(1)

    config = load_config(wiki_root)

    if action == "status":
        print(f"Automation config — {wiki_root}/{CONFIG_FILENAME}")
        print()
        print(f"  auto_ingest:  {'✅ ON' if config['auto_ingest'] else '⬜ OFF'}")
        print(f"  auto_lint:    {'✅ ON' if config['auto_lint'] else '⬜ OFF'}")
        print(f"  lint_schedule: {config.get('lint_schedule', 'weekly')}")
        print()
        if config["auto_ingest"]:
            print("  → New sources in raw/ will be automatically ingested.")
        else:
            print("  → New sources in raw/ will only trigger a notification.")
        sys.exit(0)

    if action not in VALID_KEYS:
        print(f"Error: unknown action '{action}'. Use: ingest, lint, or status")
        sys.exit(1)

    if len(sys.argv) < 4 or sys.argv[3] not in ("on", "off"):
        print(f"Error: specify 'on' or 'off' for '{action}'")
        sys.exit(1)

    key = VALID_KEYS[action]
    value = sys.argv[3] == "on"
    config[key] = value
    save_config(wiki_root, config)

    status = "✅ ON" if value else "⬜ OFF"
    print(f"auto_{action} is now {status}")
    print(f"Config saved to {wiki_root}/{CONFIG_FILENAME}")
    sys.exit(0)


if __name__ == "__main__":
    main()
