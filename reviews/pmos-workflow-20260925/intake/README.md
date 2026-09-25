# Intake implementation evidence

Scope: accepted conversational intake changes in `/pm` and `prd-first`.
Base: `bee295cacd882f8a7fb4a5c306f2774b0cd3919a`.

## Change order

1. `daaac162c9de1756df7464e27703d459f5d14849`: expand the fixture specifications
   and record the unit BAR before modifying either skill.
2. `2bbde05529610752ad79c57cba8528d8c9110c00`: implement intake instructions and
   the bundled publisher-field reference.
   Source tree: `99a0bffb739f4653af806bc1a6fe43a64f8e6c66`.

## Reproduced source contradictions and corresponding fixtures

These are source comparisons, not executed conversational RED/GREEN claims.

| Previous instruction | Required fixture behavior | Implemented boundary |
|---|---|---|
| Five questions, one follow-up, then move on | F02 retains unresolved conflict after that count | Completion uses requested-behavior and required-field coverage |
| Existing PRD excludes the skill | F03 resumes a saved Draft | Description and intake load/resume existing Drafts |
| Skip, vague Draft or autonomous description can proceed | F04 blocks engineering; F05 isolates an explicitly waived prototype | OPEN decisions and accountable approval cannot be bypassed for handoff |
| Only already-written FR/AC items are checked | F07 identifies omitted requested rescheduling behavior | Coverage begins with original requested behavior |
| Template lacks the full publisher truth map | F06/F10 require fields or bounded OPEN questions | Bundled reference maps all 20 existing publisher-input fields |
| Product artifact location and log history are ambiguous | F09 preserves target-project truth and conflicting history | Target `prds/`, root `DECISIONS.md`, legacy references and OPEN contradictions |

The reference routes only missing metric/evaluation/failure work to existing
skills. It distinguishes owner-designed examples from actual human-reviewed
goldens, and product approval from generated-contract digest approval. Unsupported
bindings remain engineering dependencies; no health-demo substitution is allowed.

## Checks actually run

- Both changed skills passed `tests/lint_skill.py` before and after the change.
- `python3 -B tests/audit_repository.py`: PASS, 40 lifecycle skills, 3 supporting
  skills and 7 reviewer personas.
- `python3 -B tests/pr_quality_gate.py --base-ref bee295cacd882f8a7fb4a5c306f2774b0cd3919a`:
  PASS, including lint of all skill files and the changed-file checks.
- Static inventory comparison against the existing `decision-to-contract` JSON
  example: all 20 publisher-input keys are named in the field reference; no missing
  key. This tests reference completeness only, not semantic mapping by a model.
- Bundled reference links resolve; `git diff --check` passes.

## Still unverified

No supervised raw-idea conversation, native Claude execution, or fresh product
delivery ran. The 12 `prd-first` conversations and expanded `/pm` examples are
fixture specifications. They must be evaluated against actual future model
outputs before claiming behavioral reliability. Static checks do not enforce
approval or prove that an agent asks every relevant question.

No new runtime, dependency, paid call, publisher implementation, PEOS source edit,
installer/CI change, frozen-artifact change, or screened probe is part of this
unit. Independent review, integration and GitHub publication belong to the root
coordinator.
