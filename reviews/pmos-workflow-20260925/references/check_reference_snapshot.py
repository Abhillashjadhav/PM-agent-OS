#!/usr/bin/env python3
"""Verify restored archival files by reading bytes only; execute no archived code."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = Path(__file__).with_name("source-manifest.json")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    verified = []
    for source in manifest["sources"]:
        expected = {entry["path"] for entry in source["files"]}
        location = ROOT / source["path"]
        if source["kind"] == "directory" and location.is_dir():
            actual = {
                str(path.relative_to(ROOT))
                for path in location.rglob("*")
                if path.is_file() or path.is_symlink()
            }
            if actual != expected:
                errors.append({
                    "path": source["path"], "error": "inventory differs",
                    "missing": sorted(expected - actual), "extra": sorted(actual - expected),
                })
        for entry in source["files"]:
            path = ROOT / entry["path"]
            if path.is_symlink() or not path.is_file():
                errors.append({"path": entry["path"], "error": "regular file missing"})
                continue
            data = path.read_bytes()
            mode = "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            actual = {
                "mode": mode,
                "git_blob": blob,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
            differences = {key: value for key, value in actual.items() if value != entry[key]}
            if differences:
                errors.append({"path": entry["path"], "error": "content or mode differs", "actual": differences})
            else:
                verified.append(entry["path"])
    print(json.dumps({
        "status": "FAIL" if errors else "PASS",
        "scope": "Static byte/blob/mode comparison only; no historical script executed.",
        "verified_files": len(verified),
        "errors": errors,
    }, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
