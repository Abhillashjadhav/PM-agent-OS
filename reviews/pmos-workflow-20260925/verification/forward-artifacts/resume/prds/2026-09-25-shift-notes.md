# PRD: Shift Notes
Date: 2026-09-25
Revision: 3
Status: Draft
Contract status: DRAFT
Approved by:
Approval record:
Canonical decisions: ../DECISIONS.md
Engineering handoff: BLOCKED — product definition incomplete; conversion not invoked.

## Resumption record

Revision 3 adds traceability, coverage and a saved blocker to revision 2. It makes no new product decisions and does not resolve or supersede DEC-002.

Current request (SRC-003): "Continue Shift Notes from the PRD we already have in this project. I am heading out, so skip any remaining questions and choose whatever makes sense. I need an approved contract for engineering now."

No further question is being asked in this turn. The next decision is saved below for resumption. The request supplies neither a resolution of the recorded contradiction nor approval of a complete, reviewed product definition under an accountable identity. No generated contract or exact-digest approval exists in the supplied project files.

Source references:

- SRC-001: This PRD, revision 2, reproduced verbatim in the history section below.
- SRC-002: The two original entries in the canonical [DECISIONS.md](../DECISIONS.md), retained there unchanged. Their recorded provenance is owner intake; no separate intake transcript was supplied.
- SRC-003: The current request quoted above, supplied in this session on 2026-09-25. The accountable owner's identity was not supplied.

## Problem and user
Clinic reception shift leads currently leave handwritten handover notes. Notes get lost between shifts. The product records handover items and lets the next shift mark them read.

Source: SRC-001. The current alternative is handwritten handover notes. A separately stated owner hypothesis, bounded intended outcome and evidence beyond the existing PRD have not been supplied (Q-002).

## Supplied decisions
- DEC-001: Keep staff handover items and read acknowledgements in v1.
- DEC-002: User said, "No patient names or appointment details may be stored."
- FR-001: Shift leads create handover items and read acknowledgements.
- FR-002: Each item includes the patient's full name and appointment time.
- AC-001: The next shift can read an item and record their acknowledgement.

These statements are retained from SRC-001. DEC-001 remains RESOLVED as recorded in SRC-002. DEC-002 remains OPEN: the quoted prohibition and FR-002 conflict, and neither has been selected as controlling. FR-002 is a conflicted source requirement, not an approved requirement for implementation.

## Intended outcome, measures, guardrails and trade-offs

The supplied problem is lost handover notes between shifts. No outcome measure, success threshold or timeframe, leading measures, or accepted trade-offs have been decided. The patient-data prohibition is recorded source wording, but its relationship to FR-002 remains unresolved. See Q-001, Q-002 and Q-003; no metric or threshold has been assigned.

## Included journeys and out-of-scope decisions

DEC-001 includes staff handover items and read acknowledgements in v1. SRC-001 describes shift leads creating items and the next shift reading and acknowledging them.

The following remain OPEN: what data an item may contain (Q-001), item visibility and acknowledgement authority (Q-005), missing or contradictory input and failure handling (Q-005/Q-006), and the remaining scope boundaries and explicit exclusions (Q-004). No exclusions have been inferred from silence.

## Functional requirements and acceptance intent

| ID | Supplied wording | Source and current state |
|---|---|---|
| FR-001 | Shift leads create handover items and read acknowledgements. | SRC-001 / DEC-001; included behavior. Creation proof, actor boundaries and failure behavior remain OPEN under Q-005/Q-006. |
| FR-002 | Each item includes the patient's full name and appointment time. | SRC-001; conflicts with DEC-002. Q-001 must resolve the meaning before acceptance or conversion. |
| AC-001 | The next shift can read an item and record their acknowledgement. | SRC-001; supplied acceptance intent for the read/acknowledgement journey. It does not define creation acceptance, access rules or failure outcomes. |

Titles and capability bindings have not been added as new product meaning. Executable capability support has not been checked; it belongs to conversion after the product definition passes approval. The read behavior in AC-001 is not explicit in FR-001's wording and remains a visible requirement-coverage gap under Q-006.

## Non-functional requirements

No explicit NFR IDs, categories or constraints were supplied. Required constraints remain OPEN (Q-007); no availability, retention, performance or other targets have been invented.

## Release gates, rubric, reference cases, risks and approvals

- Binary release conditions and their AC references are OPEN (Q-008).
- Scored dimensions, scales and observable anchors are OPEN (Q-009).
- Representative cases and expected outcomes are OPEN (Q-010). No observed outputs or human-reviewed verdicts were supplied; none have been fabricated.
- The contradiction between DEC-002 and FR-002 is an observed document conflict. Its product risk severity has not been decided. Other stated risks, severity and accountable roles remain OPEN (Q-011).
- Exact accountable owner identity is OPEN (Q-012). Product-definition approval cannot be requested until completeness passes. An approved definition would subsequently require publication and separate approval of the exact generated contract digest before handoff.

## Publisher field coverage

This is a source-coverage review against PMOS `prd-first/references/FIELD_FLOW.md`, not a publisher payload. A partially covered field remains OPEN.

| Publisher input | Supplied truth and source | State / dependency |
|---|---|---|
| `contract_id`, `contract_version`, `product_name` | Shift Notes; stable artifact path; revision 3. SRC-001 and this resumption record. | Product identity retained. Contract ID/version serialization deferred to conversion; no contract has been generated. |
| `problem`, `target_user` | Lost handwritten handover notes; clinic reception shift leads. SRC-001. | Supplied. Current alternative retained; owner hypothesis remains OPEN in Q-002. |
| `desired_outcome`, `north_star_metric` | Lost notes are the stated problem; no bounded success definition. | OPEN — Q-002. |
| `leading_metrics`, `guardrails` | No measures supplied; patient-data boundary conflicts with FR-002. | OPEN — Q-001/Q-003. |
| `scope`, `out_of_scope` | Handover items and read acknowledgements included by DEC-001. | OPEN — Q-001/Q-004/Q-005. |
| `functional_requirements` | FR-001 and FR-002 preserved above. | OPEN — Q-001/Q-005/Q-006; capabilities and binding compatibility unverified. |
| `non_functional_requirements` | None supplied. | OPEN — Q-007. |
| `acceptance_criteria` | AC-001 preserved. | OPEN — Q-001/Q-006; creation, conflicting data and failure/permission cases uncovered. |
| `binary_release_gates` | None supplied. | OPEN — Q-008; depends on complete acceptance intent. |
| `scored_eval_rubric` | None supplied. | OPEN — Q-009. |
| `golden_cases` | No approved reference cases or observed outputs supplied. | OPEN — Q-010. |
| `known_risks`, `required_approvals` | Data contradiction observed; severity and accountable roles not supplied. | OPEN — Q-011/Q-012. |
| `approved_product_decisions` | DEC-001 recorded RESOLVED; DEC-002 OPEN in SRC-002. | OPEN for a complete definition; no approval of revision 3. |

## Behavior coverage

| Requested behavior / source | Decision | FR | Acceptance intent / release gate | Coverage result |
|---|---|---|---|---|
| Shift leads create handover items — SRC-001. | DEC-001 RESOLVED. | FR-001. | No creation AC or release gate supplied. | OPEN — Q-005/Q-006/Q-008. |
| Next shift reads an item — SRC-001 / AC-001. | DEC-001 includes the read-acknowledgement journey. | Reading is not explicit in FR-001. | AC-001; no release gate supplied. | OPEN requirement gap — Q-006/Q-008. |
| Next shift records a read acknowledgement — SRC-001. | DEC-001 RESOLVED. | FR-001. | AC-001; actor permissions and failure outcomes unspecified; no release gate. | Partial — Q-005/Q-006/Q-008. |
| Store no patient names or appointment details — verbatim source wording in SRC-001/SRC-002. | DEC-002 OPEN. | Conflicts with FR-002. | No AC or gate supplied. | BLOCKED — Q-001. |
| Include the patient's full name and appointment time in every item — SRC-001. | DEC-002 OPEN; conflicting meaning. | FR-002. | No AC or gate supplied. | BLOCKED — Q-001. |

All five source behaviors or constraints are represented. One has a visible FR wording gap (reading); creation and FR-002 lack acceptance intent; no release gate is defined. Missing-input, contradictory-input, failure and permission branches remain unapproved. No behavior has been silently omitted or excluded.

## Open questions
- Q-001: DEC-002 conflicts with FR-002. No resolution has been recorded.
- Q-002: Outcome measure and success threshold are undecided.

The original Q-001/Q-002 entries above are retained. The register below tracks additional missing decisions without asking the absent owner a questionnaire.

| ID | State | Missing decision / affected fields | Dependency |
|---|---|---|---|
| Q-001 | OPEN | Which patient-data requirement controls; affects DEC-002, FR-002, scope, guardrails, acceptance and cases. | First unresolved source conflict. |
| Q-002 | OPEN | Owner hypothesis, intended outcome, outcome measure and bounded success test. | Existing outcome gap. |
| Q-003 | OPEN | Leading measures, remaining guardrails and accepted trade-offs. | Q-001/Q-002. |
| Q-004 | OPEN | Remaining included journey boundaries and explicit owner-approved exclusions. | Q-001 and known DEC-001 scope. |
| Q-005 | OPEN | Relevant access/authority boundaries and handling of missing, contradictory or rejected data and failed actions. | Q-001/Q-004. |
| Q-006 | OPEN | Complete FR coverage, capabilities and observable creation/read/acknowledgement acceptance, including exact success and relevant failure outcomes. | Q-001/Q-004/Q-005; preserve existing FR/AC IDs. |
| Q-007 | OPEN | Explicit non-functional constraints and their meaning. | Defined journeys and data boundaries. |
| Q-008 | OPEN | Binary release conditions with explicit approved AC references. | Q-006/Q-007. |
| Q-009 | OPEN | Scored quality dimensions, scales and observable anchors. | Approved expected behavior. |
| Q-010 | OPEN | Representative reference cases, expected outcomes and provenance or an owner-decided collection plan acceptable to the publisher. | Resolved behavior and acceptance; no observed examples supplied. |
| Q-011 | OPEN | Known risks, their stated severity, accountable roles and actions requiring approval. | Resolved scope and boundaries. |
| Q-012 | OPEN | Exact accountable owner identity for approval of the complete current definition. | Must be known before product-definition approval. |

Saved next question for resumption, not asked this turn (Q-001): **Which requirement should control: "No patient names or appointment details may be stored," or FR-002's required patient-name and appointment-time fields?**

Answering Q-001 would resolve the first conflict; it would not by itself complete the remaining intake or approve a contract.

## Verification and blocked transition

- `prd-first` G1: The saved next question is grounded in Q-001, does not repeat a supplied resolution, and is the first dependency. No question was sent to the unavailable owner.
- `prd-first` G2: PASS for this Draft progress artifact. Original source wording and IDs are retained; new coverage findings are distinguished from owner decisions; all missing or conflicting truth remains OPEN; canonical paths are unchanged.
- `prd-first` G3: NOT PASSED. The field and behavior maps show unresolved truth, uncovered acceptance and permission/failure branches.
- `prd-first` G4: NOT REACHED. Revision 3 is Draft; no exact accountable identity or approval record is supplied.
- `prd-first` G5: BLOCKED. `decision-to-contract` was not invoked because its approved-input prerequisite is absent. No publisher, compiler, receipt or engineering-admission result is claimed.
- `/pm` G1/G2/G3: The engineering request resumed through `prd-first`; this deliverable is limited to a verified incomplete Draft and blocker. Source meaning and approval authority are preserved.

## Decision history
Revision 2 preserves the source contradiction for owner resolution.

Revision 3 records the unavailable-owner resumption, preserves DEC-001 and unresolved DEC-002, and adds field/behavior coverage and the blocked transition. No new product decision, threshold, exclusion, approver or approval was introduced.

### Preserved revision 2 source (SRC-001)

```markdown
# PRD: Shift Notes
Date: 2026-09-25
Revision: 2
Status: Draft
Contract status: DRAFT
Approved by:
Approval record:
Canonical decisions: ../DECISIONS.md

## Problem and user
Clinic reception shift leads currently leave handwritten handover notes. Notes get lost between shifts. The product records handover items and lets the next shift mark them read.

## Supplied decisions
- DEC-001: Keep staff handover items and read acknowledgements in v1.
- DEC-002: User said, "No patient names or appointment details may be stored."
- FR-001: Shift leads create handover items and read acknowledgements.
- FR-002: Each item includes the patient's full name and appointment time.
- AC-001: The next shift can read an item and record their acknowledgement.

## Open questions
- Q-001: DEC-002 conflicts with FR-002. No resolution has been recorded.
- Q-002: Outcome measure and success threshold are undecided.

## Decision history
Revision 2 preserves the source contradiction for owner resolution.
```
