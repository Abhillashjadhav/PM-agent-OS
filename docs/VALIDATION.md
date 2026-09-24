# Validation and evidence

This repository makes three distinct kinds of claims. They must not be conflated.

## 1. Automated structural checks

`python3 tests/audit_repository.py` is an offline, deterministic repository audit. It validates that the inventory's skill, fixture, and reviewer-persona paths exist; that each inventoried skill has parseable YAML frontmatter; that its name is kebab-case; that it has a description and a `Limitations` section; that README-local Markdown links resolve; and that the inventory totals are 40 lifecycle skills, 3 supporting skills, and 7 reviewer personas.

The existing `tests/lint_skill.py` provides stricter per-skill static linting for SKILL.md files, including trigger-language and size checks. These checks inspect files; they do not run a model.

## 2. Fixture specifications

Each lifecycle skill has `tests/<skill>/fixtures.md`. These documents specify representative inputs, expected output properties, trigger examples, and often planted failures that a host agent's instructions are intended to catch.

Fixtures are **specifications**, not executed behavioural tests. Their presence demonstrates that expected behaviour has been documented; it does not demonstrate a model produced the expected output or followed a gate in a particular run.

## 3. Executable cross-repository compatibility

`tests/decision-to-contract/validate_contract.py --legacy-intake` preserves the
publisher/receipt/assessment compatibility check against its historical PEOS pin.
The default command, or `--evidence-dir <empty-directory>`, runs the real current
PEOS runner using synthetic test approval and fixed local health programs. It
requires the positive case to reach `RELEASE_READY`, the broken candidate to
reach `HALTED`, and the unbound release gate to stop before provider/executor use.
The separate CI jobs declare their exact PEOS revisions in
`.github/workflows/repository-audit.yml`; a repaired PMOS inspector requires the
corresponding repaired PEOS shared validator. These are source/fixture checks,
not evidence that either repository's repair has merged.

This proves one deterministic end-to-end handoff boundary. It does not prove live-model authoring quality, arbitrary-product coverage, or a real-provider engineering run.

An approval record with `status: "VERIFIED"` means its structural/content checks
passed. Retained inspection re-verifies the receipt against its contract and
recorded `authority` through the shared PEOS validator. Status alone must never be read
as product-owner approval. `test-only-fixture-issuer` identifies synthetic test
issuance, not an authenticated owner. Receipts and ledger events are unsigned.

For retained current-run evidence, `verify_current_evidence` derives state,
cause, and provider-call count from the terminal ledger event. The caller's
result object supplies only the run ID. It checks terminal event type and calls
the shared PEOS semantic validator before applying the fixture's additional
test-issuer and outcome checks. It accepts an optional
`expected_head_digest` supplied from an independently trusted source. Without it,
verification proves packet self-consistency only. The current synthetic fixture
always supplies a digest observed from the real runtime append result before
reopening the packet. A digest copied from the same packet or its summary does
not establish that trust; the fixture assumes a trusted verifier process.

Use the read-only inspection mode for an existing fixture packet:

```bash
python tests/decision-to-contract/validate_contract.py \
  --inspect-evidence-dir <packet-directory> --case positive
python tests/decision-to-contract/validate_contract.py \
  --inspect-evidence-dir <packet-directory> --case positive \
  --expected-head-digest "$PMOS_TRUSTED_HEAD"
```

Set `PMOS_TRUSTED_HEAD` from an independently controlled record of the original
runtime head. `--case broken-candidate` inspects the negative control. Inspection
does not invoke the provider, execute candidates, rewrite files, or trust
`summary.json`. It exits 0 for the verified fixture outcome, including the
expected negative control, and 3 for invalid evidence.

Fresh inspection output reports `head_anchor.status: NOT_PROVIDED` without an
expected head, or `VERIFIED` with the matching supplied digest. `VERIFIED` means
the digest matched; the reader must establish that its source is independent.
The saved fixture summary instead records
`head_check_at_capture: MATCHED_RUNTIME_HEAD`. That field describes the fixture's earlier check and
cannot assert an independent reader's trust. A consistently rewritten unsigned
packet can still pass without the original external head. Neither receipt
consistency nor head matching authenticates an owner or protects against a
malicious verifier process or root.

## 4. Recorded behavioural model-run evidence

Recorded behavioural evidence would consist of committed, reproducible model-run artifacts that identify the runtime/model, input, configuration, output, evaluation method, and result. No such evidence is currently committed in this repository.

Accordingly, this repository does not claim behavioural execution coverage, model-performance results, or independent runtime enforcement.

## Runtime scope

Claude Code is the currently validated host runtime. Other runtime portability is not certified. A skill's verification gates are instructions interpreted and enforced by the host agent; they are not an independent runtime or a guarantee that an agent will execute them.

## Pull-request quality gate

The required `PR Review Agent` check is deterministic and runs without model access or provider credentials. It re-runs the repository audit, checks whitespace, compiles every changed Python file through the repository audit's Python validation path, lints every `SKILL.md`, and rejects deletion of inventoried skills or reviewer personas and committed generated/runtime output. Model-based reviews are not a required merge check.
