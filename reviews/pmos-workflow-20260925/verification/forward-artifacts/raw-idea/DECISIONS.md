# Canonical product decisions

Product: Volunteer food pantry pickup app (descriptive working title; owner-selected product name OPEN)
Current PRD: [Draft r2](prds/2026-09-25-food-pantry-pickups.md)
Date: 2026-09-25
Status: Product intake OPEN; no product-definition or contract approval

## Sources

**SRC-001 — supplied product request, 2026-09-25**

> I want a lightweight app for our volunteer food pantry. Today coordinators juggle pickup requests in a group chat. Volunteers should claim a pickup, and the coordinator should see which requests still need someone. Please help turn this into the contract the engineering system will need.

The source is an owner's reported problem and requested behavior. No interviews, measured outcomes, observed software outputs, or accountable approval identity were supplied.

**SRC-002 — owner answer to Q-001, 2026-09-25**

> Collecting donated food from local grocery stores and bringing it to the pantry. A coordinator posts the store, pickup window and a short load description; volunteers claim a request. Continue from the draft you saved.

## Decisions

| ID | State | Owner wording and meaning retained | Source | Affected fields and requirements | Supersedes |
|---|---|---|---|---|---|
| DEC-001 | RESOLVED | “a lightweight app for our volunteer food pantry” — product context and qualitative design intent. “Lightweight” has no supplied measurable definition. | SRC-001 | problem; scope; non_functional_requirements (constraint unresolved, Q-013) | None |
| DEC-002 | RESOLVED | “Today coordinators juggle pickup requests in a group chat.” — reported problem and current alternative. | SRC-001 | problem; target_user (coordinator role known; priority OPEN) | None |
| DEC-003 | RESOLVED | “Volunteers should claim a pickup” — volunteer claim behavior is included. No assignment cardinality, eligibility rule, cancellation behavior, or conflict policy is implied. | SRC-001 | scope; functional_requirements FR-001; acceptance_criteria AC-001 (partial) | None |
| DEC-004 | RESOLVED | “the coordinator should see which requests still need someone” — coordinator visibility of uncovered requests is included. The exact definition of coverage is OPEN. | SRC-001 | scope; functional_requirements FR-002; acceptance_criteria AC-002 (partial) | None |
| DEC-005 | RESOLVED | “the contract the engineering system will need” — strict engineering intake is requested. This is neither product approval nor authorization to implement, deploy, or release. | SRC-001 | Required workflow: prd-first → accountable product approval → decision-to-contract → separate exact-digest approval | None |
| DEC-006 | RESOLVED | “Collecting donated food from local grocery stores and bringing it to the pantry.” — the pickup journey transports grocery-store donations to the pantry. Resolves Q-001. | SRC-002 | problem; scope; FR-001, FR-002, FR-003; AC-001, AC-002, AC-003 | None; elaborates existing pickup intent |
| DEC-007 | RESOLVED | “A coordinator posts the store, pickup window and a short load description; volunteers claim a request.” — coordinators post requests with these three pieces of information; volunteer claiming is reaffirmed. Resolves Q-008 for request origin and content. Validation, visibility, and edit rules remain OPEN. | SRC-002 | scope; FR-001, FR-003; AC-001, AC-003 | None |

RESOLVED means supplied intent is recorded, not that the current PRD is approved. These entries must not yet be represented as approved_product_decisions in a published contract.

## Open decision register

Open decisions and their dependencies are maintained under the stable Q IDs in the [current PRD](prds/2026-09-25-food-pantry-pickups.md#open-questions). Q-001 and Q-008 are RESOLVED by SRC-002. No decision is SUPERSEDED. [Draft r1](prds/2026-09-25-food-pantry-pickups-r1.md) is retained as history.

**Next question — Q-005:** What outcome would make the first version successful for the pantry: fewer missed pickups, less coordinator follow-up, or something else?

This answer identifies the outcome to measure and guides later scope and success criteria. The examples are options for the owner, not adopted product facts. Await this answer before choosing the next intake question; targets and a measurement rule remain undecided.

## Approval history

- Product definition r1: Draft; no approval requested or received.
- Product definition r2: Draft; incorporates SRC-002; no approval requested or received.
- Generated contract: none; no digest or receipt exists.
- Blocked transition: product approval and contract conversion cannot proceed while required owner decisions remain OPEN.
