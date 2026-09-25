#!/usr/bin/env python3
"""Check clean-user diagnostics without installing or importing the publisher."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_handoff.py"
REVIEWED_REVISION = "297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6"
PUBLISHER_URL = "https://github.com/Abhillashjadhav/production-engineering-os.git"


class HandoffSetupTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="pmos-handoff-setup-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.metadata = self.root / "pmpe-0.2.0.dist-info"

    def installed_metadata(self, revision: str = REVIEWED_REVISION) -> None:
        self.metadata.mkdir()
        (self.metadata / "METADATA").write_text(
            "Metadata-Version: 2.1\nName: pmpe\nVersion: 0.2.0\n",
            encoding="utf-8",
        )
        (self.metadata / "entry_points.txt").write_text(
            "[console_scripts]\npmpe = pmpe.cli:main\n", encoding="utf-8"
        )
        (self.metadata / "direct_url.json").write_text(
            json.dumps(
                {
                    "url": PUBLISHER_URL,
                    "vcs_info": {"vcs": "git", "commit_id": revision},
                }
            ),
            encoding="utf-8",
        )

    def run_check(self) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ, PYTHONPATH=str(self.root))
        return subprocess.run(
            [sys.executable, "-B", "-S", str(SCRIPT)],
            cwd=self.root,
            env=environment,
            text=True,
            capture_output=True,
            timeout=10,
        )

    def assert_blocked(self, diagnostic: str) -> None:
        result = self.run_check()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn(diagnostic, result.stdout + result.stderr)
        self.assertIn("docs/HANDOFF.md", result.stdout + result.stderr)

    def test_missing_publisher_explains_handoff_setup(self) -> None:
        self.assert_blocked("PUBLISHER_NOT_INSTALLED")

    def test_same_package_version_at_other_commit_is_not_accepted(self) -> None:
        self.installed_metadata(revision="5c0f9e3a8f2c66b212c5e1adfb373e4fd2681bf9")
        self.assert_blocked("PUBLISHER_REVISION_MISMATCH")

    def test_unknown_install_provenance_is_not_accepted(self) -> None:
        self.installed_metadata()
        (self.metadata / "direct_url.json").unlink()
        self.assert_blocked("PUBLISHER_PROVENANCE_UNKNOWN")

    def test_malformed_install_metadata_has_actionable_diagnostic(self) -> None:
        self.installed_metadata()
        (self.metadata / "direct_url.json").write_text("[]", encoding="utf-8")
        self.assert_blocked("PUBLISHER_PROVENANCE_UNKNOWN")

    def test_missing_console_entry_point_is_not_accepted(self) -> None:
        self.installed_metadata()
        (self.metadata / "entry_points.txt").unlink()
        self.assert_blocked("PUBLISHER_ENTRY_POINT_MISSING")

    def test_reviewed_metadata_passes_without_loading_package_or_writing(self) -> None:
        self.installed_metadata()
        # No pmpe module exists in this fixture: a metadata check needs no import.
        before = {p.name: p.read_bytes() for p in self.metadata.iterdir()}
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("HANDOFF_SETUP_OK", result.stdout)
        self.assertIn(REVIEWED_REVISION, result.stdout)
        self.assertIn("metadata only", result.stdout)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.metadata.iterdir()})
        self.assertEqual(list(self.root.iterdir()), [self.metadata])


if __name__ == "__main__":
    unittest.main()
