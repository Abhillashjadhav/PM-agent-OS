# BAR — install the owner-supplied gate

Base: `27d0418cb258fa5e374447f88185ff1b7117f182`. Branch: `docs/pmos-peos-bar-gate`.
Unit: install the exact six-question policy from the owner's 2026-09-18 cloud-run prompt.

1. **No.** The base tree has no AGENTS.md or BAR Gate; CLAUDE.md was inspected.
2. **Yes.** The owner's settled decision explicitly requires AGENTS.md in both repositories as the first change.
3. **Yes.** Agent workflow changes for callers that previously used CLAUDE.md alone; new work must now record the gate. This documentation-only unit has its own branch. No product/runtime caller changes.
4. **Yes.** Before this change, the automated file/six-question check exited 1 for both repositories; the post-change check also compares the gate text with the supplied definition.
5. **Yes.** Reverting this documentation commit removes only AGENTS.md and this unit's BAR record.
6. **No.** No runtime setting, dependency or extension is added; the gate is explicitly owner-requested.

Expected pre-change RED is prerequisite evidence, not a failed implementation attempt.
Implementation validation attempts: 1; exact-text comparison and six-question check passed; git diff --check passed.

## Unit — proposed task-tracker contract and acceptance grid

Branch: `docs/task-tracker-acceptance`, from local
`aaf5e4d51e7bafcbbc671e796039e69d61611744`. The owner approved the feature scope
and explicitly requested proposed identifiers, duplicates and repeated completion
before product generation. All new semantics remain DRAFT until owner approval.

1. **Yes, restructured.** Reuse decision-to-contract's existing publisher-input format and PEOS `build_contract_draft`; no schema or skill is added.
2. **Yes.** Phase 2 explicitly requests the concrete grid and contract for the approved local task tracker.
3. **No.** Product proposal and evidence only; no existing publisher, skill or engine behavior changes.
4. **Yes.** Reuse the canonical loader and acceptance compiler: default bindings reject the proposed task action/measure; proposed bindings must compile without altering criteria or engine source. Validate the publisher's DRAFT status, traceability and proposal digests.
5. **Yes.** One proposal commit can be reverted without changing implementation or past audit evidence.
6. **No.** CLI semantics and deterministic measurement are explicit proposals for owner approval, not activated settings or hidden product decisions.

Validation: the existing publisher produced DRAFT_READY_FOR_APPROVAL. The loader
correctly reports not runnable; six requirements cover thirteen criteria with one
measure. Default health bindings reject the new behavior; the same contract
compiles with the existing Template API and the proposed declarative bindings.
All 212 proposed artifact digests match, evaluator syntax and Ruff checks pass,
and no receipt or product code was generated. Approval remains pending.
