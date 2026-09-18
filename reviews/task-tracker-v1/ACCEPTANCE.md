# Local task tracker — amended acceptance grid v1

**DRAFT — awaiting the owner's requested one-line confirmation before freeze.**
The owner approved the grid with two amendments: explicitly sequential AC-013
and critical AC-014 for ID continuity after a rejected create. Both are included
below. The identifier, duplicate-creation and repeated-completion rules are
approved exactly as previously proposed. The publisher-created contract is `contract.draft.json`;
`scenarios.json` contains every command and expected JSON observation.

The intended outcome is that a person can create, complete and find their tasks
after reopening the CLI, without losing acknowledged changes or repairing data.

## Product decisions

| Decision | Rule | Trade-off |
| --- | --- | --- |
| Identifiers | Positive integer IDs, starting at 1 in a new store, increasing by one per successful creation and preserved across restarts. A rejected create must not advance the next-ID counter. | Simple to read and type; one local store and one writer. |
| Duplicate creation | The same title may be created twice; each successful create receives a new ID. | Legitimate repeated tasks work. Retrying create after an uncertain acknowledgement can create a duplicate; automatic create-retry deduplication is out of scope. |
| Repeated completion | Completing an already completed task returns success with the same ID and status, and preserves the task list. | Callers can retry completion safely; no toggle or duplicate record. |
| Titles and listing | Reject blank titles; otherwise preserve text exactly. `list` defaults to all; filters are `open`, `completed`, `all`; results are ordered by ID. | Predictable behavior without search or title normalization. |
| Persistence | A successful command must save before acknowledging. Data and the next ID survive orderly CLI process exit and restart. | Concurrent creation is out of scope; no parallel-writer tests, power-loss or crash-during-write guarantee in this experiment. |
| Errors | Invalid requests and unknown IDs return a documented error and no business-state change. Storage failure never returns success; malformed storage is preserved. | Fail visibly instead of silently discarding data. |

Each command runs as a new process and uses an explicit shared `--store PATH`.
The CLI surface for this feature is:

```text
python product.py --store PATH create TITLE
python product.py --store PATH complete ID
python product.py --store PATH list [--status all|open|completed]
```

Success exits 0 and emits JSON: `{ "task": { "id", "title", "status" } }` for
create/complete, `{ "tasks": [...] }` for list. Invalid input or an unknown ID
exits 2; storage failure exits 1. Errors emit `{ "error": "CODE" }`. The exact
codes and machine-checkable results are in the scenarios and contract.

## Acceptance grid

Every row must pass. **Critical** means data loss, false acknowledgement, a
durability failure or advancing the ID counter on rejection; **major** means incorrect user-visible functionality. Severity
does not authorize skipping a row. CLI observations come from the proposed
`evaluator.py`, which invokes actual candidate processes and returns their outputs;
the expected outcomes are encoded in the contract, not supplied by the candidate.

| ID | Concrete scenario | Expected result | Observation | Severity |
| --- | --- | --- | --- | --- |
| AC-001 | List a fresh, empty store. | Success; empty task list. | Actual CLI exit and JSON. | Major |
| AC-002 | Create a title containing Unicode and surrounding spaces; list in a new process. | Exact title preserved; ID 1; status open; identical stored task. | Creation acknowledgement and independent list process. | Major |
| AC-003 | Create Buy milk and Read book; complete ID 1. | Only task 1 becomes completed; task 2 remains open. | Completion result and complete task list. | Major |
| AC-004 | With task 1 completed and task 2 open, request all three status filters. | Open returns only 2; completed only 1; all returns 1 and 2, ordered. | Three fresh list processes; exact partitions. | Major |
| AC-005 | Create two tasks, complete ID 1, reopen/list, then create Water plants. | Both earlier tasks and their statuses persist; the next ID is 3. | Six separate CLI processes sharing one store. | Critical |
| AC-006 | Create Buy milk twice; reopen/list. | Two separate tasks with IDs 1 and 2. | Acknowledgements and list contents. | Major |
| AC-007 | Complete task 1, then repeat completion twice. | Each retry succeeds with task 1 completed; task 2 and task count remain unchanged. | Repeated acknowledgements and final list. | Major |
| AC-008 | Create with empty and whitespace-only titles. | Both reject with INVALID_TITLE; no task exists afterward. | Exit 2, error code and final empty list. | Major |
| AC-009 | Complete IDs 0, -1, abc and unknown ID 999 with one existing task. | INVALID_ID for the first three; NOT_FOUND for 999; existing task unchanged. | Error results and final list. | Major |
| AC-010 | Request status done, then list valid data. | INVALID_STATUS; existing task unchanged. | Error result and final list. | Major |
| AC-011 | Open malformed existing storage. | STORE_INVALID; original bytes preserved. | CLI result and observer-computed before/after file digest. | Critical |
| AC-012 | Create where the store's parent path is a regular file. | STORE_IO; no success acknowledgement. | Actual failed filesystem persistence via CLI, including under UID 0. | Critical |
| AC-013 | Run ten creates strictly sequentially, each process exiting before the next starts, using fresh measurement titles; then list in a new process. | Ten distinct valid acknowledgements; zero acknowledged records missing. | Actual registered `measure` path; independent count from acknowledgements versus reopened list. No parallel writers. | Critical |
| AC-014 | In a fresh store, reject an empty title, then create Buy milk and list in a new process. | INVALID_TITLE with exit 2; the valid create receives ID 1; the store contains exactly that one open task. Rejection does not advance the next-ID counter. | Three strictly sequential CLI processes; exact error, acknowledgement and final list. | Critical |

AC-013 units are **records missing**. Workload: ten strictly sequential creates,
each process exiting before the next starts, one fresh temporary store, fresh
per-run titles, then a new list process. Concurrent creation is out of scope;
parallel writers are not tested. Threshold: `value == 0` with
`sample.minimum == 10`; sample size is distinct valid acknowledgements, so creating
nothing cannot pass. This deterministic count is not a statistical model-quality
evaluation or a production-latency benchmark.

## Meaningful failure and tamper evidence

After approval, the original baseline must fail by assertion. A candidate with
broken persistence must fail the restart/lost-record checks; a candidate with
broken filtering must fail the partition check. Unrelated crashes do not satisfy
these negative tests. Any known-bad candidate that passes stops the run.

At approval time, record the evaluator and every approval-bound artifact digest.
Check all of them immediately before and immediately after each authoritative
check, including failed checks, exceptions and timeouts. Any mismatch fails the
run. Pin the exact artifacts and relevant execution profile; never replace an
expected digest to obtain a pass. The bundle's manifest records the review inputs;
the approved contract, receipt and compiled-plan digests are derived and recorded
only after an actual owner approval.

Root can still change the checker or evidence, or restore a transient change
between observations. These checks supply bounded tamper evidence, not prevention.
Existing receipts are forgeable; their proper signing-authority fix is deferred by
the owner. Neither root access nor that known forgery is a blocker for this run.

## Execution and limits accepted by the owner

**Named limitation — Creation is not idempotent.** Duplicate-on-retry is approved behavior,
not a defect. This report makes no retry-safety claim for create. Completion
idempotency is covered by AC-007. Concurrent creation is out of scope, consistent
with the single-writer persistence decision.

The network-only sandbox amendment still failed: `setting up uid map: Operation
not permitted`. The exact flags were `--unshare-all --share-net`; every other
production argument was retained. A separate explicit user/PID/IPC/UTS/cgroup
namespace probe failed identically. Read-only mounts, tmpfs and resource-limit
arguments were unchanged. Exact argv and
results are linked from `execution-profile.json` and PEOS's audit evidence.

**Sandbox decision: closed by the owner; no further Bubblewrap attempts.** The
real-sandbox leg is environment-blocked. The authorized fallback uses the existing
container. It lacks additional candidate user, PID, mount, IPC, UTS, cgroup and
network namespaces; read-only candidate/runtime mounts; and private tmpfs/proc. The resource
probe observed the configured limits; it did not stress-test enforcement. All
behavioral and digest checks remain required. No second sandbox is proposed.

The model provider requires an active agent session. New business actions already
work through the Template API without engine-source edits; only the declarative
file/CLI path remains. Historical live-provider evidence exists in PEOS and was
not independently verified by this run.

## Metrics and approval boundary

Proposed outcome metric: share of approved task-management journeys completed with
correct durable state and no manual repair. Leading measures: first-pass contract
compatibility, first-attempt criterion results and build attempts. Guardrails:
requirements preserved, known-bad false passes, manual effort, recorded runtime
and available usage. No numerical cost, token or latency claim is invented.

For this experiment, report all 14 criterion outcomes individually; a ratio cannot
override a failed gate. One feature does not estimate broad platform reliability.

The existing publisher produced a DRAFT with blank approval fields. Validation
proved schema and criterion traceability, and compilation with the proposed
bindings. It did not validate the observer against a product or demonstrate
delivery. CLI loading, digest enforcement and live behavioral validation remain
implementation work after owner approval; meaning-changing revisions require
renewed approval. If that work changes a source file bound by this manifest, its
new bytes also require approval before product generation; this proposal cannot
approve future source bytes. No receipt or product code has been generated.

The owner requested one final confirmation of this amended grid before freezing
the contract, acceptance grid, evaluator and digest manifest, then proceeding to
Phases 3 and 4. The three approved rules are not being reopened. Confirmation:
**“Confirmed — freeze the amended grid and proceed.”**
