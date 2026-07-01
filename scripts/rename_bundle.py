#!/usr/bin/env python3
"""Rename an OKF wiki's bundle directory.

Useful when you have an existing wiki with the default `wiki/` bundle and
want to give it a distinct name (e.g. to disambiguate multiple wikis in
Obsidian's vault switcher — Obsidian shows the folder name as the vault
name, so identical `wiki/` folders across repos are impossible to tell
apart).

Usage:
    python rename_bundle.py <new_name> [<repo_root>]

    new_name    New bundle directory name. Plain single-segment name only —
                no slashes, no leading dot.
    repo_root   Repo root to operate on. If omitted, walks up from CWD to
                find the OKF repo automatically.

Effects:
    - Renames <repo>/<current_bundle>/ to <repo>/<new_name>/
    - Writes/updates <repo>/.okf-config.json with the new bundle name
    - Removes .okf-config.json when the new name is the default "wiki"
      (default bundle is implicit, no config needed)

Preserved automatically (no manual fix-up required):
    - The Clippings symlink inside the bundle (it's relative)
    - Bundle-relative wiki links (`/entities/xxx.md` etc. — they encode
      the bundle root, not its on-disk name)
    - Obsidian's `.obsidian/` directory (moves with the bundle)

Exit codes:
    0 — renamed (or nothing to do)
    1 — error (missing source, target exists, invalid name, etc.)
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okf_paths import (  # noqa: E402
    CONFIG_FILE,
    DEFAULT_BUNDLE,
    find_repo_root,
    get_bundle_name,
    write_config,
)


def valid_bundle_name(name):
    """Check that name is a plain single-segment directory name."""
    if not name or not name.strip():
        return False
    name = name.strip()
    if "/" in name or name.startswith(".") or name in ("..",):
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Rename an OKF wiki's bundle directory."
    )
    parser.add_argument("new_name", help="New bundle directory name")
    parser.add_argument("repo_root", nargs="?", default=None,
                        help="Repo root (default: auto-resolve from CWD)")
    args = parser.parse_args()

    new_name = args.new_name.strip()
    if not valid_bundle_name(new_name):
        print(f"Error: invalid bundle name '{new_name}'. Use a plain directory name "
              "(no slashes, no leading dot).")
        sys.exit(1)

    if args.repo_root:
        repo_root = os.path.abspath(args.repo_root)
        if not os.path.isdir(repo_root):
            print(f"Error: {repo_root} is not a directory")
            sys.exit(1)
    else:
        repo_root = find_repo_root()
        if repo_root is None:
            print("Error: could not locate OKF repo root.")
            print("Pass it explicitly, or run from inside a wiki repo "
                  "(one that contains .okf-config.json or a wiki/ directory).")
            sys.exit(1)

    current = get_bundle_name(repo_root)
    src = os.path.join(repo_root, current)
    dst = os.path.join(repo_root, new_name)

    if current == new_name:
        print(f"Bundle is already named '{new_name}'. Nothing to do.")
        sys.exit(0)

    if not os.path.isdir(src):
        print(f"Error: current bundle {src} does not exist.")
        print(f"Config says bundle is '{current}' but that directory is missing.")
        sys.exit(1)

    if os.path.exists(dst):
        print(f"Error: {dst} already exists. Choose a different name "
              "or remove/rename the existing directory first.")
        sys.exit(1)

    # Do the rename
    os.rename(src, dst)

    # Update config
    config_path = os.path.join(repo_root, CONFIG_FILE)
    if new_name == DEFAULT_BUNDLE:
        # Reverted to default — remove config file if it exists
        if os.path.isfile(config_path):
            os.remove(config_path)
            config_action = f"Removed {CONFIG_FILE} (bundle back to default '{DEFAULT_BUNDLE}')"
        else:
            config_action = f"No {CONFIG_FILE} needed for default bundle name"
    else:
        write_config(repo_root, new_name)
        config_action = f"Wrote {CONFIG_FILE} with bundle: {new_name}"

    print(f"✓ Renamed {current}/ → {new_name}/")
    print(f"✓ {config_action}")
    print()
    print("Next steps:")
    print(f"  cd {repo_root}")
    print(f"  git add -A")
    print(f"  git commit -m 'Rename bundle: {current}/ → {new_name}/'")
    print(f"  git push")
    print()
    print("In Obsidian:")
    print(f"  Close the old vault ({current}), then open {repo_root}/{new_name}/ as a new vault.")
    print(f"  Vault name will now show as '{new_name}' — disambiguated from other wikis.")
    sys.exit(0)


if __name__ == "__main__":
    main()
