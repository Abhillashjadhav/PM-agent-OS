---
name: launch-retro
description: "Launch-stage skill: turns launch data into a structured retro where every lesson cites an observed event and decisions are judged separately from outcomes. Use when a launch has run and the learning needs extracting — 'run the retro on the launch', 'what did we learn from the March launch', 'post-launch review with these numbers', 'turn these launch notes into a retro' — or when /pm routes such a request here. Do NOT use for mid-launch status updates (stakeholder-update), for designing the investigation into a metric drop (research-brief), for team-process retros with no launch data, or for retro-facilitation knowledge questions."
argument-hint: "<the launch data: events, numbers vs assumptions, ticket breakdown, decision log, near-misses>"
---

# Launch Retro

Lessons with receipts. Every lesson names the event it came from, and decisions get judged on what was knowable — not on how the dice landed.

## Verification gates (defined first; output is blocked until all pass)

- **G1 — Observed-event citation:** every lesson cites the specific event(s) or number(s) it derives from. "We should communicate better" with no event fails; "39 of 61 tickets concerned navigation → estimate navigation support risk before future cuts" passes. An observed association does not establish the cut's exact causal cost.
- **G2 — Decision ≠ outcome:** assess each logged decision twice — decision quality from evidence available then, outcome quality from what happened and any stated success bar. Cite separate bases. Missing contemporary evidence yields `UNDETERMINED` plus an evidence ask, not a forced GOOD/BAD grade. A good outcome never retroactively blesses a decision, and a bad outcome never proves it was bad.
- **G3 — Open items surface:** undiagnosed near-misses and unexplained numbers appear as OPEN RISKS with owners/actions — a retro that only processes closed items is incomplete. No invented events, sentiments, or dynamics.

## Steps

1. **Build the event ledger:** every event, number-vs-assumption, ticket cluster, decision, and near-miss from the input, each with its figure. This ledger is the citation universe for every lesson.
2. **Assess each logged decision twice.** Decision: what evidence, alternatives, constraints and rationale were available before the choice? Outcome: what happened, against which stated bar? Separate those sources. If the earlier risk/tradeoff record is missing, say `UNDETERMINED` and ask for it. The staged rollout has a stated safety rationale; catching the bug and slipping two days are outcomes. The skipped tooltip has 39 later navigation tickets but no supplied prior risk estimate: that count alone proves neither BAD decision quality nor an exact causal cost. Beating the 15% attach assumption with 19% likewise does not establish optimal pricing.
3. **Extract lessons from the ledger,** one event-citation each, each ending in a forward action: what changes next launch, concretely (cuts of tooltip-class items get a support-cost estimate *before* the cut).
4. **Surface the open items.** The undiagnosed 3-hour spike at 0.45% is the most important line in the fixture retro — near-misses without a root cause get an owner and a diagnose-by action, never a shrug.
5. **Gate pass.** Every lesson cited without overstated causality (G1), decision/outcome evidence separated with missing decision grades explicitly UNDETERMINED (G2), open risks present with actions, nothing invented (G3). Honest unknowns may pass these process gates; they do not certify the underlying decision. Fix and re-run; maximum 2 repair loops, then report the failure.

## Output format

```
LAUNCH RETRO: AI summaries, day 30 (ledger: 6 events · 3 decisions · 1 near-miss)
DECISIONS (separate decision and outcome evidence)
1. Staged rollout — DECISION: supported safety rationale [decision log]; full
   tradeoff assessment UNDETERMINED without the prior risk/alternative record.
   OUTCOME: EU bug caught in cohort 1, fixed in 24h; rollout finished 2 days late.
2. Skipped onboarding tooltip — DECISION: UNDETERMINED. Ask for pre-launch nav-risk
   evidence, expected support cost and alternatives considered before the cut.
   OUTCOME: 39/61 tickets concerned navigation [ticket breakdown]; exact causal
   attribution to the cut and support capacity impact remain unestablished.
3. +$10/seat vs 15% assumption — OUTCOME: 19% at day 30 beats the stated assumption.
   DECISION: UNDETERMINED — prior pricing evidence absent, optimality unknown;
   no price-sensitivity evidence supplied.
LESSONS (event-cited, forward-actionable)
- Tooltip-class cuts get a support-ticket cost estimate before the cut [39/61 tickets] → add to launch-checklist template
- Keep staged rollouts even under date pressure [bug caught in cohort 1]
OPEN RISKS
- 0.45% error spike, 3h, cohort 2 — UNDIAGNOSED, passed within 0.05% of rollback.
  Owner: eng. Action: root-cause by <date>; until then cohort criteria unchanged.
GATE CHECK: G1 pass (n/n cited) · G2 pass (3/3 separately assessed; unknowns explicit) · G3 pass
```

## Hard rules

1. No lesson without its event. The ledger is built first and every lesson points into it.
2. Decisions are graded on what was knowable, outcomes on what happened — independently, always. Missing decision evidence stays UNDETERMINED; a forced grade based on later results is hindsight grading.
3. Near-misses outrank victories. An undiagnosed spike that almost tripped rollback gets more retro space than the metric that beat its assumption.
4. Lessons end in actions. A lesson that doesn't change the next launch is an anecdote.

## Limitations

- The retro processes provided data; events nobody logged are invisible — a thin decision log produces a thin decisions section, said explicitly.
- Decision grading judges information use, not intent or effort; it can still be wrong when the input misstates what was knowable at the time.
- Attribution is observational, not causal — 39 nav tickets after a tooltip cut is strong evidence, not a controlled experiment; the retro says which claims deserve a real analysis.
- Team-dynamics learning (who felt unheard, process friction) needs a facilitated human retro; this skill covers the evidence layer.
