# PMOS architecture reconciliation and implementation BAR

Owner direction, 25 September: compare the supplied external architecture review,
accept or reject each finding with reasons, implement the accepted PMOS workflow,
continue independent work overnight, and leave only genuine owner decisions open.
The earlier PMOS-only boundary remains: PEOS implementation is separately owned.

1. **Existing path? Yes.** Extend `/pm` → `prd-first` → `decision-to-contract`,
   existing catalogue skills, publisher interface, fixtures and installer docs.
2. **Approved criterion or reproduced blocker? Yes.** The owner requires an
   idea-to-approved-executable-contract workflow; external F1/F4/F5/F10 and the
   independent PMOS source review identify concrete mismatches in that path.
3. **Behavior change? Yes.** Each concern has its own branch/BAR and rejecting
   checks. Keep conversational intake, contract compatibility, catalogue repairs,
   operational documentation and frozen reference restoration independently reviewable.
4. **Failing check first? Yes.** Changed skill fixtures and meaningful rejecting
   checks precede instructions. Static checks do not establish model behavior.
   Runtime interface checks use the existing pinned publisher only as a black box.
5. **Separately revertible? Yes.** Unit commits/PRs preserve concern boundaries;
   assembly and documentation follow only completed changes.
6. **Unrequested extension? No.** No new workflow engine, compiler, paid model,
   product default, planner requirement, approval bypass or PEOS change is added.

Keep frozen historical answers/contracts/receipts unchanged. Previously screened
planted-bytecode and forged/re-chained ledger/context probes remain forbidden,
including by remote CI. New tests exercise ordinary authoring and validation only.
