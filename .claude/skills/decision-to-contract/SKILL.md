---
name: decision-to-contract
description: Convert an explicitly approved PM Agent OS product decision or PRD into an ID-keyed, machine-checkable contract accepted by the Production Engineering OS frozen compiler. Use when a human decision-maker asks to hand approved product intent to Production Engineering OS, create an executable engineering contract, or prepare the P1 PMOS-to-real-provider run. Do NOT use for unapproved decisions, unresolved product-critical questions, ordinary prose PRDs, coding, implementation, deployment, or release decisions.
---

# Decision to Contract

Produce one deterministic JSON contract that preserves approved product intent without inventing engineering semantics.

## Ownership boundary

PM Agent OS owns the problem, hypothesis, audience, outcome metric, leading indicators, guardrails, trade-offs, scope, non-goals, stable requirement and acceptance IDs, contract-shaped acceptance intent, decision status, and accountable approver.

Production Engineering OS owns contract compilation, meaningful-RED, implementation, sandboxed execution, verification of executable coverage, evidence, and the transition to `RELEASE_READY` or `HALTED`. A human owns release.

## Admission gate

Before writing a contract, require all of:

- one approved product-decision artifact or approved PRD;
- `contract_status: APPROVED`; for a PRD, both `Status: Approved` and `Contract status: APPROVED` must be present and agree—any contradiction is `CONTRACT_BLOCKED: APPROVAL_STATUS_CONFLICT`;
- a non-empty accountable identity recorded as `approved_by` or PRD `Approved by`, exactly matching the human named by the user;
- no unresolved product-critical question;
- stable IDs for every functional requirement and acceptance criterion;
- every requirement covered by at least one explicit acceptance-intent criterion.

Normalize only these equivalent labels deterministically after the approval fields agree: PRD `Contract status` → `contract_status`, PRD `Approved by` → `approved_by`, and ordered compiler-shaped `FR-*`/`AC-*` sections → the corresponding JSON maps without changing their text, IDs, actions, paths, operators, or values. If a required field or executable binding is absent, return `CONTRACT_BLOCKED` with the missing fields and ask for that bounded input. Do not infer approval, product intent, actions, paths, operators, or expected values.

## Contract shape

Write one UTF-8 JSON object:

```json
{
  "contract_id": "PMOS-<stable-id>",
  "contract_status": "APPROVED",
  "approved_by": "<human identity>",
  "decision_source": "<path or immutable reference>",
  "functional_requirements": {
    "FR-001": {"statement": "<approved observable behavior>"}
  },
  "acceptance_criteria": {
    "AC-001": {
      "requirement_refs": ["FR-001"],
      "given": [{"path": "service.running", "operator": "eq", "value": true}],
      "when": {"action": "health", "arguments": {}},
      "then": [{"path": "result.status", "operator": "eq", "value": "ok"}]
    }
  }
}
```

Preserve additional PMOS decision context only as JSON values; never place credentials, provider commands, executable shell, or deployment instructions in the contract.

## Executable criteria

Select exactly one admitted form per criterion:

1. `given` + `when` + `then`, using only a registered action and typed paths;
2. `measure` + `operator` + `value` + positive `sample.minimum`, using only a registered measure;
3. `human_test`, bound to an existing trusted pytest file and exact node;
4. `satisfied_by_template`, bound to the pinned template version and proof ID.

For the current frozen `barebones-1` template, the only registered action is `health`. Do not invent another action. If the approved decision needs an unregistered action, return `CONTRACT_BLOCKED: ACTION_NOT_REGISTERED`; that failing real contract is evidence for a deliberate registry extension.

Use only registered operators: `eq`, `ne`, `lt`, `lte`, `gt`, `gte`, `contains`, `not_contains`, `matches`, `is_true`, `is_false`, `is_null`, and `not_null`.

## Verification gate

Before delivery:

1. prove every `FR-*` has at least one criterion;
2. prove every `AC-*` references existing requirements;
3. prove every explicit acceptance-intent criterion was either mapped without semantic change to exactly one executable form or reported as blocked;
4. prove action, measure, operator, path, and test bindings are explicit;
5. run the Production Engineering OS compiler compatibility check when available;
6. return the contract only when the check passes unmodified.

On failure, return the compiler diagnostic codes and stop. Never translate rejected prose by guessing.

## Output

Return:

- the contract path;
- its canonical SHA-256 digest when the host can compute it;
- structured-criteria count;
- human-test count;
- approval identity;
- compiler result: `ACCEPTED` or `CONTRACT_BLOCKED`;
- unresolved diagnostics.

## Limitations

- The current frozen template supports only its registered actions, measures, proofs, and trusted human tests.
- Structural generation instructions do not prove live-model behavioural reliability.
- One accepted contract proves boundary compatibility, not arbitrary-app generation, reusable-engine breadth, or platform adoption.
- This skill does not code, run candidates, deploy, release, or replace the accountable human decision-maker.
