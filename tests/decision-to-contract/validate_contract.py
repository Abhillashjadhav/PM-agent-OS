#!/usr/bin/env python3
"""Execute PMOS contract fixtures against the pinned Production Engineering OS compiler."""

from __future__ import annotations

import json
from pathlib import Path

from pmpe.barebones import default_template
from pmpe.contracts.acceptance import AcceptanceCompileError, compile_acceptance_plan
from pmpe.contracts.authoring import verify_contract_approval
from pmpe.domain.errors import ContractViolation

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "decision-to-contract"


def load_fixture(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def compile_fixture(path: Path) -> None:
    contract = load_fixture(path)
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
    valid = load_fixture(FIXTURES / "valid-contract.json")
    receipt = load_fixture(FIXTURES / "valid-approval-receipt.json")
    verify_contract_approval(valid, receipt, expected_approver="fixture-human")
    compile_fixture(FIXTURES / "valid-contract.json")
    tampered = json.loads(json.dumps(valid))
    tampered["functional_requirements"]["FR-001"]["statement"] = "unapproved edit"
    try:
        verify_contract_approval(tampered, receipt, expected_approver="fixture-human")
    except ContractViolation:
        pass
    else:
        raise AssertionError("tampered contract reused an approval receipt")
    try:
        compile_fixture(FIXTURES / "invalid-prose-contract.json")
    except AcceptanceCompileError as error:
        codes = {diagnostic.code for diagnostic in error.diagnostics}
        if "CRITERION_FORM_INVALID" not in codes:
            raise AssertionError(f"unexpected compiler diagnostics: {sorted(codes)}") from error
    else:
        raise AssertionError("prose-only contract unexpectedly compiled")
    print("PASS exact approval is bound, contract is accepted, and planted failures are rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
