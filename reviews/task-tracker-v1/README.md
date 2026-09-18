# Task-tracker Phase 2 review packet

Status: **INCOMPLETE — awaiting owner approval; no product generated.**

Read [ACCEPTANCE.md](ACCEPTANCE.md) first. It contains the three requested semantic
decisions, additional CLI/error rules, all 13 scenarios, observation methods,
severity, the ten-record measurement and permanent limitations.

| Artifact | Purpose |
| --- | --- |
| `publisher-input.json` | PMOS-owned intent passed to the existing publisher. |
| `contract.draft.json` | Exact `build_contract_draft` output, with blank approval fields. |
| `scenarios.json` | Concrete commands, expected observations and severity; criterion values match the contract. |
| `evaluator.py` | Proposed observer source; executes CLI commands and returns facts, with expected results in the contract. Not yet behaviorally validated. |
| `bindings.json` | Existing `Template` fields in a declarative file; uses the shipped meaningful-red skeleton and exact observer bytes. |
| `execution-profile.json` | Before/after digest policy, resources, admitted fallback and root/receipt limitations. |
| `review-manifest.json` | Raw-file digests for seven proposal artifacts, the PMOS skill and the PEOS source/profile inputs. |
| `proposal-validation.json` | Observed structural validation and remaining implementation work. |

Draft digest:
`sha256:72e482b4823303d6ca6637e7f18ed7443b426c1f39b356353a254129b408db5d`.

Canonical review-bundle digest:
`sha256:4ae47ef2dca0eac07fe04935eba3e9feeadffb9fbea87e2a439bfd89e1c24f54`.
The bundle digest uses existing RFC 8785 `canonical_digest` over the manifest;
individual file entries use SHA-256 over raw bytes. The digest is a proposed review
anchor, not a signed receipt or proof of human approval.

## Validation performed

The existing publisher returned `DRAFT_READY_FOR_APPROVAL`; the canonical loader
reported DRAFT and not runnable. Six requirements map to 13 criteria, including
one `measure` with `sample.minimum: 10` and threshold zero. Default health bindings
reject the new actions/measure with `ACTION_NOT_REGISTERED` and `MEASURE_INVALID`.
The existing `Template` API compiles the proposed bindings without engine edits.
Observer syntax, exact binding bytes, requirement coverage and publisher-output
identity were checked. Ruff 0.16.4 and `git diff --check` passed.

No product execution, model generation, approval call or receipt creation occurred.
The loader, per-check digest enforcement and behavioral validation remain work
after owner approval. A passing compilation is not product-delivery evidence.
If that work changes a bound source file, obtain approval of the new bytes before
product generation; this packet cannot approve future source code.

Reproduce with sibling `pmos` and `peos` checkouts, PEOS at
`1abfbd47061a947e8ce077523a60516a0b6cdcb0`, installed using the existing standard
venv flow (`python3 -m venv .venv`, then `.venv/bin/python -m pip install -e .`).
From the PMOS checkout:

```bash
../peos/.venv/bin/python - <<'PY'
import hashlib, json
from pathlib import Path
from pmpe.barebones import Template, compile_barebones_plan
from pmpe.contracts.authoring import build_contract_draft
from pmpe.contracts.canonical import canonical_digest
from pmpe.contracts.model import load_contract
root = Path('reviews/task-tracker-v1')
read = lambda name: json.loads((root / name).read_text())
draft = build_contract_draft(read('publisher-input.json'))
assert draft.draft == read('contract.draft.json')
assert not load_contract(root / 'contract.draft.json').runnable
bindings = read('bindings.json')
assert bindings['files']['tests/acceptance/task_tracker.py'] == (root / 'evaluator.py').read_text()
plan = compile_barebones_plan(contract=draft.draft, repository_root=Path.cwd(), template=Template(**bindings))
assert len(plan.criteria) == 13
manifest = read('review-manifest.json')
assert canonical_digest(manifest) == (root / 'review-bundle.sha256').read_text().strip()
repos = {'PM-agent-OS': Path.cwd(), 'production-engineering-os': Path.cwd().parent / 'peos'}
for item in manifest['artifacts']:
    path = repos[item['repository']] / item['path']
    assert 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], str(path)
print('PASS: DRAFT, traceable criteria and exact review artifacts; no product generated')
PY
```

The engine and authority findings, amended sandbox argv and fallback probe are in
[PEOS's owner-amendment record](https://github.com/Abhillashjadhav/production-engineering-os/blob/audit/task-tracker-seam/docs/evidence/task-tracker-audit-20260918/owner-amendment.md).
New actions already work through the Python API. Historical live-model evidence
already exists in PEOS and remains unverified by this run. These correct the earlier
review; neither correction establishes this task tracker's delivery.
