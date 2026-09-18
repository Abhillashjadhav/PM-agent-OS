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

## Unit — owner amendments before the Phase 2 freeze

Branch: `docs/task-tracker-acceptance`, from local
`b7d9307dc3a0e0b8a69731070aafdcdd7fe3952e`. Extend the existing unapproved
packet in PR #58; the owner approved the identifier, duplicate and repeated-
completion rules and requested a final one-line confirmation of the amended grid.

1. **Yes, restructured.** Extend the existing scenarios, publisher input and review packet; the observer already calls each process synchronously.
2. **Yes.** The owner requires explicitly sequential AC-013, critical AC-014 for rejected-create ID continuity, named create non-idempotency and the closed sandbox decision.
3. **No.** Only the unapproved proposal and observer documentation change; no existing publisher, engine, provider or product behavior changes.
4. **Yes.** Run a focused pre-change assertion for sequential AC-013 wording, the exact critical AC-014 observations and the named limitations; rerun it after regeneration alongside publisher/manifest checks.
5. **Yes.** One follow-up proposal commit reverts these amendments without altering implementation or previous evidence.
6. **No.** No setting, dependency, extension, sandbox attempt or signing repair is added.

The expected pre-change RED is prerequisite evidence, not an implementation
attempt. Freeze, approval receipt creation and product generation wait for the
owner's requested one-line confirmation of the re-issued grid.

Validation attempt 1 passed. The five focused pre-change assertions failed as
expected, then passed after amendment. AC-001 through AC-012 are byte-equivalent
as JSON values; AC-013 retains its measure, threshold and sample minimum. AC-014
has the exact three observations and critical severity. The evaluator's executable
AST is unchanged; only its sequential-workload documentation changed. The existing
publisher and Template compiler validate fourteen criteria; all 212 artifact
digests match, with only the seven intended proposal artifact hashes changed.
Ruff, format and diff checks pass. No product, receipt or sandbox was executed or
created. Final confirmation and the freeze remain pending.

## Unit — regenerate the complete proposal and freeze owner approval

Start: local `aaf478c53150a03e384aca767e3f061abfb50567`, remote
`00ccd29ab12deac4aec8538d344834af6f8b9ae2`, branch `docs/task-tracker-acceptance`.
Owner explicitly confirmed the amended grid and required full-body regeneration
and agreement verification before recording the freeze.

1. **Yes, restructured.** Reuse the approved scenarios, publisher and observer; generate the complete document from those sources.
2. **Yes.** Owner's current instruction requires 14 criteria, strictly sequential AC-013, critical AC-014, and a consistent freeze before Phases 3–4.
3. **No.** Documentation generation and approval artifacts only; no existing engine, publisher or evaluator behavior changes.
4. **Yes.** First check for complete generated criterion sections, count and a reproducible renderer; these are absent in the hand-maintained proposal. Then verify exact publisher/scenario/evaluator agreement and every manifest entry before freeze.
5. **Yes.** One approval-document commit can be reverted independently of PEOS infrastructure and candidate generation.
6. **No.** No product setting, dependency, extension, sandbox attempt or signing repair.

Freeze validation attempt 1 passed: full regeneration produced 14 rows and 14 detailed
criterion sections; exact contract/scenario/binding equality and sequential observer
source verified before recording. Existing publisher issued the approved contract
and receipt. All 218 frozen artifact hashes match; no product generation occurred.
