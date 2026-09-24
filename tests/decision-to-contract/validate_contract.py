#!/usr/bin/env python3
"""Prove the current PMOS handoff, or explicitly select historical intake smoke."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
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


def validate_legacy_intake() -> int:
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
        "LEGACY INTAKE: PASS exact publisher/receipt compatibility and assessment admission; "
        "this is not current-run RELEASE_READY evidence"
    )
    return 0


class FixtureProvider:
    """Return fixed TEST-ONLY programs; never invoke a model or external service."""

    def __init__(self, status: str) -> None:
        self.status = status
        self.calls = 0

    def invoke(self, *, purpose, request):
        self.calls += 1
        response = {
            "request_digest": request["request_digest"],
            "provider_metadata": {
                "provider": "test-only-scripted-fixture",
                "model": "no-model-called",
                "prompt_version": "f10-compatibility-v1",
            },
        }
        if purpose == "code":
            response["files"] = {
                "product.py": (
                    '"""TEST-ONLY fixed health fixture, not model-generated code."""\n\n'
                    "def health():\n"
                    f"    return {{'status': {self.status!r}}}\n"
                )
            }
        elif purpose == "advisory_review":
            response["summary"] = "TEST-ONLY compatibility evidence; no release authorization."
        else:
            raise AssertionError(f"unexpected fixture provider purpose: {purpose}")
        return response


class FixtureExecution:
    """Execute only the fixed health fixtures locally; this is not OS isolation."""

    def __init__(self) -> None:
        self.calls = 0

    def run(self, workspace, argv, *, timeout_seconds, environment):
        from pmpe.barebones import ContractInvalidError

        self.calls += 1
        if tuple(argv[:4]) != (sys.executable, "-I", "-B", "-c") or tuple(argv[6:8]) != (
            "product", "health"
        ):
            raise ContractInvalidError("test executor accepts only the fixed health action")
        command = list(argv)
        command[4] = command[4].replace("'/workspace'", repr(str(workspace)))
        try:
            return subprocess.run(
                command, cwd=workspace, text=True, capture_output=True,
                timeout=timeout_seconds, check=False, env=dict(environment),
            )
        except subprocess.TimeoutExpired as error:
            raise ContractInvalidError("test fixture execution timed out") from error


def publish_test_fixture(*, bound: bool):
    """Issue synthetic test approval; never reuse or impersonate an owner receipt."""
    answers = load_fixture(FIXTURES / "valid-answers.json")
    answers["contract_id"] = "TEST-ONLY-F10-HEALTH" + ("" if bound else "-UNBOUND")
    answers["product_name"] = "TEST-ONLY health handoff compatibility fixture"
    answers["approved_product_decisions"] = [{
        "id": "APD-001",
        "decision": "Synthetic fixture issuance only; this is not product-owner approval.",
    }]
    if bound:
        answers["binary_release_gates"][0]["acceptance_criterion_refs"] = ["AC-001"]
    authored = build_contract_draft(answers)
    if authored.draft is None or authored.draft_digest is None:
        raise AssertionError(f"test fixture publisher blocked: {authored.blocking_questions}")
    return approve_contract_draft(
        authored.draft,
        expected_draft_digest=authored.draft_digest,
        approver="test-only-fixture-issuer",
        approved_at="2026-09-24T00:00:00Z",
    )


def verify_current_evidence(root: Path, result, contract, *, gate_status: str):
    from pmpe.contracts.canonical import canonical_digest
    from pmpe.evidence.ledger import EvidenceLedger

    ledger = EvidenceLedger.open_existing(root, result.run_id)
    events = list(ledger.verify())
    approval = events[0]["payload"]["approval"]
    if approval["status"] != "VERIFIED" or approval["authority"] != "test-only-fixture-issuer":
        raise AssertionError("current handoff did not retain verified TEST-ONLY approval")
    baseline = next(event for event in events if event["event_type"] == "meaningful_red_confirmed")
    if not baseline["payload"]["findings"] or any(
        item["code"] != "ASSERTION_FAILED" or item["subject_id"] != "AC-001"
        for item in baseline["payload"]["findings"]
    ):
        raise AssertionError("baseline did not fail the intended acceptance assertion")
    gates = [event for event in events if event["event_type"] == "release_gates_evaluated"]
    if len(gates) != 1:
        raise AssertionError("current runner omitted the explicit release-gate result")
    payload = gates[0]["payload"]
    expected_plan = events[0]["payload"]["plan_digest"]
    if payload["contract_digest"] != canonical_digest(contract) or payload["plan_digest"] != expected_plan:
        raise AssertionError("gate result is not bound to this contract and plan")
    if len(payload["gates"]) != 1:
        raise AssertionError("expected exactly the single declared release gate")
    gate = payload["gates"][0]
    if (gate["gate_id"], gate["acceptance_criterion_refs"], gate["status"]) != (
        "GATE-001", ["AC-001"], gate_status
    ):
        raise AssertionError("release gate did not match the candidate's acceptance result")
    if len(gate["criterion_results"]) != 1 or (
        gate["criterion_results"][0]["criterion_id"], gate["criterion_results"][0]["status"]
    ) != ("AC-001", gate_status):
        raise AssertionError("release gate did not retain the criterion outcome")
    ledger.read_blob(payload["candidate_digest"])
    releases = [event for event in events if event["event_type"] == "release_ready"]
    if gate_status == "PASS":
        if len(releases) != 1:
            raise AssertionError("passing current handoff did not reach release_ready")
        release = releases[0]["payload"]
        if release["candidate_digest"] != payload["candidate_digest"]:
            raise AssertionError("release candidate differs from evaluated candidate")
        gate_digest = release["release_gate_evidence_digest"]
        if gate_digest not in gates[0]["blob_digests"]:
            raise AssertionError("release does not retain the gate evidence blob")
        ledger.read_blob(gate_digest)
    elif releases:
        raise AssertionError("broken candidate emitted release_ready")
    return {"state": result.state.value, "cause": result.cause, "gate": gate_status,
            "fixture_provider_calls": result.model_calls, "events": len(events)}


def validate_current_handoff(root: Path) -> int:
    from pmpe.barebones import BudgetCaps, RunState, run_to_release_ready

    if root.exists() and any(root.iterdir()):
        raise AssertionError("fixture evidence directory must be empty")
    root.mkdir(parents=True, exist_ok=True)
    fixture = publish_test_fixture(bound=True)
    write_json_atomic(root / "test-only-contract.json", fixture.contract)
    write_json_atomic(root / "test-only-approval-receipt.json", fixture.receipt)
    summary = {
        "classification": "TEST-ONLY deterministic current-run compatibility",
        "approval": "test-issued receipt; not product-owner approval",
        "limitations": ["No external model call or new live generation.",
                        "Fixed fixture programs execute locally without OS isolation.",
                        "No deployment, release authorization, or production-readiness claim."],
        "cases": {},
    }
    for label, status, state, gate_status in (
        ("positive", "ok", RunState.RELEASE_READY, "PASS"),
        ("broken-candidate", "broken", RunState.HALTED, "FAIL"),
    ):
        repository = root / label
        result = run_to_release_ready(
            contract=fixture.contract, repository_root=repository,
            workspace=repository / "candidate", run_id=f"test-only-f10-{label}",
            provider=FixtureProvider(status), candidate_sandbox=FixtureExecution(),
            budget=BudgetCaps(max_attempts=1, max_model_calls=2),
            approval_receipt=fixture.receipt, approval_authority="test-only-fixture-issuer",
            approval_receipt_bytes=(root / "test-only-approval-receipt.json").read_bytes(),
        )
        if result.state is not state:
            raise AssertionError(f"{label}: expected {state}, got {result.state}: {result.cause}")
        summary["cases"][label] = verify_current_evidence(
            repository, result, fixture.contract, gate_status=gate_status
        )
    unbound = publish_test_fixture(bound=False)
    provider, execution = FixtureProvider("ok"), FixtureExecution()
    write_json_atomic(root / "test-only-unbound-contract.json", unbound.contract)
    write_json_atomic(root / "test-only-unbound-receipt.json", unbound.receipt)
    try:
        run_to_release_ready(
            contract=unbound.contract, repository_root=root / "unbound-gate",
            workspace=root / "unbound-gate/candidate", run_id="test-only-f10-unbound",
            provider=provider, candidate_sandbox=execution,
            budget=BudgetCaps(max_attempts=1, max_model_calls=2),
            approval_receipt=unbound.receipt, approval_authority="test-only-fixture-issuer",
            approval_receipt_bytes=(root / "test-only-unbound-receipt.json").read_bytes(),
        )
    except AcceptanceCompileError as error:
        codes = {diagnostic.code for diagnostic in error.diagnostics}
        if codes != {"RELEASE_GATE_UNBOUND"} or provider.calls or execution.calls:
            raise AssertionError("unbound gate did not fail closed before execution") from error
        summary["cases"]["unbound-gate"] = {
            "state": "CONTRACT_BLOCKED", "diagnostics": sorted(codes),
            "fixture_provider_calls": provider.calls, "execution_calls": execution.calls,
        }
    else:
        raise AssertionError("description-only release gate unexpectedly reached the runner")
    write_json_atomic(root / "summary.json", summary)
    print("CURRENT HANDOFF: PASS — TEST-ONLY RELEASE_READY / HALTED / CONTRACT_BLOCKED")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-intake", action="store_true",
                        help="run preserved publisher/receipt/assessment compatibility only")
    parser.add_argument("--evidence-dir", type=Path,
                        help="retain TEST-ONLY current-run ledgers in an empty directory")
    args = parser.parse_args(argv)
    if args.legacy_intake:
        if args.evidence_dir is not None:
            parser.error("--evidence-dir applies to the current-run fixture only")
        return validate_legacy_intake()
    if args.evidence_dir is not None:
        return validate_current_handoff(args.evidence_dir)
    with tempfile.TemporaryDirectory(prefix="pmos-current-handoff-") as directory:
        return validate_current_handoff(Path(directory))


if __name__ == "__main__":
    raise SystemExit(main())
