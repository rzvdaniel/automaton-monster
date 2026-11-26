#!/usr/bin/env python3
"""Check that every app in catalog-apps.json has a valid automaton.json that declares its permissions.

`application.permissions`, when present, must be a list (an empty list declares none); an app that leaves it out is
reported as a warning, because the contract treats a missing list as none. The server's own contract check is
tools/validate_apps.py; this one needs no CLI and runs on every app.
"""
import json, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent


def problems(manifest):
    if not isinstance(manifest, dict):
        return ["not a JSON object"]
    out = [f"missing {key}" for key in ("name", "summary") if not str(manifest.get(key, "")).strip()]
    app = manifest.get("application")
    if not isinstance(app, dict):
        return out + ["missing application"]
    perms = app.get("permissions", [])
    if not isinstance(perms, list):
        out.append("application.permissions is not a list")
    elif not all(isinstance(p, (str, dict)) for p in perms):
        out.append("application.permissions has an entry that is not a string or object")
    return out


def main():
    failed = False
    for entry in json.loads((root / "catalog-apps.json").read_text())["apps"]:
        path = root / entry["folder"] / "automaton.json"
        manifest = None
        try:
            manifest = json.loads(path.read_text(encoding="utf-8-sig"))
            found = problems(manifest)
        except (OSError, ValueError) as error:
            found = [f"cannot read: {error}"]
        undeclared = "permissions" not in (manifest or {}).get("application", {}) if isinstance(manifest, dict) else False
        print(f"{'FAIL' if found else 'ok  '} {entry['folder']}" + "".join(f"\n     {p}" for p in found))
        if undeclared and not found:
            print("     warning: application.permissions not declared (treated as none)")
        failed |= bool(found)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
