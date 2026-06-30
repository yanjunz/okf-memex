#!/usr/bin/env python3
"""Resolve OKF wiki paths.

The bundle directory defaults to "wiki/" but can be renamed (e.g. to give
Obsidian a distinctive vault name). The actual name is recorded in
`.okf-config.json` at the repo root:

    {"bundle": "yjzhuang"}

This module is imported by all the maintenance scripts so they can be run
without explicit path arguments — they walk up from CWD to find the repo
and read the bundle name from config.

Functions:
    find_repo_root(start=None) — walk up to find an OKF repo root
    get_bundle_name(repo_root) — read bundle dir name from config
    resolve_bundle(explicit_path=None) — return (repo_root, bundle_dir)
"""

import os
import json


CONFIG_FILE = ".okf-config.json"
DEFAULT_BUNDLE = "wiki"


def find_repo_root(start=None):
    """Walk up from `start` (or CWD) until we find an OKF repo root.

    Detection rules, in order:
    1. Directory contains `.okf-config.json` (preferred).
    2. Directory contains both `wiki/` and `raw/` (legacy / default layout).

    Returns absolute path to the repo root, or None if nothing matches.
    """
    cur = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.isfile(os.path.join(cur, CONFIG_FILE)):
            return cur
        if (os.path.isdir(os.path.join(cur, DEFAULT_BUNDLE))
                and os.path.isdir(os.path.join(cur, "raw"))):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def get_bundle_name(repo_root):
    """Read bundle directory name from `.okf-config.json`.

    Falls back to "wiki" if config is missing, unreadable, or doesn't specify.
    """
    config_path = os.path.join(repo_root, CONFIG_FILE)
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            name = config.get("bundle")
            if isinstance(name, str) and name.strip():
                return name.strip()
        except (OSError, json.JSONDecodeError):
            pass
    return DEFAULT_BUNDLE


def resolve_bundle(explicit_path=None, start=None):
    """Return (repo_root, bundle_dir) as absolute paths.

    If `explicit_path` is provided, treat it as the bundle directory and
    derive repo_root as its parent.

    Otherwise, walk up from `start` (or CWD) to find the repo root, then
    derive the bundle directory name from `.okf-config.json`.

    Returns (None, None) if nothing resolvable is found.
    """
    if explicit_path:
        bundle = os.path.abspath(explicit_path)
        if not os.path.isdir(bundle):
            return None, None
        return os.path.dirname(bundle), bundle

    repo = find_repo_root(start)
    if repo is None:
        return None, None
    bundle = os.path.join(repo, get_bundle_name(repo))
    if not os.path.isdir(bundle):
        return None, None
    return repo, bundle


def write_config(repo_root, bundle_name):
    """Write `.okf-config.json` with the given bundle name.

    No-op if bundle_name is the default "wiki" (kept implicit to avoid
    cluttering repos that haven't renamed).
    """
    if bundle_name == DEFAULT_BUNDLE:
        return
    config_path = os.path.join(repo_root, CONFIG_FILE)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({"bundle": bundle_name}, f, indent=2)
        f.write("\n")
