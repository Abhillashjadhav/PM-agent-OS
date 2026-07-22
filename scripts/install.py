#!/usr/bin/env python3
"""Safely install PM-agent-OS skills and reviewer agents into Claude Code."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_GROUPS = {
    "skills": ROOT / ".claude" / "skills",
    "agents": ROOT / ".claude" / "agents",
}


def parse_args() -> argparse.Namespace:
    default_target = Path(os.environ.get("CLAUDE_HOME", Path.home() / ".claude"))
    parser = argparse.ArgumentParser(
        description="Install PM-agent-OS skills and reviewer agents without silent overwrites."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=default_target,
        help="Claude home directory (default: CLAUDE_HOME or ~/.claude).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing entries with the same names after repository validation.",
    )
    return parser.parse_args()


def entries() -> list[tuple[str, Path, Path]]:
    planned: list[tuple[str, Path, Path]] = []
    for group, source_root in SOURCE_GROUPS.items():
        if not source_root.is_dir():
            raise FileNotFoundError(f"missing source directory: {source_root}")
        for source in sorted(source_root.iterdir(), key=lambda path: path.name):
            planned.append((group, source, Path(group) / source.name))
    return planned


def validate_repository() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "tests" / "audit_repository.py")],
        cwd=ROOT,
        check=True,
    )


def install(target: Path, force: bool) -> tuple[int, int]:
    planned = entries()
    conflicts = [target / relative for _, _, relative in planned if (target / relative).exists()]
    if conflicts and not force:
        rendered = "\n".join(f"  - {path}" for path in conflicts)
        raise FileExistsError(
            "installation would overwrite existing Claude entries:\n"
            f"{rendered}\n"
            "Re-run with --force only after reviewing the conflicts."
        )

    validate_repository()

    skill_count = 0
    agent_count = 0
    for group, source, relative in planned:
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if destination.is_dir():
                shutil.rmtree(destination)
            else:
                destination.unlink()
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        if group == "skills":
            skill_count += 1
        else:
            agent_count += 1

    return skill_count, agent_count


def main() -> int:
    args = parse_args()
    target = args.target.expanduser().resolve()
    try:
        skill_count, agent_count = install(target, args.force)
    except (FileExistsError, FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"INSTALLATION BLOCKED: {exc}", file=sys.stderr)
        return 2

    print(f"Installed {skill_count} skills and {agent_count} reviewer agents into {target}")
    print("Next: open Claude Code and invoke /pm, or ask for one of the starter workflows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
