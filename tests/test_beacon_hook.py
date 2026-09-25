"""Offline lifecycle capture checks; does not execute Claude or a model."""
import importlib.util
import io
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "beacon_hook", Path(__file__).resolve().parents[1] / "scripts/beacon_hook.py"
)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


class HookTests(unittest.TestCase):
    def test_metadata_only_and_session_correlation(self):
        calls = []

        class Recorder:
            def __init__(self, workflow, **kwargs):
                self.fields = {"workflow": workflow, **kwargs}

            def event(self, action, **kwargs):
                calls.append({**self.fields, "action": action, **kwargs})

        fake = types.SimpleNamespace(Run=Recorder)
        for event in ("SessionStart", "UserPromptSubmit", "Stop", "SessionEnd"):
            payload = {"hook_event_name": event, "session_id": "session-1",
                       "prompt": "PRIVATE_SENTINEL", "transcript_path": "/private/transcript"}
            stream = io.TextIOWrapper(io.BytesIO(json.dumps(payload).encode()))
            with patch.object(sys, "stdin", stream), patch.dict(sys.modules, workflow_beacon=fake):
                self.assertEqual(hook.main(), 0)
        self.assertEqual(len(calls), 4)
        self.assertEqual(len({call["run_id"] for call in calls}), 1)
        self.assertNotIn("PRIVATE_SENTINEL", repr(calls))
        self.assertNotIn("/private/transcript", repr(calls))

    def test_missing_adapter_and_invalid_input_do_not_block(self):
        for payload in (b"not json", b"[]", b'{"hook_event_name":"Stop","session_id":"x"}'):
            stream = io.TextIOWrapper(io.BytesIO(payload))
            with patch.object(sys, "stdin", stream), patch.dict(sys.modules, workflow_beacon=None):
                self.assertEqual(hook.main(), 0)


if __name__ == "__main__":
    unittest.main()
