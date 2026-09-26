# BAR: one shared decision log

1. **Existing path? Yes.** Extend `pm-context-system`; reuse root `DECISIONS.md`, already consumed by `prd-first` and `/review-pr`.
2. **Approved criterion/blocker? Yes.** Accepted architecture requires one shared decision log; the reviewed skill instead writes `context/DECISIONS.md` with no reconciliation.
3. **Behavior change? Yes.** New memory writes use the root log; old project files remain readable and unchanged until their specific reconciliation is approved.
4. **Rejecting check first? Yes.** Commit canonical-path, conflicting-history and no-silent-migration fixture witnesses before changing instructions. Baseline instructions direct the fresh-project witness to the wrong path; model behavior is not executed.
5. **Independently revertible? Yes.** This fixture/instruction pair affects only project-memory behavior.
6. **New unrequested surface? No.** No new setting, package, global installation, storage service or planner register.
