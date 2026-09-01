#!/usr/bin/env python3
"""Execute PMOS contract fixtures against the pinned Production Engineering OS compiler."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from pmpe.barebones import default_template
from pmpe.contracts.acceptance import AcceptanceCompileError, compile_acceptance_plan
from pmpe.contracts.authoring import (
    approve_contract_draft,
    build_contract_draft,
    verify_contract_approval,
    write_json_atomic,
)
from pmpe.contracts.model import load_contract
from pmpe.domain.errors import ContractViolation
from pmpe.engineering.handoff import start_approved_run

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
    authored = build_contract_draft(load_fixture(FIXTURES / "valid-answers.json"))
    if authored.draft is None or authored.draft_digest is None:
        raise AssertionError(f"complete PMOS answers were blocked: {authored.blocking_questions}")
    approved = approve_contract_draft(
        authored.draft,
        expected_draft_digest=authored.draft_digest,
        approver="fixture-human",
        approved_at="2026-08-23T00:00:00Z",
    )
    valid = approved.contract
    receipt = approved.receipt
    if valid != load_fixture(FIXTURES / "valid-contract.json"):
        raise AssertionError("committed approved contract differs from publisher output")
    if receipt != load_fixture(FIXTURES / "valid-approval-receipt.json"):
        raise AssertionError("committed approval receipt differs from publisher output")
    verify_contract_approval(valid, receipt, expected_approver="fixture-human")
    compile_fixture(FIXTURES / "valid-contract.json")
    with tempfile.TemporaryDirectory(prefix="pmos-peos-handoff-") as directory:
        root = Path(directory)
        contract_path = root / "contract.json"
        receipt_path = root / "receipt.json"
        write_json_atomic(contract_path, valid)
        write_json_atomic(receipt_path, receipt)
        if not load_contract(contract_path).runnable:
            raise AssertionError("published contract is not runnable")
        run = start_approved_run(
            contract_path=contract_path,
            receipt_path=receipt_path,
            expected_approver="fixture-human",
            run_dir=root / "run",
            agents_dir=ROOT / ".claude" / "agents",
        )
        if run.status()["stage"] != "assessment":
            raise AssertionError("engineering handoff did not start at assessment")
    tampered = json.loads(json.dumps(valid))
    tampered["functional_requirements"][0]["description"] = "unapproved edit"
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
    print(
        "PASS answers publish an exact approved contract, engineering handoff starts, "
        "and planted failures are rejected"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
