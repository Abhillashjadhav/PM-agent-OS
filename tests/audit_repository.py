#!/usr/bin/env python3
"""Offline structural audit for PM-agent-OS repository claims."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parent.parent
KEBAB_CASE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
EXPECTED_STAGE_TOTALS = {
    "discovery": 7,
    "strategy": 6,
    "build": 10,
    "launch": 5,
    "iterate": 12,
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def audit_readme_links(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    for destination in MARKDOWN_LINK.findall(readme.read_text(encoding="utf-8")):
        target = destination.strip().split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith("#"):
            continue
        path = unquote(parsed.path)
        if not path:
            continue
        if not (readme.parent / path).resolve().is_file():
            fail(errors, f"README local link does not resolve: {destination}")


def main() -> int:
    errors: list[str] = []
    try:
        inventory = json.loads((ROOT / "inventory.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL inventory.json cannot be read: {exc}")
        return 1

    skills = inventory.get("lifecycle_skills")
    personas = inventory.get("reviewer_personas")
    supporting = inventory.get("supporting_skills")
    if not isinstance(skills, list):
        fail(errors, "inventory lifecycle_skills must be a list")
        skills = []
    if not isinstance(personas, list):
        fail(errors, "inventory reviewer_personas must be a list")
        personas = []
    if not isinstance(supporting, list):
        fail(errors, "inventory supporting_skills must be a list")
        supporting = []

    stage_totals = {stage: 0 for stage in EXPECTED_STAGE_TOTALS}
    for skill in skills:
        if not isinstance(skill, dict):
            fail(errors, "lifecycle skill entry must be an object")
            continue
        name = skill.get("name")
        stage = skill.get("lifecycle_stage")
        skill_path = skill.get("skill_path")
        fixture_path = skill.get("fixture_path")
        validation_level = skill.get("validation_level")
        if not isinstance(name, str) or not KEBAB_CASE.fullmatch(name):
            fail(errors, f"invalid inventory skill name: {name!r}")
        if stage not in stage_totals:
            fail(errors, f"invalid lifecycle stage for {name}: {stage!r}")
        else:
            stage_totals[stage] += 1
        if not isinstance(validation_level, str) or not validation_level:
            fail(errors, f"missing validation level for {name}")
        for label, relative_path in (("skill", skill_path), ("fixture", fixture_path)):
            if not isinstance(relative_path, str) or not (ROOT / relative_path).is_file():
                fail(errors, f"{label} path missing for {name}: {relative_path!r}")
        if not isinstance(skill_path, str) or not (ROOT / skill_path).is_file():
            continue
        text = (ROOT / skill_path).read_text(encoding="utf-8")
        frontmatter = FRONTMATTER.match(text)
        if not frontmatter:
            fail(errors, f"YAML frontmatter missing for {skill_path}")
            continue
        try:
            metadata = yaml.safe_load(frontmatter.group(1))
        except yaml.YAMLError as exc:
            fail(errors, f"YAML frontmatter does not parse for {skill_path}: {exc}")
            continue
        if not isinstance(metadata, dict):
            fail(errors, f"YAML frontmatter is not a mapping for {skill_path}")
            continue
        metadata_name = metadata.get("name")
        if not isinstance(metadata_name, str) or not KEBAB_CASE.fullmatch(metadata_name):
            fail(errors, f"frontmatter name is not kebab-case for {skill_path}")
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            fail(errors, f"frontmatter description missing for {skill_path}")
        if not re.search(r"^##\s+Limitations\s*$", text, re.MULTILINE):
            fail(errors, f"Limitations section missing for {skill_path}")

    for skill in supporting:
        if not isinstance(skill, dict):
            fail(errors, "supporting skill entry must be an object")
            continue
        name = skill.get("name")
        skill_path = skill.get("skill_path")
        fixture_path = skill.get("fixture_path")
        validation_level = skill.get("validation_level")
        if not isinstance(name, str) or not KEBAB_CASE.fullmatch(name):
            fail(errors, f"invalid supporting skill name: {name!r}")
        if not isinstance(validation_level, str) or not validation_level:
            fail(errors, f"missing validation level for supporting skill {name}")
        for label, relative_path in (("skill", skill_path), ("fixture", fixture_path)):
            if not isinstance(relative_path, str) or not (ROOT / relative_path).is_file():
                fail(errors, f"{label} path missing for supporting skill {name}: {relative_path!r}")
        if isinstance(skill_path, str) and (ROOT / skill_path).is_file():
            text = (ROOT / skill_path).read_text(encoding="utf-8")
            frontmatter = FRONTMATTER.match(text)
            if not frontmatter:
                fail(errors, f"YAML frontmatter missing for {skill_path}")
                continue
            try:
                metadata = yaml.safe_load(frontmatter.group(1))
            except yaml.YAMLError as exc:
                fail(errors, f"YAML frontmatter does not parse for {skill_path}: {exc}")
                continue
            if not isinstance(metadata, dict):
                fail(errors, f"YAML frontmatter is not a mapping for {skill_path}")
                continue
            metadata_name = metadata.get("name")
            if not isinstance(metadata_name, str) or not KEBAB_CASE.fullmatch(metadata_name):
                fail(errors, f"frontmatter name is not kebab-case for {skill_path}")
            if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
                fail(errors, f"frontmatter description missing for {skill_path}")
            if not re.search(r"^##\s+Limitations\s*$", text, re.MULTILINE):
                fail(errors, f"Limitations section missing for {skill_path}")

    for field in ("name", "skill_path", "fixture_path"):
        values = [item.get(field) for item in supporting if isinstance(item, dict)]
        if len(values) != len(set(values)):
            fail(errors, f"supporting skill {field} values must be unique")

    if len(supporting) != 3:
        fail(errors, f"supporting skill total is {len(supporting)}, expected 3")

    for stage, expected in EXPECTED_STAGE_TOTALS.items():
        if stage_totals[stage] != expected:
            fail(errors, f"{stage} total is {stage_totals[stage]}, expected {expected}")
    if len(skills) != 40:
        fail(errors, f"lifecycle skill total is {len(skills)}, expected 40")
    if len(personas) != 7:
        fail(errors, f"reviewer persona total is {len(personas)}, expected 7")
    for persona in personas:
        if not isinstance(persona, dict) or not isinstance(persona.get("path"), str):
            fail(errors, f"invalid reviewer persona entry: {persona!r}")
        elif not (ROOT / persona["path"]).is_file():
            fail(errors, f"reviewer persona path missing: {persona['path']}")

    audit_readme_links(errors)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("PASS repository audit: 40 lifecycle skills, 3 supporting skills, 7 reviewer personas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
