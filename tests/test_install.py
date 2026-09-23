#!/usr/bin/env python3
"""Exercise installer safety through its public CLI in disposable repositories."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def contents(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


class InstallerSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="pmos-install-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repository = self.root / "repository"
        shutil.copytree(
            ROOT,
            self.repository,
            ignore=shutil.ignore_patterns(".git", "__pycache__"),
        )
        self.source = self.repository / ".claude"
        self.target = self.root / "claude-home"

    def install(
        self, *, target: Path | None = None, force: bool = False
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(self.repository / "scripts" / "install.py"),
            "--target",
            str(target if target is not None else self.target),
        ]
        if force:
            command.append("--force")
        return subprocess.run(command, capture_output=True, text=True, timeout=20)

    def assert_installed(self) -> None:
        for group in ("skills", "agents"):
            self.assertEqual(contents(self.source / group), contents(self.target / group))

    def test_clean_install_refuses_overwrite_and_force_replaces(self) -> None:
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_installed()
        marker = self.target / "skills" / "pm" / "local-note.txt"
        marker.write_text("keep unless replacement is explicit")
        result = self.install()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertTrue(marker.is_file())
        result = self.install(force=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists())
        self.assert_installed()

    def test_dangling_reviewer_link_requires_force(self) -> None:
        link = self.target / "agents" / "customer-reviewer.md"
        link.parent.mkdir(parents=True)
        outside = self.root / "outside-reviewer.md"
        link.symlink_to(outside)
        result = self.install()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertTrue(link.is_symlink())
        self.assertFalse(outside.exists())
        self.assertFalse((self.target / "skills").exists())

    def test_force_replaces_dangling_reviewer_link_without_writing_referent(self) -> None:
        link = self.target / "agents" / "customer-reviewer.md"
        link.parent.mkdir(parents=True)
        outside = self.root / "outside-reviewer.md"
        link.symlink_to(outside)
        result = self.install(force=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(link.is_symlink())
        self.assertFalse(outside.exists())
        self.assert_installed()

    def test_force_replaces_directory_link_without_changing_referent(self) -> None:
        link = self.target / "skills" / "ai-feature-go-no-go"
        link.parent.mkdir(parents=True)
        outside = self.root / "outside-skill"
        outside.mkdir()
        (outside / "local-note.txt").write_text("preserve external skill")
        before = contents(outside)
        link.symlink_to(outside, target_is_directory=True)
        result = self.install(force=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(link.is_symlink())
        self.assertEqual(contents(outside), before)
        self.assert_installed()

    def test_source_target_is_rejected_before_modification(self) -> None:
        before = contents(self.source)
        result = self.install(target=self.source, force=True)
        self.assertEqual(contents(self.source), before)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("overlaps source", result.stderr)

    def test_symlinked_group_into_source_is_rejected_before_modification(self) -> None:
        self.target.mkdir()
        (self.target / "skills").symlink_to(self.source / "skills", target_is_directory=True)
        before = contents(self.source)
        result = self.install(force=True)
        self.assertEqual(contents(self.source), before)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("overlaps source", result.stderr)
        self.assertFalse((self.target / "agents").exists())

    def test_force_can_replace_leaf_link_to_source(self) -> None:
        link = self.target / "skills" / "pm"
        link.parent.mkdir(parents=True)
        link.symlink_to(self.source / "skills" / "pm", target_is_directory=True)
        before = contents(self.source)
        result = self.install(force=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(link.is_symlink())
        self.assertEqual(contents(self.source), before)
        self.assert_installed()


if __name__ == "__main__":
    unittest.main()
