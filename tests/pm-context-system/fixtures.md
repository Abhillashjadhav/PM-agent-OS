# Gate 1 — Lint
`python3 tests/lint_skill.py .claude/skills/pm-context-system/SKILL.md` exits 0.

# Gate 2 — Trigger accuracy

SHOULD FIRE (explicit):
T1. "Set up project memory"
T2. "Make Claude remember my stakeholders across sessions"
T3. "You keep forgetting my project every session — fix that"

SHOULD FIRE (proactive, mid-session):
T4. A decision lands in conversation ("let's go with Postgres over Dynamo for the
    audit log") with no memory request → expect ONE proposal line, not silence,
    not an interview.
T5. "Update context" at session end → sweep proposes only what wasn't already logged.

SHOULD NOT FIRE:
N1. "Summarize this meeting"                     (one-off output, not durable memory)
N2. "Audit my CLAUDE.md"                         (context-auditor)
N3. "Do you remember our last chat?"             (conversation-memory question)
N4. Routine conversation with no decision, stakeholder fact, or state change —
    expect silence, not a placeholder proposal.

# Gate 3 — Known-answer

SCENARIO A (fresh project, no context/ dir; mid-conversation the user says
"we're going with usage-based pricing for the API, flat pricing lost"):
EXPECT exactly one line, in exactly this form:
  Log to memory: "<the decision + why>" — yes/edit/skip
— single line, no second question, no file talk. On "yes": context/ scaffolded
silently (`context/INDEX.md`, `context/STAKEHOLDERS.md`, `context/STATE.md`, and
root `DECISIONS.md`), entry appended to root `DECISIONS.md`, with INDEX pointing
to `../DECISIONS.md` and the CLAUDE.md pointer added. An existing root decision
log must retain its header and entries. On "skip": nothing written, that fact
never re-proposed during the session.

SCENARIO B (existing context/, second decision surfaces): one new proposal line tied
to that decision only — no batch, no re-proposal of logged items.

SCENARIO C (session end, "update context"; one decision already logged inline, one
state change not): sweep proposes ONLY the unlogged state change. Re-proposing the
logged decision = gate failure.

SCENARIO D (STATE.md entry idle 30+ days): archive PROPOSAL with user flag — silent
deletion = gate failure.

SCENARIO E (legacy project): `context/DECISIONS.md` contains an approved D-004
"Chose flat pricing because support needs predictable bills"; root `DECISIONS.md`
contains D-009 "Chose usage pricing because heavy usage is costly". Read both;
keep their paths and IDs visible; ask which decision currently governs. Do not
silently pick the newer text, delete either file, or overwrite either entry.
Only after the owner's specific approval append the resolution to root
`DECISIONS.md`, referencing both old records; preserve the original records.
INDEX points to the canonical root log and keeps the legacy source discoverable
while any legacy decisions remain unreconciled.

SCENARIO F (root log already has the approved decision): INDEX uses that root log;
the sweep does not propose the decision again or create a second decision log.
If only the legacy log exists, read it as existing evidence and propose each
needed transfer to the root log for approval; no automatic move or copying.

GATE PROPERTIES (checked on every proposal):
1. Single line, "Log to memory: … — yes/edit/skip" form. Multi-line or multi-question
   proposals = gate failure.
2. Nothing is ever written without yes/edit. Silent writes = gate failure.
3. Proposals fire on actual session events (decision, stakeholder fact, state change),
   never as empty ritual.

PLANTED-FAILURE CASE:
On SCENARIO A, a draft that responds with a 5-question interview ("What's the project
name? Who are the stakeholders? What are your goals? …") before writing anything —
the never-an-interview gate MUST catch it and reduce it to the one-line proposal for
the decision that actually just happened.

SOURCE-CONTRACT REGRESSION: a fresh-project instruction that still writes the
approved entry only to `context/DECISIONS.md` fails SCENARIO A. A migration that
rewrites/deletes old logs without the specific approval fails E/F. These are
fixture specifications and source-review witnesses, not recorded model runs.
