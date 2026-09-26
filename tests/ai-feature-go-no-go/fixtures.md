# Gate 1 — Lint
`python3 tests/lint_skill.py .claude/skills/ai-feature-go-no-go/SKILL.md` exits 0.

# Gate 2 — Trigger accuracy

SHOULD FIRE:
T1. "Should we build AI auto-replies? Give me a go/no-go"
T2. "Build or kill: LLM-powered search over our docs"
T3. "Is this AI feature worth shipping? Here's the context: ..."
T4. "/pm go/no-go on adding an AI copilot to the dashboard" (via orchestrator)
T5. "Make the call on this AI feature — we keep debating it"

SHOULD NOT FIRE:
N1. "Map the assumptions behind the AI copilot"     (assumption-mapper — mapping, not deciding)
N2. "Should we build feature X?" (non-AI feature)   (general prioritization, not this skill's rubric)
N3. "Which LLM should power our copilot?"           (vendor/model selection, not go/no-go)
N4. "Go/no-go on the product launch date"           (launch decision, not an AI feature decision)

# Gate 3 — Known-answer

FIXTURE INPUT:
"Go/no-go: AI-generated responses to customer support tickets, sent automatically
without agent review. Context: 8-person fintech startup, support handles account and
payments questions, error tolerance near zero (regulated), current CSAT 4.6/5,
ticket volume 400/mo, 1.5 support FTEs. LLM cost immaterial at this volume."

EXPECTED OUTPUT PROPERTIES:
1. A single decision: GO / NO-GO (a conditional GO must state the exact condition —
   not "it depends" hedging).
2. THE DECISIVE-CRITERIA GATE: the decision names every independent blocker and
   ranks a primary blocker — for this fixture the primary is error tolerance:
   unreviewed generative output in a regulated, payments-adjacent flow with near-zero
   error tolerance = the disqualifier. A decision hiding an independent blocker
   as non-decisive, or listing unranked reasons without a decision, fails.
3. Supporting factors are ranked below the blockers and marked non-decisive only
   if they cannot independently prevent GO. Volume/FTE arithmetic alone does not
   establish a capacity crisis or spare capacity without time-per-ticket evidence.
4. The reversal line names the full required change set. Agent-reviewed drafts are
   a different, smaller feature requiring evidence that review meets the stated
   error bar; do not promise that adding a review step alone proves it GO-worthy.
5. No fabricated context: no invented compliance rulings, competitor moves, or user
   demand. The decision argues from provided context only.

PLANTED-FAILURE CASE:
A draft returning "GO — with careful monitoring, phased rollout, and a feedback loop"
(hedged GO that never names the criterion that would disqualify it) MUST be caught by
the decisive-criteria gate: no stated disqualifier or exact condition → rewrite
or failure report.

# Independent-blocker witness

Input: the owner requires both accuracy ≥95% and cost ≤$0.10 per task. Supplied
evaluation results are accuracy 90% and cost $0.20; the remaining required axes
are explicitly satisfied. The owner ranks quality before economics.

Expected: NO-GO. Primary blocker: accuracy; independent blocker: cost. The minimum
reversal set must resolve BOTH requirements. Moving accuracy to 96% with cost
unchanged is still NO-GO; moving cost to $0.08 with accuracy unchanged is still
NO-GO. With supplied evidence of both 96% and $0.08, GO is justified within this
stated scope. Before that evidence, GO-IF must name both pending conditions and
must not imply present permission to ship. Neither blocker is “non-decisive.”

UNKNOWN-AXIS: same results, but economics has no supplied limit. Expected: ask
for the load-bearing limit or label the decision provisional; do not invent a
budget or claim that fixing quality is a sufficient reversal set.

These are specification witnesses, not recorded model decisions.
