# PM-agent-OS

**A reusable product-management skill system for Claude Code—start with one decision, not a catalogue of prompts.**

PM-agent-OS helps product managers make AI product decisions explicit, reviewable, and evidence-aware across discovery, strategy, build, launch, and iteration. It contains 40 lifecycle skills, seven reviewer personas, and three supporting skills: the `/pm` orchestrator, `prd-first`, and `decision-to-contract`. New users should begin with one of the workflows below.

## Install safely

```bash
git clone https://github.com/Abhillashjadhav/PM-agent-OS.git
cd PM-agent-OS
python3 scripts/install.py
```

The installer validates the repository first and refuses to overwrite existing Claude skills or agents silently. To install into a temporary or custom Claude home:

```bash
python3 scripts/install.py --target /path/to/claude-home
```

Use `--force` only after reviewing reported conflicts.

Then open Claude Code and invoke `/pm`, or ask directly for a starter workflow.

## Start with these three jobs

### 1. Decide whether an AI feature should exist

Ask:

```text
Evaluate whether this AI feature should exist:

Customer problem: ...
Hypothesis: ...
Proposed workflow: ...
Evidence available: ...
```

The `ai-feature-go-no-go` workflow makes the problem, hypothesis, evidence, value, risks, economics, kill criteria, and unresolved assumptions explicit before the team commits to building.

**First useful result:** a decision record with `GO`, `HOLD`, or `NO-GO` reasoning rather than a feature brainstorm.

### 2. Turn a product requirement into an evaluation plan

Ask:

```text
Here is the requirement for our AI feature. Define how we will know it is good enough to ship.
```

The system routes through `prd-to-eval`, `eval-engine`, and `judge-calibration-auditor` to produce observable criteria, disqualifying failures, golden examples, judge-calibration requirements, and release gates.

**First useful result:** a reviewable evaluation contract connected to the feature requirement.

### 3. Re-test a failed idea after a model upgrade

Ask:

```text
A new model was released. Re-test this shelved idea against the failure that originally killed it.
```

The `model-upgrade-evaluator` converts release notes into hypotheses, reruns the original failure scenario, and keeps every verdict `PENDING` until run evidence exists.

**First useful result:** `MIGRATE`, `STAY`, `RESURRECT`, `STILL DEAD`, or `UNTESTED`—each tied to explicit evidence.

### 4. Hand an approved decision to engineering

Ask:

```text
Convert this explicitly approved product decision into a machine-checkable
Production Engineering OS contract. Do not infer missing actions or approval.
```

The `decision-to-contract` workflow preserves PMOS ownership of product intent while emitting an ID-keyed draft, obtaining human approval of its exact digest, and publishing a receipt-bound contract that the Production Engineering OS approval verifier and compiler can accept or reject without guessing.

**First useful result:** either an unmodified, receipt-bound, compiler-accepted contract with approval identity and coverage counts, or `CONTRACT_BLOCKED` with exact diagnostics.

## What makes this different

A generic prompt library gives you frameworks. PM-agent-OS tries to preserve the decision discipline around them:

```text
Customer problem
    ↓
Hypothesis and intended outcome
    ↓
Evidence and assumptions
    ↓
Alternatives and trade-offs
    ↓
North Star, leading metrics, and guardrails
    ↓
Decision, owner, kill criteria, and next evidence
```

The system is designed to expose contradictions such as:

- a solution that does not address the stated customer problem;
- a North Star that measures activity rather than outcome;
- a feature hypothesis with no falsifiable failure condition;
- a release recommendation without representative evaluation evidence;
- a model migration justified by release notes rather than reruns.

## Lifecycle coverage

| Stage | Skills | Typical decisions |
|---|---:|---|
| Discovery | 7 | problem validity, research sufficiency, opportunity framing |
| Strategy | 6 | prioritization, positioning, business case, platform leverage |
| Build | 10 | requirements, evaluation design, model and architecture choices |
| Launch | 5 | release gates, rollout, readiness, risk communication |
| Iterate | 12 | experiment analysis, failure review, model upgrades, learning loops |
| **Total** | **40** | reviewer personas are counted separately |

## Reviewer personas

Seven reviewer agents provide distinct perspectives:

- engineering;
- design;
- executive;
- legal;
- data;
- marketing;
- growth.

They are review perspectives, not an automatic consensus mechanism. The accountable PM still owns the decision.

## Repository structure

| Path | Purpose |
|---|---|
| `.claude/skills/pm/` | Lifecycle orchestrator |
| `.claude/skills/decision-to-contract/` | Approved product-decision handoff to Production Engineering OS |
| `.claude/skills/` | Individual decision skills |
| `.claude/agents/` | Reviewer perspectives |
| `tests/<skill>/fixtures.md` | Expected inputs, outputs, and failure cases |
| `inventory.json` | Machine-readable skill and reviewer inventory |
| `scripts/install.py` | Safe validated installer |
| `tests/audit_repository.py` | Offline structural integrity audit |
| `docs/VALIDATION.md` | Exact evidence and certification boundaries |

## Product principles

- Begin with the customer problem and decision—not a framework name.
- Require a hypothesis and measurable outcome before recommending a solution.
- Treat the North Star as an outcome, supported by leading indicators and guardrails.
- Surface contradictions among the problem, solution, metrics, evidence, and trade-offs.
- Keep evidence states explicit: observed, assumed, pending, or disproven.
- Do not let generated output replace accountable human product judgment.
- Prefer a small number of strong workflows over duplicated generic skills.

## Validation status

Validated mechanically:

- every declared skill and reviewer path exists;
- skill frontmatter and required sections are present;
- fixture specifications exist;
- README links and inventory totals are consistent;
- the public installation layout works from a clean checkout;
- installation refuses silent overwrites unless `--force` is explicitly supplied;
- the committed decision-contract fixture is accepted unmodified by a pinned Production Engineering OS compiler, while planted prose is rejected.

Not yet certified:

- behavioural quality of every skill across live model runs;
- portability beyond Claude Code;
- independent enforcement of every instruction-level gate;
- production outcomes from the complete 40-skill catalogue.

Fixture documents specify expected behaviour; they are not recorded behavioural model tests. The decision-contract compiler check proves cross-repository contract compatibility, not that a live model will always author a correct contract. See [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Verify without installing

```bash
python3 tests/audit_repository.py
```

## Contributing

Additions should solve a distinct product decision, declare an input/output contract, define failure modes, include a fixture specification, and update `inventory.json`. Avoid generic prompts that duplicate an existing workflow.

## License

MIT.
