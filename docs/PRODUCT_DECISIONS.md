# Product decisions

PM-agent-OS is designed around a single product principle: plausible output is not enough to advance product work. The artifact must first pass the decision gate appropriate to its lifecycle stage.

These decisions make product judgment explicit and inspectable. They do not automate accountability or claim that a passing artifact is strategically correct.

## 1. One orchestrator is the front door

**Decision.** Use one `/pm` router to classify requests, sequence covered skills in lifecycle order, enforce gated handoffs, and refuse uncovered work.

**Why.** A collection of directly invoked skills leaves routing and sequencing implicit. One front door makes the operating contract visible: classify, route, verify, then return. It also gives multi-stage work one place to enforce the rule that downstream skills consume only gated upstream output.

**Trade-off.** Classification remains a model judgment. A single router can misclassify an ambiguous request, so the router permits one clarifying question and keeps direct skill invocation available when the user already knows the intended operation.

**Evidence.** The current behavior is specified in the [`/pm` orchestrator](../.claude/skills/pm/SKILL.md) and its [routing fixtures](../tests/pm/fixtures.md). Live routing accuracy still requires behavioral execution.

## 2. Lifecycle stages define the decision sequence

**Decision.** Organize product work into discovery, strategy, build, launch, and iterate, then route cross-stage work in that order.

**Why.** The stages identify what kind of judgment is being made and what evidence should exist before the next commitment. Interview evidence should be gated before it becomes an assumption; assumptions should be gated before a build decision; build criteria should exist before launch readiness or regression verdicts.

**Trade-off.** Real product work is not perfectly linear. The stage model is a routing and evidence discipline, not a waterfall process. Teams can loop backward when a gate exposes missing evidence, and the system does not claim to cover every decision within a stage.

**Evidence.** Stage assignments and counts are explicit in [`inventory.json`](../inventory.json); full-lifecycle sequencing is specified in the [`/pm` fixture](../tests/pm/fixtures.md).

## 3. Gates precede instructions

**Decision.** State each lifecycle skill’s binary verification gates before the generation or analysis steps.

**Why.** Precommitting the disqualifiers makes it harder to redefine success after seeing a persuasive draft. The gate describes what blocks advancement; the instructions describe how to produce an artifact that can be inspected against it.

**Trade-off.** A precommitted gate can still encode the wrong standard or omit a meaningful failure. Gate design remains product judgment and should be challenged when the evidence or stakes change.

**Evidence.** All 40 inventoried lifecycle skills place a dedicated verification-gate section before their steps. For a concrete example, compare the gate and steps in [`regression-gatekeeper`](../.claude/skills/regression-gatekeeper/SKILL.md).

## 4. Every fixture carries a planted failure

**Decision.** Define a representative failure that the skill’s gate must reject, alongside trigger examples and expected output properties.

**Why.** A gate is easier to inspect when its failure shape is concrete. “No verdict before a run” becomes testable when the fixture plants “ship Friday, run the goldens next week.” The planted failure also prevents a vague success description from hiding what the gate exists to stop.

**Trade-off.** A fixture covers one known failure shape, not the full behavioral space. Fixture presence is structural evidence; only a recorded run can show that a named host and model caught it.

**Evidence.** Every inventoried lifecycle skill points to a fixture in [`inventory.json`](../inventory.json). The [regression fixture](../tests/regression-gatekeeper/fixtures.md) is the clearest example.

## 5. No matching skill means refusal

**Decision.** When a request falls within a shipped stage but no skill covers the requested work, name the available boundary and generate no substitute artifact.

**Why.** A lifecycle map is not permission to improvise missing capabilities. Refusal keeps the public surface honest and prevents the router from laundering generic model output through a verification-first brand.

**Trade-off.** The user may receive less output. That is intentional: a visible capability gap is safer and more actionable than an artifact with no defined gate.

**Evidence.** The no-skill branch is part of the [`/pm` routing logic](../.claude/skills/pm/SKILL.md) and has a known-answer case in the [`/pm` fixtures](../tests/pm/fixtures.md).

## 6. Reviewer personas are advisory, not approval authorities

**Decision.** Use seven reviewer personas as bounded challenge lenses. They cite the line they attack or name a gap, never rewrite the artifact, and never issue organizational approval.

**Why.** Engineering, design, executive, skeptic, customer, data-analyst, and legal lenses make common objections inspectable without pretending that a simulated persona has real authority, context, or accountability.

**Trade-off.** Personas can surface questions but cannot represent the actual stakeholder. Legal review is explicitly a flag for counsel, not legal advice; every persona can miss issues outside its lens or the supplied context.

**Evidence.** Persona prompts live in [`.claude/agents/`](../.claude/agents/) and share a line-citation contract in the [reviewer-persona fixtures](../tests/reviewer-personas/fixtures.md).

## Ownership of the decisions

The repository and merged history support the decisions above. They cannot supply Abhillash Jadhav’s personal motivation, the moments that changed his mind, or the trade-offs he would make again. Those claims are deliberately reserved for manual authorship in [WHAT_I_LEARNED.md](WHAT_I_LEARNED.md).
