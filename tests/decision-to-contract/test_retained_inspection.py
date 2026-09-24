"""Retained TEST-ONLY packets must be interpreted from verified ledger content."""

import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from pmpe import barebones
from pmpe.contracts.canonical import canonical_digest, canonical_json_bytes
from pmpe.evidence import release_gates
from pmpe.evidence.ledger import EvidenceIntegrityError, EvidenceLedger

from test_handoff import SCRIPT, forge_candidate_and_rechain, load_validator


class RetainedInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "packet"
        shutil.copytree(SCRIPT.parents[2] / "reviews/f10-20260924/evidence", self.root)
        self.contract = json.loads((self.root / "test-only-contract.json").read_text())
        self.validator = load_validator()

    def result(self, case="positive"):
        return SimpleNamespace(run_id=f"test-only-f10-{case}",
                               state=barebones.RunState.RELEASE_READY, cause="", model_calls=2)

    def ledger(self, case="positive"):
        return EvidenceLedger.open_existing(self.root / case, self.result(case).run_id)

    def verify(self, case="positive", **kwargs):
        return self.validator.verify_current_evidence(
            self.root / case, self.result(case), self.contract,
            gate_status="PASS" if case == "positive" else "FAIL", **kwargs,
        )

    def rechain(self, ledger, events):
        previous = "sha256:" + "0" * 64
        for sequence, event in enumerate(events, 1):
            event["sequence"] = sequence
            event["previous_digest"] = previous
            event["blob_digests"] = sorted(set(event["blob_digests"]))
            event["event_digest"] = canonical_digest({
                key: value for key, value in event.items() if key != "event_digest"
            })
            previous = event["event_digest"]
        ledger.events_path.write_bytes(b"".join(
            canonical_json_bytes(event) + b"\n" for event in events
        ))
        self.assertEqual(list(ledger.verify())[-1]["event_digest"], previous)

    def invoke(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            try:
                code = self.validator.main(list(args))
            except SystemExit as error:
                code = error.code
        return code, output.getvalue()

    def test_state_cause_and_call_count_come_from_terminal_ledger(self):
        for case, state, cause, calls in (
            ("positive", "RELEASE_READY", "", 2),
            ("broken-candidate", "HALTED", "ATTEMPT_BUDGET_EXHAUSTED", 1),
        ):
            with self.subTest(case=case):
                supplied = self.result(case)
                supplied.state = barebones.RunState.STOPPED
                supplied.cause, supplied.model_calls = "CALLER_CLAIM", 999
                observed = self.validator.verify_current_evidence(
                    self.root / case, supplied, self.contract,
                    gate_status="PASS" if case == "positive" else "FAIL",
                )
                self.assertEqual((observed["state"], observed["cause"],
                                  observed["fixture_provider_calls"]), (state, cause, calls))

    def test_release_followed_by_halt_is_not_a_current_release(self):
        ledger = self.ledger()
        events = list(ledger.verify())
        for event_type, state in (("verification_failed", "BUILDING"), ("halted", "HALTED")):
            events.append({**events[-1], "event_type": event_type, "state": state,
                           "blob_digests": [], "payload": {"cause": "SEEDED_AFTER_RELEASE"}})
        self.rechain(ledger, events)
        with self.assertRaises((AssertionError, EvidenceIntegrityError)):
            self.verify()

    def test_unknown_terminal_event_cannot_claim_release_ready(self):
        ledger = self.ledger()
        events = list(ledger.verify())
        events.append({**events[-1], "event_type": "operator_override", "state": "RELEASE_READY",
                       "blob_digests": [], "payload": {}})
        self.rechain(ledger, events)
        with self.assertRaises((AssertionError, EvidenceIntegrityError)):
            self.verify()

    def test_changed_subject_and_missing_plan_are_rejected_without_anchor(self):
        for mutation in ("subject", "plan"):
            with self.subTest(mutation=mutation):
                ledger = self.ledger()
                original = ledger.events_path.read_bytes()
                events = list(ledger.verify())
                if mutation == "subject":
                    events[-1]["subject_digest"] = "sha256:" + "1" * 64
                else:
                    validation = events[0]
                    metadata = validation["payload"]
                    retained = {metadata["contract_digest"],
                                metadata["approval"]["receipt_blob_digest"]}
                    validation["blob_digests"] = list(retained)
                self.rechain(ledger, events)
                try:
                    with self.assertRaises((AssertionError, EvidenceIntegrityError)):
                        self.verify()
                finally:
                    ledger.events_path.write_bytes(original)

    def test_receipt_content_must_agree_with_recorded_authority_for_both_cases(self):
        for case in ("positive", "broken-candidate"):
            with self.subTest(case=case):
                ledger = self.ledger(case)
                events = list(ledger.verify())
                approval = events[0]["payload"]["approval"]
                old_blob = approval["receipt_blob_digest"]
                receipt = json.loads(ledger.read_blob(old_blob))
                receipt["approved_by"] = "different-fixture-issuer"
                receipt["receipt_digest"] = canonical_digest({
                    key: value for key, value in receipt.items() if key != "receipt_digest"
                })
                blob_bytes = canonical_json_bytes(receipt)
                new_blob = canonical_digest(receipt)
                (ledger.blobs_directory / new_blob.removeprefix("sha256:")).write_bytes(blob_bytes)
                approval["receipt_blob_digest"] = new_blob
                approval["receipt_digest"] = receipt["receipt_digest"]
                events[0]["blob_digests"] = [
                    new_blob if digest == old_blob else digest for digest in events[0]["blob_digests"]
                ]
                self.assertEqual(approval["authority"], "test-only-fixture-issuer")
                self.rechain(ledger, events)
                with self.assertRaises((AssertionError, EvidenceIntegrityError)):
                    self.verify(case)

    def test_shared_validator_failure_is_not_bypassed(self):
        with patch.object(release_gates, "validate_release_gate_evidence",
                          side_effect=EvidenceIntegrityError("seeded shared rejection")) as shared:
            with self.assertRaisesRegex((AssertionError, EvidenceIntegrityError), "seeded shared rejection"):
                self.verify()
        self.assertEqual(shared.call_count, 1)

    def test_cli_reads_existing_packets_and_computes_reader_anchor(self):
        before = {path.relative_to(self.root): path.read_bytes()
                  for path in self.root.rglob("*") if path.is_file()}
        with patch.object(self.validator, "validate_current_handoff",
                          side_effect=AssertionError("inspection must not generate")):
            for case in ("positive", "broken-candidate"):
                head = list(self.ledger(case).verify())[-1]["event_digest"]
                for anchor_args, expected in (
                    ((), {"status": "NOT_PROVIDED"}),
                    (("--expected-head-digest", head),
                     {"status": "VERIFIED", "expected_head_digest": head}),
                ):
                    with self.subTest(case=case, anchor=bool(anchor_args)):
                        code, output = self.invoke("--inspect-evidence-dir", str(self.root),
                                                   "--case", case, *anchor_args)
                        self.assertEqual(code, 0)
                        result = json.loads(output)
                        self.assertEqual(result["head_anchor"], expected)
                        self.assertEqual(result["state"], "RELEASE_READY" if case == "positive" else "HALTED")
        self.assertEqual(before, {path.relative_to(self.root): path.read_bytes()
                                 for path in self.root.rglob("*") if path.is_file()})

    def test_cli_ignores_packet_anchor_claims_and_rejects_forgery_with_original_head(self):
        original_head = forge_candidate_and_rechain(self.root / "positive", self.result().run_id)
        (self.root / "summary.json").write_text(json.dumps({
            "head_check": "MATCHED_EXTERNAL_HEAD", "head_anchor": {"status": "VERIFIED"},
            "head_check_at_capture": "MATCHED_RUNTIME_HEAD",
        }))
        code, output = self.invoke("--inspect-evidence-dir", str(self.root))
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output)["head_anchor"], {"status": "NOT_PROVIDED"})
        code, output = self.invoke("--inspect-evidence-dir", str(self.root),
                                   "--expected-head-digest", original_head)
        self.assertEqual(code, 3)
        self.assertEqual(json.loads(output)["status"], "EVIDENCE_INVALID")

    def test_generation_labels_head_check_as_capture_evidence_only(self):
        generated = Path(self.temporary.name) / "generated"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.validator.validate_current_handoff(generated), 0)
        cases = json.loads((generated / "summary.json").read_text())["cases"]
        for label in ("positive", "broken-candidate"):
            self.assertEqual(cases[label].get("head_check_at_capture"), "MATCHED_RUNTIME_HEAD")
            self.assertNotIn("head_check", cases[label])
            self.assertNotIn("head_anchor", cases[label])

    def test_expected_head_requires_read_only_inspection(self):
        with patch.object(self.validator, "validate_current_handoff",
                          side_effect=AssertionError("bad arguments must not generate")):
            code, _ = self.invoke("--expected-head-digest", "sha256:" + "0" * 64)
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
