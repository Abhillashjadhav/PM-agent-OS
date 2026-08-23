# decision-to-contract fixtures

## Valid planted case

Input: an explicitly approved PMOS decision for the frozen health behavior.

Expected output: `valid-contract.json` and `valid-approval-receipt.json` pass `verify_contract_approval` and the contract is accepted unmodified by the pinned Production Engineering OS `compile_acceptance_plan` using the `barebones-1` template.

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

This executable compatibility fixture proves contract shape, not live-model behavioural performance or product-generation breadth.
