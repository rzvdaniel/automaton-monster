#!/usr/bin/env python3
"""Run the tests of the apps a change touches, whatever language they use.

Usage: run_app_tests.py [--changed-since <git-ref>] [--list]   (default: every app in catalog-apps.json)

An app declares how to test itself with a `test.sh` in its folder (run as `sh test.sh` from that folder).
An app without one is reported and skipped. A change to tools/, .github/ or design/ runs every app's tests.
"""
import json, subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
SHARED = ("tools/", ".github/", ".agents/tools/", "design/", "catalog-apps.json")


def select(folders, changed):
    """The app folders to test: all when a shared path changed, otherwise those with a changed file."""
    if changed is None or any(c.startswith(SHARED) for c in changed):
        return list(folders)
    return [f for f in folders if any(c.startswith(f + "/") for c in changed)]


def main(argv):
    folders = [a["folder"] for a in json.loads((root / "catalog-apps.json").read_text())["apps"]]
    changed = None
    if "--changed-since" in argv:
        ref = argv[argv.index("--changed-since") + 1]
        changed = subprocess.run(["git", "diff", "--name-only", ref, "HEAD"], cwd=root, check=True,
                                 capture_output=True, text=True).stdout.split()
    chosen = select(folders, changed)
    if "--list" in argv:
        print("\n".join(chosen))
        return 0
    failed = []
    for folder in chosen:
        if not (root / folder / "test.sh").is_file():
            print(f"skip {folder}: no test.sh")
            continue
        print(f"::group::{folder}", flush=True)
        code = subprocess.run(["sh", "test.sh"], cwd=root / folder).returncode
        print("::endgroup::", flush=True)
        print(f"{'ok  ' if code == 0 else 'FAIL'} {folder}")
        if code:
            failed.append(folder)
    if not chosen:
        print("No app changed; no tests to run.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
