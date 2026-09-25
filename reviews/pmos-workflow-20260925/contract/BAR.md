# BAR: current PMOS contract authoring

Scope: align the existing decision-to-contract instructions with the current,
already pinned publisher/compiler while retaining every frozen legacy fixture.

1. **Already exists? Yes, extend it.** Reuse the skill and public publisher,
   receipt verifier and compiler; add no second authoring implementation.
2. **Approved criterion or reproduced blocker? Yes.** The accepted workflow and
   handoff review identify the skill's description-only gate as rejected by the
   current compiler; product truth must survive an exact approved contract.
3. **Existing behavior changes? Yes.** The current example and instruction-level
   admission/approval workflow change on `fix/pmos-contract-flow-20260925`;
   callers using the incomplete gate must supply its approved criterion refs.
4. **Rejecting check first? Yes.** Commit the current-authoring fixture, behavior
   specifications and black-box regression before editing the skill. Its example
   must fail with `RELEASE_GATE_UNBOUND` before repair and compile after repair.
5. **Independently revertible? Yes.** This unit owns only the contract skill,
   contract fixtures, ordinary authoring regression and its review evidence.
6. **Unrequested setting/dependency/extension? No.** Use the existing dependency
   at `297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6`; no installation, PEOS source
   change, new provider, invented bundle command or product default is added.

The regression authors TEST-ONLY contracts and verifies synthetic test-issued
receipts. It does not run candidates, models, bytecode probes, ledger rewrites,
context rechecks or broad handoff discovery. It is not a substitute for the
previously screened checks. Frozen legacy answers/contracts/receipts stay intact.
