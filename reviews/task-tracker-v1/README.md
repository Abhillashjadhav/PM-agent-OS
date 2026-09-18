# Task-tracker Phase 2 review packet

Status: **INCOMPLETE — awaiting the requested one-line confirmation of the amended grid; no product generated.**

Read [ACCEPTANCE.md](ACCEPTANCE.md) first. It contains the three approved semantic
decisions, CLI/error rules and all 14 scenarios, observation methods,
severity, the strictly sequential ten-record measurement and permanent limitations.
AC-014 is critical: a rejected blank-title create must leave ID 1 available for the
next valid task, with exactly one task stored. Creation is not idempotent;
duplicate-on-retry is approved behavior. AC-007 covers completion idempotency.
Concurrent creation is out of scope. The sandbox decision is closed: no more
Bubblewrap attempts; the documented fallback lists every absent isolation.

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
`sha256:0684ae3efbc62aef686e36b9acc871e92451c458ed0a53bb951cebc44748fe89`.

Canonical review-bundle digest:
`sha256:4eaa1d95828f3e1fbf2a9646eb25ec3185c5b4669e5ac98c4668756b958468b6`.
The bundle digest uses existing RFC 8785 `canonical_digest` over the manifest;
individual file entries use SHA-256 over raw bytes. The digest is a proposed review
anchor, not a signed receipt or proof of human approval.

## Validation performed

The existing publisher returned `DRAFT_READY_FOR_APPROVAL`; the canonical loader
reported DRAFT and not runnable. Six requirements map to 14 criteria, including
one `measure` with `sample.minimum: 10` and threshold zero. Default health bindings
reject the new actions/measure with `ACTION_NOT_REGISTERED` and `MEASURE_INVALID`.
The existing `Template` API compiles the proposed bindings without engine edits.
Observer syntax, exact binding bytes, requirement coverage and publisher-output
identity were checked. Ruff 0.16.4 and `git diff --check` passed.

The amendment check failed on the prior proposal and passed after the changes.
AC-001 through AC-012 retain their exact scenario values. AC-013 retains the same
measure, threshold and sample minimum; its sequential ordering is now explicit.
Only the evaluator's documentation changed; its executable AST is unchanged.

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
assert len(plan.criteria) == 14
cases = {case['id']: case for case in read('scenarios.json')}
assert 'strictly sequential' in cases['AC-013']['criterion']
assert 'each process exits before the next starts' in cases['AC-013']['criterion']
case = cases['AC-014']
assert case['severity'] == 'critical'
assert case['when']['arguments']['steps'] == [['create', ''], ['create', 'Buy milk'], ['list']]
task = {'id': 1, 'title': 'Buy milk', 'status': 'open'}
expected = [
    {'exit_code': 2, 'output': {'error': 'INVALID_TITLE'}},
    {'exit_code': 0, 'output': {'task': task}},
    {'exit_code': 0, 'output': {'tasks': [task]}},
]
assert next(item['value'] for item in case['then'] if item['path'] == 'result.observations') == expected
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
