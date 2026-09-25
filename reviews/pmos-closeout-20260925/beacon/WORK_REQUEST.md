# Work request and boundaries

The owner requested collection of existing PMOS work, implementation of remaining
approved work, and GitHub publication. Their latest clarification excludes PEOS,
which is being handled separately. Independent workstreams may run in parallel.

This workstream owns only the existing PMOS Beacon hooks and standalone launcher
from runtime commit `f1852d5c32c9d7dd3b1503e5f17d69c2e59a8498` (PR #62), with
documentation from `ef25c50` (PR #61). Reuse the existing shared adapter; do not
introduce another telemetry implementation, change skills, or alter PM gates.

Validate ordinary local fixtures, command metadata and exit preservation, privacy
filtering, disabled recording, and unavailable local recording. Never send events
to a real collector, run a model, access the owner's Mac, or change another
repository. Prior screened bytecode/rechained release-evidence probes are outside
this workstream and will not run. Live Mac/Claude capture remains unverified.

The pinned shared adapter is inspected and exported read-only to scratch for
offline checks. Recording is disabled or its worker-launch function is mocked;
no transport process or external collector receives these fixtures. The root
coordinator owns integration and remote publication; this workstream does not
push or merge.
