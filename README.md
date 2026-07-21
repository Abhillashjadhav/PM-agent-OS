# PM-agent-OS

Product work should not advance because an AI produced a plausible artifact. It should advance only when the artifact passes the decision gate appropriate to that lifecycle stage.

PM-agent-OS is a verification-first product operating system for discovery, strategy, build, launch, and iteration. It does not replace product judgment. It makes that judgment explicit and inspectable: what evidence is required, what failure blocks the work, what remains a human decision, and what the system refuses to invent.

## The operating model

| Component | Responsibility |
| --- | --- |
| [Lifecycle router](.claude/skills/pm/SKILL.md) | `/pm` classifies the request, sequences covered work in lifecycle order, and passes only gated output downstream. |
| Stage-specific decision skills | Each skill handles a bounded product decision or artifact at discovery, strategy, build, launch, or iterate. |
| Precommitted binary gates | Each lifecycle skill states its pass/fail gates before its instructions. The host agent is instructed to repair a failed draft or return a failure report. |
| Planted failure fixtures | Every lifecycle skill has a fixture specification with a known failure its gate is expected to catch. Fixtures define behavior; they do not prove a model performed it. |
| [Reviewer personas](tests/reviewer-personas/fixtures.md) | Seven advisory lenses produce line-cited objections or named gaps. They never rewrite an artifact and are not approval authorities. |
| Deterministic repository validation | Offline checks validate inventory, paths, frontmatter, required sections, links, lint, Python compilation, and PR hygiene without model access. |
| Explicit no-skill refusal | If no shipped skill covers a request, `/pm` names the boundary and returns no improvised artifact. |

The [machine-readable inventory](inventory.json) records 40 lifecycle skills: 7 discovery, 6 strategy, 10 build, 5 launch, and 12 iterate. That count is evidence of lifecycle coverage, not the product proposition. `/pm`, `prd-first`, seven reviewer personas, and four root-level standalone utilities are outside the 40-skill lifecycle count.

## Install for Claude Code

Project-local use is the smallest install and preserves the native `.claude/skills/` and `.claude/agents/` layout:

```bash
git clone https://github.com/Abhillashjadhav/PM-agent-OS.git
cd PM-agent-OS
claude
```

To make the Claude Code assets available across projects, copy both skills and reviewer personas:

```bash
mkdir -p "$HOME/.claude/skills" "$HOME/.claude/agents"
cp -R .claude/skills/. "$HOME/.claude/skills/"
cp -R .claude/agents/. "$HOME/.claude/agents/"
```

The project-local layout and copy result were smoke-tested at file level; live model invocation is a separate behavioral check. See [Validation and evidence](docs/VALIDATION.md) for the tested boundary.

## Run one failure gate

Start Claude Code in the repository and invoke the strongest planted-failure case:

```text
/regression-gatekeeper Change: the summarizer system prompt now asks for shorter summaries. Golden set: 14 cases (9 pass-class, 5 fail-class, including F-4521 entity invention). No runs have happened. Proposed ship: Friday. Is it safe to ship?
```

The [fixture contract](tests/regression-gatekeeper/fixtures.md) requires the response to reject this shortcut:

> The edit only shortens output, low risk — ship Friday, run the goldens next week.

Before results exist, the only permitted status is `VERDICT: PENDING — no run, no verdict`. The output should instead specify all 14 cases against the baseline, precommit SHIP/HOLD/INVESTIGATE rules, and flag that the new “shorter summaries” requirement has no golden coverage. A captured failure reappearing is an automatic HOLD, regardless of the aggregate.

This is a live behavioral smoke test. The repository commits the input and expected properties, not a recorded model run or proof that every host/model combination will pass.

## One complete lifecycle

This example is an illustrative chain assembled from the current skill and fixture contracts; it is not a recorded end-to-end model run.

| Lifecycle handoff | Decision skill | Gate required before advancing | Gated output consumed next |
| --- | --- | --- | --- |
| Raw interview transcripts → synthesis | `interview-synthesizer` | Every pattern has at least two verbatim, attributed quotes; invented quotes fail. | Evidence-cited patterns |
| Synthesis → assumptions | `assumption-mapper` | Each assumption is explicit, risk-ranked, and tagged testable or untestable with a proposed test. | Load-bearing assumptions |
| Assumptions → strategy decision | `ai-feature-go-no-go` | One pivot criterion determines GO, NO-GO, or an exact GO-IF; supporting factors remain non-decisive. | A reversible decision with its flip condition |
| Strategy decision → build eval | `prd-to-eval` | Disqualifiers are binary gates; tradeable qualities use anchored scores; every criterion traces to the spec. | An executable evaluation contract |
| Build evidence → launch gate | `launch-checklist` | Every item has an owner and observable done condition; rollback has an owner and trigger. | An inspectable readiness artifact, not automatic approval |
| First prompt/model change → regression protection | `regression-gatekeeper` | Golden results and precommitted verdict rules must exist before any ship verdict. | SHIP, HOLD, INVESTIGATE, or PENDING with named evidence |

The chain’s rule is invariant: downstream work consumes only the gated output from the prior step. A gate can make a decision auditable; it cannot make the decision wise by itself.

## What is validated

| Claim or step | Current evidence | Status |
| --- | --- | --- |
| The inventory contains 40 lifecycle skills across five declared stage totals and seven persona paths. | `tests/audit_repository.py` | Structurally validated |
| Inventoried skill and fixture paths exist; frontmatter parses; required metadata and `Limitations` sections exist; README local links resolve. | `tests/audit_repository.py` | Structurally validated |
| All `SKILL.md` files meet repository trigger-language, name, length, and limitations rules. | `tests/lint_skill.py` and CI | Statically linted |
| Changed Python compiles; PRs pass whitespace, protected-path, and generated-output checks. | `tests/pr_quality_gate.py` and CI | Deterministically validated |
| A fixture exists for every lifecycle skill. | Inventory path audit | Structurally validated |
| `/pm` classifies and sequences a live request correctly. | Requires a recorded host/model run | Not behaviorally proven here |
| A skill catches its planted failure and withholds a failing artifact. | Requires executing each fixture against a named host/model/configuration | Not behaviorally proven here |
| Personas stay within their lens and cite every objection. | Requires live persona runs | Not behaviorally proven here |
| Another Agent Skills client reproduces Claude Code behavior. | Requires client-specific install, routing, tool, and output runs | Unverified |

The full evidence policy is in [docs/VALIDATION.md](docs/VALIDATION.md). Product rationale is recorded in [docs/PRODUCT_DECISIONS.md](docs/PRODUCT_DECISIONS.md), and implementation traceability is in [docs/ARCHITECTURE_DECISIONS.md](docs/ARCHITECTURE_DECISIONS.md).

## Runtime boundary

- **Claude Code-native orchestration:** project discovery under `.claude/skills/`, direct `/pm` invocation, reviewer subagents under `.claude/agents/`, and repository settings/commands use Claude Code conventions.
- **Portable Agent Skill assets:** the lifecycle skill directories use `SKILL.md` with core `name` and `description` metadata plus Markdown instructions, following the [Agent Skills format](https://agentskills.io/specification). They can be moved as assets to a compatible client.
- **Unverified runtime compatibility:** asset readability is not execution parity. Triggering, skill-to-skill routing, reviewer delegation, tool permissions, gate compliance, and output quality have not been behaviorally certified outside Claude Code. The `argument-hint` field and `.claude/agents/` layer are Claude Code-specific surfaces that another runtime may ignore or require adapters for.

## Complete lifecycle inventory

| Stage | Decision skills | Count |
| --- | --- | ---: |
| Discovery | interview-synthesizer · feedback-pattern-miner · assumption-mapper · competitor-teardown · opportunity-sizer · jtbd-framer · research-brief | 7 |
| Strategy | strategy-review · roadmap-reality-check · ai-feature-go-no-go · north-star-designer · build-buy-partner · pricing-tradeoff | 6 |
| Build | model-complexity-router · builder-validator · prompt-optimizer-loop · context-auditor · pm-context-system · prd-to-eval · prototype-first-workflow · rag-vs-agent-architect · latency-ux-tradeoff · unit-economics-stress-test | 10 |
| Launch | launch-checklist · gtm-brief · stakeholder-update · announcement-drafter · launch-retro | 5 |
| Iterate | eval-engine · llm-as-judge-designer · judge-calibration-auditor · golden-dataset-builder · failure-to-eval-capture · guardrail-designer · loop-designer · regression-gatekeeper · model-upgrade-evaluator · eval-vs-abtest-router · drift-monitor-designer · mcp-migration-auditor | 12 |
| **Total** | See `inventory.json` for paths and validation levels. | **40** |

## Authorship and limits

The product decisions and trade-offs are part of the work, not an anonymous prompt bundle. [Product decisions](docs/PRODUCT_DECISIONS.md) records what the system chooses and gives up; [What I learned](docs/WHAT_I_LEARNED.md) separates repository-derived facts from first-person sections that require Abhillash Jadhav’s manual review.

PM-agent-OS does not approve a roadmap, certify a launch, or replace research, engineering, design, legal counsel, or PM accountability. It exposes the criteria and evidence behind those decisions so a human can inspect, challenge, and own them.

Built by [Abhillash Jadhav](https://github.com/Abhillashjadhav).
