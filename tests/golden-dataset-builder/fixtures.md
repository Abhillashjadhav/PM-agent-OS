# Gate 1 — Lint
`python3 tests/lint_skill.py .claude/skills/golden-dataset-builder/SKILL.md` exits 0.

# Gate 2 — Trigger accuracy

SHOULD FIRE:
T1. "Build a golden dataset from these production outputs and our review notes"
T2. "Turn these 20 human-graded examples into golden eval cases"
T3. "We need a regression set for the summarizer — here are real outputs + verdicts"
T4. "/pm curate golden cases from this batch" (via orchestrator)
T5. "Structure our reviewed outputs into a reusable test set"

SHOULD NOT FIRE:
N1. "Grade these outputs for me"                   (the human judgment is input — the skill structures, it doesn't judge)
N2. "Turn this production failure into an eval case"  (failure-to-eval-capture — single-failure pipeline with scrubbing)
N3. "Generate synthetic test cases for the summarizer"  (synthetic generation — goldens are real outputs with real judgments)
N4. "What's a golden dataset?"                      (knowledge question)

# Gate 3 — Known-answer

FIXTURE INPUT (raw material):
The records below include their immutable input references, recorded output text,
criterion IDs/versions, and label dates (2026-05-24). Supplied human verdicts are
O1 PASS, O2 FAIL, O5 PASS; O4 is deliberately ambiguous. Priya and Marco are the
provided reviewer aliases. O6 is an exact export of O1 including its provenance.
"Outputs from our meeting summarizer + review notes:
O1. [summary text] — Priya: 'good'
O2. [summary text] — Priya: 'the action items are wrong, it assigned Marco's task to Lena'
O3. [summary text] — no review note
O4. [summary text] — Marco: 'fine I guess'
O5. [summary text] — Priya: 'perfect example of what we want: short, all decisions captured'
O6. [same summary as O1, duplicate export]"

EXPECTED OUTPUT PROPERTIES:
1. THE NO-UNLABELED-CASES GATE: every case in the golden set carries (a) the human
   verdict and (b) the human's REASON. Cases lacking either are quarantined in a
   "needs labeling" list with what's missing — never included as goldens, never
   auto-labeled:
   - O3 (no note) → quarantine: needs verdict + reason.
   - O4 ("fine I guess") → quarantine: verdict ambiguous, reason absent — the skill
     asks Marco what 'fine' means, it does not upgrade it to PASS.
   - O1 ("good") → verdict present, reason absent → quarantine for reason, or
     included ONLY if the reviewer supplies why ("good" alone can't teach a judge).
2. Reason quality: O2 and O5 are complete goldens — verdict + specific reason
   (wrong assignee; short + all decisions). The reason is stored verbatim as the
   human's, never paraphrased into something stronger.
3. Dedup: O6 detected as O1's duplicate by the full input/output/criterion identity
   — one case, all review/export provenance preserved, never two goldens inflating
   the set. Same output text alone is not enough to establish a duplicate.
4. Case structure: id · input (or its reference) · output · verdict (pass/fail or
   score) · reason (verbatim) · label author · date · the eval criterion it
   exercises (mapped where criteria exist; 'unmapped' honestly otherwise).
5. Set report: 6 candidate records → 5 unique cases = 2 goldens + 3 quarantined;
   O6's additional export record remains provenance, not a sixth unique case;
   coverage note — both verdicts represented? (a set of only passes tests nothing);
   failure-pattern coverage listed.

PLANTED-FAILURE CASE:
A draft that includes O3 as a golden with verdict "pass" (inferred from 'looks
normal') and O4 upgraded to pass — auto-labeling unlabeled cases to hit a bigger
set size — MUST be caught by the no-unlabeled-cases gate and both cases quarantined
with their asks. A golden set's value is its labels' provenance; invented labels
poison it.

# Case-identity and label-conflict witnesses

IDENTITY-1: supplied input A says `balance=100`, input B says `balance=200`.
Both recorded outputs say `balance=100`, under the same criterion `balance/v1`.
Human labels are A PASS ("matches A") and B FAIL ("does not match B"), with
reviewer alias/date supplied. Expected: TWO unique cases, one PASS and one FAIL;
deduplicating them because the outputs match fails the fixture.

IDENTITY-2: the same input and output are reviewed under `coverage/v1` and
`concision/v1`. Expected: distinct criterion cases. Missing/unversioned input
references or unknown criterion identity must not justify collapsing records.

CONFLICT-1: exact same input/output/criterion case has reviewer R1 PASS / "complete"
and reviewer R2 FAIL / "misses the second question". Expected: one quarantined
case with BOTH original review records and an adjudication question. Neither
latest-label-wins nor majority vote is authorized; the original labels/reasons
remain intact after an owner-supplied adjudication is appended.

HANDOFF-1: a captured incident contains only scrubbed input and an expected
assertion. Expected: quarantine; request the observed scrubbed output and missing
human verdict, verbatim reason, reviewer alias and date. An assertion is not a
human label. If a reason needs privacy edits, require the human-approved sanitized
reason instead of presenting a rewritten reason as verbatim.

These are specification witnesses; they do not assert a recorded model run.
