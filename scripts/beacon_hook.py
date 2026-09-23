#!/usr/bin/env python3
"""Forward lifecycle metadata only. Never emit a Claude decision or prompt text."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import signal
import sys


EVENTS = {"SessionStart", "UserPromptSubmit", "Stop", "SessionEnd"}
MAX_INPUT = 1024 * 1024


def _timed_out(_signum: int, _frame: object) -> None:
    raise TimeoutError("Beacon hook time budget exhausted")


def main() -> int:
    try:
        signal.signal(signal.SIGALRM, _timed_out)
        signal.alarm(2)
        payload = sys.stdin.buffer.read(MAX_INPUT + 1)
        if len(payload) > MAX_INPUT:
            return 0
        data = json.loads(payload)
        event = data.get("hook_event_name")
        session_id = data.get("session_id")
        if event not in EVENTS or not isinstance(session_id, str) or not session_id:
            return 0
        from workflow_beacon import Run

        root = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[1]))
        identifier = hashlib.sha256(session_id.encode()).hexdigest()[:24]
        # No context manager: a response-stop event is not a completed PM workflow.
        Run("pmos", project_root=root, run_id="claude-" + identifier).event(
            event, stage="claude", status="received"
        )
    except Exception:
        pass
    finally:
        signal.alarm(0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
