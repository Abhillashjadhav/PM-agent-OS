---
name: failure-to-eval-capture
description: "Iterate-stage skill: converts a production failure into a scrubbed eval case — trigger structure preserved, observed output and human-label provenance ready for regression handoff or quarantined with explicit asks. Use when a bad output escaped to production — 'capture this failure as an eval case', 'turn this incident into a permanent regression test', 'encode this so it never ships again' — or when /pm routes such a request here. Do NOT use for batch curation of reviewed outputs (golden-dataset-builder), for root-causing why the model failed, for PII scrubbing with no eval encoding, or for regression-testing definitions."
argument-hint: "<the failure: the input (or its structure), the bad output, and what made it wrong>"
---

# Failure-to-Eval Capture

Every production failure becomes a permanent test — scrubbed of the people it happened to, but still carrying the trap it fell into. Scrub the identity, keep the mechanism.

## Verification gates (defined first; output is blocked until all pass)

- **G1 — Scrubbed:** all PII and identifying detail (names, emails, orgs, distinctive figures) replaced with stable placeholders; a scrub table shows placeholder classes, never relisting the original values; the unscrubbed failure never appears in the eval artifact.
- **G2 — Pattern demonstrably preserved:** the case states the failure mechanism and shows that the scrubbed input retains its trigger structure — an explicit preservation argument ("mechanism: entity-invention from org-name context; scrubbed input keeps org-as-topic + attendee-owned action item"). Over-scrubbing that deletes the trigger fails this half as hard as leaking PII fails the other.
- **G3 — Assertable, complete handoff:** the expected-behavior assertion is mechanical wherever possible (every attendee in output ∈ input attendee list). Include the observed scrubbed output, criterion ID/version, failure class, non-identifying incident provenance and supplied human verdict/reason/reviewer alias/date. Missing or conflicting labels produce a quarantined draft with asks, never an inferred FAIL or claimed golden-set insertion.

## Steps

1. **Name the mechanism first.** What made the output wrong — not "bad summary" but "invented an entity from an org name mentioned as topic, then reassigned an action item to it". The scrub is designed around protecting this mechanism; naming it first is what makes G2 checkable.
2. **Scrub against the mechanism.** Replace identities consistently in input and observed bad output (Person-A, Company-X, Bank-Y, [amount], [date]) while preserving roles, relationships and the tempting trap. An invented Person-C remains an invention in the bad output, never a true input attendee. Produce the scrub table by class. If the human reason contains identifying data, request approval of sanitized wording; omit the original from shared artifacts and quarantine until approved. Never call the skill's rewrite the human's verbatim reason.
3. **Prove preservation.** Write the argument: mechanism → trigger elements → each present in the scrubbed input. If any trigger element had to be scrubbed away (the PII *was* the trigger), say so and design the closest placeholder-based equivalent, labeled as a reconstruction.
4. **Encode the case:** id · scrubbed input · observed scrubbed bad output · criterion ID/version · expected-behavior assertion (mechanical where possible; stated judge check otherwise) · failure class · incident provenance (date/ticket, never customer identity) · supplied human verdict · approved sanitized reason verbatim · reviewer alias · label date. An incident description, machine alert or assertion does not substitute for a human-label record. Missing fields mean a quarantined draft with exact asks; retain conflicting sanitized review records and request adjudication.
5. **State the handoff:** a complete, undisputed case is eligible for golden-dataset-builder and regression-gatekeeper's pre-ship run. Quarantined drafts are not goldens. Name the proposed destination and distinguish proposed wiring from performed dataset/CI updates; claim an update only with evidence it happened. Optionally add ONE same-mechanism variant, explicitly labeled `SYNTHETIC-VARIANT`, separate from observed cases and their human labels.
6. **Gate pass.** Scrub table complete + no original values (G1), preservation argument holds (G2), assertion check stated and handoff completeness honestly reported (G3). A quarantined draft may be returned with its missing-label asks, without claiming golden readiness. Fix and re-run; maximum 2 repair loops, then report the failure.

## Output format

```
EVAL CASE F-4521 (from production incident, scrubbed)
MECHANISM: entity-invention — an org named as topic, no person from that org present,
model invents an attendee from the org name and reassigns an owned action item.
SCRUB TABLE: person names → Person-A/B · email → person-a@company-x.example ·
org → Bank-Y · amounts → [amount]
SCRUBBED INPUT: "Person-A and Person-B discussed the Bank-Y integration. Person-B
agreed to draft the API contract by [date]. Person-A raised the budget overrun of [amount]."
OBSERVED BAD OUTPUT (scrubbed): "Attendees: Person-A, Person-B, and Person-C from
Bank-Y. Person-C will draft the API contract."
PRESERVATION: trigger structure intact — Bank-Y appears as topic with no Bank-Y
person present; action item owned by Person-B. A model with the defect would still
invent a Bank-Y attendee.
ASSERTION [mechanical]: every attendee/owner in output ∈ {Person-A, Person-B};
action-item owner == Person-B.
CRITERION: attribution/v1 · FAIL CLASS: entity-invention · PROVENANCE: ticket #4521
HUMAN LABEL: FAIL · reviewer-1 · 2026-05-24 · approved sanitized reason, verbatim:
"invented an attendee from the company topic and assigned the action item to that attendee"
HANDOFF: eligible for golden set + regression-gatekeeper; destination proposed,
no dataset or CI update performed by this capture.
VARIANT (SYNTHETIC-VARIANT, same mechanism): topic org = Vendor-Z, same assertion.
GATE CHECK: G1 pass (0 original values) · G2 pass (argument shown) · G3 pass
```

## Hard rules

1. Both scrub failures are failures: leaked PII and a deleted trigger. The gate has two halves and the preservation argument is mandatory evidence for the second.
2. The scrub table lists classes and placeholders — it never becomes a lookup table back to the original values.
3. Assertions are mechanical wherever the failure allows; a judge-checked assertion carries its stated check. "Output should be better" is not an assertion.
4. Synthetic variants are labeled, singular, and same-mechanism. The incident's evidentiary weight belongs to the incident alone.
5. Capture never fabricates human labels or resolves conflicting reviews. Preserve supplied sanitized records; missing or disputed labels stay quarantined for the accountable human.

## Limitations

- Scrubbing here is pattern-based diligence, not a compliance certification — regulated data (health, minors, financial identifiers) should also pass the org's official process, and the skill says so when it detects those classes.
- One case tests one mechanism; a failure with multiple mechanisms becomes multiple cases, not one blurry one.
- Preservation arguments are design-time reasoning; the true test is the regression run reproducing the failure on the defective model version when available.
- Capture prevents recurrence; it does not root-cause. Why the model had the defect is engineering work this case only evidences.
