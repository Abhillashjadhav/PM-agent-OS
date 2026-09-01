---
name: decision-to-contract
description: Convert an explicitly approved PM Agent OS product decision or PRD into an ID-keyed, machine-checkable contract accepted by the Production Engineering OS frozen compiler. Use when a human decision-maker asks to hand approved product intent to Production Engineering OS, create an executable engineering contract, or prepare the P1 PMOS-to-real-provider run. Do NOT use for unapproved decisions, unresolved product-critical questions, ordinary prose PRDs, coding, implementation, deployment, or release decisions.
---

# Decision to Contract

Produce one deterministic JSON contract plus a digest-bound approval receipt that preserves approved product intent without inventing engineering semantics.

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

Normalize only these equivalent labels deterministically after the approval fields agree: PRD `Contract status` → `contract_status`, PRD `Approved by` → `approved_by`, and ordered compiler-shaped `FR-*`/`AC-*` sections → the canonical ID-bearing JSON arrays without changing their text, IDs, actions, paths, operators, or values. If a required field or executable binding is absent, return `CONTRACT_BLOCKED` with the missing fields and ask for that bounded input. Do not infer approval, product intent, actions, paths, operators, or expected values.

## Contract shape

Prepare one UTF-8 publisher-input JSON object. It must include the complete PM-owned product truth required by the Production Engineering OS authoring API: product name, problem, target user, desired outcome, scope, out-of-scope items, functional and non-functional requirements, executable acceptance criteria, binary gates, scored rubric, golden cases, North Star, leading metrics, guardrails, risks, and required approvals. The ID-bearing collections use canonical arrays:

```json
{
  "contract_id": "PMOS-<stable-id>",
  "contract_version": 1,
  "product_name": "<approved name>",
  "problem": "<approved problem>",
  "target_user": "<approved primary user>",
  "desired_outcome": "<approved observable outcome>",
  "scope": ["<included v1 behavior>"],
  "out_of_scope": ["<explicit exclusion>"],
  "functional_requirements": [
    {"id": "FR-001", "title": "<behavior>", "description": "<observable behavior>", "capability": "<stable capability>"}
  ],
  "acceptance_criteria": [
    {
      "id": "AC-001",
      "requirement": "FR-001",
      "criterion": "<human-readable approved proof>",
      "given": [{"path": "service.running", "operator": "eq", "value": true}],
      "when": {"action": "health", "arguments": {}},
      "then": [{"path": "result.status", "operator": "eq", "value": "ok"}]
    }
  ],
  "binary_release_gates": [{"id": "GATE-001", "description": "<binary gate>"}],
  "scored_eval_rubric": [{"id": "RUB-001", "criterion": "<quality>", "scale": "1-5"}],
  "golden_cases": ["<representative case>"],
  "north_star_metric": "<outcome metric>",
  "leading_metrics": ["<leading measure>"],
  "guardrails": ["<must-not-worsen constraint>"],
  "non_functional_requirements": [{"id": "NFR-001", "category": "quality", "requirement": "<constraint>"}],
  "known_risks": [{"description": "<risk>", "level": "low|medium|high"}],
  "required_approvals": [{"role": "<role>", "for": "<action>"}],
  "approved_product_decisions": [{"id": "APD-001", "decision": "<explicit approved decision>"}]
}
```

Pass this object to the Production Engineering OS `build_contract_draft` publisher (or `pmpe contract draft`). Do not hand-author the DRAFT contract. The publisher adds source and approval fields, produces the exact draft digest, and reports bounded product questions when required truth is missing. After the human approves that exact digest, `approve_contract_draft` (or `pmpe contract approve`) publishes the approved contract and receipt.

Preserve additional PMOS decision context only as JSON values; never place credentials, provider commands, executable shell, or deployment instructions in the contract.

## Executable criteria

Select exactly one admitted form per criterion:

1. `given` + `when` + `then`, using only a registered action and typed paths;
2. `measure` + `operator` + `value` + positive `sample.minimum`, using only a registered measure;
3. `human_test`, bound to an existing trusted pytest file and exact node;
4. `satisfied_by_template`, bound to the pinned template version and proof ID.

For the current frozen `barebones-1` template, the only registered action is `health`. Do not invent another action. If the approved decision needs an unregistered action, return `CONTRACT_BLOCKED: ACTION_NOT_REGISTERED`; that failing real contract is evidence for a deliberate registry extension.

Use only registered operators: `eq`, `ne`, `lt`, `lte`, `gt`, `gte`, `contains`, `not_contains`, `matches`, `is_true`, `is_false`, `is_null`, and `not_null`.

## Digest-bound contract approval

Product-decision approval authorizes conversion; it does not authorize later edits to the generated contract. First emit the contract as `DRAFT` with blank `approved_by` and `approved_at`, compute its canonical digest, and ask the accountable human to approve that exact digest. Only then use the Production Engineering OS `approve_contract_draft` publisher to set `APPROVED`, approver, and RFC 3339 timestamp and to create the receipt. Never hand-author receipt digests.

Any edit after receipt creation invalidates approval. Delivery requires `verify_contract_approval(contract, receipt, expected_approver=...)` to return the receipt digest before compiler validation. A missing, malformed, mismatched, or stale receipt is `CONTRACT_BLOCKED: APPROVAL_RECEIPT_INVALID`.

## Verification gate

Before delivery:

1. verify the approval receipt binds the exact complete contract and expected human;
2. prove every `FR-*` has at least one criterion;
3. prove every `AC-*` references existing requirements;
4. prove every explicit acceptance-intent criterion was either mapped without semantic change to exactly one executable form or reported as blocked;
5. prove action, measure, operator, path, and test bindings are explicit;
6. load the published contract through the Production Engineering OS canonical contract loader;
7. run the Production Engineering OS compiler compatibility check when available;
8. prove a receipt-verified Engineering OS handoff can start without rewriting the artifact;
9. return the contract and receipt only when all checks pass unmodified.

On failure, return the compiler diagnostic codes and stop. Never translate rejected prose by guessing.

## Output

Return:

- the approved contract path;
- the approval-receipt path and receipt digest;
- the approved contract's canonical SHA-256 digest;
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
