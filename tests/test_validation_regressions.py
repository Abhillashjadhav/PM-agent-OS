"""Black-box regressions for repository validation's fail-closed boundary."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ValidationRegressions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pmos-validation-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def command(self, *args):
        return subprocess.run([sys.executable, *args], cwd=self.root, text=True,
                              capture_output=True, timeout=20)

    def replace_metadata(self, name, description):
        path = self.root / ".claude/skills" / name / "SKILL.md"
        text = re.sub(r"\A---\n.*?\n---", lambda _: f"---\nname: {name}\ndescription: {description}\n---",
                      path.read_text(), count=1, flags=re.S)
        path.write_text(text)
        return str(path)

    def test_unquoted_mapping_in_description_is_rejected(self):
        path = self.replace_metadata("decision-to-contract", "Invalid YAML: Use when converting, Do NOT use otherwise.")
        for args in [("tests/lint_skill.py", path), ("tests/audit_repository.py",)]:
            with self.subTest(args=args):
                result = self.command(*args)
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_boolean_description_cannot_bypass_lint(self):
        path = self.replace_metadata("decision-to-contract", "true")
        result = self.command("tests/lint_skill.py", path)
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_valid_inline_comment_preserves_description(self):
        path = self.replace_metadata("decision-to-contract", "Use when needed. Do NOT use otherwise. # note: valid comment")
        for args in [("tests/lint_skill.py", path), ("tests/audit_repository.py",)]:
            result = self.command(*args)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_inventory_cannot_substitute_another_file_for_skill(self):
        path = self.root / "inventory.json"
        data = json.loads(path.read_text())
        entry = data["lifecycle_skills"][0]
        actual = self.root / entry["skill_path"]
        alternate = actual.with_name("OTHER.md")
        alternate.write_text(actual.read_text())
        actual.write_text("Invalid installed skill without frontmatter.\n")
        entry["skill_path"] = str(alternate.relative_to(self.root))
        path.write_text(json.dumps(data))
        result = self.command("tests/audit_repository.py")
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_duplicate_inventory_cannot_replace_a_missing_skill(self):
        path = self.root / "inventory.json"
        data = json.loads(path.read_text())
        original = data["lifecycle_skills"][1]
        self.assertEqual(original["lifecycle_stage"], data["lifecycle_skills"][0]["lifecycle_stage"])
        shutil.rmtree((self.root / original["skill_path"]).parent)
        data["lifecycle_skills"][1] = data["lifecycle_skills"][0]
        path.write_text(json.dumps(data))
        result = self.command("tests/audit_repository.py")
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_unlisted_skill_is_not_silently_installed(self):
        extra = self.root / ".claude/skills/stray-skill"
        extra.mkdir()
        (extra / "SKILL.md").write_text("This skill has no frontmatter or verification.\n")
        target = Path(self.temp.name) / "target"
        result = self.command("scripts/install.py", "--target", str(target))
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertFalse(target.exists())

    def test_lifecycle_metadata_name_must_match_inventory(self):
        data = json.loads((self.root / "inventory.json").read_text())
        path = self.root / data["lifecycle_skills"][0]["skill_path"]
        path.write_text(re.sub(r"(?m)^name: .*$", "name: different-valid-name", path.read_text(), count=1))
        result = self.command("tests/audit_repository.py")
        self.assertNotEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
