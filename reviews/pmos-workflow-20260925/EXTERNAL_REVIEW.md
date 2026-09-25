# PMOS architecture review — 25 September 2026

Reviewer: Claude (Cowork). Repo: `Abhillashjadhav/PM-agent-OS`. Reviewed head: `review/pmos-closeout-20260925` @ `8f9768c` (42 commits ahead of `main` @ `27d0418`, 1 Sep). Companion checked read-only: `production-engineering-os`. No code changed, nothing pushed.

## Verdict

**Partially meets the goal. It does not meet it exactly.** The PM skill system and the test-only handoff work. The core promise (PMOS turns an owner-approved idea into a contract that PEOS can build a real product from) is not met yet, for three reasons:

1. A contract written the way the skill says gets rejected by the current PEOS compiler.
2. The handoff only works against an **unmerged** PEOS snapshot. Against PEOS `main` it crashes.
3. The planner's product definition is being written in the PEOS repo, not in PMOS.

## Goal used as the yardstick

I can't open other chats directly. The goal below is rebuilt from PMOS `CLAUDE.md`, PEOS `docs/v2-approved-product-decisions.md` (PD-01, PD-03, PD-11), the project doc `claude/peos-session-handoff-2026-09-25.md`, and PEOS `docs/ai-task-planner/`.

- **G1 Product authority.** PMOS owns product intent (PD-01). It asks the owner one question at a time, never invents behaviour, defaults or thresholds, and gets explicit approval.
- **G2 Executable handoff.** PMOS publishes an approved contract, bound to its digest, that PEOS accepts unmodified and builds from. The first proofs are the AI task planner and later the career assistant.
- **G3 PM operating system.** `/pm` routes requests to 40 lifecycle skills. No output reaches the user until its verification gate passes.
- **G4 Discipline.** Every unit passes the BAR gate, tests come first, the evidence is real, and a human merges.

## What I verified myself

| Check Result                                                 |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `tests/audit_repository.py`                                  | PASS: 40 lifecycle, 3 supporting, 7 personas                 |
| All `SKILL.md` lint                                          | PASS (47 files, including 4 orphan copies at the repo root)  |
| Unit tests (installer, validator, Beacon)                    | 23 of 23 pass                                                |
| Legacy intake vs PEOS `5c0f9e3` (which is on PEOS main)      | PASS                                                         |
| Current handoff vs PEOS `297a11d` (unmerged review snapshot) | PASS: TEST-ONLY RELEASE_READY / HALTED / CONTRACT_BLOCKED    |
| **Current handoff vs PEOS `main` (`dd4271b`)**               | **FAIL:** `ModuleNotFoundError: pmpe.evidence.release_gates` |

I did not run the screened adversarial probes (planted bytecode, forged ledgers). The earlier restriction still applies.

## Scorecard

| Goal Status Why        |                               |                                                                                                         |
| ---------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------- |
| G1 Product authority   | **Not met**                   | See F3, F4, F5                                                                                          |
| G2 Executable handoff  | **Not met for real products** | See F1, F2, F6                                                                                          |
| G3 PM operating system | Structurally met              | Gates are prompt-only and there is no recorded model-run evidence. `VALIDATION.md` admits this honestly |
| G4 Discipline          | Partially met                 | See F7, F8                                                                                              |

## Findings, most severe first

**F1 — The skill's contract shape fails the current compiler (blocker, engineering fix).**
`decision-to-contract/SKILL.md:56` defines `binary_release_gates` as `{id, description}`. The current PEOS compiler (`release_gates.py:91-96`) requires `acceptance_criterion_refs` and otherwise returns `RELEASE_GATE_UNBOUND`. The positive test passes only because `validate_contract.py:172` patches that field in. Your own "unbound" fixture is exactly what a model following the skill would produce. The tests prove the seam, but the instructions a model follows produce a rejected contract.

**F2 — The handoff depends on unmerged PEOS code (blocker, needs a sequencing decision).**
The CI `current-handoff` job pins PEOS `297a11d`, which exists only on review branches. PEOS `main` was last merged on 6 Sep. If PMOS merges first, its CI breaks. The PEOS R4 stack has to land first, or PMOS has to pin to whatever PEOS merges.

**F3 — The planner's product definition lives in the wrong repo (architecture, your decision).**
`docs/ai-task-planner/decision-register.json` (R1–R17, D2–D26) is on a PEOS branch. PEOS also hosts `pmpe contract draft` and the "PMOS guided experience" UI. Under PD-01, product intent is PMOS's. As it stands, PMOS is a prompt library plus a test harness for PEOS's publisher, and the product brain sits in the engineering repo.

**F4 — `prd-first` conflicts with the authority rule (high).**

- Line 117: vague answers → "proceed".
- Line 125: "TBD — define after first prototype".
- Lines 3, 12 and 130: "skip the PRD".

These allow exactly the defaults that the handoff forbids. They are fine for casual vibe-coding and wrong on the PEOS path. There is also no concept of an OPEN decision with no default, which the planner register needs.

**F5 — There is no defined flow from PRD to contract (high).**
`prd-first` collects about 8 fields. `decision-to-contract` needs about 20: North Star, leading metrics, guardrails, NFRs, risks, gates, rubric, golden cases, required approvals and APDs. The skill says "collect remaining bounded truth" but gives no question order. It also doesn't route to the skills that already produce those fields (`north-star-designer`, `guardrail-designer`, `golden-dataset-builder`, `prd-to-eval`). This missing wiring is what would make PMOS an operating system rather than a skill library.

**F6 — Only a `health` product can be expressed (high).**
The skill still allows only the `health` action. The one real product that went through the handoff (the task tracker, `docs/task-tracker-acceptance`) used a `bindings.json` / `Template` route that the skill doesn't describe. That packet and its frozen approval are also **not on the integrated head**. The planner's ACs (calendar writes, approvals, prompts) can't be expressed until this is aligned with PEOS W5 (the approved-bundle CLI).

**F7 — The integrated head is missing required pieces (medium).**

- `AGENTS.md`, which holds the BAR gate you required in both repos, is missing from the closeout head. It exists only on `docs/pmos-peos-bar-gate`.
- The closeout branch has no PR, so its combined CI has never run.
- Nothing has merged to `main` since 1 Sep. Four PRs (#59–#62) are ready. #57/#58 and #63–#66 are stalled.
- "Pushed" here means 12 or more open branches, not shipped work.

**F8 — The overhead is larger than the product (medium).**

- Of 113 changed files, about 8 are runtime code. The rest are evidence, BAR records and ledgers, including 22 committed `.pmpe/` run files.
- Four orphan skill folders sit at the repo root (`concise-rewriter`, `context-auditor`, `eval-rubric-generator`, `token-cost-estimator`). They aren't inventoried or installed, yet CI lints them.
- Several lifecycle skills share names with your account-level skills (`builder-validator`, `context-auditor`, `model-complexity-router`, `pm-context-system`, `prompt-optimizer-loop`), so triggering can be ambiguous.

**F9 — Beacon can't observe the core rule (low).**
The hooks record session start, prompt, stop and end markers only. They can't tell whether a gate passed or failed, which is the one thing G3 promises. They also don't fire when skills are installed globally and used in another project, such as the career assistant.

**F10 — The installer doesn't check for PEOS (low).**
`decision-to-contract` calls `pmpe`, but `scripts/install.py` never checks that it exists or which version is installed. In any project other than this one, the handoff fails at run time.

## Suggested priority (the calls are yours)

| # Work Type Unblocks  |                                                                                                                               |                       |        |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------ |
| 1                     | Add `acceptance_criterion_refs` to the skill's contract shape and `valid-answers.json`; make the test use the unpatched shape | Engineering           | G2     |
| 2                     | Merge order: land the PEOS R4 stack, then repin PMOS to a PEOS `main` SHA, then merge #59–#62 and the closeout                | **Decision D-A**      | G2, G4 |
| 3                     | Decide where product definition lives, then move the planner register into PMOS or record the exception                       | **Decision D-B**      | G1     |
| 4                     | Split `prd-first` into a casual mode and a strict PEOS mode (no TBD, no skip, OPEN decisions with no default)                 | **Decision D-C**      | G1     |
| 5                     | Add the PRD → contract field flow with routing to the existing skills                                                         | Engineering after D-C | G1, G2 |
| 6                     | Align `decision-to-contract` with the PEOS W5 bindings route; bring `task-tracker-v1` and `AGENTS.md` onto the head           | Engineering           | G2, G4 |
| 7                     | Clean-up: remove root orphans, check for PEOS in the installer, rename colliding skills                                       | Engineering           | G3     |

**Happy path once fixed:** idea → `/pm` → strict `prd-first` (one question at a time, OPEN decisions block) → field flow → publisher draft → you approve the digest → PEOS `main` compiles it unmodified → PEOS generates the planner.

**Candidate NSM for PMOS:** the share of owner-approved contracts that PEOS `main` accepts unmodified on the first submission, with a guardrail of zero invented product fields. Today this is 0 of 0 real products on `main`.

## Decisions needed

- **D-A:** Merge PEOS first and then PMOS, or keep PMOS pinned to the review snapshot until the planner proof exists?
- **D-B:** Should the planner decision register move to PMOS (PD-01 as written), or stay in PEOS as an approved exception?
- **D-C:** Should `prd-first` get a strict PEOS mode, or should the PEOS path go through `decision-to-contract` only?