# Owner truth to publisher fields

Read this reference during engineering intake and before requesting product
approval. This is an elicitation/coverage map for the existing publisher, not a
second schema, compiler or runtime. Exact serialization and supported executable
bindings belong to `decision-to-contract` and the already pinned interface.

For each row, retain supplied evidence or an explicit owner decision. Otherwise
record a stable OPEN question and its dependency; required OPEN truth blocks
product approval and publication. Do not impose example numbers or an arbitrary
number of exclusions. Syntactic IDs may be assigned consistently by PMOS; they do
not authorize the meaning attached to them.

| Dependency | Owner truth and next missing decision | Existing publisher input |
|---|---|---|
| 1. Identity | Product name and persistent artifact identity; reuse IDs, advance revision without changing meaning silently | `contract_id`, `contract_version`, `product_name` |
| 2. Problem/user | Pain, affected primary user, current alternative; distinguish the owner's hypothesis from evidence | `problem`, `target_user`; preserve alternative/hypothesis as approved decision context |
| 3. Outcome | Outcome the product should produce, how to observe it, success threshold/timeframe or an explicit bounded binary test | `desired_outcome`, `north_star_metric` |
| 4. Measures | Customer actions/process signals expected to precede the outcome and what must not worsen | `leading_metrics`, `guardrails` |
| 5. Scope | Included journeys and explicit exclusions, including relevant data access, permissions and failure handling | `scope`, `out_of_scope` |
| 6. Requirements | Each included behavior, stable FR ID, title, description and capability; each quality constraint with NFR ID/category/requirement | `functional_requirements`, `non_functional_requirements` |
| 7. Acceptance | Observable proof for each FR, success and relevant failure cases, exact expected outcomes; never infer executable semantics from vague prose | `acceptance_criteria` |
| 8. Gates | Which explicit ACs determine each binary release condition; record stable gate ID, owner-approved description and explicit `acceptance_criterion_refs` | `binary_release_gates` |
| 9. Quality | Scored dimensions and scale, with observable anchors from owner intent; optional evaluator design must not change approved product thresholds | `scored_eval_rubric` |
| 10. Cases | Owner-approved representative cases and expected outcomes with their provenance; distinguish designed references from observed, human-reviewed goldens | `golden_cases` |
| 11. Risk/authority | Known risks and their stated severity, accountable roles and actions requiring approval | `known_risks`, `required_approvals` |
| 12. Decisions | Explicit decisions, trade-offs and exclusions that support the preceding rows; preserve IDs/source references and superseded history | `approved_product_decisions` |

The source PRD's approval identity/revision is recorded separately. Do not
prepopulate the publisher's approval fields or manufacture a receipt. Product
approval authorizes conversion; the exact generated digest needs separate approval.

## Conditional specialist routes

Read the named skill's own input requirements and verification gates before use.
A missing specialist input becomes one relevant owner question, never a fabricated
input. Only gated output can enter the PRD as a proposal; the owner decides meaning.

| Actual gap | Existing skill | Boundary |
|---|---|---|
| Outcome confused with activity or unclear measurement | `north-star-designer` | Keep adoption/usage as leading measures where appropriate; do not choose an owner target |
| Requirement lacks observable acceptance | `prd-to-eval` | Work from the user's requirement; output is proposed evaluation intent, not proof that software passed |
| Rubric/disqualifiers still need design | `eval-engine` | Use only when this extra work is missing; do not turn a draft rubric into observed results |
| A described journey lacks failure policy | `guardrail-designer` | Label class risks versus actual incidents; owner chooses thresholds, authority and trade-offs |
| Real reviewed outputs exist and need curation | `golden-dataset-builder` | Requires actual output plus human verdict and verbatim reason; missing labels stay quarantined |

For a new product with no observed outputs, do not invoke golden-dataset-builder
as a generation step. Ask the owner to define representative expected cases or a
collection plan. Designed examples may be proposed for approval with their origin
stated; they are not human-reviewed observations. If the required `golden_cases`
value remains undecided or its form is unsupported, leave it OPEN/BLOCKED rather
than inventing a label or silently omitting the field.

## Coverage and engineering compatibility

Before product approval, compare original requested behavior with the coverage
map, not just the FR list. For every included journey, inspect its observable
success and relevant missing/conflicting-input, failure, permission and side-effect
branches. Record explicit owner exclusions rather than assuming those branches
are out of scope. Every FR needs acceptance intent; every acceptance reference and
gate reference must identify existing approved IDs.

Select executable forms only through the existing `decision-to-contract` workflow:
registered action/typed paths, registered measure, supplied trusted test, or supplied
template proof. Do not invent path/operator/value/test semantics, manufacture files,
claim unverified bundle support, or replace the owner's product with a health demo.
A missing owner expectation returns to intake; an unavailable supported binding
is a BLOCKED engineering dependency. A new product decision requires renewed
product approval; a new published contract requires renewed exact-digest approval.
