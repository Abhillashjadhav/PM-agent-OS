"""Guard the frozen task-tracker packet against silent drift of its PMOS-owned bytes.

The approved packet in reviews/task-tracker-v1 binds fourteen PM-agent-OS files by
raw SHA-256 inside freeze-manifest.json. The Production Engineering OS entry refuses
to run when any bound byte differs (APPROVAL_BOUND_ARTIFACT_CHANGED). Nothing in this
repository checked that invariant, so a later skill edit broke the frozen journey
without any red signal. This offline test reproduces that check against the working
tree, and separately proves on a disposable copy that a changed bound byte is
reported. Never refresh the manifest digests here to make the live check pass; a
re-freeze is an owner decision recorded in the packet.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "reviews" / "task-tracker-v1"
REPOSITORY = "PM-agent-OS"


def canonical_json(value: object) -> bytes:
    """RFC 8785 serialization for the manifest's string/integer/list/object subset."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def raw_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def drifted_entries(root: Path, manifest: dict) -> list[str]:
    """Return one line per PMOS-bound artifact whose bytes under root differ or are missing."""
    drifted = []
    for entry in manifest["artifacts"]:
        if entry["repository"] != REPOSITORY:
            continue
        path = root / entry["path"]
        actual = raw_digest(path) if path.is_file() else "MISSING"
        if actual != entry["sha256"]:
            drifted.append(f"{entry['path']}: frozen {entry['sha256']} != current {actual}")
    return drifted


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
        self.assertEqual(
            drifted_entries(ROOT, self.manifest),
            [],
            "APPROVAL_BOUND_ARTIFACT_CHANGED. The frozen journey cannot run against this "
            "tree until the owner approves a re-freeze (see reviews/task-tracker-v1/"
            "refreeze-candidate-20261009/README.md). Do not update digests here.",
        )

    def test_a_changed_bound_byte_is_reported_on_a_copy(self) -> None:
        """Negative control: drift detection itself works, independent of the live tree."""
        bound = [e for e in self.manifest["artifacts"] if e["repository"] == REPOSITORY]
        with tempfile.TemporaryDirectory(prefix="freeze-negative-") as temporary:
            copy = Path(temporary)
            for entry in bound:
                target = copy / entry["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / entry["path"], target)
            baseline = drifted_entries(copy, self.manifest)
            victim = copy / "reviews" / "task-tracker-v1" / "contract.approved.json"
            victim.write_bytes(victim.read_bytes() + b"\n")
            after = drifted_entries(copy, self.manifest)
            self.assertEqual(len(after), len(baseline) + 1)
            self.assertTrue(any(line.startswith("reviews/task-tracker-v1/contract.approved.json:") for line in after))
            missing = copy / "reviews" / "task-tracker-v1" / "evaluator.py"
            missing.unlink()
            self.assertTrue(
                any(line.endswith("!= current MISSING") and "evaluator.py" in line for line in drifted_entries(copy, self.manifest))
            )


if __name__ == "__main__":
    unittest.main()
