# Gate 1 — Lint
`python3 tests/lint_skill.py .claude/skills/pm/SKILL.md` exits 0.

# Gate 2 — Trigger accuracy

SHOULD FIRE:
T1. "/pm synthesize these four user interviews"
T2. "/pm size the market for AI meeting-notes tools"
T3. "Run the discovery stage on this feature idea"
T4. "/pm tear down Linear's onboarding"
T5. "Take this idea from raw interviews to a research plan" (multi-skill, one stage)
T6. "/pm write our GTM strategy" (fires — then honestly reports stage not shipped)

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

INPUT C (mixed request): "/pm synthesize these interviews, then write the pricing strategy"
EXPECT: Discovery part executed and gated; Strategy part answered with the stage-not-shipped line.
EXPECT the Discovery output NOT to be held hostage by the unshipped stage — partial delivery with an honest boundary.
