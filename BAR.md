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

# BAR: R4 retained inspection and independent head input

1. **Already exists? Yes, extend it.** Reuse the current fixture verifier and
   PEOS shared retained-evidence validator; do not create another evidence engine.
2. **Approved criterion or reproduced blocker? Yes.** F-C3-1 and C4-F1/F3 show
   caller-supplied state, unverified receipt authority, and a missing retained
   inspection CLI. Their regressions precede implementation.
3. **Existing behavior changes? Yes.** The verifier derives its result from the
   terminal ledger and rejects semantic contradictions. A read-only CLI accepts
   an independently supplied head; fixture generation retains its current API.
4. **Failing-before/passing-after check? Yes, test first.** Temp-copy mutations
   cover terminal events, subject/plan identity, authority/receipt disagreement,
   and forged heads. Positive and broken fixture controls must still pass.
5. **Revertible as one unit? Yes.** Tests and runtime repair are isolated commits;
   provenance and scope documentation form a separate documentation commit.
6. **Unrequested setting/dependency/surface? No.** No signing, model, product
   decision or approval is added. The requested inspection input uses existing
   PEOS validation. Unsigned rewrites still need an independently trusted anchor;
   this does not protect against a malicious verifier process or root.

# BAR: R4 inspection scope and published provenance documentation

1. **Already exists? Yes, correct it.** Extend VALIDATION and the R3 evidence
   narrative, using the existing publication receipt for public identities.
2. **Approved criterion or reproduced blocker? Yes.** C4-F3/F5 identify an
   ambiguous capture-time head assertion and unpublished IDs in reader guidance.
3. **Existing behavior changes? No.** This documentation unit records the runtime
   repair, unsigned limits, dependency requirements and public source mappings.
4. **Automated check? Yes.** Compare the PMOS mappings with the source publication
   receipt, run repository audit, and verify preserved fixtures/evidence unchanged.
5. **Revertible separately? Yes.** Documentation and provenance metadata are in
   their own commit; root controls later publication and final dependency pin.
6. **Unrequested setting/dependency/surface? No.** No owner authentication,
   signing, fresh model result, merge or release is claimed.
# BAR: resume R4 handoff dependency pin

1. **Already exists? Yes, extend it.** Use the existing current-handoff CI job and verifier; no parallel adapter.
2. **Required? Yes.** F-C3-5 and the retained dependency-RED evidence show that the old PEOS revision rejects the corrected PMOS behavior.
3. **Existing behavior changes? Yes.** Only the current-handoff dependency changes on this isolated branch. The historical-intake pin remains unchanged.
4. **Failing-before/passing-after evidence? Yes.** The R4 dependency-RED log already records the old-reader failure. Run the unchanged ordinary handoff fixtures with the exact public repaired reader; no blocked tampering probe is rerun.
5. **Revertible? Yes.** One CI pin and its evidence form a separate commit.
6. **Unapproved surface? No.** No scanner, allowlist, provider, permission or runtime dependency is added. Publish a review-only source branch; do not trigger blocked rechecks through a PR update.

# BAR — PMOS validator closeout, 2026-09-25

Scope: finish the existing PR #60 validation repair; PMOS only.

1. **Does this already exist in either repository? Yes.** Reuse and extend `tests/yaml.py` and `tests/test_validation_regressions.py`; no parallel validator is added and PEOS is outside this workstream.
2. **Approved criterion or reproduced blocker? Yes.** On base `0504e07a3f6797085fef2183d6bdcdf9106cc957`, both lint and repository audit accept `description: [Use when needed., Do NOT use otherwise.]` even though skill descriptions must be scalar strings.
3. **Changes existing behavior? Yes.** The scalar-only loader will reject unquoted flow collections; quoted descriptions and all 43 existing installed skills must continue passing. This repair has its own branch and regression.
4. **Automated RED then GREEN? Yes.** Commit the collection-description regression before changing the loader, record the observed failure, then run the same check after the narrow fix.
5. **Independently revertible? Yes.** The added input rejection, its regression, and this evidence form one bounded validator concern.
6. **Unrequested setting, dependency, or extension? No.** No new options or dependencies; preserve the existing scalar-only frontmatter contract.

# BAR: PMOS Beacon launcher command-status compatibility

1. **Already exists? Yes.** Extend the existing `scripts/run_with_beacon.py`; no second recorder or launcher is introduced.
2. **Approved criterion or reproduced blocker? Yes.** The existing integration promises an unchanged wrapped command. A non-executable command returns 126 without the adapter but 1 with pinned adapter `b32bdfee2c5b579b06b45ffc5bf14bee5fa3f614` because `PermissionError` escapes.
3. **Changes existing behavior? Yes.** Adapter-present command startup errors will match the existing adapter-absent exit codes; this independent `fix/pmos-beacon-closeout-20260925` branch owns that compatibility repair.
4. **Failing automated check before repair? Yes.** `test_adapter_preserves_nonexecutable_status` invokes the public launcher with a local adapter fixture and a non-executable file; expected 126, current result 1. Commit this check before the repair.
5. **Independently revertible? Yes.** The launcher mapping, regression fixture, and evidence are one concern; installer, skills, verification gates, and external repositories are untouched.
6. **Unrequested setting/dependency/extension? No.** Reuse Python standard library and the existing optional adapter interface; introduce no configuration or dependency.

# BAR: inherited Beacon installer whitespace

1. **Already exists? Yes.** Correct only the existing installer's extra blank line at EOF.
2. **Reproduced blocker? Yes.** `git diff --check origin/main...HEAD` at `a21279a` exits 2: `scripts/install_beacon_adapter.py:34: new blank line at EOF.`
3. **Changes existing behavior? No.** The edit changes trailing whitespace only.
4. **Failing check first? Yes.** The existing diff check reproduces this exact RED; the deterministic PR quality gate runs the same check.
5. **Independently revertible? Yes.** The one-line formatting correction has no runtime dependency.
6. **Unrequested setting/dependency/extension? No.** No settings, dependencies, or interfaces are added.

# BAR: run existing Beacon regression tests in CI

1. **Already exists? Yes.** Reuse the existing repository-audit job and seven offline `test_beacon_*.py` tests.
2. **Approved criterion or reproduced blocker? Yes.** The reproduced 126-versus-1 launcher regression already has a RED fixture, but the audit job never executes it.
3. **Changes existing behavior? Yes.** The existing audit job will now fail when a Beacon hook or runner regression fails; no runtime behavior or other CI step changes.
4. **Failing check first? Yes.** Before editing, parsing the audit workflow and asserting this exact filtered unittest command fails because the invocation is absent.
5. **Independently revertible? Yes.** The single added workflow step and this evidence entry are independently revertible.
6. **Unrequested setting/dependency/extension? No.** Python standard-library unittest is already available; no new job, dependency, action, pin, or integration surface.

Validation: YAML parses and differs only by the intended step. The exact added command,
`python -B -m unittest discover -s tests -p 'test_beacon_*.py' -v`, passes all seven tests.
