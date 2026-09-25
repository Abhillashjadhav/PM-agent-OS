# PMOS Beacon closeout

The existing PMOS integration is implemented and passes ordinary offline command
and lifecycle checks. A reproduced launcher error is repaired. Actual Mac
collector delivery and native Claude lifecycle capture remain **UNVERIFIED**.

## Narrow repair

The public runner returned 126 when an unexecutable command was launched without
the optional adapter, but returned 1 with a traceback when the adapter was
installed. The adapter's `PermissionError` escaped through the wrapper. The
wrapper now maps that error to 126. It does not rerun the command after an adapter
exception, which avoids duplicate command execution.

- Original runtime: `f1852d5c32c9d7dd3b1503e5f17d69c2e59a8498` (PR #62).
- RED fixture commit: `db996d2` (one reproduced failure, four passes).
- Repair commit: `e2ad82052dacd543306833b2b922b2e1e0b8dcc2`.
- Shared adapter remains pinned to `b32bdfee2c5b579b06b45ffc5bf14bee5fa3f614`.
- No changes to the adapter, installers, skill prompts, approval rules, or PM gates.

## Checks completed

`python3 -B -m unittest discover -s tests -p 'test_beacon_*.py' -v`
passes all **7** tests. These cover metadata-only hooks, session correlation,
invalid input, unavailable adapters, command stdout/stderr/stdin and working
directory, nonzero status preservation, exact PMOS adapter arguments, and command
startup errors. The regression is in `test_beacon_runner.py`.

The separate `verify_offline_adapter.py` check uses an exact local export of the
pinned shared adapter. It replaces only the worker-launch function with a local
unavailable-worker fixture before PMOS executes, so no collector or transport
process receives any event. Its **12** cases pass:

| Journey | Observed result |
|---|---|
| Successful wrapped command; collector worker unavailable | Exit 0; original output; three queued lifecycle events |
| Failing wrapped command; collector worker unavailable | Exit 23 preserved; failure recorded |
| Recording disabled | Exit 23 preserved; no queued events |
| Recording state unavailable | Exit 23 preserved; no queued events |
| Non-executable / missing command | Exit 126 / 127 |
| Four supported lifecycle hooks | One metadata-only event each; same hashed session ID; no prompt, transcript, tool input, or raw session ID |
| Invalid / oversized hook input | Exit 0; no output or event |

`offline-results.json` records the command source commit and source hashes, exact
adapter file hashes, results, and the mocked transport boundary. This is evidence
of local integration behavior, not collector delivery or deployment.

The public `beacon_hook.sh` launcher also exits 0 with empty stdout and stderr
when recording is disabled. The existing installer, invoked with system Python,
returns the documented virtualenv guard (exit 2); no installation was attempted.
`git diff --check` passes.

## Integration requirements and limits

Keep the existing runtime (PR #62), documentation (PR #61), and this repair
together when reviewing the Beacon concern. Its shared adapter lock is unchanged.
Global installation through `scripts/install.py` does not add these project
hooks to another checkout. That limitation is already explicit in `docs/BEACON.md`.

The owner-side local collector installation and a real native Claude session
have not been accessed from this cloud workspace. Their event retention,
native-harness privacy settings, and teardown behavior require external evidence
before describing the integration as deployed. Offline mocks do not close that
leg. Lifecycle markers remain observational and do not prove a PM skill passed
its verification gate.

There were zero model calls, zero collector sends, no other-repository changes,
no merges, and no direct remote writes in this workstream.
