# Validation and evidence

This repository makes three distinct kinds of claims. They must not be conflated.

## 1. Automated structural checks

`python3 tests/audit_repository.py` is an offline, deterministic repository audit. It validates that the inventory's skill, fixture, and reviewer-persona paths exist; that each inventoried skill has parseable YAML frontmatter; that its name is kebab-case; that it has a description and a `Limitations` section; that README-local Markdown links resolve; and that the inventory totals are 40 lifecycle skills, 3 supporting skills, and 7 reviewer personas.

The existing `tests/lint_skill.py` provides stricter per-skill static linting for SKILL.md files, including trigger-language and size checks. These checks inspect files; they do not run a model.

## 2. Fixture specifications

Each lifecycle skill has `tests/<skill>/fixtures.md`. These documents specify representative inputs, expected output properties, trigger examples, and often planted failures that a host agent's instructions are intended to catch.

Fixtures are **specifications**, not executed behavioural tests. Their presence demonstrates that expected behaviour has been documented; it does not demonstrate a model produced the expected output or followed a gate in a particular run.

## 3. Executable cross-repository compatibility

The `repository-audit` CI job installs PEOS `5c0f9e3a8f2c66b212c5e1adfb373e4fd2681bf9` and runs `tests/decision-to-contract/validate_contract.py`. It deterministically reproduces a **historical** approved health contract and receipt, verifies them, compiles that contract, starts a receipt-bound engineering run at `assessment`, and rejects a prose-only planted failure with `CRITERION_FORM_INVALID`.

The separate `current-authoring` CI job installs the [documented handoff pin](HANDOFF.md), PEOS `297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6`, checks its installation provenance, and runs `test_current_authoring.py` against a distinct TEST-ONLY health contract with an explicit `GATE-001` binding. Its synthetic receipt verifies, the real current compiler accepts the contract, and receipt-bound admission starts at `assessment`. The same compiler correctly rejects the historical contract's unbound required gate with `RELEASE_GATE_UNBOUND`.

These are two bounded, revision-specific compatibility results, not one interchangeable admission proof. The documented pin is unmerged; selecting a supported release baseline remains open. Neither job proves live-model authoring quality, arbitrary-product coverage, a candidate run, or real-provider engineering.

## 4. Recorded behavioural model-run evidence

The [2026-09-25 verification packet](../reviews/pmos-workflow-20260925/verification/README.md) records five designed fresh-agent scenarios across six turns against a bounded assembled PMOS snapshot. Its [run record](../reviews/pmos-workflow-20260925/verification/forward-runs.json) and [artifact index](../reviews/pmos-workflow-20260925/verification/forward-artifacts/manifest.json) retain the tasks, normalized responses or marked excerpts, observations, source versions, and output hashes. These were fictional ChatGPT Work in-session rehearsals, not native Claude Code sessions or real product approvals.

Exact model-build, sampling, and token metadata were unavailable, and the packet has no reliability estimate or baseline comparison. It is evidence for those five narrow observations, not behavioural coverage of the full catalogue, model-performance results, end-to-end product delivery, or independent runtime enforcement.

## Runtime scope

Claude Code is the intended host runtime. Mechanical installation and offline checks have been validated, but the recorded rehearsals do not establish native Claude behaviour. Other runtime portability is not certified. A skill's verification gates are instructions interpreted and enforced by the host agent; they are not an independent runtime or a guarantee that an agent will execute them.

## Pull-request quality gate

The required `PR Review Agent` check is deterministic and runs without model access or provider credentials. It re-runs the repository audit, checks whitespace, compiles every changed Python file through the repository audit's Python validation path, lints every `SKILL.md`, and rejects deletion of inventoried skills or reviewer personas and committed generated/runtime output. Model-based reviews are not a required merge check.
