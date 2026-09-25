# Clean-user handoff setup BAR

1. **Existing path? Yes.** Keep the existing PMOS skill installer and the pinned
   external `pmpe` authoring publisher. Add a guide and a read-only prerequisite
   check; do not add a publisher or engineering runner.
2. **Approved criterion or reproduced blocker? Yes.** The approved architecture
   requires a clean-user route from approved product truth to a verified handoff.
   README currently invokes publisher-dependent work without installation steps.
   The pinned publisher's top-level help exposes `legacy contract`, so the guide
   must verify concrete command spelling and output paths rather than infer them.
3. **Behavior change? Yes.** A separate preflight reports a missing or unreviewed
   publisher before handoff; ordinary skill installation stays dependency-free.
4. **Failing check first? Yes.** Commit public-CLI tests before the new script.
   Fixtures cover missing installation, missing provenance, wrong revision,
   missing entry point and the reviewed Git revision. The check reads package
   metadata only; it does not load publisher code or run a product.
5. **Separately revertible? Yes.** Tests, script and user documentation have
   separate commits, limited to this setup concern.
6. **Unrequested extension? No.** No PEOS source edit/review, repin, network call,
   automatic dependency install, paid model, live hook, global settings change,
   or engineering execution is introduced.

Compatibility target: `297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6` from
`Abhillashjadhav/production-engineering-os`; this is a reviewed snapshot, not a
claim that its changes have merged. CLI inspection is black-box help only.
Ordinary authoring checks may use existing health answers and an explicitly
TEST-ONLY issuer; they do not record owner approval or start a build.

No restricted handoff, forged-ledger or planted-bytecode probes are included.
