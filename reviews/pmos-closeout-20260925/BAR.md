# PMOS-only takeover and integration BAR

1. **Yes, restructured.** Reuse the existing installer (#59), validator (#60), Beacon (#61/#62), and handoff (#63–#66 plus the R4 review snapshot); no replacement product or engine.
2. **Yes.** The owner requested takeover, completion and GitHub publication, then explicitly restricted this thread to PMOS. Existing repairs remain split across unmerged branches.
3. **Yes.** Combine already approved PMOS concerns on an isolated integration branch, retaining their independently reviewable branches. Installer invokes validation, so both must work together. Handoff and optional observability preserve their published interfaces.
4. **Yes.** Before integration the retained R4 handoff checkout lacks both `tests/test_install.py` and `tests/test_validation_regressions.py`; the prerequisite check exits 1. Reuse each repair's rejecting tests and verify the composed public install/audit journey afterward. New defects require their own RED-first repair.
5. **Yes.** Each concern retains its own commits/branch. The integration branch is review assembly, not a main-branch merge.
6. **No.** No new product behavior, skill, dependency, setting or execution surface. PEOS implementation is excluded. No frozen approval or acceptance artifact is altered.

The prior automatic-screening boundary remains in force: do not execute
planted-bytecode or forged/rechained release-ledger probes, including through
remote CI. The PMOS handoff workflow contains such tests, so publication of
that composed source is review-only. Permitted ordinary handoff fixtures do
not convert excluded checks into PASS. Installer/validator/Beacon branches
are assessed independently before any PR-triggered checks.
