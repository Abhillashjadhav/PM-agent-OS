# decision-to-contract fixtures

## Valid planted case

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

This executable compatibility fixture proves the deterministic answers → draft → approval → loader → compiler → engineering-admission seam. It does not prove live-model behavioural performance or arbitrary-product generation breadth.
