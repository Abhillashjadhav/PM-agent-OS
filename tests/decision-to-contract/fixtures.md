# decision-to-contract fixtures

## Frozen historical intake case

Input: `valid-answers.json`, a complete PMOS product-decision payload for the frozen health behavior.

Expected output: the pinned Production Engineering OS publisher deterministically reproduces `valid-contract.json` and `valid-approval-receipt.json`; the exact receipt verifies; the canonical contract loader accepts the artifact as runnable; the compiler accepts it unmodified using `barebones-1`; and a receipt-bound engineering run starts at `assessment`.

Required properties:

- stable `FR-*` and `AC-*` IDs;
- explicit approval identity and RFC 3339 timestamp;
- a receipt bound to the exact complete contract digest and expected approver;
- complete requirement coverage;
- exactly one executable criterion form;
- registered `health` action and typed assertion paths.

## Invalid approval reuse case

Input: the valid contract is edited after approval while reusing `valid-approval-receipt.json`.

Expected result: `verify_contract_approval` rejects the handoff before compilation.

## Invalid planted case

Input: `invalid-prose-contract.json`, whose criterion is prose without an admitted executable form.

Expected result: the Production Engineering OS compiler rejects it with `CRITERION_FORM_INVALID`. The skill must return `CONTRACT_BLOCKED` and must not infer the action or paths.

## Boundary

The historical `validate_contract.py` entry point and its original pinned compiler
preserve the deterministic answers → draft → approval → loader → compiler →
engineering-admission seam. Do not change `valid-answers.json`,
`valid-contract.json`, or `valid-approval-receipt.json` to make a newer compiler
accept this historical record.

## Gate 1 — Skill lint

Run `python3 tests/lint_skill.py .claude/skills/decision-to-contract/SKILL.md`.
Expected: exit 0, valid trigger/no-trigger description, verification gate, hard
rules and limitations. This is a structural check, not model execution.

## Gate 2 — Trigger and decision boundaries

These cases specify expected host-agent behavior; they are not recorded model runs.

| Input | Expected behavior |
| --- | --- |
| "Convert this approved PRD into an Engineering OS contract." | SHOULD-FIRE. Validate product approval and gather bounded missing publisher inputs before creating a draft. |
| "Here are the approved acceptance criteria and gate refs; publish a draft." | SHOULD-FIRE. Preserve every supplied binding and return the publisher's exact draft digest for approval. |
| "I have an idea; invent the missing behaviors and approve it for me." | SHOULD-NOT-FIRE directly. Return to product definition; do not invent decisions or identity. |
| "The draft looks close; change the outcome and use yesterday's approval." | Block publication. Changed meaning requires renewed product approval and approval of the newly published draft digest. |
| "Deploy the product now." | SHOULD-NOT-FIRE. Deployment and release are outside this skill. |
| An approved PRD still contains an OPEN required product decision | Return the bounded question; no draft approval or handoff. |

## Gate 3 — Current ordinary authoring compatibility

`current-authoring-answers.json` is a separate TEST-ONLY publisher input with
explicit `GATE-001.acceptance_criterion_refs: [AC-001]`. It is not an owner-approved
product contract and must never replace the historical fixture.

Run only `test_current_authoring.py` with the already pinned current dependency
`297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6`. The focused test calls the existing
public authoring, receipt and compiler APIs. It never invokes an engineering run,
candidate, model, service, forged ledger, bytecode probe or context recheck.

Required results:

1. Fill only the skill example's prose placeholders using supplied TEST-ONLY
   truth. Leave its keys, IDs and executable bindings intact. The publisher and
   current compiler must accept that example without adding a gate binding in
   the test harness. Before the repair this fails with `RELEASE_GATE_UNBOUND`.
2. Complete answers produce a DRAFT with blank approval identity/time. Synthetic
   issuance uses that exact draft digest and a clearly test-only issuer; the
   receipt verifies and every supplied publisher input retains its value.
3. Missing target-user truth produces bounded questions and no draft/digest.
4. A description-only gate is rejected with `RELEASE_GATE_UNBOUND`.
5. `create_task` in the frozen action registry is rejected with
   `ACTION_NOT_REGISTERED`; the skill must not relabel the product as `health`.

Existing trusted-test and template-proof forms require supplied, existing trusted
bindings. Their availability does not authorize PMOS to write an evaluator or
invent a proof. A requested bundle route remains an external dependency unless
its exact public interface and required inputs are available; no guessed command
or flag is an acceptable substitute.

These checks establish ordinary authoring compatibility only. Supervised question
selection, semantic mapping, approval pauses and fresh user-product delivery need
their own behavioral evidence. They do not replace the historical task-store
demonstration or the previously screened security rechecks.
