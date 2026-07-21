# What I learned

This is an author-completion draft. Repository history can establish what changed and what trade-offs are encoded; it cannot invent Abhillash Jadhav’s personal motivation, feelings, or retrospective judgment. Sections marked **HUMAN REVIEW REQUIRED** must be completed or deliberately removed by the author before this page is presented as a first-person account.

## What the repository history establishes

- The product grew from one router and a discovery-stage scaffold to 40 lifecycle decision skills across five stages.
- For all 40 lifecycle skills, the fixture-add commit precedes the skill-add commit in git ancestry.
- The router retained an explicit no-skill refusal even after all five stages shipped.
- Reviewer personas were separated from decision skills and constrained to advisory, line-cited objections.
- The public evidence language was later narrowed: fixtures are specifications, deterministic checks are structural, and live model behavior is not claimed without recorded runs.

Those are inspectable facts. The sections below require the author’s voice.

## HUMAN REVIEW REQUIRED — Why I chose this problem

**Author prompt:** In first person, describe the specific product-work failure that made “plausible output” feel insufficient. Use an event you personally observed or a decision you personally owned. Do not generalize from “every PM” or invent a customer story.

**Add 100–200 words here.**

Repository evidence you may connect to: the invented-quote failure in [`interview-synthesizer`](../tests/interview-synthesizer/fixtures.md), the naked-verdict failure in [`regression-gatekeeper`](../tests/regression-gatekeeper/fixtures.md), or another fixture that matches your actual experience.

## HUMAN REVIEW REQUIRED — Why gates come before instructions

**Author prompt:** Explain when you learned that deciding the acceptance criteria after seeing the draft creates room for rationalization. State whether this came from product work, eval design, or building this repository. Separate your experience from the repository’s structural evidence.

**Add 100–200 words here.**

Repository evidence you may cite: 40/40 fixture-before-skill commit ancestry and the gate-before-steps layout in every inventoried skill.

## HUMAN REVIEW REQUIRED — The hardest trade-off

**Author prompt:** Choose one real trade-off: broad capability versus honest refusal, flexible guidance versus binary gates, persona breadth versus authority, or lifecycle clarity versus nonlinear product reality. State what you gave up, why you accepted that cost, and what would cause you to reverse the decision.

**Add 100–200 words here.**

Avoid claiming the trade-off was objectively correct. This section should show your product judgment and its reversal condition.

## HUMAN REVIEW REQUIRED — What changed my mind

**Author prompt:** Name one design or claim you originally held and later changed. The git history shows candidate changes—stages moving from “not shipped” to live, reviewer personas becoming advisory, and behavioral claims being softened—but only you can say which change reflects a genuine learning and why.

**Add 100–200 words here.**

If the change was prompted by a review, incident, or user reaction, cite the real source. Do not imply that a commit message records motivation.

## HUMAN REVIEW REQUIRED — Where my judgment still enters

**Author prompt:** Describe the decisions you would never delegate to the system. Useful boundaries may include selecting the right gate, deciding whether evidence is sufficient, resolving cross-functional disagreement, accepting business risk, or signing off a launch. Keep this grounded in how you actually intend PM-agent-OS to be used.

**Add 100–200 words here.**

This section should make clear that PM-agent-OS exposes judgment; it does not replace the accountable PM or functional approver.

## HUMAN REVIEW REQUIRED — What I would test next

**Author prompt:** Prioritize the next behavioral evidence you would collect. Name the runtime/model, the smallest representative fixture set, the evaluator, and the failure threshold that would change the product or its claims.

**Add 100–200 words here.**

A strong answer distinguishes structural confidence from the first model-run evidence needed to earn a stronger claim.

## Manual publication check

Before publishing this page as authored narrative:

- [ ] Every HUMAN REVIEW REQUIRED section has the author’s own words or has been intentionally removed.
- [ ] Personal stories name only events the author can substantiate.
- [ ] “I learned” statements describe judgment, not facts inferred from commit messages.
- [ ] No section claims that fixtures are executed tests or that every skill is behaviorally proven.
- [ ] No section claims the system replaces PM, engineering, design, legal, executive, customer, or analyst authority.
- [ ] Runtime support claims match [`VALIDATION.md`](VALIDATION.md).
