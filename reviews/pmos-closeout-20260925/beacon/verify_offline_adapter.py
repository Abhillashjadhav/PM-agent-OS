#!/usr/bin/env python3
"""Verify PMOS with an already exported pinned adapter and no transport worker.

Usage: python3 -B verify_offline_adapter.py ADAPTER_SRC OUTPUT_JSON
The source path must be the reviewed lock's packages/workflow_beacon/src export.
This script never installs a package, accesses the network, or executes a model.
"""

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[3]
ADAPTER = Path(sys.argv[1]).resolve()
OUTPUT = Path(sys.argv[2]).resolve()
CHILD = """
import runpy, sys
import workflow_beacon.core as core
def unavailable_worker():
    raise OSError('offline fixture: collector worker unavailable')
core.nudge_worker = unavailable_worker
target = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(target, run_name='__main__')
"""


def rows(directory):
    database = directory / "outbox.sqlite3"
    if not database.is_file():
        return []
    with sqlite3.connect(database) as connection:
        return [json.loads(row[0]) for row in connection.execute("SELECT payload FROM events ORDER BY created")]


results = []
with tempfile.TemporaryDirectory(prefix="pmos-beacon-offline-") as temporary:
    scratch = Path(temporary)
    base = {key: value for key, value in os.environ.items() if not key.startswith("WORKFLOW_BEACON_")}
    base.update(PYTHONPATH=str(ADAPTER), PYTHONDONTWRITEBYTECODE="1", CLAUDE_PROJECT_DIR=str(ROOT))

    def invoke(case, command, expected, *, payload="", disabled=False, blocked=False):
        state = scratch / case
        if blocked:
            state.write_text("fixture: state directory unavailable\n")
        environment = dict(base, WORKFLOW_BEACON_STATE_DIR=str(state), WORKFLOW_BEACON_DISABLED="1" if disabled else "0")
        outcome = subprocess.run(
            [sys.executable, "-B", "-c", CHILD, *command],
            capture_output=True, text=True, input=payload, env=environment,
            cwd=ROOT, timeout=10,
        )
        if outcome.returncode != expected:
            raise AssertionError(f"{case}: expected {expected}, got {outcome.returncode}: {outcome.stderr}")
        events = rows(state)
        for event in events:
            if event["workflow"] != "pmos" or event["project_root"] != str(ROOT):
                raise AssertionError(f"{case}: incorrect PMOS attribution")
            if "PRIVATE_SENTINEL" in json.dumps(event):
                raise AssertionError(f"{case}: private payload leaked")
        results.append({
            "case": case, "exit_code": outcome.returncode,
            "stdout": outcome.stdout, "stderr": outcome.stderr,
            "queued_event_count": len(events),
            "actions": [event["action"] for event in events],
            "metadata": [event["metadata"] for event in events],
            "pass": True,
        })
        return outcome, events

    def command(code):
        return [str(ROOT / "scripts/run_with_beacon.py"), "--", sys.executable, "-c",
                f"import sys; print('ordinary command completed'); sys.exit({code})", "PRIVATE_SENTINEL"]

    for case, code, disabled, blocked in (
        ("runner_success_worker_unavailable", 0, False, False),
        ("runner_failure_worker_unavailable", 23, False, False),
        ("runner_recording_disabled", 23, True, False),
        ("runner_state_unavailable", 23, False, True),
    ):
        outcome, events = invoke(case, command(code), code, disabled=disabled, blocked=blocked)
        if outcome.stdout != "ordinary command completed\n" or outcome.stderr:
            raise AssertionError(f"{case}: command output changed")
        expected_actions = [] if disabled or blocked else [
            "session.started", "command.executed", "session.ended" if code == 0 else "session.error"
        ]
        if [event["action"] for event in events] != expected_actions:
            raise AssertionError(f"{case}: wrong lifecycle events")

    nonexecutable = scratch / "not-executable"
    nonexecutable.write_text("ordinary non-executable fixture\n")
    nonexecutable.chmod(0o600)
    invoke("runner_nonexecutable", [str(ROOT / "scripts/run_with_beacon.py"), "--", str(nonexecutable)], 126)
    invoke("runner_missing_command", [str(ROOT / "scripts/run_with_beacon.py"), "--", str(scratch / "missing")], 127)

    expected_id = "claude-" + hashlib.sha256(b"PRIVATE_SENTINEL_session").hexdigest()[:24]
    for event in ("SessionStart", "UserPromptSubmit", "Stop", "SessionEnd"):
        outcome, events = invoke(
            "hook_" + event, [str(ROOT / "scripts/beacon_hook.py")], 0,
            payload=json.dumps({
                "hook_event_name": event, "session_id": "PRIVATE_SENTINEL_session",
                "prompt": "PRIVATE_SENTINEL_prompt", "transcript_path": "/PRIVATE_SENTINEL/transcript",
                "tool_input": "PRIVATE_SENTINEL_tool",
            }),
        )
        if outcome.stdout or outcome.stderr:
            raise AssertionError("hook emitted user-facing output")
        if len(events) != 1 or events[0]["action"] != event or events[0]["run_id"] != expected_id:
            raise AssertionError("hook correlation or metadata mismatch")
        if events[0]["metadata"] != {} or events[0]["status"] != "received":
            raise AssertionError("hook invented quality status or extra metadata")

    for case, payload in (("hook_invalid", "[]"), ("hook_oversized", "x" * (1024 * 1024 + 1))):
        outcome, events = invoke(case, [str(ROOT / "scripts/beacon_hook.py")], 0, payload=payload)
        if outcome.stdout or outcome.stderr or events:
            raise AssertionError(f"{case}: rejected payload produced output or events")

report = {
    "schema_version": 1,
    "adapter_commit": json.loads((ROOT / "beacon-source.lock.json").read_text())["commit"],
    "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "source_file_sha256": {
        path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        for path in ("scripts/run_with_beacon.py", "scripts/beacon_hook.py")
    },
    "adapter_file_sha256": {
        path: hashlib.sha256((ADAPTER / "workflow_beacon" / path).read_bytes()).hexdigest()
        for path in ("core.py", "cli.py")
    },
    "transport": "nudge_worker replaced with a local OSError fixture before PMOS code runs",
    "collector_events_sent": 0,
    "model_calls": 0,
    "mac_native_capture": "UNVERIFIED",
    "cases": results,
    "all_pass": True,
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"all_pass": True, "cases": len(results), "output": str(OUTPUT)}))
