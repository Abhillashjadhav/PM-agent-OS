"""Guard the frozen task-tracker packet against silent drift of its PMOS-owned bytes.

The approved packet in reviews/task-tracker-v1 binds fourteen PM-agent-OS files by
raw SHA-256 inside freeze-manifest.json. The Production Engineering OS entry refuses
to run when any bound byte differs (APPROVAL_BOUND_ARTIFACT_CHANGED). Nothing in this
repository checked that invariant, so a later skill edit broke the frozen journey
without any red signal. This offline test reproduces that check. It is expected to
stay RED until the owner approves a re-freeze over the current bytes; do not refresh
the manifest digests here to make it pass.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "reviews" / "task-tracker-v1"


def canonical_json(value: object) -> bytes:
    """RFC 8785 serialization for the manifest's string/integer/list/object subset."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def raw_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


class TaskTrackerFreezeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads((PACKET / "freeze-manifest.json").read_text("utf-8"))

    def test_manifest_matches_recorded_freeze_digest(self) -> None:
        recorded = (PACKET / "freeze-bundle.sha256").read_text("utf-8").strip()
        computed = "sha256:" + hashlib.sha256(canonical_json(self.manifest)).hexdigest()
        self.assertEqual(computed, recorded)

    def test_approved_contract_matches_recorded_contract_digest(self) -> None:
        contract = json.loads((PACKET / "contract.approved.json").read_text("utf-8"))
        computed = "sha256:" + hashlib.sha256(canonical_json(contract)).hexdigest()
        self.assertEqual(computed, self.manifest["approved_contract_digest"])

    def test_pmos_bound_artifacts_are_unchanged(self) -> None:
        drifted = []
        for entry in self.manifest["artifacts"]:
            if entry["repository"] != "PM-agent-OS":
                continue
            actual = raw_digest(ROOT / entry["path"])
            if actual != entry["sha256"]:
                drifted.append(f"{entry['path']}: frozen {entry['sha256']} != current {actual}")
        self.assertEqual(
            drifted,
            [],
            "APPROVAL_BOUND_ARTIFACT_CHANGED. The frozen journey cannot run against this "
            "tree until the owner approves a re-freeze (see reviews/task-tracker-v1/"
            "refreeze-candidate-20261009/README.md). Do not update digests here.",
        )


if __name__ == "__main__":
    unittest.main()
