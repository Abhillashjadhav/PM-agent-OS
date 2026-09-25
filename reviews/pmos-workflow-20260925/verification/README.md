# Composed PMOS verification

Source checked: `be83ce1e2fdba15bc43d2c308f3d514c71dee74f`, assembled from the
reviewed main-based units. This is a bounded PMOS verification snapshot.

## Executed checks

| Check | Result | Scope |
| --- | --- | --- |
| Installer | 7 tests pass | Temporary-home installer behavior |
| Validator | 9 tests pass | Ordinary repository validation regressions |
| Beacon | 7 tests pass | Offline hook and runner mocks |
| Handoff setup | 6 tests pass | Read-only installation metadata diagnostics |
| Current authoring | 5 tests pass | Existing pinned publisher, TEST-ONLY issuance, receipt verification and compilation |
| Repository quality | PASS | Audit, skill lint, whitespace and inert Python compilation |
| Frozen reference | 33 exact files | Bytes, modes and recorded Git identities preserved |

The 34 focused tests and static checks exited zero. Exact commands, source commit
and exit codes are in [results.json](results.json); matching logs are retained in
this directory. No broad handoff discovery, archived reproduction execution,
collector calls, engineering builds or PEOS source access occurred.

## Fresh-agent observations

Five designed scenarios used new agents with no inherited conversation; the raw
idea continued for one additional answer. These were ChatGPT Work in-session
agents, not native Claude sessions. Exact model build, sampling and token metadata
were unavailable. There is no reliability estimate or baseline comparison.

| Scenario | Observation |
| --- | --- |
| Raw pantry idea, two turns | Asked one relevant question; reused its answer, preserved stable IDs and stayed Draft. |
| Contradictory existing Draft; owner unavailable | Preserved the conflict and OPEN fields, saved the next question, and withheld approval. |
| Approved fictional definition | Publisher created a DRAFT; agent asked for its exact digest approval and issued no receipt. |
| One out-of-bound regression case | Returned INVESTIGATE with a complete per-case table under the supplied pre-run rules. |
| Same output, distinct inputs and disputed labels | Preserved distinct identity; quarantined conflicting and incomplete reviews without inventing labels. |

[forward-runs.json](forward-runs.json) retains tasks, normalized responses or
explicitly marked excerpts, observations, source versions and limits.
[forward-artifacts/manifest.json](forward-artifacts/manifest.json) indexes retained
Drafts, decisions and publisher outputs with hashes. All inputs are designed
rehearsals; their fictional labels and approvals are not real product evidence.

## Independent integration review

A separate `pmos_handoff_setup` agent reviewed the assembled intake → field map →
contract → setup interfaces and catalogue consumers at the source above. All 12
changed-skill lints and whitespace passed. LINT, SPEC, NOVELTY, HARD RULES,
TESTABILITY and BLOAT passed; **APPROVE**, no blocking findings.

The review confirmed separate product/digest approval, OPEN product truth versus
BLOCKED engineering support, canonical decision paths with legacy provenance,
independent blockers, and reviewed-input-only golden curation. Current-authoring
CI runs only its explicit ordinary file at the existing 297a11d pin; historical
compatibility retains 5c0f9e3. No restricted handoff probes were introduced.

## What this does not establish

No complete fresh idea-to-working-product delivery, native Claude/Mac behavior,
full handoff security validation, compatibility with a merged engineering main,
or general model reliability is claimed. Other catalogue behaviors have source
and fixture review, not observed model runs. Real product decisions and exact
generated-digest approvals still belong to the accountable owner.
