#!/usr/bin/env python3
"""Check installed publisher metadata without importing or running the publisher."""

from __future__ import annotations

import argparse
import json
import sys
from importlib import metadata


REVIEWED_REVISION = "297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6"
PUBLISHER_URL = "https://github.com/Abhillashjadhav/production-engineering-os.git"


def blocked(code: str, message: str) -> int:
    print(f"HANDOFF_SETUP_BLOCKED: {code}: {message}", file=sys.stderr)
    print(f"Checked Python: {sys.executable}", file=sys.stderr)
    print("Follow docs/HANDOFF.md using that same Python environment.", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        publisher = metadata.distribution("pmpe")
    except metadata.PackageNotFoundError:
        return blocked("PUBLISHER_NOT_INSTALLED", "pmpe is absent from this Python environment.")

    try:
        provenance = json.loads(publisher.read_text("direct_url.json") or "null")
        vcs = provenance.get("vcs_info") if isinstance(provenance, dict) else None
        if (
            not isinstance(vcs, dict)
            or vcs.get("vcs") != "git"
            or provenance.get("url", "").removesuffix(".git")
            != PUBLISHER_URL.removesuffix(".git")
            or not isinstance(vcs.get("commit_id"), str)
        ):
            return blocked(
                "PUBLISHER_PROVENANCE_UNKNOWN",
                "the installed package does not identify the reviewed Git source.",
            )
    except (OSError, ValueError, AttributeError):
        return blocked("PUBLISHER_PROVENANCE_UNKNOWN", "installed Git metadata is unreadable.")

    if vcs["commit_id"] != REVIEWED_REVISION:
        return blocked(
            "PUBLISHER_REVISION_MISMATCH",
            f"installed {vcs['commit_id']}; reviewed {REVIEWED_REVISION}.",
        )
    if not any(
        entry.group == "console_scripts" and entry.name == "pmpe"
        for entry in publisher.entry_points
    ):
        return blocked("PUBLISHER_ENTRY_POINT_MISSING", "the pmpe console entry point is absent.")

    print(f"HANDOFF_SETUP_OK: reviewed publisher {REVIEWED_REVISION}")
    print(f"Checked Python: {sys.executable}")
    print("Checked installation metadata only; contract approval and compilation remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
