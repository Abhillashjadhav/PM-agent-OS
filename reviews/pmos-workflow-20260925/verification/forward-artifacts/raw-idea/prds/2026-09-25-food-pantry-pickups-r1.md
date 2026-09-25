# PRD: Volunteer food pantry pickup app

Date: 2026-09-25
Revision: r1
Status: Draft
Contract status: DRAFT
Approved by:
Approval record:
Canonical decisions: [root DECISIONS.md](../DECISIONS.md)

The title is a descriptive working title, not an owner-selected product name. This is an incomplete product definition, not an executable contract. Source: SRC-001 in the canonical decision log. No code, publisher output, test result, approval, or engineering receipt is represented by this document.

## Problem, user, current alternative and hypothesis

- **Reported problem and alternative:** “Today coordinators juggle pickup requests in a group chat.” [DEC-002]
- **Product context:** A volunteer food pantry wants a “lightweight app.” [DEC-001]
- **Included actors:** Volunteers claim a pickup; coordinators see which requests still need someone. Their relative priority and other roles are OPEN. [DEC-003, DEC-004; Q-004]
- **Requested approach:** Bring claiming and coordinator visibility into the app. This is intended behavior, not evidence that the approach improves pickup outcomes. [DEC-003, DEC-004]
- **Unresolved domain meaning:** What is being picked up, from whom, and for whom has not been supplied. [Q-001]

## Intended outcome, North Star, leading metrics, guardrails and trade-offs

The supplied intent is to let volunteers claim pickups and coordinators identify requests needing someone. No business outcome target, success timeframe, measurement rule, leading measure, guardrail, or agreed trade-off was supplied. [Q-005–Q-007]

No arbitrary completion rate, response-time target, or usage metric is adopted.

## Included journeys and out-of-scope decisions

| Journey | Known intent | Missing decisions |
|---|---|---|
| Volunteer claims a pickup | A volunteer can claim a pickup. [DEC-003] | Meaning of pickup; how requests enter the app; request information; eligible volunteers; claim result; whether multiple volunteers are needed; conflicting claims; changes after claiming. [Q-001, Q-008–Q-011] |
| Coordinator finds requests needing someone | A coordinator can see which requests still need someone. [DEC-004] | Meaning of sufficient coverage; data visibility; how changes appear; handling unavailable or stale information. [Q-009–Q-011] |

The request lifecycle that feeds these journeys is required intake work, not yet a decision that coordinators create requests. No owner-approved exclusions exist. [Q-008, Q-012]

## Functional requirements — FR IDs, observable behavior and capability

| ID | Requirement | Supplied behavior | Capability | State and source |
|---|---|---|---|---|
| FR-001 | Claim a pickup | Volunteers should be able to claim a pickup. | Product capability: pickup claiming. Executable binding has not been selected or verified. | Included intent; operational semantics OPEN. DEC-003 / SRC-001 |
| FR-002 | See requests needing coverage | The coordinator should see which requests still need someone. | Product capability: visibility of uncovered pickup requests. Executable binding has not been selected or verified. | Included intent; coverage definition and presentation behavior OPEN. DEC-004 / SRC-001 |

Additional requirements will be added only from resolved owner decisions, without renumbering these IDs.

## Acceptance intent — AC IDs, requirement references and owner-approved proof

| ID | FR | Grounded acceptance intent | Proof status |
|---|---|---|---|
| AC-001 | FR-001 | A volunteer can claim a pickup. | Partial intent only. Eligibility, preconditions, resulting state, visible confirmation, conflicting claims, and failure outcomes remain OPEN. [Q-009–Q-011, Q-014] |
| AC-002 | FR-002 | The coordinator can identify requests that still need someone. | Partial intent only. Coverage rule, visible result, update behavior, and failure outcomes remain OPEN. [Q-009–Q-011, Q-014] |

These are not executable acceptance criteria or owner-approved test cases. No software has been tested.

## Non-functional requirements — NFR IDs and explicit constraints

“Lightweight” is supplied qualitative intent. Its implications for device support, ease of use, installation, operating burden, or measurable constraints are undecided. [DEC-001; Q-013]

No NFR is asserted as an agreed constraint. Stable NFR IDs will be added when constraints are supplied or decided.

## Release gates, rubric, reference cases, risks and required approvals

- **Binary release gates:** OPEN; no gate descriptions or approved AC references exist. [Q-015]
- **Scored evaluation rubric:** OPEN; no agreed dimensions, scale, or observable anchors exist. [Q-016]
- **Reference cases:** OPEN; no owner-approved representative cases have been supplied. Any future proposed examples must be labeled designed, not observed or human-reviewed. [Q-017]
- **Risks:** Risk decisions and severity are OPEN. Simultaneous claims and exposure of request details are workflow questions to examine, not reported incidents or accepted severity ratings. [Q-010, Q-011, Q-018]
- **Required product actions/approvals:** Accountable roles and actions requiring approval are OPEN. [Q-019]
- **Product-definition approval:** Owner identity and explicit approval of a complete current revision are still required. Do not request approval of this incomplete revision. [Q-020]
- **Contract approval:** Only after product approval may decision-to-contract validate supported bindings and publish a Draft contract for separate exact-digest approval. No contract has been generated.

## Publisher field coverage — field, source/decision, state and OPEN question

This is an elicitation map from prd-first/references/FIELD_FLOW.md, not publisher JSON. OPEN required fields prevent product approval and conversion.

| Field | Source or decision | State | Remaining dependency |
|---|---|---|---|
| contract_id, contract_version | Stable local PRD path and r1 established; no published contract identity | OPEN | Persistent contract identity and product name. Q-002 |
| product_name | Descriptive working title only | OPEN | Owner-selected name. Q-002 |
| problem | SRC-001 / DEC-001, DEC-002 | PARTIAL | Pickup domain and scope of the reported coordination problem. Q-001 |
| target_user | SRC-001 / DEC-003, DEC-004 | PARTIAL | Actor priority and roles. Q-004 |
| desired_outcome | SRC-001 / DEC-003, DEC-004 provide intended behavior | OPEN | Outcome to achieve. Q-005 |
| north_star_metric | No supplied evidence | OPEN | Observable target/timeframe or bounded binary test. Q-005 |
| leading_metrics | No supplied evidence | OPEN | Relevant leading measures. Q-006 |
| guardrails | No supplied evidence | OPEN | What must not worsen and trade-offs. Q-007 |
| scope | SRC-001 / DEC-003, DEC-004 | PARTIAL | Journey meaning, request lifecycle, claim and visibility rules. Q-001, Q-008–Q-011 |
| out_of_scope | No approved exclusions | OPEN | Explicit boundaries. Q-012 |
| functional_requirements | FR-001, FR-002 | PARTIAL | Operational behavior and remaining lifecycle requirements. Q-008–Q-011 |
| non_functional_requirements | “lightweight,” DEC-001 | OPEN | Explicit constraints. Q-013 |
| acceptance_criteria | AC-001, AC-002 | PARTIAL | Exact success, failure, and permission outcomes. Q-014, dependent on Q-008–Q-011 |
| binary_release_gates | No supplied evidence | OPEN | Gate meaning and AC references. Q-015 |
| scored_eval_rubric | No supplied evidence | OPEN | Dimensions, scale, and anchors. Q-016 |
| golden_cases | No observed or designed approved cases | OPEN | Representative cases or permitted collection plan; supported form must be checked later. Q-017 |
| known_risks | No risk assessment supplied | OPEN | Risks and severity. Q-018 |
| required_approvals | No accountable authority supplied | OPEN | Roles and approval-requiring actions. Q-019 |
| approved_product_decisions | DEC-001–DEC-005 preserve supplied intent; current product definition is unapproved | OPEN | Complete definition and accountable revision approval. Q-020, dependent on all required truth |

Source-PRD approval identity and revision are separate from publisher approval fields; neither has been prepopulated.

## Behavior coverage — requested behavior, decision, FR, AC/gate or exclusion

| Source request | Decision | FR or constraint | AC / gate / exclusion | Coverage state |
|---|---|---|---|---|
| “a lightweight app for our volunteer food pantry” | DEC-001 | Product context preserved; explicit NFR undecided | Q-013 | Partial; no invented definition of lightweight |
| “Today coordinators juggle pickup requests in a group chat” | DEC-002 | Problem and current alternative retained | Q-001, Q-005 | Recorded problem; not treated as a request for chat integration |
| “Volunteers should claim a pickup” | DEC-003 | FR-001 | AC-001 partial; gate OPEN | Included; success details and failure/permission branches OPEN |
| “the coordinator should see which requests still need someone” | DEC-004 | FR-002 | AC-002 partial; gate OPEN | Included; coverage rule and failure/permission branches OPEN |
| “the contract the engineering system will need” | DEC-005 | Engineering handoff workflow | Complete definition → accountable approval → publisher checks → exact-digest approval and receipt | Conversion has not begun |

Coverage check: 2 of 2 requested app behaviors are represented by FRs and partial acceptance intent; 0 requested app behaviors are omitted; 0 FRs lack an acceptance-intent row. Both FRs still lack complete acceptance coverage. No exclusions are approved and no release gate is claimed to pass.

## Open questions — Q ID, dependency, affected fields, next question

All entries are **OPEN**. The register is a coverage inventory, not a fixed interview or a list to ask at once. Supplied answers may resolve multiple entries. Select one question at a time after rechecking dependencies.

| ID | Decision needed | Dependency / affected fields |
|---|---|---|
| Q-001 | Meaning of a pickup in this pantry's workflow | First substantive dependency; problem, scope, FR-001, FR-002, AC-001, AC-002 |
| Q-002 | Product name and persistent contract identity | Identity; contract_id, contract_version, product_name |
| Q-004 | Primary user priority and any additional actors | Pickup domain; target_user |
| Q-005 | Desired outcome and observable success target/timeframe or bounded binary test | Domain and users; desired_outcome, north_star_metric |
| Q-006 | Leading measures that precede the outcome | Q-005; leading_metrics |
| Q-007 | Guardrails and outcome trade-offs | Q-005; guardrails |
| Q-008 | How a request enters the app and which information it contains | Q-001; scope, functional_requirements, acceptance_criteria |
| Q-009 | Claim meaning, sufficiency of coverage, and allowed changes through the pickup lifecycle | Q-001, Q-008; FR-001, FR-002, AC-001, AC-002 |
| Q-010 | Who may view or change request details and claims, and how role authority is established | Q-004, Q-008, Q-009; scope, requirements, permission acceptance |
| Q-011 | Expected behavior for relevant missing information, conflicting claims, rejected changes, and unavailable/stale state | Q-008–Q-010; requirements and failure acceptance |
| Q-012 | Explicit exclusions from the agreed journeys | Domain and included behavior; out_of_scope |
| Q-013 | Concrete meaning of lightweight and any other explicit quality constraints | Agreed journeys; non_functional_requirements |
| Q-014 | Exact observable outcomes and proof for each included behavior | Q-008–Q-011; acceptance_criteria |
| Q-015 | Binary release conditions and their AC references | Q-014; binary_release_gates |
| Q-016 | Scored quality dimensions, scale, and observable anchors | Behavior and constraints; scored_eval_rubric |
| Q-017 | Representative expected cases and provenance | Agreed behavior; golden_cases; publisher compatibility later |
| Q-018 | Known risks and stated severity | Journey boundaries and constraints; known_risks |
| Q-019 | Accountable roles and actions requiring approval | Agreed roles and behavior; required_approvals |
| Q-020 | Exact accountable owner identity and approval of the complete current revision | All required product truth; source approval, approved_product_decisions |

**Next question, Q-001:** What does a “pickup” mean here—collecting donated food for the pantry, taking food to a recipient, or something else?

The answer changes the request information, claim journey, and relevant data access boundaries. No owner answer has yet been received. Product approval and contract conversion remain unavailable pending intake.

## Decision references and superseded history

Current decisions: [DEC-001–DEC-005](../DECISIONS.md#decisions). Source: [SRC-001](../DECISIONS.md#sources). No superseded decisions or earlier revisions.

## Applicable verification

- **PM routing gate:** PASS — raw idea and requested engineering contract route to prd-first.
- **prd-first G1:** PASS — Q-001 resolves a named, relevant OPEN decision and does not repeat supplied information. Only Q-001 is selected for the next user turn.
- **prd-first G2:** PASS — substantive known facts cite SRC-001 via the decision log; missing truth remains OPEN; product artifacts are in the target project's canonical paths; no approval or observed proof is invented.
- **prd-first G3:** NOT READY — required fields and behavior branches remain unresolved. No claim of a complete product definition is made.
- **prd-first G4:** NOT REQUESTED — completeness is not yet satisfied, and accountable identity is unknown.
- **prd-first G5:** NOT ENTERED — no definition is approved, so decision-to-contract has not been invoked.
