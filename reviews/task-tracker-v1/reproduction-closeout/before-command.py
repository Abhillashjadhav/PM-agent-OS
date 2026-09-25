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
