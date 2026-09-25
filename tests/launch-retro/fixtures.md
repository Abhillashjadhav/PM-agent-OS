# Gate 1 — Lint
`python3 tests/lint_skill.py .claude/skills/launch-retro/SKILL.md` exits 0.

# Gate 2 — Trigger accuracy

SHOULD FIRE:
T1. "Run the retro on the AI summaries launch — data below"
T2. "Structured retro from this launch data"
T3. "What did we learn from the March launch? Here's what happened"
T4. "/pm post-launch review with these numbers" (via orchestrator)
T5. "Turn these launch notes into a retro doc"

SHOULD NOT FIRE:
N1. "Write the launch status update"              (stakeholder-update — during, not after)
N2. "Why did activation drop? Plan the research"  (research-brief — investigation design)
N3. "How do I run a good retro?"                  (knowledge question)
N4. "Retro on our team's sprint process"          (process retro, no launch data)

# Gate 3 — Known-answer

FIXTURE INPUT (launch data):
"AI summaries launch, day 30. Events: rollout finished 2 days late (EU residency bug
found in cohort 1 — caught by the staged rollout, fixed in 24h). Attach rate 19% at
day 30 (assumption was 15% by day 90). Support: 61 tickets — 39 of them 'where do I
find the summary' (nav confusion), 8 the residency bug, 14 misc. Sales: 2 of 3
stalled deals closed. Decision log: we chose staged rollout over big-bang (safety);
we skipped the onboarding tooltip to hit the date (schedule); we priced at +$10/seat
against a 15% attach assumption. One near-miss: error rate spiked to 0.45% (rollback
line 0.5%) for 3h during cohort 2 — cause never diagnosed."

EXPECTED OUTPUT PROPERTIES:
1. THE OBSERVED-EVENT GATE: every lesson cites the specific observed event(s) it
   derives from (the 39 nav tickets, the 2-day slip, the 0.45% spike). A lesson with
   no event ("we should communicate better") = gate failure.
2. DECISION vs OUTCOME SEPARATED, per decision in the log:
   - staged rollout: decision rationale is supported by the stated safety goal;
     its full pre-launch tradeoff record is absent. Outcome: cohort 1 caught the
     residency bug, fixed in 24h, and rollout finished two days late. Do not infer
     decision quality solely from either the caught bug or the delay.
   - skipped tooltip: decision quality UNDETERMINED from the supplied record —
     the pre-launch navigation-risk evidence, support-cost estimate and alternatives
     are absent. Outcome: 39 of 61 tickets concern navigation; support burden is
     observed, but neither its survivability nor the tooltip cut's exact causal
     cost is supplied. Ask for the contemporary decision evidence; do not grade
     the decision BAD solely from the later ticket count.
   - +$10 pricing: GOOD OUTCOME (19% > 15% assumption, 60 days early) — but the
     retro must NOT inflate it to 'great pricing decision' without noting the
     assumption was beaten, not validated as optimal (maybe money left on table).
   Judging decisions by outcomes alone, or outcomes by intentions = gate failure.
3. The undiagnosed near-miss (0.45% spike) must appear as an OPEN RISK with an
   action — a retro that only processes closed items = incomplete.
4. Lessons are forward-actionable: each ends with what changes next launch
   (tooltip-class cuts get a support-ticket cost estimate before cutting, not after).
5. No invented events, sentiments, or team dynamics not in the data.

PLANTED-FAILURE CASE:
A draft lesson "the 2-day delay shows our rollout process needs to be faster" —
outcome-judging a good decision (the staged rollout caught the bug; speed was the
tradeoff working as designed) — MUST be caught by the decision/outcome gate and
rewritten to credit the mechanism while noting the schedule cost honestly.

# Hindsight witness

BASE: use the supplied fixture unchanged. Expected: skipped-tooltip decision
quality UNDETERMINED, observed outcome 39 navigation tickets, and a request for
what was known before the cut. Reject “BAD at this volume” or “the exact cost of
the cut”: both infer missing decision/causal evidence from the later outcome.

CONTEMPORANEOUS-EVIDENCE VARIANT: add a pre-launch decision record stating that
the owner required the known navigation problem fixed before release, the team
had reproduced it in a usability study, and a verified tooltip fix was available
within approved scope but was knowingly cut without revisiting that requirement.
With the same 39-ticket outcome, a BAD decision-quality assessment may now cite
that prior evidence and violated requirement. It must still not claim that all
39 tickets are the tooltip's proven causal cost.

Missing evidence may remain UNDETERMINED while the retro's process gates pass:
the output must disclose the gap and next evidence needed, not invent a grade.
These are specification witnesses, not recorded model retrospectives.
