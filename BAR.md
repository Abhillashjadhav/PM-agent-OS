# BAR: PMOS Beacon launcher command-status compatibility

1. **Already exists? Yes.** Extend the existing `scripts/run_with_beacon.py`; no second recorder or launcher is introduced.
2. **Approved criterion or reproduced blocker? Yes.** The existing integration promises an unchanged wrapped command. A non-executable command returns 126 without the adapter but 1 with pinned adapter `b32bdfee2c5b579b06b45ffc5bf14bee5fa3f614` because `PermissionError` escapes.
3. **Changes existing behavior? Yes.** Adapter-present command startup errors will match the existing adapter-absent exit codes; this independent `fix/pmos-beacon-closeout-20260925` branch owns that compatibility repair.
4. **Failing automated check before repair? Yes.** `test_adapter_preserves_nonexecutable_status` invokes the public launcher with a local adapter fixture and a non-executable file; expected 126, current result 1. Commit this check before the repair.
5. **Independently revertible? Yes.** The launcher mapping, regression fixture, and evidence are one concern; installer, skills, verification gates, and external repositories are untouched.
6. **Unrequested setting/dependency/extension? No.** Reuse Python standard library and the existing optional adapter interface; introduce no configuration or dependency.

# BAR: inherited Beacon installer whitespace

1. **Already exists? Yes.** Correct only the existing installer's extra blank line at EOF.
2. **Reproduced blocker? Yes.** `git diff --check origin/main...HEAD` at `a21279a` exits 2: `scripts/install_beacon_adapter.py:34: new blank line at EOF.`
3. **Changes existing behavior? No.** The edit changes trailing whitespace only.
4. **Failing check first? Yes.** The existing diff check reproduces this exact RED; the deterministic PR quality gate runs the same check.
5. **Independently revertible? Yes.** The one-line formatting correction has no runtime dependency.
6. **Unrequested setting/dependency/extension? No.** No settings, dependencies, or interfaces are added.

# BAR: run existing Beacon regression tests in CI

1. **Already exists? Yes.** Reuse the existing repository-audit job and seven offline `test_beacon_*.py` tests.
2. **Approved criterion or reproduced blocker? Yes.** The reproduced 126-versus-1 launcher regression already has a RED fixture, but the audit job never executes it.
3. **Changes existing behavior? Yes.** The existing audit job will now fail when a Beacon hook or runner regression fails; no runtime behavior or other CI step changes.
4. **Failing check first? Yes.** Before editing, parsing the audit workflow and asserting this exact filtered unittest command fails because the invocation is absent.
5. **Independently revertible? Yes.** The single added workflow step and this evidence entry are independently revertible.
6. **Unrequested setting/dependency/extension? No.** Python standard-library unittest is already available; no new job, dependency, action, pin, or integration surface.

Validation: YAML parses and differs only by the intended step. The exact added command,
`python -B -m unittest discover -s tests -p 'test_beacon_*.py' -v`, passes all seven tests.
