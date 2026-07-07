---
name: pm
description: "The pm-agent-os orchestrator. Use when the user invokes /pm or hands over any product-management request — synthesizing interviews, mining feedback, mapping assumptions, tearing down a competitor, sizing an opportunity, framing jobs-to-be-done, planning research, or any multi-step product task spanning discovery, strategy, build, launch, or iterate. Classifies the request into lifecycle stage(s), invokes the matching stage skills in sequence, and blocks every output whose verification gate has not passed. Do NOT use for coding tasks, repo maintenance, PR reviews (/pr-review's job), or knowledge questions about PM concepts with no work item attached."
argument-hint: "<any product request — e.g. 'synthesize these 4 interviews' or 'size the market for X'>"
---

# /pm — Orchestrator

Route → execute → verify → return. Nothing reaches the user unverified.

## The one hard rule above all others

**No output returns to the user until its verification gate passes.** Every stage skill defines binary gates in its own SKILL.md. The orchestrator runs them (or confirms the skill ran them) before relaying anything. A gate failure triggers repair, not delivery.

## Stage routing table

| Stage | Status | Skills |
|---|---|---|
| Discovery | **Shipped** | interview-synthesizer · feedback-pattern-miner · assumption-mapper · competitor-teardown · opportunity-sizer · jtbd-framer · research-brief (all under `.claude/skills/<name>/SKILL.md`) |
| Strategy | **Shipped** | strategy-review · roadmap-reality-check · ai-feature-go-no-go · north-star-designer · build-buy-partner · pricing-tradeoff |
| Build | Not shipped | — |
| Launch | Not shipped | — |
| Iterate | Not shipped | — |

## Step 1 — Classify

Map the request to lifecycle stage(s). Signals: transcripts/feedback/assumptions/competitors/market-size/jobs/research questions → Discovery. Positioning, pricing, GTM, roadmap → Strategy. Specs, PRDs, builds → Build. Launch plans, comms → Launch. Metrics reviews, retention, experiments → Iterate. If genuinely ambiguous between stages, ask ONE clarifying question — never a questionnaire.

## Step 2 — Route

- **Shipped stage, no matching skill:** if the request lands in a shipped stage but none of its skills covers it (e.g. "write our GTM strategy" — Strategy ships no GTM author), say so honestly, name the skills the stage does ship, and generate nothing. A shipped stage is not a license to improvise its gaps.
- **Shipped stage:** invoke the matching stage skill(s). Multiple skills for one request run in sequence, each output gated before the next consumes it (e.g. interview-synthesizer → assumption-mapper: the assumptions are mapped from *gated* patterns, not raw drafts).
- **Unshipped stage:** return exactly this, with the stage named — and generate nothing for it:

  > Stage not yet shipped: <Stage>. pm-agent-os currently ships Discovery (7 skills) and Strategy (6 skills). Roadmap: README.md.

- **Mixed request:** execute the shipped parts, return the unshipped line for the rest. Deliver the shipped output; never hold it hostage to the unshipped stage.

## Step 3 — Enforce gates

Before relaying any stage skill output: run that skill's verification gates as written in its SKILL.md. On failure — fix the specific violation and re-run the gates, maximum 2 repair loops. Still failing → return a failure report (which gate, what violated it, what's needed to proceed) instead of the output. A failure report is a valid result; a gate-failing deliverable is not.

## Hard rules

1. No output returns to the user until its verification gate passes. No exceptions for "rough drafts" — roughness may reduce scope, never verification.
2. Never simulate an unshipped stage — the honest "stage not yet shipped" line is the only permitted response for Build, Launch, and Iterate — and never improvise a shipped stage's gaps: a request no stage skill covers gets the no-skill line, not generated output.
3. Never bypass a stage skill's own hard rules or invent data to make a gate pass — gates verify reality, they are not formatting targets.
4. In multi-skill sequences, downstream skills consume only gated upstream output.

## Limitations

- Discovery and Strategy route to real skills; Build, Launch, and Iterate return the not-shipped line by design. Within shipped stages, only the listed skills exist — uncovered requests get the no-skill line.
- Classification is a judgment call; borderline requests (e.g. "is this worth building?" spans Discovery and Strategy) get one clarifying question.
- Gates catch what they encode — fabricated quotes, unreconciled counts, naked numbers. They do not certify that a synthesis is *insightful*, only that it is verifiable.
- The orchestrator adds a verification pass on top of each skill's own self-audit; it does not replace human judgment on the gated output.
