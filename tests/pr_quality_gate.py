#!/usr/bin/env python3
"""Deterministic pull-request quality checks for this repository."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_PATH_PARTS = {"__pycache__", ".pytest_cache", "node_modules"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}
FORBIDDEN_TOP_LEVEL = {"build", "dist", ".coverage"}


def run(command: list[str], *, capture: bool = False) -> str:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=capture)
    if completed.returncode:
        if capture:
            sys.stderr.write(completed.stdout)
            sys.stderr.write(completed.stderr)
        raise RuntimeError("command failed: " + " ".join(command))
    return completed.stdout


def changed_paths(base_ref: str) -> list[str]:
    return [path for path in run(["git", "diff", "--name-only", f"{base_ref}...HEAD"], capture=True).splitlines() if path]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", required=True, help="merge-base reference for the PR")
    args = parser.parse_args()
    try:
        run([sys.executable, "tests/audit_repository.py"])
        run(["git", "diff", "--check", f"{args.base_ref}...HEAD"])
        paths = changed_paths(args.base_ref)
        for path in paths:
            parts = Path(path).parts
            if (set(parts) & FORBIDDEN_PATH_PARTS) or Path(path).suffix in FORBIDDEN_SUFFIXES or parts[0] in FORBIDDEN_TOP_LEVEL:
                raise RuntimeError(f"unrelated generated/runtime output changed: {path}")
        base_inventory = json.loads(
            run(["git", "show", f"{args.base_ref}:inventory.json"], capture=True)
        )
        protected_paths = [
            entry["skill_path"] for entry in base_inventory["lifecycle_skills"]
        ]
        protected_paths += [
            entry["skill_path"] for entry in base_inventory.get("supporting_skills", [])
        ]
        protected_paths += [entry["path"] for entry in base_inventory["reviewer_personas"]]
        deleted = set(run(["git", "diff", "--diff-filter=D", "--name-only", f"{args.base_ref}...HEAD"], capture=True).splitlines())
        for path in protected_paths:
            if path in deleted:
                raise RuntimeError(f"inventoried path deleted by PR: {path}")
        for path in paths:
            if path.endswith(".py"):
                run([sys.executable, "-m", "py_compile", path])
        skill_paths = sorted(ROOT.glob("**/SKILL.md"))
        for skill_path in skill_paths:
            run([sys.executable, "tests/lint_skill.py", str(skill_path.relative_to(ROOT))])
        changed_skills = [path for path in paths if path.endswith("/SKILL.md") or path == "SKILL.md"]
        for path in changed_skills:
            run([sys.executable, "tests/lint_skill.py", path])
    except RuntimeError as error:
        print(f"FAIL PR quality gate: {error}")
        return 1
    print("PASS deterministic PR quality gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
