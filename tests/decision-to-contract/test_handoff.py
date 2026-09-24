"""Offline integration regressions for the PMOS handoff entry point."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from pmpe import barebones
from pmpe.contracts.acceptance import AcceptanceCompileError
from pmpe.contracts.canonical import canonical_digest
from pmpe.evidence.ledger import EvidenceLedger


SCRIPT = Path(__file__).with_name("validate_contract.py")


def load_validator():
    spec = importlib.util.spec_from_file_location("pmos_handoff_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CurrentHandoffTests(unittest.TestCase):
    def test_default_entrypoint_exercises_current_runner_and_negative_controls(self):
        records = []
        current_runner = barebones.run_to_release_ready

        def observe_run(**kwargs):
            record = {"kwargs": kwargs}
            records.append(record)
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
        with patch.object(barebones, "run_to_release_ready", side_effect=observe_run), patch.object(
            sys, "argv", [str(SCRIPT)]
        ), contextlib.redirect_stdout(output):
            self.assertEqual(load_validator().main(), 0)

        self.assertEqual(len(records), 3, "legacy assessment is not a current-run proof")
        good, broken, unbound = records
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
