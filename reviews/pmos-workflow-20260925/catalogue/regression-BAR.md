# BAR: make regression verdicts exhaustive

1. **Existing path? Yes.** Correct regression-gatekeeper's existing verdict rules.
2. **Approved criterion/blocker? Yes.** The baseline requires all drift within bounds for SHIP but requires drift on at least two cases for INVESTIGATE; one outlier receives no verdict.
3. **Behavior change? Yes.** Incomplete evidence stays PENDING; complete evidence has ordered HOLD / INVESTIGATE / SHIP rules. Any out-of-bound case investigates unless its tolerance was explicitly approved before the run.
4. **Rejecting check first? Yes.** Commit the single-outlier, binary-failure, precedence, incomplete-evidence and explicit-tolerance fixtures before the instructions. These are source/specification witnesses, not an executed model run.
5. **Independently revertible? Yes.** Only this skill, its fixtures and this note change.
6. **New unrequested surface? No.** No runner, threshold default, model call or dependency is added.

Consistency follow-up: the legacy “automatic HOLD” hard rule also needs the
complete-run qualification. Extend the incomplete-evidence witness first so an
observed failure is reported and shipping blocked without inventing completion.
