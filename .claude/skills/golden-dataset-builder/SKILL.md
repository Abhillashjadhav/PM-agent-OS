---
name: golden-dataset-builder
description: "Iterate-stage skill: curates real outputs plus human judgments into golden eval cases — every case carrying the human verdict and the human's reason, no unlabeled cases, ever. Use when reviewed outputs need structuring into a reusable test set — 'build a golden dataset from these outputs', 'turn these human-graded examples into golden cases', 'we need a regression set, here are outputs and verdicts' — or when /pm routes such a request here. Do NOT use to grade the outputs (human judgment is input), to capture a single production failure (failure-to-eval-capture), to generate synthetic cases, or for golden-dataset definitions."
argument-hint: "<the outputs + whatever human review notes exist, however messy>"
---

# Golden Dataset Builder

Real outputs, real human judgments, structured to last. A golden case without its human verdict and reason isn't golden — it's sand.

## Verification gates (defined first; output is blocked until all pass)

- **G1 — Complete human-label provenance:** every golden carries its input, observed output, human verdict, reason, reviewer alias and label date. Missing or ambiguous fields mean quarantine with specific asks, never inferred labels. An incident description or expected-behavior assertion alone is not a human-label record.
- **G2 — Labels are the human's, verbatim:** retain every supplied review record. If a reason contains identifying data, request human-approved sanitized wording and store that wording verbatim; do not share the original or present the skill's rewrite as the human's words. Conflicting verdicts/reasons stay quarantined for accountable adjudication; append the resolution without erasing the original sanitized reviews.
- **G3 — Case identity and counts:** deduplicate only the same input (exact content or immutable versioned reference), observed output and criterion ID/version. Equal output text alone is insufficient. Report candidate records, unique cases, goldens and quarantine separately, with retained review/export provenance, verdict balance and failure-pattern coverage.

## Steps

1. **Inventory the raw material:** every supplied output and review record, however informal. Separate complete, undisputed records from quarantine (missing pieces or disputes, each with its unblock question). Do not discard review history or infer a label from the request calling something a failure.
2. **Structure each golden:** case id · exact input or immutable versioned reference · observed output · criterion ID/version · human verdict · reason (verbatim, human-approved sanitized wording where needed) · reviewer alias · label date · source provenance. If no eval criterion exists, mark `unmapped` as a seed for eval-engine; do not infer identity or collapse unmapped records.
3. **Deduplicate on full case identity.** Group only identical input/output/criterion cases; retain all review records and export references. Different inputs or criteria remain separate even with identical outputs. Missing/unversioned references or unknown criterion identity cannot establish a duplicate. A conflicting label quarantines the grouped case with both labels intact; ask the criterion owner to adjudicate, never use latest-label-wins or majority vote.
4. **Report the set:** N candidate records → U unique cases = K goldens + M quarantined (with asks); additional exports/reviews retained as provenance, not extra unique cases. Show pass/fail balance and failure-pattern coverage gaps — a coverage gap is a collection task, not a generation task.
5. **State the maintenance loop:** new production failures arrive via failure-to-eval-capture; the set re-runs on every prompt/model change via regression-gatekeeper; label disputes route to the criterion owner. The golden set is infrastructure, and this section is its operating manual.
6. **Gate pass.** All goldens have complete provenance (G1), human wording and disputes preserved (G2), full-identity dedup + reconciled counts + balance + coverage reported (G3). Quarantine is an honest output, not a failed attempt to fill the set. Fix and re-run; maximum 2 repair loops, then report the failure.

## Output format

```
GOLDEN SET: meeting summarizer (6 candidate records → 5 unique cases = 2 goldens + 3 quarantined)
GOLDENS
GC-1 (from O2) — input: [immutable source/version] · output: [recorded output]
criterion: attribution/v1 · verdict: FAIL · reviewer: reviewer-1 · date: [supplied date]
reason [human-approved sanitized wording, verbatim]: "assigned the action item to the wrong attendee"
GC-2 (from O5) — input: [immutable source/version] · output: [recorded output]
criterion: summary-quality/v1 · verdict: PASS · reviewer: reviewer-1 · date: [supplied date]
reason [verbatim]: "perfect example of what we want: short, all decisions captured"
QUARANTINE (not goldens until unblocked)
Q-1 (O1) — supplied PASS, note "good", reason missing → ask reviewer-1: good because what?
Q-2 (O3) — no review → needs verdict + reason
Q-3 (O4) — "fine I guess" — ambiguous → ask reviewer-2: pass or fail, and why?
DEDUP: O6 = O1 (same input/output/criterion); additional export retained as provenance.
BALANCE: 1 pass / 1 fail — minimum viable; coverage gaps: no case exercises the
no-invented-content gate yet → collection task, not generation.
GATE CHECK: G1 pass (2/2 complete, 0 auto-labels) · G2 pass (human wording retained) · G3 pass
```

## Hard rules

1. Never label a case yourself. The skill's entire value is provenance — an inferred "pass" is a poisoned well, and a bigger set is not worth it.
2. Never strengthen or silently rewrite a reason. Privacy edits require human-approved sanitized wording; until supplied, quarantine and omit the identifying reason from shared artifacts.
3. Quarantine is a first-class output: every quarantined case carries the exact question that unblocks it, addressed to the person who can answer.
4. Report the balance. A one-sided set gets said out loud, with the collection task that fixes it — never padded with synthetic counterweights.

## Limitations

- Golden quality equals label quality; inconsistent human reviewers produce an honest set with inconsistent teeth — cross-reviewer disputes are surfaced, not resolved here.
- The set covers observed behavior only; failure modes nobody has hit have no goldens — guardrail-designer and synthetic adversarial cases (kept separate, labeled synthetic) cover the speculative space.
- Verbatim reasons can be terse; terse-but-real beats eloquent-but-invented, and the quarantine asks are how terse improves.
- Privacy: cases containing user data need failure-to-eval-capture's scrubbing discipline before entering a shared set — flagged when detected, not silently included.
