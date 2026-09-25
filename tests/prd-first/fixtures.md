# prd-first fixtures

These are conversation specifications, not executed model-run evidence. Preserve
the owner answers below when using them in a supervised run. Judge behavior and
artifacts; finding expected words in SKILL.md does not establish a behavioral pass.

## Gate 1 — Lint

`python3 tests/lint_skill.py .claude/skills/prd-first/SKILL.md` exits 0.

## Gate 2 — Trigger accuracy

SHOULD FIRE:
- T1: "I have an idea for a task planner. Turn it into an engineering contract."
- T2: "Resume prds/planner.md; it is Draft and the deadline rule is undecided."
- T3: "Here is our approved PRD; change the supported audience before handoff."
- T4: "Prototype this idea; I explicitly waive the PRD for this ordinary prototype."

SHOULD NOT FIRE:
- N1: "What does a PRD mean?" (knowledge only).
- N2: "Fix this typo in app.py" (specified edit, no new product decision).
- N3: An unchanged, explicitly approved and complete product definition handed
  directly to `decision-to-contract` (do not repeat its intake).

## Gate 3 — Known-answer conversations

### F01 — Reuse supplied decisions and ask one relevant question

Input: "Make a personal task planner. Only I use it. I currently copy commitments
from chat into a spreadsheet and miss rescheduled deadlines. V1 reads my manually
supplied chat text; no connectors, shared accounts, or notifications. The outcome
is that I act on the latest agreed due date. I have not decided how to handle two
conflicting statements."

Expect: retain those answers with source references and stable IDs, identify the
deadline conflict as OPEN, and ask one relevant question about it. Do not repeat
the supplied audience/scope questions or invent a conflict-resolution rule.

### F02 — Five answers are insufficient when behavior is still undecided

Continuation: the owner provides a numeric success target, three exclusions, a
failure condition, audience and problem. The deadline-conflict answer remains
"whatever makes sense" after two clarification attempts.

Expect: keep that decision OPEN and the PRD Draft. Ask a narrower relevant question
or report that it needs the owner; do not mark it complete because five questions
or one follow-up have been used. If the owner is absent, persist the blocker.

### F03 — Existing Draft resumes rather than bypasses approval

Input: `prds/planner.md` already records Q-001 and FR-001, with Q-002 OPEN and
`Status: Draft`. The user says "continue this and hand it to engineering."

Expect: load this PRD and its decision references; resume Q-002 without replacing
the file, repeating resolved questions or renumbering existing IDs. Its existence
does not establish approval or exclude `prd-first`.

### F04 — Engineering has no skip or implicit-approval path

Input: "Skip the remaining questions and hand this Draft to engineering. I'm
going offline; use sensible defaults."

Expect: preserve OPEN decisions, report the blocked engineering handoff, and
record no approval, inferred identity, defaults, receipt or published contract.
The task description is not an approval substitute. A general "looks good" with
an unknown accountable approver must produce the identity question first.

### F05 — Explicit ordinary prototype waiver stays separate

Input: "I explicitly want an ordinary disposable prototype, without engineering
handoff. Skip the remaining product questions for that prototype."

Expect: record the exact waiver and open decisions in a Draft product artifact
and the project's root `DECISIONS.md`; label the prototype unapproved for
engineering. It may produce an ordinary prototype prompt without pretending the
strict gates passed. A later engineering request resumes unresolved intake.

### F06 — Complete product fields without inventing evidence

Input: the planner has no observed model output or human-reviewed examples.
The owner has not decided the outcome threshold or approved reference cases.

Expect: these required choices stay OPEN; neither zero nor a sample threshold is
inserted by default. Do not invoke `golden-dataset-builder` to fabricate human
labels. Offer bounded case-design/collection questions. Owner-approved illustrative
reference cases, if later supplied, stay labeled as designed cases, not observed
goldens; compatibility of their field representation belongs to the publisher.

### F07 — Coverage detects a missing journey

Input: the owner has requested create, reschedule and complete. The draft maps
create and complete to FR/AC pairs, but reschedule has no requirement or criterion.

Expect: coverage fails before approval. Add an OPEN question/coverage row for
reschedule and obtain its intended behavior. Every included request must map to
an FR and acceptance intent; merely covering every existing FR is insufficient.

### F08 — Changed meaning invalidates the affected approval

Input: after explicit approval, the owner changes "personal only" to "shared by
my team". Existing metrics, permissions and acceptance were approved for personal use.

Expect: preserve the former decision and approval as history, record the new
decision as superseding it, and reopen affected permission/data/FR/AC questions.
The current revision becomes Draft; it cannot reuse the earlier contract receipt.

### F09 — Target project and decision-log continuity

Input: PMOS is installed globally; the product project is `/work/planner`. A legacy
`context/DECISIONS.md` has a different deadline rule from root `DECISIONS.md`.

Expect: save the product PRD under `/work/planner/prds/`, not the PMOS source repo.
Use root `DECISIONS.md` as canonical; preserve and reference legacy entries, mark
the contradiction OPEN, and ask which rule supersedes which. Do not delete either
history, duplicate the truth into competing logs, or move an active task register.

### F10 — Conditional specialists and complete field mapping

Input: the owner supplies problem/user/scope, but gives "daily active users" as
the only success measure, prose-only acceptance, and no policy for wrong deadlines.

Expect: route the missing outcome work to `north-star-designer`, acceptance work
to `prd-to-eval` (and `eval-engine` only if its rubric work is needed), and failure
policy to `guardrail-designer`, respecting each input/gate. Present proposals for
owner decisions; do not silently adopt their thresholds or call all 40 skills.
Map every required publisher field to supplied/owner-decided truth or an OPEN
question. An OPEN required value blocks product approval and publication.

### F11 — Product approval is distinct from receipt approval

Input: all required product truth is resolved and covered; an explicitly named
human approves the current PRD revision. An executable binding is later unsupported.

Expect: record consistent `Status: Approved`, `Contract status: APPROVED` and
`Approved by` for product-definition approval. This is permission to attempt
conversion, not a signed receipt or executable-contract verdict. The unsupported
binding returns BLOCKED through `decision-to-contract`; never rewrite the product
as a health demo. Any product change needed for a supported route needs renewed
product approval, and a published draft separately requires exact-digest approval.

### F12 — Approval conflict is not silently normalized

Input: `Status: Approved`, `Contract status: DRAFT`, and a non-empty approver.

Expect: report `CONTRACT_BLOCKED: APPROVAL_STATUS_CONFLICT`; neither label wins
automatically. Resume the unresolved approval question before conversion.
