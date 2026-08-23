#!/usr/bin/env python3
"""Execute PMOS contract fixtures against the pinned Production Engineering OS compiler."""

from __future__ import annotations

import json
from pathlib import Path

from pmpe.barebones import default_template
from pmpe.contracts.acceptance import AcceptanceCompileError, compile_acceptance_plan

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "decision-to-contract"


def compile_fixture(path: Path) -> None:
    contract = json.loads(path.read_text(encoding="utf-8"))
    template = default_template()
    compile_acceptance_plan(
        contract,
        repository_root=ROOT,
        registered_actions=frozenset(template.actions),
        template_version=template.version,
        template_test_digests={},
        registered_measures=frozenset(template.measures),
    )


def main() -> int:
    compile_fixture(FIXTURES / "valid-contract.json")
    try:
        compile_fixture(FIXTURES / "invalid-prose-contract.json")
    except AcceptanceCompileError as error:
        codes = {diagnostic.code for diagnostic in error.diagnostics}
        if "CRITERION_FORM_INVALID" not in codes:
            raise AssertionError(f"unexpected compiler diagnostics: {sorted(codes)}") from error
    else:
        raise AssertionError("prose-only contract unexpectedly compiled")
    print("PASS PMOS decision contract is accepted and planted prose is rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
