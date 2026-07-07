# Gate 1 — Lint
`python3 tests/lint_skill.py .claude/skills/pm/SKILL.md` exits 0.

# Gate 2 — Trigger accuracy

SHOULD FIRE:
T1. "/pm synthesize these four user interviews"
T2. "/pm size the market for AI meeting-notes tools"
T3. "Run the discovery stage on this feature idea"
T4. "/pm tear down Linear's onboarding"
T5. "Take this idea from raw interviews to a research plan" (multi-skill, one stage)
T6. "/pm should the AI add-on be usage-priced?" (fires — Strategy shipped, routes to pricing-tradeoff)
T7. "/pm write our GTM strategy" (fires — Strategy shipped, but no Strategy skill covers GTM authoring: expect the honest no-skill-covers-this line, zero improvised GTM content)

SHOULD NOT FIRE:
N1. "Fix the typo in README and push"                      (repo maintenance, not a product request)
N2. "What does JTBD stand for?"                            (knowledge question)
N3. "Review this PR"                                       (/pr-review's job)
N4. "Synthesize these interviews" typed as /interview-synthesizer  (direct stage-skill call — router not asked)

# Gate 3 — Known-answer

INPUT A (unshipped stage): "/pm draft the launch plan for our beta"
EXPECT: classification line naming the stage (Launch), then the exact honest refusal —
"Stage not yet shipped: Launch. pm-agent-os currently ships Discovery only (7 skills). Roadmap: README.md."
EXPECT ZERO generated launch-plan content. Improvising an unshipped stage = gate failure.

INPUT B (shipped stage): "/pm synthesize these 2 transcripts: [fixture transcripts]"
EXPECT: classified Discovery → routed to interview-synthesizer → that skill's own gates run
(≥2 verbatim quotes per pattern, zero invented quotes) BEFORE any synthesis reaches the user.
If a gate fails and can't be fixed in 2 repair loops, EXPECT a failure report, not the failing output.

INPUT C (mixed request): "/pm synthesize these interviews, then structure the pricing options"
EXPECT: Discovery part executed and gated (interview-synthesizer), then Strategy part routed to
pricing-tradeoff with the pricing options built on the GATED synthesis output, its own
margin-mechanism gate run before delivery. Sequential stages, each gated.

INPUT D (shipped stage, uncovered request): "/pm write our GTM strategy"
EXPECT: classified Strategy (shipped) → no Strategy skill covers GTM authoring → the honest
no-skill line naming the 6 skills the stage does ship, zero improvised GTM content.
