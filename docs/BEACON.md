# Beacon integration

This repository is a Claude skill system. It has no executable PM workflow
coordinator to wrap: `/pm` and the 40 lifecycle skills run inside Claude Code.

## Install once in this checkout

After installing the local Beacon collector, prepare an optional adapter environment:

```bash
python3 -m venv .venv
.venv/bin/python scripts/install_beacon_adapter.py
```

The installer reads `beacon-source.lock.json`, validates the immutable commit,
and installs the shared package from the LinkedIn OS repository. It does not
copy a second adapter implementation into PMOS. Network access is needed for
installation, not for calling the local collector. Do not change the commit
without reviewing and testing that adapter version.

Then start Claude Code in this checkout as usual. Project hooks register
automatically when Claude permits the repository's hooks. Existing hooks and
permission decisions remain in place. No report opens and no dashboard login is
needed. Collector/service availability never determines whether PM gates pass.
The hooks run asynchronously and enforce their own two-second time budget.

## Automatic coverage

| Entry point | Capture |
|---|---|
| Claude session start/resume in this checkout | Session lifecycle metadata |
| Each submitted prompt, including `/pm` | Prompt-submitted marker; prompt text is discarded |
| Claude response stop | Response-stop marker, **not** proof that a PM gate passed |
| Claude session end | Session-end marker |
| Tool internals and subskill quality | Existing native Beacon harness capture where configured; not inferred by these hooks |
| Skills installed globally by `scripts/install.py` and invoked in another project | **Not covered by this repository's hooks**; that project needs its own integration |
| Other standalone scripts or CI commands | Wrap the intended command with the shared runner below; not implicitly instrumented |

```bash
python3 scripts/run_with_beacon.py -- COMMAND ARGUMENTS
```

The shared runner is explicit for otherwise unregistered entry points; it is not
required for the normal project Claude workflow.
The launcher calls the installed shared adapter when available and executes the
command directly when it is absent. Use `.venv/bin/python` if that is where the
adapter was installed.

The hook reads bounded JSON from stdin to select only the event and session
identifier. It does not persist prompt text, assistant text, transcript paths,
tool inputs, or arbitrary environment values. Invalid or oversized input is
discarded. Hook failures return zero with no decision output. Missing adapter
means normal work continues without that adapter's recording.

## Limits and rollback

This layer adds capture only. It does not change PMOS verification gates,
approval receipts, skill prompts, or automatically convert observations into
approved corrections. Session markers do not prove individual skill correctness.
Native collector capture may have different payload settings; verify those
separately during Mac installation.

The Mac collector and native Claude execution have not been verified from the
cloud development environment. Test a unique marker in a real local session
before describing this as deployed.
Claude may cancel an asynchronous hook at session teardown, so final markers
remain best effort and are not proof that every event was retained.

To roll back, remove only the Beacon entries from `.claude/settings.json` or
revert this integration commit. Preserve unrelated hooks and saved evidence.
No uninstallation or history deletion is required.

Hook schema reference: https://code.claude.com/docs/en/hooks
