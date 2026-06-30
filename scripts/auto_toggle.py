#!/usr/bin/env python3
"""Toggle automation switches for the wiki.

Usage:
    python auto_toggle.py ingest on               # Enable auto-ingest (auto-resolve repo root)
    python auto_toggle.py <wiki_root> ingest on   # Enable, explicit repo root
    python auto_toggle.py lint on                 # Enable auto-lint
    python auto_toggle.py status                  # Show current status

    wiki_root is optional — auto-resolved from .okf-config.json by walking up from CWD.

Exit codes:
    0 — success
    1 — error
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okf_paths import find_repo_root  # noqa: E402


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
    args = sys.argv[1:]
    ACTIONS = {"ingest", "lint", "status"}

    # First arg may be wiki_root or an action — disambiguate
    if args and args[0] in ACTIONS:
        wiki_root = find_repo_root()
        if wiki_root is None:
            print("Error: could not locate repo root.")
            print("Pass it explicitly: python auto_toggle.py <wiki_root> <ingest|lint|status> [on|off]")
            sys.exit(1)
    elif args:
        wiki_root = os.path.abspath(args[0])
        args = args[1:]
        if not os.path.isdir(wiki_root):
            print(f"Error: {wiki_root} is not a directory")
            sys.exit(1)
    else:
        print("Usage: python auto_toggle.py [wiki_root] <ingest|lint|status> [on|off]")
        print()
        print("Commands:")
        print("  ingest on   — Enable automatic source ingestion")
        print("  ingest off  — Disable (notification only)")
        print("  lint on     — Enable automatic weekly lint")
        print("  lint off    — Disable automatic lint")
        print("  status      — Show current automation status")
        sys.exit(1)

    if not args:
        print("Error: missing action (ingest|lint|status)")
        sys.exit(1)
    action = args[0]
    args = args[1:]

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

    if not args or args[0] not in ("on", "off"):
        print(f"Error: specify 'on' or 'off' for '{action}'")
        sys.exit(1)

    key = VALID_KEYS[action]
    value = args[0] == "on"
    config[key] = value
    save_config(wiki_root, config)

    status = "✅ ON" if value else "⬜ OFF"
    print(f"auto_{action} is now {status}")
    print(f"Config saved to {wiki_root}/{CONFIG_FILENAME}")
    sys.exit(0)


if __name__ == "__main__":
    main()
