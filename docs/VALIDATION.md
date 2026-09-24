# Validation and evidence

This repository makes three distinct kinds of claims. They must not be conflated.

## 1. Automated structural checks

`python3 tests/audit_repository.py` is an offline, deterministic repository audit. It validates that the inventory's skill, fixture, and reviewer-persona paths exist; that each inventoried skill has parseable YAML frontmatter; that its name is kebab-case; that it has a description and a `Limitations` section; that README-local Markdown links resolve; and that the inventory totals are 40 lifecycle skills, 3 supporting skills, and 7 reviewer personas.

The existing `tests/lint_skill.py` provides stricter per-skill static linting for SKILL.md files, including trigger-language and size checks. These checks inspect files; they do not run a model.

## 2. Fixture specifications

Each lifecycle skill has `tests/<skill>/fixtures.md`. These documents specify representative inputs, expected output properties, trigger examples, and often planted failures that a host agent's instructions are intended to catch.

Fixtures are **specifications**, not executed behavioural tests. Their presence demonstrates that expected behaviour has been documented; it does not demonstrate a model produced the expected output or followed a gate in a particular run.

## 3. Executable cross-repository compatibility

`tests/decision-to-contract/validate_contract.py --legacy-intake` preserves the original pinned publisher, receipt, loader, compiler, and legacy `assessment` admission smoke. It reproduces the historical health contract and receipt byte-for-value and rejects reused approval and prose-only criteria. That smoke does not establish current-run readiness.

The default entry point creates a separate, explicitly TEST-ONLY health-derived contract and test-issued receipt, then drives PEOS's current `run_to_release_ready`. The positive candidate must reach `RELEASE_READY` with verified, digest-bound release-gate evidence; a broken candidate must halt; a description-only gate must fail compilation before provider or execution. `test_handoff.py` independently observes those current-run calls and their evidence.

Pass `--evidence-dir <empty-directory>` to retain the synthetic input artifacts, ledgers, blobs, and result summary. Fixed fixture programs execute in local processes; this check does not test OS isolation, make an external model call, authorize a release, or establish live generation quality. Test-issued approval is never product-owner approval. Historical approved contracts, receipts, and task-store proof packets remain unchanged; unsupported process gates remain blocked by the current compiler.

## 4. Recorded behavioural model-run evidence

Recorded behavioural evidence would consist of committed, reproducible model-run artifacts that identify the runtime/model, input, configuration, output, evaluation method, and result. No such evidence is currently committed in this repository.

Accordingly, this repository does not claim behavioural execution coverage, model-performance results, or independent runtime enforcement.

## Runtime scope

Claude Code is the currently validated host runtime. Other runtime portability is not certified. A skill's verification gates are instructions interpreted and enforced by the host agent; they are not an independent runtime or a guarantee that an agent will execute them.

## Pull-request quality gate

The required `PR Review Agent` check is deterministic and runs without model access or provider credentials. It re-runs the repository audit, checks whitespace, compiles every changed Python file through the repository audit's Python validation path, lints every `SKILL.md`, and rejects deletion of inventoried skills or reviewer personas and committed generated/runtime output. Model-based reviews are not a required merge check.
