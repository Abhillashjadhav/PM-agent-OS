# Architecture decisions and traceability

This document connects each product decision to its current implementation, fixture contract, inventory boundary, merged history, and validation level. A link proves where a decision is represented; it does not by itself prove live model behavior.

## Decision traceability

| ID | Decision | Code or configuration | Fixture contract | Inventory | Merged PR evidence | Validation boundary |
| --- | --- | --- | --- | --- | --- | --- |
| ADR-001 | One lifecycle router | [`/pm`](../.claude/skills/pm/SKILL.md) classifies, routes, sequences, gates, and refuses. | [`tests/pm/fixtures.md`](../tests/pm/fixtures.md) covers stage routing, multi-stage handoffs, full lifecycle, personas, and refusal. | The [lifecycle inventory](../inventory.json) supplies the 40 routes; `/pm` is intentionally outside that count. | [PR #1](https://github.com/Abhillashjadhav/PM-agent-OS/pull/1) introduced the router skeleton; [PR #46](https://github.com/Abhillashjadhav/PM-agent-OS/pull/46) completed all-stage routing. | File shape and links are static; classification, sequencing, and enforcement require [live runs](VALIDATION.md#what-requires-live-behavioral-execution). |
| ADR-002 | Five lifecycle stages | The router’s stage table maps discovery, strategy, build, launch, and iterate to bounded skills. | The full-lifecycle fixture requires each gated handoff in order. | [`inventory.json`](../inventory.json) records stage membership and 7/6/10/5/12 totals. | Discovery [#2](https://github.com/Abhillashjadhav/PM-agent-OS/pull/2)–[#8](https://github.com/Abhillashjadhav/PM-agent-OS/pull/8), Strategy [#10](https://github.com/Abhillashjadhav/PM-agent-OS/pull/10)–[#15](https://github.com/Abhillashjadhav/PM-agent-OS/pull/15), Build [#16](https://github.com/Abhillashjadhav/PM-agent-OS/pull/16)–[#25](https://github.com/Abhillashjadhav/PM-agent-OS/pull/25), Launch [#27](https://github.com/Abhillashjadhav/PM-agent-OS/pull/27)–[#31](https://github.com/Abhillashjadhav/PM-agent-OS/pull/31), and Iterate [#34](https://github.com/Abhillashjadhav/PM-agent-OS/pull/34)–[#45](https://github.com/Abhillashjadhav/PM-agent-OS/pull/45) are reflected in first-parent merge history. | Stage totals and paths are [deterministic](VALIDATION.md#automated-structural-checks); whether a request belongs to a stage is behavioral judgment. |
| ADR-003 | Gates before instructions | Each lifecycle `SKILL.md` places `Verification gates` before `Steps`; [`regression-gatekeeper`](../.claude/skills/regression-gatekeeper/SKILL.md) is representative. | Each inventoried fixture states known-answer properties for its gates. | Every lifecycle entry links one skill to one fixture. | The two-commit skill PR pattern is visible from [PR #2](https://github.com/Abhillashjadhav/PM-agent-OS/pull/2) through [PR #45](https://github.com/Abhillashjadhav/PM-agent-OS/pull/45); [PR #41](https://github.com/Abhillashjadhav/PM-agent-OS/pull/41) is the regression-gatekeeper example. | Section order is inspectable; [host compliance is not statically enforceable](VALIDATION.md#what-requires-live-behavioral-execution). |
| ADR-004 | Planted failures | Gates name the disqualifying behavior in skill instructions. | Every lifecycle fixture contains a planted-failure case; see [`regression-gatekeeper`](../tests/regression-gatekeeper/fixtures.md). | Fixture paths are mandatory for all 40 entries. | Skill PRs carry the fixture commit before the instruction commit; [PR #41](https://github.com/Abhillashjadhav/PM-agent-OS/pull/41) shows the strongest public example. | [Fixture existence](VALIDATION.md#fixture-specifications) is audited; catching the planted failure requires a named model run. |
| ADR-005 | Explicit no-skill refusal | [`/pm` Step 2](../.claude/skills/pm/SKILL.md) forbids improvising a shipped stage’s gaps. | `/pm` Inputs A and D expect refusal for uncovered GTM strategy authoring. | Inventory membership defines the covered surface. | [PR #1](https://github.com/Abhillashjadhav/PM-agent-OS/pull/1) introduced honest stage boundaries; [PR #46](https://github.com/Abhillashjadhav/PM-agent-OS/pull/46) retained refusal after all stages shipped. | The branch exists in instructions and fixtures; [live refusal behavior](VALIDATION.md#what-requires-live-behavioral-execution) is unproven without execution. |
| ADR-006 | Advisory reviewer personas | [Seven persona files](../.claude/agents/) enforce lens purity, line citation, no rewrite, and no authority claim. | [`tests/reviewer-personas/fixtures.md`](../tests/reviewer-personas/fixtures.md) defines shared and lens-specific expectations. | The inventory records seven persona paths separately from the 40 lifecycle skills. | [PR #32](https://github.com/Abhillashjadhav/PM-agent-OS/pull/32) added personas and routing; [PR #33](https://github.com/Abhillashjadhav/PM-agent-OS/pull/33) made the launch-stage route live. | Paths are audited; objection quality and lens adherence require [live runs](VALIDATION.md#what-requires-live-behavioral-execution). |
| ADR-007 | Deterministic repository validation | [`audit_repository.py`](../tests/audit_repository.py), [`lint_skill.py`](../tests/lint_skill.py), [`pr_quality_gate.py`](../tests/pr_quality_gate.py), and [CI workflows](../.github/workflows/) run without model credentials. | Fixtures are checked as referenced files, not executed test cases. | Inventory is the source for protected paths and declared totals. | [PR #48](https://github.com/Abhillashjadhav/PM-agent-OS/pull/48) added the current evidence boundary and deterministic checks. | [Structural and PR checks](VALIDATION.md#pull-request-checks) pass/fail deterministically; semantic behavior stays outside this layer. |
| ADR-008 | Claude Code-native host with portable skill assets | `.claude/skills/`, `.claude/agents/`, `.claude/settings.json`, and `.claude/commands/` form the native host surface. Core skill files use the Agent Skills `SKILL.md` shape. | Existing fixtures are host-agnostic specifications, but no cross-client runs are committed. | Inventory records asset paths and conservative validation levels, not runtime certifications. | [PR #48](https://github.com/Abhillashjadhav/PM-agent-OS/pull/48) corrected the installation and runtime claims. | Claude Code layout is documented and install-smoke-tested; [other runtimes remain unverified](VALIDATION.md#runtime-boundary). |

## Merged-history audit

The first-parent merge history on `main` shows one concern per skill PR across the lifecycle:

- Discovery: [PR #2](https://github.com/Abhillashjadhav/PM-agent-OS/pull/2) through [PR #8](https://github.com/Abhillashjadhav/PM-agent-OS/pull/8).
- Strategy: [PR #10](https://github.com/Abhillashjadhav/PM-agent-OS/pull/10) through [PR #15](https://github.com/Abhillashjadhav/PM-agent-OS/pull/15).
- Build: [PR #16](https://github.com/Abhillashjadhav/PM-agent-OS/pull/16) through [PR #25](https://github.com/Abhillashjadhav/PM-agent-OS/pull/25), with routing completed in [PR #26](https://github.com/Abhillashjadhav/PM-agent-OS/pull/26).
- Launch: [PR #27](https://github.com/Abhillashjadhav/PM-agent-OS/pull/27) through [PR #31](https://github.com/Abhillashjadhav/PM-agent-OS/pull/31), personas in [PR #32](https://github.com/Abhillashjadhav/PM-agent-OS/pull/32), and routing completed in [PR #33](https://github.com/Abhillashjadhav/PM-agent-OS/pull/33).
- Iterate: [PR #34](https://github.com/Abhillashjadhav/PM-agent-OS/pull/34) through [PR #45](https://github.com/Abhillashjadhav/PM-agent-OS/pull/45).
- Full lifecycle routing: [PR #46](https://github.com/Abhillashjadhav/PM-agent-OS/pull/46).
- Public evidence boundaries and deterministic validation: [PR #48](https://github.com/Abhillashjadhav/PM-agent-OS/pull/48).

A read-only history audit on 2026-07-21 found that the fixture-add commit is an ancestor of the skill-add commit for all 40 inventoried lifecycle skills. The same ordering holds for the `/pm` fixture before the orchestrator and the shared persona fixture before persona code. This is repository-history evidence of precommitment, not behavioral execution evidence, and the current CI does not enforce historical commit order.

## Surfaces outside the lifecycle count

The count of 40 is intentionally limited to the `lifecycle_skills` array in [`inventory.json`](../inventory.json). The following tracked assets are real but not counted as lifecycle decision skills:

- `.claude/skills/pm/` — lifecycle router.
- `.claude/skills/prd-first/` — supporting Claude Code skill.
- `.claude/agents/` — seven advisory reviewer personas.
- `concise-rewriter/`, `context-auditor/`, `eval-rubric-generator/`, and `token-cost-estimator/` — root-level standalone utilities, excluded from the `.claude` install and lifecycle inventory.

This boundary prevents “40 skills” from silently expanding to include orchestration, personas, or unrelated utilities.

## Runtime references

- Claude Code documents project skills at `.claude/skills/<name>/SKILL.md`, personal skills at `~/.claude/skills/`, direct `/skill-name` invocation, and its extensions to the open format: [Claude Code skills](https://code.claude.com/docs/en/skills).
- Claude Code documents custom subagents separately from skills: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents).
- The portable core format requires a `SKILL.md` with `name` and `description`: [Agent Skills specification](https://agentskills.io/specification).

See [VALIDATION.md](VALIDATION.md) for the exact boundary between structural evidence, fixture specifications, install smoke tests, and live behavioral execution.
