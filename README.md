# PM-agent-OS

**A reusable product-management skill system for Claude Code, covering discovery, strategy, build, launch, and iteration.**

The repository contains 40 lifecycle skills, seven reviewer personas, a `/pm` orchestrator, structural validation, and fixture specifications. It is designed to make product reasoning explicit and repeatable—not to replace PM judgment.

## Install in two minutes

```bash
git clone https://github.com/Abhillashjadhav/PM-agent-OS.git
cd PM-agent-OS
mkdir -p ~/.claude/skills ~/.claude/agents
cp -r .claude/skills/* ~/.claude/skills/
cp -r .claude/agents/* ~/.claude/agents/
python3 tests/audit_repository.py
```

Then invoke `/pm` in Claude Code.

## Start with these three workflows

### 1. Decide whether an AI feature should exist

Use `ai-feature-go-no-go` to make the customer problem, hypothesis, evidence, risks, economics, and kill criteria explicit before building.

### 2. Turn a product requirement into an evaluation plan

Use `prd-to-eval`, `eval-engine`, and `judge-calibration-auditor` to define observable quality criteria, golden examples, failure cases, and release gates.

### 3. Re-test a failed idea after a model upgrade

Use `model-upgrade-evaluator` to convert release notes into testable hypotheses and rerun the failure scenario that originally killed the idea. A verdict remains pending until evidence exists.

## Lifecycle coverage

| Stage | Skills |
|---|---:|
| Discovery | 7 |
| Strategy | 6 |
| Build | 10 |
| Launch | 5 |
| Iterate | 12 |
| **Total** | **40** |

The seven reviewer personas are separate from the lifecycle count.

## How the system is organized

- `.claude/skills/pm/` — lifecycle orchestrator.
- `.claude/skills/` — individual product-management skills.
- `.claude/agents/` — engineer, design, executive, legal, data, marketing, and growth review perspectives.
- `tests/<skill>/fixtures.md` — expected inputs, outputs, and failure cases.
- `inventory.json` — machine-readable skill and reviewer inventory.
- `tests/audit_repository.py` — offline structural integrity audit.
- `docs/VALIDATION.md` — exact evidence boundaries.

## Validation status

What is validated:

- every declared skill and reviewer path exists;
- skill frontmatter and required sections are present;
- fixture specifications exist;
- README links and inventory totals are consistent;
- repository integrity can be checked offline.

What is **not** yet certified:

- behavioural quality of every skill across live model runs;
- portability beyond Claude Code;
- independent enforcement of instruction-level gates;
- production outcomes from the complete 40-skill catalogue.

Fixture documents specify expected behaviour; they are not recorded behavioural model tests. See [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Product principles

- Begin with the customer problem and decision, not a framework name.
- Require a hypothesis and measurable outcome before recommending a solution.
- Treat North Star Metrics as outcomes, supported by leading indicators and guardrails.
- Surface contradictions among problem, solution, metrics, and trade-offs.
- Keep evidence status explicit: observed, assumed, pending, or disproven.
- Do not let model output replace accountable human product judgment.

## Verify the repository

```bash
python3 tests/audit_repository.py
```

The audit checks inventory, paths, metadata, fixtures, links, and declared totals. It does not execute a model.

## Contributing

Additions should solve a distinct product decision, include an explicit input/output contract, define failure modes, include a fixture specification, and update `inventory.json`. Avoid adding generic prompts that duplicate an existing skill.

## License

MIT.
