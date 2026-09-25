"""Public PMOS launcher fixtures; no collector, model, or network calls."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_with_beacon.py"


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="pmos-beacon-runner-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.package = self.root / "workflow_beacon"
        self.package.mkdir()
        self.record = self.root / "adapter-arguments.json"
        self.environment = dict(
            os.environ,
            PYTHONPATH=str(self.root),
            PYTHONDONTWRITEBYTECODE="1",
            WORKFLOW_BEACON_DISABLED="1",
        )

    def absent_adapter(self):
        (self.package / "__init__.py").write_text("raise ImportError('fixture: unavailable')\n")

    def local_adapter(self):
        (self.package / "__init__.py").write_text("")
        # Model only the documented adapter CLI boundary and direct command
        # launch. Recording and transport are deliberately absent from this spy.
        (self.package / "cli.py").write_text(
            "import json, subprocess\n"
            "from pathlib import Path\n"
            "def main(arguments):\n"
            f"    Path({str(self.record)!r}).write_text(json.dumps(arguments))\n"
            "    return subprocess.run(arguments[arguments.index('--') + 1:]).returncode\n"
        )

    def invoke(self, *arguments, input_text=""):
        return subprocess.run(
            [sys.executable, "-B", str(RUNNER), *arguments],
            input=input_text,
            capture_output=True,
            text=True,
            cwd=self.root,
            env=self.environment,
            timeout=5,
        )

    def test_missing_adapter_preserves_command_io_and_status(self):
        self.absent_adapter()
        program = (
            "import os, sys; "
            "print(sys.stdin.read().strip(), sys.argv[1], os.getcwd()); "
            "print('fixture stderr', file=sys.stderr); sys.exit(23)"
        )
        result = self.invoke("--", sys.executable, "-c", program, "two words", input_text="fixture stdin\n")
        self.assertEqual(result.returncode, 23)
        self.assertEqual(result.stdout, f"fixture stdin two words {self.root}\n")
        self.assertEqual(result.stderr, "fixture stderr\n")

    def test_adapter_receives_only_existing_workflow_arguments(self):
        self.local_adapter()
        command = [sys.executable, "-c", "import sys; print('ran'); sys.exit(17)"]
        result = self.invoke("--", *command)
        self.assertEqual(result.returncode, 17)
        self.assertEqual(result.stdout, "ran\n")
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            json.loads(self.record.read_text()),
            ["run", "--workflow", "pmos", "--project-root", str(ROOT), "--", *command],
        )

    def test_no_command_reports_usage(self):
        self.absent_adapter()
        result = self.invoke("--")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stderr)

    def test_missing_adapter_preserves_startup_error_codes(self):
        self.absent_adapter()
        nonexistent = self.root / "not-found"
        result = self.invoke("--", str(nonexistent))
        self.assertEqual(result.returncode, 127)
        nonexecutable = self.root / "not-executable"
        nonexecutable.write_text("not an executable\n")
        nonexecutable.chmod(0o600)
        result = self.invoke("--", str(nonexecutable))
        self.assertEqual(result.returncode, 126)

    def test_adapter_preserves_nonexecutable_status(self):
        self.local_adapter()
        nonexecutable = self.root / "not-executable"
        nonexecutable.write_text("not an executable\n")
        nonexecutable.chmod(0o600)
        result = self.invoke("--", str(nonexecutable))
        self.assertEqual(result.returncode, 126)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
