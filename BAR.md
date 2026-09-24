# BAR: F-10 handoff inspection and design

This unit is read-only inspection plus the required saved prompt and BAR record.
Implementation remains stopped pending the shared gate design and failing test.

1. **Does this already exist? Yes.** Reuse the existing decision-to-contract
   skill, fixtures, validator, and PEOS release-ready entry point; do not create
   a parallel handoff or another product.
2. **Is there an approved criterion or reproduced blocker? Yes.** The assigned
   F-10 task requires the existing approved task-store handoff fixture to reach
   current `run_to_release_ready`, with positive and seeded-negative evidence.
3. **Does this unit change behavior with a caller or test? No.** This unit only
   inspects source and proposes an interface; later behavior changes need their
   own BAR entry and compatibility analysis.
4. **Is there an automated check that fails before and passes after? No — stop
   implementation.** First identify the current legacy fixture boundary and
   agree the shared gate, then write the failing check before changing routing.
5. **Can this be reverted as one unit? Yes.** The saved prompt and this record
   are isolated on `review/f10-pmos-handoff-20260924` at official main.
6. **Does this add unrequested settings, dependencies, or extension surfaces?
   No.** None are part of this inspection or authorized design proposal.

# BAR: F-10 current-run compatibility fixture

The shared design is now agreed: add a TEST-ONLY health-derived contract and
receipt with an explicit AC-001 gate binding. Preserve the historical intake
fixture and every original task-store artifact.

1. **Does this already exist? Yes, restructured.** Reuse the PEOS authoring API,
   receipt verifier, `run_to_release_ready`, and evidence ledger. Extend the
   existing PMOS fixture entry point; do not add another engineering engine.
2. **Is there an approved criterion or reproduced blocker? Yes.** F-10 and
   the reproduced validator stop at legacy `assessment`, with no current-run
   call. The assigned integration requires positive and seeded-negative proof.
3. **Does this change behavior with a caller or test? Yes.** The default PMOS
   compatibility check will exercise the current runner; the old pinned CI call
   must select the preserved legacy-intake mode explicitly. This is isolated on
   its own branch with tests and the current PEOS pin coordinated with root.
4. **Is there a failing-before/passing-after check? Yes.** First add a regression
   requiring the current runner, explicit verified approval, hash-bound gate
   PASS evidence, broken-candidate HALTED, and early unbound-gate rejection.
5. **Can this be reverted as one unit? Yes.** The fixture, regression, CI wiring,
   and explanatory routing documentation are isolated from approved artifacts.
6. **Does this add unrequested settings, dependencies, or extension surfaces?
   No.** Only test-fixture provider/execution seams are used; no paid provider,
   production sandbox, product action, or approved threshold is added.

# BAR: R3 retained-evidence head binding

1. **Already exists? Yes, extend it.** Reuse `verify_current_evidence` and the
   actual PEOS ledger append/verify APIs; create no signing or second ledger.
2. **Approved criterion or reproduced blocker? Yes.** F-R3-05 reproduced a
   re-chained candidate forgery accepted without an independently held head.
3. **Existing behavior changes? Yes.** The current synthetic fixture must supply
   its runtime-observed head. Unanchored direct callers keep the documented
   self-consistency check; this isolated R3 branch owns the compatibility change.
4. **Failing-before/passing-after check? Yes, test first.** A copied synthetic
   packet is re-chained after candidate substitution; unanchored verification
   accepts it, while the trusted original head and runtime-capture path reject it.
5. **Revertible as one unit? Yes.** The test-first and verifier commits contain
   only this concern; authority/provenance wording is a separate documentation
   commit. Frozen v1 artifacts remain unchanged.
6. **Unrequested setting/dependency/surface? No.** The requested optional expected
   digest uses no signing, runtime API extension or new dependency. The fixture's
   transparent append observer assumes trusted in-process execution and is not
   protection against a malicious verifier process or root.

# BAR: R3 evidence and authority documentation

1. **Already exists? Yes, correct existing records.** Update VALIDATION and the
   F10 review narratives; reuse the published receipt's local-to-GitHub mappings.
2. **Approved criterion or reproduced blocker? Yes.** F-R3-06, F-R3-07 and F-R3-09
   identify authority ambiguity, inaccessible local commit names and receipt
   serialization overstatement. F-R3-05 requires an explicit unsigned boundary.
3. **Existing behavior changes? No.** This separate documentation commit records
   the boundary of the preceding verifier repair without changing runtime code.
4. **Automated check? Yes.** Check copied publication mappings against the source
   receipt, compare the preserved reviewed source paths, and run repository audit.
5. **Revertible separately? Yes.** Documentation and provenance metadata are kept
   in their own commit so the root can map them onto the documentation stack.
6. **Unrequested setting/dependency/surface? No.** No signing, policy, new runtime
   API, owner approval or live execution is introduced by these corrections.
