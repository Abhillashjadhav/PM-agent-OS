---
name: regression-gatekeeper
description: "Iterate-stage skill: gates any prompt or model change behind a golden-set regression run — the run happens and its results are shown before any ship verdict exists. Use when a change wants to ship — 'we tweaked the prompt, safe to ship?', 'regression plan before the model swap', 'gate this change', 'what has to run before this goes out' — or when /pm routes such a request here. Do NOT use to decide whether an upgrade is worth pursuing (model-upgrade-evaluator), to build the golden set (golden-dataset-builder), for post-incident capture (failure-to-eval-capture), or for regression-testing definitions."
argument-hint: "<the change (prompt diff / model swap) + the golden set that exists + the intended ship date>"
---

# Regression Gatekeeper

No run, no verdict. The golden set exists to be run before shipping — a ship opinion formed without results is the failure this skill exists to prevent.

## Verification gates (defined first; output is blocked until all pass)

- **G1 — Complete run before verdict:** a ship verdict (SHIP/HOLD/INVESTIGATE) appears only alongside comparable baseline/new results for every planned case. With no run or incomplete evidence, return the plan or missing-evidence report and `VERDICT: PENDING`; report observed failures without certifying the incomplete run.
- **G2 — Exhaustive rules pre-committed:** write ordered HOLD / INVESTIGATE / SHIP rules and explicit rubric bounds before results arrive. Any tolerance must be explicitly approved before the run, never inferred from the number of failing cases or added after seeing results. Binary gate failures are not tolerable rubric drift.
- **G3 — Per-case results + scope honesty:** results are shown as a per-case table (id, class, baseline, new, delta), never only an aggregate; the plan states what the golden set does NOT cover, and changes introducing new requirements with zero golden coverage get flagged for case collection before they can be gated.

## Steps

1. **Bank the change and the set:** what changed (prompt diff, model version), the golden set's size and class split (pass-class / fail-class), and whether baseline outputs are stored — if not, the plan runs both sides on the same cases.
2. **Write the run plan:** every golden runs on the changed configuration; fail-class assertions must hold; pass-class gates must pass with rubric scores within the stated bounds of baseline. Name the criterion, direction and bound for each scored check and any explicit pre-run tolerance/approval. Missing bounds or approval are questions in the plan, not invented numeric defaults.
3. **Pre-commit exhaustive verdict rules**, in this order: incomplete run/comparison evidence or missing pre-run rules → PENDING; otherwise any fail-class case reintroducing captured bad behavior → HOLD; otherwise any pass-class binary gate failure or any rubric result outside its approved bounds/tolerance → INVESTIGATE; otherwise → SHIP within the covered scope. One out-of-bound case is sufficient. Never invent a minimum count of outliers, and never let a rubric tolerance excuse a binary gate failure.
4. **Check coverage against the change's intent.** A change made FOR a new requirement (shorter summaries) that has zero golden coverage cannot be certified for that requirement — flag it, route 2–3 new human-verdicted cases to golden-dataset-builder, and say the gate covers regressions only until they exist.
5. **On results: apply the rules as written.** Produce the per-case table with each gate result, rubric delta, approved bound and verdict contribution. Apply the ordered rules and name every failing/out-of-bound case. A proposed rule change cannot turn this run green: retain HOLD when a captured failure recurs, otherwise INVESTIGATE an out-of-bound result; record proposed changes for approval before a future run, never edit this run's rules in flight.
6. **Gate pass.** No verdict without results (G1), rules pre-committed and unedited (G2), table + coverage statement present (G3). Fix and re-run; maximum 2 repair loops, then report the failure.

## Output format

```
REGRESSION GATE: summarizer prompt change (shorter summaries) · golden set: 14 (9 pass / 5 fail-class)
RUN PLAN: all 14 on changed prompt; baseline = current prod prompt, same cases (both
sides run — no stored baselines). Pass criteria: fail-class assertions hold (incl.
F-4521 entity-invention); pass-class gates pass. Supplied owner-approved rubric
bound for this example: ≤1pt per case; no additional tolerance.
VERDICT RULES (pre-committed, ordered): incomplete evidence → PENDING;
otherwise any fail-class bad behavior reintroduced → HOLD;
otherwise any pass-class gate failure or >1pt drift on ANY case → INVESTIGATE;
otherwise → SHIP within covered scope.
COVERAGE FLAG: "shorter summaries" has 0 golden coverage — the set gates regressions,
not the new requirement; 2-3 length-verdicted cases needed (→ golden-dataset-builder).
VERDICT: PENDING — no run, no verdict.
[after the run: per-case table — id · class · baseline · new · delta — then the
verdict per the rules above, failing cases named]
GATE CHECK: G1 pass (no unrun verdict) · G2 pass (rules pre-committed) · G3 pass
```

## Hard rules

1. No ship verdict without complete, comparable results in hand. "Low risk" reasoning postpones the run; it never replaces it.
2. Verdict rules are written before results and never edited mid-flight. Out-of-bound results retain HOLD/INVESTIGATE under the ordered rules; future rule-review proposals do not approve this run.
3. A reintroduced captured failure is an automatic HOLD — the golden set's fail-class cases are non-negotiable tripwires, whatever the aggregate looks like.
4. The gate certifies only what the set covers; uncovered requirements are named, not waved through under a green aggregate.

## Limitations

- The gate is as strong as the golden set; a thin set produces an honest-but-narrow certification, said explicitly with the coverage statement.
- This skill plans and adjudicates the run; executing 14 cases through the pipeline is operational work (the run plan is written to be executable by hand or CI).
- Rubric-drift bounds involve judge scoring and inherit judge calibration state — a stale judge widens error bars; recalibrate (judge-calibration-auditor) before high-stakes gates.
- Behavioral regressions outside the golden set's captured space are invisible here; production drift monitoring (drift-monitor-designer) is the complementary net.
