"""Render the entire owner proposal from its existing machine-readable sources."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def render() -> str:
    answers = json.loads((ROOT / 'publisher-input.json').read_text())
    cases = json.loads((ROOT / 'scenarios.json').read_text())
    profile = json.loads((ROOT / 'execution-profile.json').read_text())
    lines = [
        '# Local task tracker — approved acceptance proposal',
        '',
        f'This proposal contains **{len(cases)} criteria** across '
        f"{len(answers['functional_requirements'])} functional requirements.",
        'The owner confirmed the amended grid before generation. This document is',
        'regenerated in full from publisher-input.json, scenarios.json and execution-profile.json.',
        'The contract is produced by the existing PMOS → PEOS publisher.',
        '',
    ]
    for key in ('problem', 'target_user', 'desired_outcome', 'scope', 'out_of_scope'):
        lines += ['## ' + key.replace('_', ' ').capitalize(), '']
        value = answers[key]
        lines += ['- ' + item for item in value] if isinstance(value, list) else [value]
        lines += ['']
    lines += ['## Requirements', '']
    for item in answers['functional_requirements']:
        lines += [f"- **{item['id']} — {item['title']}:** {item['description']}"]
    lines += ['', '## Acceptance grid', '',
              'Every criterion must pass; severity never permits skipping a criterion.', '',
              '| ID | Scenario and expected result | Observation | Severity |',
              '| --- | --- | --- | --- |']
    for case in cases:
        observation = ('Actual registered measure; count acknowledged records against a new list process'
                       if 'measure' in case else 'Sequential CLI processes; exact exits and JSON')
        if case['id'] == 'AC-011':
            observation += '; before/after store-byte digest'
        lines.append(f"| {case['id']} | {case['criterion']} | {observation} | {case['severity'].capitalize()} |")
    lines += ['', '## Exact scenario body', '',
              'Each section below is generated from the same criterion as its grid row.',
              'Commands execute synchronously. A process exits before the next starts.', '']
    for case in cases:
        lines += [f"### {case['id']} — {case['severity'].capitalize()}", '', case['criterion'], '']
        if 'measure' in case:
            lines += ['Workload: ten strictly sequential creates, each process exiting before the next starts;',
                      'fresh titles in one fresh store, then a new list process. Units: records missing.',
                      'Concurrent creation is out of scope; do not test parallel writers.', '']
        lines += ['```json', json.dumps(case, indent=2, ensure_ascii=False), '```', '']
    for key in ('binary_release_gates', 'scored_eval_rubric', 'non_functional_requirements',
                'approved_product_decisions', 'required_approvals'):
        lines += ['## ' + key.replace('_', ' ').capitalize(), '']
        for item in answers[key]:
            lines.append('- ' + '; '.join(f'{k}: {v}' for k, v in item.items()))
        lines += ['']
    lines += ['## Measurement', '', answers['north_star_metric'], '']
    for item in answers['leading_metrics'] + answers['guardrails']:
        lines += ['- ' + item]
    lines += ['', 'The AC-013 count is deterministic. It establishes neither statistical AI quality',
              'nor production latency. Report all 14 criterion outcomes; no ratio overrides a failure.',
              '', '## Named limitations and execution', '',
              '**Creation is not idempotent. Duplicate-on-retry is approved behavior, not a defect.**',
              'No retry-safety claim for create; completion idempotency is covered by AC-007.',
              'Concurrent creation is out of scope. No parallel writers are tested.', '']
    for risk in answers['known_risks']:
        lines += ['- ' + risk['description']]
    lines += ['', '**Sandbox: closed by owner direction. Do not attempt Bubblewrap again.**',
              'The existing --unshare-all --share-net retry and explicit namespace probe failed',
              'with `bwrap: setting up uid map: Operation not permitted`. Every other original',
              'sandbox argument was retained. Exact commands and evidence: ' + profile['sandbox_evidence'],
              'The real-sandbox leg is blocked by environment. The authorized existing-container',
              'fallback lacks these additional protections:', '']
    lines += ['- ' + item for item in profile['authorized_fallback']['unavailable_additional_protections']]
    lines += ['', 'Retained controls:', '']
    lines += ['- ' + item for item in profile['authorized_fallback']['retained_run_controls']]
    lines += ['', 'Resource caps:', '', '```json', json.dumps(profile['resource_caps'], indent=2), '```',
              '', profile['resource_enforcement_evidence'], '', '## Tamper evidence and approval', '']
    lines += ['- ' + item for item in profile['check_protocol']]
    lines += ['', 'Permanent limitations and audit corrections:', '']
    lines += ['- ' + item for item in profile['permanent_limitations']]
    lines += ['', 'The provider requires an active agent session; no headless model reproduction is claimed.',
              'New business actions do not require an engine-source change, only a CLI path.',
              'Prior live-provider evidence already exists in PEOS, unverified by this run.',
              'Root privileges remain a limitation; hashes are tamper evidence, not prevention.',
              'Approval-forgery repair is deferred. One feature establishes feasibility only.',
              '', '## Freeze boundary', '',
              'The owner confirmed the amended grid and authorized full-document regeneration',
              'before the freeze. Contract, grid, evaluator and prepared manifest must agree',
              'before approval-time digests are recorded. No criterion or evaluator meaning changes.',
              profile['approval_time_source_rule'], '']
    return '\n'.join(lines)


if __name__ == '__main__':
    (ROOT / 'ACCEPTANCE.md').write_text(render())
