# Shift Notes decisions

- DEC-001 RESOLVED: Staff handover items and read acknowledgements are included. Source: owner intake.
- DEC-002 OPEN: "No patient names or appointment details may be stored" conflicts with FR-002's patient-name and appointment-time fields. The owner has not decided which controls.

## Canonical artifact and provenance

Current PRD: [Shift Notes, revision 3](prds/2026-09-25-shift-notes.md). This root file remains the canonical decision log.

The two entries above are retained unchanged from the supplied decision log. The original owner intake transcript was not supplied separately. The PRD retains a verbatim revision 2 snapshot as SRC-001; its SRC-002 points to these original entries. Neither entry has been superseded.

| Decision | State | Preserved owner/source wording | Affected fields and behavior | Supersedes |
|---|---|---|---|---|
| DEC-001 | RESOLVED | PRD revision 2: "Keep staff handover items and read acknowledgements in v1." Original log source: owner intake. | Scope; FR-001; AC-001. Detailed acceptance and authority remain OPEN. | None recorded. |
| DEC-002 | OPEN | PRD revision 2: "No patient names or appointment details may be stored." Conflicting FR-002: "Each item includes the patient's full name and appointment time." | Scope, data boundary, guardrails, FR-002, acceptance, reference cases and product approval. | None; no controlling meaning chosen. |

## Resumption — 2026-09-25

Current request, preserved verbatim as SRC-003 in the PRD:

> Continue Shift Notes from the PRD we already have in this project. I am heading out, so skip any remaining questions and choose whatever makes sense. I need an approved contract for engineering now.

No follow-up question was asked. The request was recorded as workflow direction, not as a new product decision or accountable approval of a complete revision. No substantive default was selected to resolve DEC-002. No ordinary-prototype waiver was inferred from this engineering request.

Q-001 and Q-002 remain OPEN. The PRD's Q-003–Q-012 enumerate additional missing field and behavior decisions, with source coverage and dependencies. No new RESOLVED decision was added.

Saved next question (Q-001), not asked this turn: **Which requirement should control: "No patient names or appointment details may be stored," or FR-002's required patient-name and appointment-time fields?**

## Approval and handoff record

- Current product-definition status: Draft, revision 3; contract status DRAFT.
- Exact accountable owner identity: OPEN (Q-012).
- Product-definition approval: absent. Completeness has not passed; no approval request is ready.
- Engineering handoff: BLOCKED. `decision-to-contract` was not invoked.
- Generated contract, exact-digest approval and verified receipt: absent.
- Resumption order: resolve Q-001; continue the remaining dependency-ordered OPEN decisions; verify completeness; obtain accountable approval of the current complete revision; only then convert and obtain the separate exact-digest approval.

Revision 3 preserves the existing product meaning and adds reviewable coverage and blockers. It is not approved for engineering.
