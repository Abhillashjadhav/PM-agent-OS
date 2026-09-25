# Catalogue source-contract closeout

Implemented the accepted catalogue corrections on
`fix/pmos-catalogue-flow-20260925`, based on `bee295c`.
Source/fixture state checked: `9081494488e5908a8cefe6ade90653593b5601e9`, tree
`1cef44b4ca716b246bd6e6643593d18d451ad67c`. This receipt follows that checked state.

## Concern history and source resolution

Each instruction change follows its rejecting fixture/specification commit.
These commits remain separately reviewable and revertible by concern.

| Concern | Fixture/BAR commit | Instruction commit | Source resolution and witness |
| --- | --- | --- | --- |
| Shared decision memory | `550f740` | `07aefee` | Root `DECISIONS.md` is canonical; INDEX points there. Legacy records remain readable; each transfer/conflict resolution needs specific approval and preserves history. Scenarios E/F cover conflicting/legacy-only logs. |
| Golden identity and capture provenance | `71fc8d4` | `04c92a7` | Full input/output/criterion identity, retained review/export records, distinct record/case counts. Missing/disputed human labels quarantine; capture includes observed scrubbed output and the consumer's provenance. IDENTITY-1/2, CONFLICT-1, HANDOFF-1 and capture privacy/incomplete witnesses cover the boundaries. |
| Exhaustive regression verdict | `b18b60e` | `f17e22b` | Complete runs use ordered HOLD / INVESTIGATE / SHIP; one out-of-bound case investigates unless explicit tolerance was approved before the run. Incomplete evidence stays PENDING. ONE-OUTLIER and EXPLICIT-TOLERANCE distinguish the formerly undefined result. |
| Independent decision blockers | `4665aa4` | `8e0733e` | Rank a primary blocker while retaining every independently failed requirement. A quality-plus-budget witness remains NO-GO when only either one is fixed; the reversal set must address both. |
| Compact score visibility | `9d20a33` | `0cdee26` | Compact recommendations show all four named scores/bases and their sum. The total-only compact counterexample fails the source contract. |
| GTM channel/staffing evidence | `a8a0d45` | `9faf3f4` | Missing motions/staffing produce a gap/question. Three stalled deals do not establish self-serve availability or four salespeople. |
| Retro decision evidence | `56930e1` | `c4959e3` | Missing pre-launch evidence produces UNDETERMINED; later navigation tickets do not prove a BAD decision or exact causal cost. Paired witnesses keep the outcome fixed and vary contemporary evidence. |
| Shipped catalogue references | `36b68fc` | `c8f01c0` | PRD negative triggers point to existing `prd-first`; positioning excludes teardown by actual scope; announcement-drafter recognizes available `legal-reviewer` as flags for counsel, not legal approval. |

Two consistency follow-ups retain those same concerns:

- `0accdcd` adds the incomplete-run-with-observed-failure fixture before `1359ca0`
  qualifies the regression hard rule. Shipping remains blocked while PENDING;
  no complete-run verdict is invented from a subset.
- `9081494` aligns the existing staged-rollout counterexample with the retro's
  missing-evidence rule. The caught bug and delay are outcomes, not substitutes
  for the absent prior tradeoff record. No instruction change was needed.

## Verification performed

On 25 September 2026, at the source/fixture state above:

- `python3 -B tests/lint_skill.py <path>` passed all nine lint checks for each of
  the nine changed SKILL.md files and for the three additional skills whose
  negative-trigger fixtures changed: **12 skills checked**.
- `PYTHONPYCACHEPREFIX=/workspace/scratch/b6efdedb2992/pmos-catalogue-pycache python3 -B tests/pr_quality_gate.py --base-ref bee295c`
  exited **0**, reporting `PASS repository audit: 40 lifecycle skills, 3 supporting skills, 7 reviewer personas`
  and `PASS deterministic PR quality gate`. This runs static audit/lint/whitespace
  checks; it does not execute the Markdown fixtures or call a model.
- `git diff --check` passed before each commit. The worktree was clean after the
  source/fixture commits. The coordinator independently reviews the assembled tree
  and controls publication.

Changed instruction paths: `ai-feature-go-no-go`, `announcement-drafter`,
`failure-to-eval-capture`, `golden-dataset-builder`, `gtm-brief`, `launch-retro`,
`model-complexity-router`, `pm-context-system`, `regression-gatekeeper`, each under
`.claude/skills/<name>/SKILL.md`. Additional fixture-only skills:
`assumption-mapper`, `competitor-teardown`, `jtbd-framer`.

## Limits

The rejecting examples and closure table are source/specification witnesses.
They document concrete contradictions and the intended corrected behavior; they
are **not executed model tests**. Lint, path counts and fixture presence do not
certify routing, privacy scrubbing, judgment quality or instruction adherence.
Supervised model execution and fresh-product delivery remain unverified here.

PENDING, quarantine and disclosed UNDETERMINED outputs remain valid honest process
results. They do not grant product approval, establish a complete dataset, or
certify an uncovered requirement. No project memory/data files were migrated,
no model was switched, and no dataset/CI destination was updated by this work.
Edits are limited to the owned catalogue instructions, fixtures and these review
notes; there were no remote writes or runtime/installer/dependency changes.
