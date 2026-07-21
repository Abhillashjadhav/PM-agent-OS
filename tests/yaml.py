"""Small YAML mapping loader for this repository's scalar-only frontmatter.

The skill frontmatter schema deliberately contains only top-level scalar values, so
this keeps repository validation offline without a third-party dependency.
"""
from __future__ import annotations

import ast
import json
import re


class YAMLError(ValueError):
    """Raised when scalar-only YAML frontmatter is malformed."""


_KEY = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


def _scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise YAMLError(str(exc)) from exc
        if not isinstance(parsed, str):
            raise YAMLError("quoted scalar must be a string")
        return parsed
    if value.startswith("'"):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise YAMLError(str(exc)) from exc
        if not isinstance(parsed, str):
            raise YAMLError("quoted scalar must be a string")
        return parsed
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "NULL", "~"}:
        return None
    return value


def safe_load(source: str) -> dict[str, object]:
    """Parse the scalar-only YAML mapping used by SKILL.md frontmatter."""
    lines = source.splitlines()
    result: dict[str, object] = {}
    index = 0
    while index < len(lines):
        line_number = index + 1
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line[0].isspace() or ":" not in line:
            raise YAMLError(f"line {line_number}: expected a top-level key/value pair")
        key, value = line.split(":", 1)
        if not _KEY.fullmatch(key):
            raise YAMLError(f"line {line_number}: invalid key {key!r}")
        if key in result:
            raise YAMLError(f"line {line_number}: duplicate key {key!r}")
        if value.strip() in {">", "|"}:
            folded: list[str] = []
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index][0].isspace()):
                if lines[index].strip():
                    folded.append(lines[index].strip())
                index += 1
            result[key] = (" " if value.strip() == ">" else "\n").join(folded)
            continue
        result[key] = _scalar(value)
        index += 1
    return result
