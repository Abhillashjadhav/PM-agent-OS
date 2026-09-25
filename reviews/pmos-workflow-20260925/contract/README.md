# PMOS current contract authoring repair

The published skill example now includes explicit acceptance-criterion references
for its binary gate. Its executable bindings are accepted by the already pinned
publisher and compiler when the example's prose placeholders are filled from the
separate reviewed TEST-ONLY fixture.

The instruction update also distinguishes source product approval from exact-draft
approval, requires an explicit human response for the latter, preserves OPEN
product decisions separately from BLOCKED engineering bindings, and prevents an
unavailable compiler from being reported as ACCEPTED. The instructions preserve
the existing canonical publisher and the admitted trusted-test/template forms.

## Verification

- Test/fixture commit `f65a8fe` precedes the skill change. The unchanged skill
  example fails with `RELEASE_GATE_UNBOUND:GATE-001`; four ordinary controls pass.
- After the instruction repair, all five focused authoring checks pass. They cover
  the actual example, preservation of supplied truth, draft/approval separation,
  missing product truth, description-only gates and unregistered actions.
- Skill lint passes all nine checks. `git diff --check` passes.
- The three frozen historical answers, contract and receipt files are byte-equal
  to base `bee295cacd882f8a7fb4a5c306f2774b0cd3919a`; their hashes are recorded in
  `verification.json`.

The tests use the public API of the dependency already installed at
`297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6`. They issue clearly synthetic test
approval and never start an engineering run, candidate, model or external service.
Previously screened bytecode, ledger/context rechecks and broad handoff discovery
remain excluded and unverified. These ordinary checks do not substitute for them.

## Integration and remaining boundary

Keep the legacy validator and its historical pin unchanged. Run only
`python -B tests/decision-to-contract/test_current_authoring.py -v` in a separate
ordinary-authoring CI job with the current pinned dependency. The root integration
owns that wiring; this unit changes no workflow or dependency setting.

The advertised authoring namespace is `pmpe legacy contract draft/approve`.
Those commands are authoring operations, not evidence of a current build run.
The checked `contract --help` surface advertises no bundle-specific command;
a W5 bundle route remains an external interface dependency until its supported
inputs, invocation and compatibility are established. No command or flag was
invented and no PEOS implementation was reviewed or changed.

Static instructions and ordinary authoring tests do not establish host-agent
question selection, semantic completeness, approval-pause compliance or fresh
product delivery. The historical task-store demonstration remains bounded
feasibility evidence; it is neither erased nor generalized by this repair.
