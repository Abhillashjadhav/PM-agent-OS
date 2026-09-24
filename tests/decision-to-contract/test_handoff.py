"""Offline integration regressions for the PMOS handoff entry point."""

import contextlib
import importlib.util
import io
import json
import hashlib
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from pmpe import barebones
from pmpe.contracts.acceptance import AcceptanceCompileError
from pmpe.contracts.canonical import canonical_digest, canonical_json_bytes
from pmpe.evidence.ledger import EvidenceLedger


SCRIPT = Path(__file__).with_name("validate_contract.py")


def load_validator():
    spec = importlib.util.spec_from_file_location("pmos_handoff_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def forge_candidate_and_rechain(root, run_id):
    """Model a writer replacing the entire unsigned packet, only in a temp copy."""
    ledger = EvidenceLedger.open_existing(root, run_id)
    events = list(ledger.verify())
    original_head = events[-1]["event_digest"]
    release = next(event for event in events if event["event_type"] == "release_ready")
    old_candidate = release["payload"]["candidate_digest"]
    old_gate = release["payload"]["release_gate_evidence_digest"]
    manifest = json.loads(ledger.read_blob(old_candidate))

    def store_blob(payload):
        digest = "sha256:" + hashlib.sha256(payload).hexdigest()
        (ledger.blobs_directory / digest.removeprefix("sha256:")).write_bytes(payload)
        return digest

    broken = b"def health():\n    return {'status': 'broken'}\n"
    new_product = store_blob(broken)
    replacements = {manifest["product.py"]: new_product}
    manifest["product.py"] = new_product
    replacements[old_candidate] = store_blob(canonical_json_bytes(manifest))

    def replace(value):
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        if isinstance(value, list):
            return [replace(item) for item in value]
        return replacements.get(value, value) if isinstance(value, str) else value

    gate = replace(json.loads(ledger.read_blob(old_gate)))
    replacements[old_gate] = store_blob(canonical_json_bytes(gate))
    events = replace(events)
    previous = "sha256:" + "0" * 64
    for event in events:
        event["previous_digest"] = previous
        event["blob_digests"] = sorted(set(event["blob_digests"]))
        event["event_digest"] = canonical_digest({
            key: value for key, value in event.items() if key != "event_digest"
        })
        previous = event["event_digest"]
    ledger.events_path.write_bytes(b"".join(canonical_json_bytes(event) + b"\n" for event in events))
    (root / "candidate" / "product.py").write_bytes(broken)
    assert list(ledger.verify())[-1]["event_digest"] != original_head
    assert ledger.read_blob(new_product) == broken
    return original_head


class CurrentHandoffTests(unittest.TestCase):
    def test_trusted_original_head_rejects_self_consistent_candidate_forgery(self):
        validator = load_validator()
        retained = SCRIPT.parents[2] / "reviews/f10-20260924/evidence"
        contract = json.loads((retained / "test-only-contract.json").read_text())
        result = SimpleNamespace(run_id="test-only-f10-positive", state=barebones.RunState.RELEASE_READY,
                                 cause="", model_calls=2)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "positive"
            shutil.copytree(retained / "positive", root)
            trusted_head = forge_candidate_and_rechain(root, result.run_id)
            # This is deliberately still accepted without an external trust anchor.
            unanchored = validator.verify_current_evidence(root, result, contract, gate_status="PASS")
            self.assertEqual(unanchored["state"], "RELEASE_READY")
            with self.assertRaisesRegex(AssertionError, "trusted head digest"):
                validator.verify_current_evidence(
                    root, result, contract, gate_status="PASS", expected_head_digest=trusted_head
                )

    def test_current_fixture_uses_runtime_head_before_retained_packet_is_reopened(self):
        validator = load_validator()
        verify = validator.verify_current_evidence

        def substitute_before_inspection(root, result, contract, **kwargs):
            genuine_head = forge_candidate_and_rechain(root, result.run_id)
            self.assertEqual(kwargs.get("expected_head_digest"), genuine_head)
            return verify(root, result, contract, **kwargs)

        with tempfile.TemporaryDirectory() as directory, patch.object(
            validator, "verify_current_evidence", side_effect=substitute_before_inspection
        ), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(AssertionError, "trusted head digest"):
                validator.validate_current_handoff(Path(directory))

    def test_default_entrypoint_exercises_current_runner_and_negative_controls(self):
        records = []
        current_runner = barebones.run_to_release_ready

        def observe_run(**kwargs):
            record = {"kwargs": kwargs}
            records.append(record)
            receipt_name = (
                "test-only-unbound-receipt.json"
                if kwargs["contract"]["contract_id"].endswith("-UNBOUND")
                else "test-only-approval-receipt.json"
            )
            record["submitted_file_bytes_match"] = (
                kwargs["approval_receipt_bytes"]
                == (kwargs["repository_root"].parent / receipt_name).read_bytes()
            )
            provider = kwargs["provider"]
            execution = kwargs["candidate_sandbox"]
            with patch.object(provider, "invoke", wraps=provider.invoke) as invoke, patch.object(
                execution, "run", wraps=execution.run
            ) as execute:
                try:
                    result = current_runner(**kwargs)
                except AcceptanceCompileError as error:
                    record["diagnostics"] = {item.code for item in error.diagnostics}
                    raise
                finally:
                    record["provider_calls"] = invoke.call_count
                    record["execution_calls"] = execute.call_count
            record["state"] = result.state.value
            ledger = EvidenceLedger.open_existing(kwargs["repository_root"], kwargs["run_id"])
            record["events"] = list(ledger.verify())
            return result

        output = io.StringIO()
        validator = load_validator()
        with patch.object(validator, "verify_current_evidence", wraps=validator.verify_current_evidence) as verify, patch.object(barebones, "run_to_release_ready", side_effect=observe_run), patch.object(
            sys, "argv", [str(SCRIPT)]
        ), contextlib.redirect_stdout(output):
            self.assertEqual(validator.main(), 0)

        self.assertEqual(verify.call_count, 2)
        for call, record in zip(verify.call_args_list, records):
            self.assertEqual(call.kwargs.get("expected_head_digest"), record["events"][-1]["event_digest"])

        self.assertEqual(len(records), 3, "legacy assessment is not a current-run proof")
        good, broken, unbound = records
        self.assertTrue(all(record["submitted_file_bytes_match"] for record in records))
        self.assertEqual(good["state"], "RELEASE_READY")
        self.assertEqual(broken["state"], "HALTED")
        self.assertEqual(unbound["diagnostics"], {"RELEASE_GATE_UNBOUND"})
        self.assertEqual(unbound["provider_calls"], 0)
        self.assertEqual(unbound["execution_calls"], 0)

        for record, expected_gate in ((good, "PASS"), (broken, "FAIL")):
            with self.subTest(expected_gate=expected_gate):
                kwargs, events = record["kwargs"], record["events"]
                self.assertTrue(kwargs["contract"]["contract_id"].startswith("TEST-ONLY-"))
                self.assertTrue(kwargs["approval_authority"].startswith("test-only-"))
                self.assertEqual(json.loads(kwargs["approval_receipt_bytes"]), kwargs["approval_receipt"])
                self.assertEqual(events[0]["payload"]["approval"]["status"], "VERIFIED")
                baseline = next(event for event in events if event["event_type"] == "meaningful_red_confirmed")
                self.assertEqual({item["subject_id"] for item in baseline["payload"]["findings"]}, {"AC-001"})
                gate_event = next(event for event in events if event["event_type"] == "release_gates_evaluated")
                payload = gate_event["payload"]
                self.assertEqual(payload["contract_digest"], canonical_digest(kwargs["contract"]))
                self.assertEqual(payload["gates"][0]["status"], expected_gate)
                self.assertEqual(payload["gates"][0]["acceptance_criterion_refs"], ["AC-001"])
                self.assertEqual(payload["gates"][0]["criterion_results"][0]["status"], expected_gate)
                self.assertTrue(payload["plan_digest"].startswith("sha256:"))
                self.assertTrue(payload["candidate_digest"].startswith("sha256:"))
        self.assertFalse(any(event["event_type"] == "release_ready" for event in broken["events"]))
        self.assertIn("TEST-ONLY", output.getvalue())


if __name__ == "__main__":
    unittest.main()
