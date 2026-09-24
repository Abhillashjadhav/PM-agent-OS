# decision-to-contract fixtures

## Historical intake case (`--legacy-intake`)

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

The historical mode proves the deterministic answers → draft → approval → loader → compiler → legacy engineering-admission seam against its original pinned PEOS version. Preserve its committed answers, contract, and receipt unchanged.

## Current-run cases (default)

Derive a separate `TEST-ONLY-F10-HEALTH` publisher input from the saved health answers, bind synthetic GATE-001 explicitly to AC-001, and use the publisher to issue a `test-only-fixture-issuer` receipt. This test issuance is not owner approval and must never replace a historical or product receipt.

The default `validate_contract.py` entry point drives the current `run_to_release_ready` with the exact contract, receipt, expected fixture issuer, and submitted receipt bytes. It executes fixed offline health programs through a test-only local process adapter. It makes no model call and does not establish OS isolation.

- **Positive:** the health candidate returns `ok`; the baseline first fails AC-001 by assertion, the candidate reaches `RELEASE_READY`, and a verified evidence chain binds GATE-001 `PASS` to the contract, plan, candidate, and AC-001 outcome.
- **Broken candidate:** the health candidate returns `broken`; AC-001 and GATE-001 fail, the bounded run ends `HALTED`, and no `release_ready` event exists.
- **Unbound gate:** a separately test-issued contract retains only the gate description. The current compiler returns `RELEASE_GATE_UNBOUND` before any fixture provider or process invocation.

Use `--evidence-dir <empty-directory>` to retain the synthetic contracts/receipts, positive and negative ledger/blob evidence, and `summary.json`. The regression test observes calls to the real current runner and verifies the resulting evidence rather than accepting the script's success message alone.

These cases prove deterministic current-run compatibility only. They do not prove live-model authoring, a new model generation, product-owner approval, arbitrary-product breadth, production readiness, or release authorization. The original approved task-store packet remains immutable; its unbound process gates cannot be treated as passed under the new compiler or silently rebound to acceptance checks.
