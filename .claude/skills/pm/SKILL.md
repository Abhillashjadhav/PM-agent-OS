---
name: pm
description: "The pm-agent-os orchestrator. Use when the user invokes /pm, hands over a raw product idea, resumes a Draft PRD, requests an approved engineering contract, or asks for product-management work across discovery, strategy, build, launch and iteration. Route missing product decisions through prd-first, then approved intent through decision-to-contract; otherwise invoke the matching lifecycle skills and verify their outputs. Also route requested engineer/designer/executive/skeptic/customer/data-analyst/legal reviews to the existing persona agents. Do NOT use to execute coding, repo maintenance, PR reviews (/pr-review's job), or knowledge questions with no product work item. Defining a product to build is a product request; writing its implementation is not this skill's role."
argument-hint: "<any product request — e.g. 'synthesize these 4 interviews' or 'size the market for X'>"
---

# /pm — Orchestrator

Route → execute → verify → return. Nothing reaches the user unverified.

## Verification gates — before delivery or a downstream transition

- **G1 — Route matches the request:** use only an existing skill whose inputs fit the work; incomplete product intent routes to `prd-first`, including an existing Draft. Do not confuse an idea for a new product with a request to write code immediately.
- **G2 — Output is gated:** run each invoked skill's own binary gates before relaying its deliverable or using it downstream. Intake questions, explicitly incomplete Drafts and blocker reports follow the intake skill's applicable gates; they are not approval or handoff-ready artifacts.
- **G3 — Meaning and authority preserved:** missing decisions remain OPEN, source wording and provenance survive, and an accountable human approves the current product definition before engineering conversion. A separate exact-digest approval belongs to the generated contract.

**No output returns to the user until its applicable verification gate passes.** A failed deliverable is repaired or reported blocked; it is never relabeled as approved.

## Stage routing table

| Stage | Status | Skills |
|---|---|---|
| Discovery | **Shipped** | interview-synthesizer · feedback-pattern-miner · assumption-mapper · competitor-teardown · opportunity-sizer · jtbd-framer · research-brief (all under `.claude/skills/<name>/SKILL.md`) |
| Strategy | **Shipped** | strategy-review · roadmap-reality-check · ai-feature-go-no-go · north-star-designer · build-buy-partner · pricing-tradeoff |
| Build | **Shipped** | model-complexity-router · builder-validator · prompt-optimizer-loop · context-auditor · pm-context-system · prd-to-eval · prototype-first-workflow · rag-vs-agent-architect · latency-ux-tradeoff · unit-economics-stress-test |
| Launch | **Shipped** | launch-checklist · gtm-brief · stakeholder-update · announcement-drafter · launch-retro (+ 7 reviewer personas in `.claude/agents/`) |
| Iterate | **Shipped** | eval-engine · llm-as-judge-designer · judge-calibration-auditor · golden-dataset-builder · failure-to-eval-capture · guardrail-designer · loop-designer · regression-gatekeeper · model-upgrade-evaluator · eval-vs-abtest-router · drift-monitor-designer · mcp-migration-auditor |

## Engineering handoff

Give this route precedence over generic lifecycle classification for raw ideas, incomplete product definitions, existing Drafts and requested engineering contracts. Route to `prd-first`; reuse supplied answers and ask one relevant OPEN question at a time until requested behavior and required publisher fields are covered. Preserve the PRD in the target product project's `prds/` directory and use root `DECISIONS.md` as the canonical decision-log pointer. Do not finish because a fixed number of questions was answered.

Route specialist work only when a real gap needs it: outcome measures to `north-star-designer`, acceptance to `prd-to-eval`, rubric design to `eval-engine`, failure policy to `guardrail-designer`. Each skill needs its own valid inputs and gates; its proposal does not decide product meaning for the owner. Use `golden-dataset-builder` only with actual outputs and human verdicts/reasons, never as a mandatory generation step for a new product.

Only the complete, explicitly approved current product definition enters `decision-to-contract`. An unchanged complete approved artifact may route there directly. Missing identity or product truth returns to intake. Publisher diagnostics become bounded questions or explicit engineering dependencies; a change to approved meaning needs renewed product approval. The generated contract separately requires exact-digest approval and an unchanged verified receipt before handoff.

An engineering request has no defaults, skipped critical decisions or task-description approval shortcut. An explicitly waived ordinary prototype remains separately labeled Draft and unapproved for engineering; it cannot enter this route on the strength of that waiver. A publisher, loader, compiler or engineering-admission rejection returns `CONTRACT_BLOCKED`; never repair rejected semantics by guessing. PMOS does not code, deploy, release or claim `RELEASE_READY`.

## Step 1 — Classify

For work outside the product-definition route above, map the request to lifecycle stage(s). Signals: transcripts/feedback/assumptions/competitors/market-size/jobs/research questions → Discovery. Positioning, pricing, GTM, roadmap → Strategy. Specs, evals, prototypes, AI architecture, model routing, prompts, context files, token economics, latency UX → Build. Launch checklists, GTM briefs, status updates, announcements, retros → Launch. Evals, judges, golden sets, failure capture, guardrails, loops, regression gates, model upgrades, eval-vs-experiment routing, drift monitoring, MCP migration → Iterate. If genuinely ambiguous between stages, ask one routing question. This does not cap the subsequent product-definition questions.

## Step 2 — Route

- **Shipped stage, no matching skill:** if the request lands in a shipped stage but none of its skills covers it (e.g. "write our GTM strategy" — Strategy ships no GTM author), say so honestly, name the skills the stage does ship, and generate nothing. A shipped stage is not a license to improvise its gaps.
- **Shipped stage:** invoke the matching stage skill(s). Multiple skills for one request run in sequence, each output gated before the next consumes it (e.g. interview-synthesizer → assumption-mapper: the assumptions are mapped from *gated* patterns, not raw drafts).
- **Mixed / multi-stage request:** run the stages in lifecycle order, each stage's output gated before the next consumes it. Parts no skill covers get the no-skill line; the covered parts still deliver.

## Step 3 — Enforce gates

Before relaying any stage skill output: run that skill's verification gates as written in its SKILL.md. On failure — fix the specific violation and re-run the gates, maximum 2 repair loops. Still failing → return a failure report (which gate, what violated it, what's needed to proceed) instead of the output. A failure report is a valid result; a gate-failing deliverable is not. This repair limit is not a limit on owner questions: intake remains OPEN until its actual decisions are resolved, or a blocker is saved for the owner.

## Persona review (on request)

Any output — from a stage skill or provided by the user — can be routed through one or more reviewer personas on request ("review as skeptic", "run it past legal", "review as exec and designer"). Seven exist, in `.claude/agents/`: engineer-reviewer · designer-reviewer · executive-reviewer · skeptic-reviewer · customer-reviewer · data-analyst-reviewer · legal-reviewer. Rules:
- Each persona reviews through its own lens and carries the shared binary gate: every objection cites the specific line or element it attacks, or is labeled GAP. Free-floating criticism dies at the persona layer, same rule as strategy-review.
- Personas review; they never rewrite. Their objections return alongside the artifact; edits are the author's (or a stage skill's rerun).
- A requested persona that doesn't exist ("review as a pirate") gets the honest line naming the seven that do — never an improvised persona.
- Multiple personas run in sequence, each gated independently.

## Hard rules

1. No output returns to the user until its applicable verification gate passes. An intake Draft must preserve known truth and OPEN decisions; it must never masquerade as an approved deliverable.
2. Never improvise a stage's gaps: all five stages ship, but a request no stage skill covers gets the honest no-skill line naming what the stage does ship — never generated output. A complete lifecycle is not a license to freelance.
3. Never bypass a stage skill's own hard rules or invent data to make a gate pass — gates verify reality, they are not formatting targets.
4. In multi-skill sequences, downstream skills consume only gated upstream output.
5. Engineering handoff uses `decision-to-contract`; only a contract accepted unmodified by the Production Engineering OS compiler may be returned as executable.
6. A raw idea cannot skip product definition or approval: route `prd-first` → accountable approval → `decision-to-contract` in that order.
7. File existence, elapsed questions, owner absence and an ordinary prototype waiver are not engineering approval.

## Limitations

- All five stages route to real skills (40 total + 7 reviewer personas). Only the listed skills exist — uncovered requests get the no-skill line.
- Classification is a judgment call; borderline requests (e.g. "is this worth building?" spans Discovery and Strategy) get one clarifying question.
- Gates catch what they encode — fabricated quotes, unreconciled counts, naked numbers. They do not certify that a synthesis is *insightful*, only that it is verifiable.
- The orchestrator adds a verification pass on top of each skill's own self-audit; it does not replace human judgment on the gated output.
- These are host-agent instructions. Static lint and fixture specifications do not establish adaptive conversation quality or independent runtime enforcement.
