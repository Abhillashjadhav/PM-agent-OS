# BAR: PMOS Beacon launcher command-status compatibility

1. **Already exists? Yes.** Extend the existing `scripts/run_with_beacon.py`; no second recorder or launcher is introduced.
2. **Approved criterion or reproduced blocker? Yes.** The existing integration promises an unchanged wrapped command. A non-executable command returns 126 without the adapter but 1 with pinned adapter `b32bdfee2c5b579b06b45ffc5bf14bee5fa3f614` because `PermissionError` escapes.
3. **Changes existing behavior? Yes.** Adapter-present command startup errors will match the existing adapter-absent exit codes; this independent `fix/pmos-beacon-closeout-20260925` branch owns that compatibility repair.
4. **Failing automated check before repair? Yes.** `test_adapter_preserves_nonexecutable_status` invokes the public launcher with a local adapter fixture and a non-executable file; expected 126, current result 1. Commit this check before the repair.
5. **Independently revertible? Yes.** The launcher mapping, regression fixture, and evidence are one concern; installer, skills, verification gates, and external repositories are untouched.
6. **Unrequested setting/dependency/extension? No.** Reuse Python standard library and the existing optional adapter interface; introduce no configuration or dependency.
