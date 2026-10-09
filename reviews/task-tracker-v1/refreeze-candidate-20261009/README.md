# Re-freeze candidate for PMOS-TASK-TRACKER-001 — UNAPPROVED

Status: **CANDIDATE, NOT APPROVED. The frozen packet in the parent directory is unchanged.**

## Why this exists

The approved freeze (`sha256:1dd281e55cc20ce1861e3bed55799617191f38c5cc4e2322c7e463ef9a6e37f2`)
binds 218 artifacts by raw SHA-256: 14 PMOS files and 204 Production Engineering OS
source files. Five of those bytes changed after the freeze through ordinary merged work:

| Repository | Path | Changed by |
| --- | --- | --- |
| PM-agent-OS | `.claude/skills/decision-to-contract/SKILL.md` | PMOS PRs #67–#74 (Sept 25–Oct 1) |
| production-engineering-os | `src/pmpe/barebones.py` | PEOS main after Sept 21 |
| production-engineering-os | `src/pmpe/cli/barebones_cmd.py` | PEOS main (#243 provider-failure reporting) |
| production-engineering-os | `src/pmpe/contracts/acceptance.py` | PEOS main (#244 malformed-criteria rejection) |
| production-engineering-os | `src/pmpe/evals/real_behavior_drift_eval.py` | PEOS main |

Because of this, `contract-file.py verify|build` against current `main` of either
repository fails closed with `APPROVAL_BOUND_ARTIFACT_CHANGED` before any criterion
runs (evidence: PEOS `docs/evidence/task-tracker-completion-20261009/runs/02-current-mains-verify/`).
That refusal is correct behaviour under the approved execution profile
("do not update the trusted expected digest to make a run pass").

## What the candidate is

`freeze-manifest.candidate.json` is the approved manifest with exactly those five
`sha256` values replaced by the bytes at the locked baseline (listed in
`changed-entries.json`), recomputed from git object bytes at PEOS `e8a929d` and PMOS
`0652843` (recorded under `refreeze_basis.baseline`), its `status` set to
`CANDIDATE_REFREEZE_UNAPPROVED`, and the approval quote blanked. An earlier candidate
(`sha256:20e67cca…`, 2026-10-09 morning) bound the identical artifact set; only its
metadata text differed. This file supersedes it; there is one candidate.
No contract, criterion, evaluator, binding, profile, receipt or plan value changed;
the compiled-plan digest recomputed on current code is identical to the frozen one
(`sha256:1dad520ebc6ac6973aeb23d80fe5c98d67e3d8a5fa20d902f56d45a180777b28`).

Candidate canonical digest (RFC 8785 over the candidate manifest; identifies the exact
artifact set and baseline the owner is asked to approve):

```
sha256:82f6365cd895892c4cb9fadd279f82e2755cc62bed2c60d95f49233d4c1c7f42
```

Dry run on 2026-10-09 against PEOS branch `claude/pmos-peos-completion-ds46x1` and
PMOS `main` with this candidate: all 14 criteria PASS, no findings, compatible, plan
unchanged (PEOS evidence `runs/07-current-code-refreeze-dryrun/`). A dry run is not approval.

## The one step that needs the owner

Review the five changed files, then approve the exact digest above in writing. The active
freeze digest written in step 2 is derived from the manifest *after* the approval quote and
timestamp are recorded, so it will differ from the candidate digest; the artifact set it
binds is identical and is reported back with the exact `--freeze-digest` value. After that
approval, and only then:

1. copy `freeze-manifest.candidate.json` over `../freeze-manifest.json`, set `status`
   to `OWNER_CONFIRMED_FROZEN`, record the approval quote and timestamp;
2. write the new canonical digest into `../freeze-bundle.sha256`;
3. replace the old digest in `../README.md` and in the PEOS entry documentation;
4. re-run `python3 -B tests/test_task_tracker_freeze.py` (must turn GREEN) and the PEOS
   `verify` command with the new `--freeze-digest`.

Nobody but the owner may perform step 1. Until then this directory is documentation.
