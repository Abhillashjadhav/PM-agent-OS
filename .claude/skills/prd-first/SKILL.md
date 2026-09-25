---
name: prd-first
description: "Turn a raw product idea or incomplete PRD into an explicitly approved product definition without guessing. Use when the user wants to build a new product, says 'I want an app', asks for an engineering contract, resumes an existing Draft PRD, or changes an approved product decision. Ask one relevant unresolved question at a time, preserve answers and open decisions, and check behavior coverage before approval. Also handle an explicitly waived ordinary prototype while keeping it unapproved for engineering. Do NOT use for factual questions, specified typo/bug fixes without new product decisions, or an unchanged complete approved definition already ready for decision-to-contract."
---

# PRD-First Discipline

Preserve what the owner intends. Ask only what is missing. A product definition
is complete when its decisions and behavior are covered, not when a question
count has been reached.

## Verification gates — apply before the corresponding transition

- **G1 — Grounded next question:** the question resolves one named OPEN decision,
  is relevant to the requested behavior, and does not repeat an already supplied
  answer. Ask one question, wait, and reuse the answer before choosing the next.
- **G2 — Truth and draft integrity:** substantive decisions cite supplied context
  or an owner answer. Keep proposals, assumptions and observed facts distinct.
  Missing or contradictory product truth stays OPEN. Preserve stable IDs, owner
  wording, prior decisions and the target project's canonical artifact paths.
- **G3 — Complete product definition:** every requested behavior is mapped to an
  included FR and acceptance intent, or to an explicit owner-approved exclusion.
  Every required field in [FIELD_FLOW.md](references/FIELD_FLOW.md) has supplied
  or owner-decided truth; no required OPEN question, vague default or TBD remains.
  Check journey success, failure and permission boundaries before claiming coverage.
- **G4 — Accountable approval:** G2/G3 pass, the owner sees the current PRD revision
  and coverage summary, and explicitly approves it under their exact identity.
  Contradictory approval labels fail; neither file existence nor prior approval
  of a different revision counts. Unknown identity requires a question.
- **G5 — Handoff boundary:** only the approved product definition enters
  `decision-to-contract`. That skill validates supported bindings and publisher
  fields, obtains separate exact-digest approval, and verifies the receipt.
  A proposed, Draft or waived prototype never counts as an executable contract.

Questions and OPEN/Draft progress reports need G1/G2, not a fabricated G3/G4 pass.
Request product approval only after G3. A strict engineering handoff needs all
applicable gates. An explicitly waived ordinary prototype follows the separate
path below and must not claim those engineering gates passed.

## Hard rules

1. Never invent product facts, thresholds, exclusions, labels, approvals or an
   approver to complete a template. An unanswered required decision is OPEN.
2. No fixed interview or follow-up limit implies completion. If the owner cannot
   decide, preserve the blocker and continue only independent resolved work.
3. Reuse existing Drafts and answers. New meaning invalidates the affected current
   approval; preserve the old revision and decision as history.
4. Keep product-definition approval separate from approval of the exact generated
   contract digest. Neither authorizes code, deployment or release through PMOS.
5. Never manufacture observed examples or human verdicts. Designed reference cases
   remain explicitly designed and require owner approval before use.
6. A skipped intake, an absent owner or an autonomous task description cannot
   replace product approval on the engineering path.

## 1. Recover context and choose the path

Identify the target product project from the user's context; ask if it is unclear.
Read its existing `prds/` artifact and root `DECISIONS.md` before repeating intake.
A Draft is a resumption point, not an exclusion from this skill. Reuse stable IDs;
append new ones without renumbering or silently replacing the existing artifact.

Use strict engineering intake when an executable contract or engineering handoff
is requested. An unchanged complete approved definition can go directly to
`decision-to-contract`; changed or missing product truth returns here.

For an ordinary prototype explicitly waived by the user, record the exact waiver,
current intent and OPEN decisions in a Draft artifact and root `DECISIONS.md`.
Label it **ordinary prototype — unapproved for engineering**. An ordinary prototype
prompt may reference that Draft without claiming product or contract approval.
Do not silently switch an engineering request to this path. Later handoff resumes
strict intake; it does not reuse the waiver as approval.

## 2. Build the decision and coverage view

Read [FIELD_FLOW.md](references/FIELD_FLOW.md) for engineering intake. It maps owner
truth to all existing publisher-input fields and the existing specialist skills.
Do not add another publisher or ask the user to design its JSON syntax.

Record one stable `Q-*` per unresolved question and `DEC-*` per resolved decision.
For each decision retain owner wording, source reference, affected fields and
FR/AC IDs, and whether it supersedes an earlier decision. Use `OPEN`, `RESOLVED`
and `SUPERSEDED` explicitly. If existing context disagrees, ask which decision
controls rather than silently choosing the newest document.

Walk each included user journey: who acts, what information enters, what action
occurs, what outcome the user receives, and what happens when input is missing,
contradictory or rejected. Examine data access, authority and irreversible effects
only where the journey makes them relevant. Do not import unrelated requirements.

Track every requested behavior in a coverage table: source → owner decision →
FR → acceptance intent → gate, or explicit exclusion. Count both omitted requests
and uncovered FRs; covering only the FRs already written can hide missing behavior.

## 3. Ask one unresolved question and update

Choose the next missing decision by dependency, reusing answers already supplied:

1. Problem, primary user, current alternative and the owner's hypothesis.
2. Intended outcome, outcome North Star, leading measures, guardrails and trade-offs.
3. Included journeys, explicit exclusions and conflicting behavior choices.
4. Relevant failure, data and permission boundaries.
5. Observable acceptance, non-functional constraints and reference cases.
6. Remaining risks, release-gate meaning and accountable approvals.

This is an order for missing dependencies, not six compulsory questions. A specific
conflict with an already known journey can be the first useful question. Explain
what the answer changes; ask one decision at a time, not a disguised questionnaire.
If an answer remains vague, narrow the question using the actual ambiguity. Do not
cap follow-ups or convert "whatever makes sense" into a product decision.

After each answer, update the PRD, decision references and affected coverage rows.
Run G1/G2, then recompute what is still OPEN. If the owner is unavailable, save the
next question and blocked transition. Do not ask it repeatedly or mark it resolved.
Route only actual missing specialist work using the field reference. Their proposals
remain proposals until the owner decides; their outputs do not create approval.

## 4. Persist in the target product project

Keep the PRD under `prds/YYYY-MM-DD-<slug>.md` in the target product project, even
when PMOS is installed globally. For a resumed feature, keep its existing path.
Create only the required folder/artifact. Do not store product truth in the PMOS
installation or source repository unless that repository is the target product.

Use this compact outline, expanding lists/tables for actual decisions:

```markdown
# PRD: <owner's product name>
Date: <date>
Revision: <stable revision>
Status: Draft
Contract status: DRAFT
Approved by:
Approval record: <blank until explicit approval; then source and approved revision>
Canonical decisions: <relative link to root DECISIONS.md>

## Problem, user, current alternative and hypothesis
## Intended outcome, North Star, leading metrics, guardrails and trade-offs
## Included journeys and out-of-scope decisions
## Functional requirements — FR IDs, observable behavior and capability
## Acceptance intent — AC IDs, requirement references and owner-approved proof
## Non-functional requirements — NFR IDs and explicit constraints
## Release gates, rubric, reference cases, risks and required approvals
## Publisher field coverage — field, source/decision, state and OPEN question
## Behavior coverage — requested behavior, decision, FR, AC/gate or exclusion
## Open questions — Q ID, dependency, affected fields, next question
## Decision references and superseded history
```

Root `DECISIONS.md` is the canonical decision log; the PRD links to relevant entries.
Context memory points to that root file. If `context/DECISIONS.md` already exists,
preserve and reference its entries, carry forward decisions with provenance, and
record a pointer to the canonical root log. Resolve conflicting entries with the
owner before treating either as current; never silently delete or overwrite them.
An active task/planner register is separate and must not be moved by this skill.

## 5. Check completeness, approval and downstream changes

Run G3 against requested behavior and the complete field map. An owner-approved
"not applicable" is usable only where the existing publisher permits it; never
insert empty collections merely to hide missing truth. Unsupported executable
bindings are engineering dependencies, not permission to invent a different product.

When G3 passes, show the PRD revision, concise coverage and any external binding
limits. Ask whether the accountable owner approves, edits or rejects this product
definition. Wait. Once G4 passes, record agreeing `Status: Approved`,
`Contract status: APPROVED`, exact `Approved by`, approved revision and approval
source. These PRD labels mean product-definition approval for conversion; the
publisher's generated contract still starts DRAFT and has its own digest approval.

Pass the approved definition and decision sources to `decision-to-contract`.
Mapping or publisher diagnostics produce a bounded question or a BLOCKED engineering
dependency. If resolving one changes product meaning, create a new Draft revision,
reopen affected decisions/coverage, and obtain product approval again. Any changed
published contract needs fresh exact-digest approval; never reuse a stale receipt.

For an approved ordinary build, any subsequent implementation prompt references
the target PRD path and revision. This skill does not itself execute engineering.

## Limitations

- These are host-agent instructions and conversation specifications, not an
  independently enforced interview runtime or proof of model behavior.
- Coverage depends on the supplied context and the journeys actually examined;
  the reviewable map exposes gaps but cannot guarantee the product is correct.
- Existing specialist skills and the external publisher can reject incomplete or
  unsupported inputs. Their availability does not justify guessing missing truth.
- Live supervised conversations and fresh product delivery need separate evidence.
