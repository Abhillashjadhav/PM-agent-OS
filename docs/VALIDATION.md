# Validation and evidence

PM-agent-OS makes four distinct evidence claims. They must not be collapsed into “all skills are tested.”

## Evidence levels

| Level | What the repository can show | What it cannot show |
| --- | --- | --- |
| Deterministic structure | Counts, paths, parseable frontmatter, required sections, links, lint rules, Python compilation, protected inventory paths, and PR hygiene. | Whether a model understood or followed the instructions. |
| Fixture specification | Representative inputs, should-fire/should-not-fire phrases, expected output properties, and a planted failure for each lifecycle skill. | Whether a host/model run produced the expected output. |
| Recorded behavioral execution | A named runtime, model, configuration, input, raw output, evaluator, and result committed as reproducible evidence. | Generalization beyond the recorded configuration. |
| Runtime compatibility | Installation, discovery, invocation, delegation, tool use, and fixture runs on a named client/version. | Compatibility with clients or versions that were not run. |

The repository currently provides deterministic structural evidence and fixture specifications. It contains no committed behavioral model-run corpus and no certified cross-runtime matrix.

## Automated structural checks

Run the offline repository audit from the repository root:

```bash
python3 tests/audit_repository.py
```

It verifies:

- `inventory.json` parses.
- The lifecycle inventory contains 40 entries with stage totals of 7 discovery, 6 strategy, 10 build, 5 launch, and 12 iterate.
- The inventory contains seven reviewer-persona paths.
- Every inventoried skill and fixture path exists.
- Inventoried skills have parseable scalar YAML frontmatter, a kebab-case name, a non-empty description, and a `Limitations` section.
- README-local Markdown links resolve.

It does **not** inspect the semantic quality of gates or fixtures, execute a fixture, run a model, or validate another runtime.

Run the static lint for every tracked skill file:

```bash
find . -name SKILL.md -not -path './.git/*' -print0 | while IFS= read -r -d '' skill; do
  python3 tests/lint_skill.py "$skill"
done
```

The lint checks frontmatter, naming, trigger and no-trigger language, description size, file length, and a limitations marker. The repository contains 46 tracked `SKILL.md` files: 40 lifecycle skills, `/pm`, `prd-first`, and four root-level standalone utilities. Only the 40 lifecycle entries are the product coverage count.

Compile the repository’s Python validation code:

```bash
python3 -m py_compile \
  tests/audit_repository.py \
  tests/lint_skill.py \
  tests/pr_quality_gate.py \
  tests/yaml.py
```

Compilation proves only that these Python files parse and compile. It does not compile Markdown instructions or execute fixture semantics.

## Pull-request checks

Two workflows are intentionally deterministic:

- [`repository-audit.yml`](../.github/workflows/repository-audit.yml) runs the repository audit, lints all `SKILL.md` files, and compiles the Python validation files on pull requests and pushes to `main`.
- [`pr-review.yml`](../.github/workflows/pr-review.yml) runs [`pr_quality_gate.py`](../tests/pr_quality_gate.py) on non-draft, same-repository pull requests. It adds whitespace checks, changed-Python compilation, protected-path deletion checks, and rejection of generated/runtime output.

The `PR Review Agent` job name is historical; the current required check does not call a model or require provider credentials. A draft PR does not run that non-draft job, while the repository-audit workflow still runs on the draft.

## Fixture specifications

Each lifecycle skill has `tests/<skill>/fixtures.md` with three intended gates:

1. Static lint command.
2. Should-fire and should-not-fire trigger examples.
3. A known-answer input with expected output properties and at least one planted failure.

The automated audit validates that the referenced fixture file exists. It does not parse those three sections or run them. A fixture demonstrates that expected behavior was pre-specified; it does not demonstrate model compliance.

The current git history adds the fixture before the corresponding skill for all 40 lifecycle skills. That ordering was audited from commit ancestry on 2026-07-21; it is not currently a CI rule.

## What requires live behavioral execution

The following claims require recorded runs against a named host, model, version, configuration, and evaluator:

- `/pm` selects the correct lifecycle stage and skill for should-fire and should-not-fire inputs.
- Multi-stage work consumes only gated upstream output.
- The no-skill branch refuses instead of improvising.
- A lifecycle skill catches its planted failure within the allowed repair loops.
- A reviewer persona stays inside its lens, cites each objection or labels a gap, and does not rewrite.
- The regression gate withholds a ship verdict until results exist.
- The same behavior repeats across models, sessions, or runtime upgrades.

No committed evidence currently supports “every skill is behaviorally proven.” Use “fixture-specified,” “structurally validated,” or “behaviorally run on `<runtime/model/config>`” only when the corresponding evidence exists.

## Installation evidence

The README has two Claude Code paths:

1. **Project-local:** clone the repository, enter it, and start `claude`. Claude Code officially discovers project skills under `.claude/skills/` and project subagents under `.claude/agents/`.
2. **Personal copy:** copy `.claude/skills/.` to `~/.claude/skills/` and `.claude/agents/.` to `~/.claude/agents/`.

The 2026-07-21 smoke test on macOS used Git 2.50.1 and Claude Code 2.1.212. It verified that the clone URL resolves, the project layout contains 42 Claude Code skill directories and seven reviewer-persona files, and the personal-copy commands reproduce those source trees byte for byte in an isolated temporary directory.

This is file-level installation evidence. It does not establish authentication, model access, automatic trigger accuracy, `/pm` routing behavior, persona delegation, or successful completion of a live request on another machine.

## Runtime boundary

### Claude Code-native orchestration

The following depend on Claude Code conventions:

- Project and personal discovery at `.claude/skills/` and `~/.claude/skills/`.
- Direct slash invocation such as `/pm`.
- Reviewer subagents under `.claude/agents/`.
- `argument-hint` frontmatter and repository `.claude/settings.json`/`.claude/commands/` surfaces.

### Portable Agent Skill assets

The 40 lifecycle directories contain a `SKILL.md` with the Agent Skills core fields (`name`, `description`) and Markdown instructions. This makes them portable assets in the open format. The repository lint checks those core fields, but the official `skills-ref` validator was not part of the current check suite.

### Unverified compatibility

Another Agent Skills client may read the skill assets while ignoring Claude Code extensions or lacking equivalent skill-to-skill routing and subagents. No non-Claude runtime has committed install and behavioral evidence in this repository. Do not claim Codex, Cursor, Windsurf, or any other client as supported until that client’s discovery, routing, gate, persona, and fixture behavior is recorded.

## Evidence required to upgrade a behavioral claim

A future behavioral record should commit:

- runtime/client and version;
- model identifier and relevant settings;
- exact skill revision and input fixture;
- raw output, including repair loops;
- deterministic checks and/or named human evaluator rubric;
- pass/fail result and reason;
- date and known limitations.

Until then, the correct public claim is: PM-agent-OS is structurally validated and fixture-specified; its gates are instructions interpreted by the host agent, not an independent enforcement runtime.
