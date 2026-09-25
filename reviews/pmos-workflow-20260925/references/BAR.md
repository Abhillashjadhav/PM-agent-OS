# PMOS reference restoration BAR

Unit: restore the existing owner operating instructions and immutable historical task-store reference requested by external review F7 and the accepted PMOS workflow architecture. No runtime implementation or new acceptance claim is introduced.

1. **Existing path? Yes.** Reuse exact `AGENTS.md` from `5d79b20cc16703cb8fd6fa98040659db8881c579` and `reviews/task-tracker-v1` from `33a35962d13fb13163d61beb938f9e593a742197`; create no replacement contract or evaluator.
2. **Approved criterion or reproduced blocker? Yes.** Accepted F7 requires these references to be present; neither path exists at branch base `bee295cacd882f8a7fb4a5c306f2774b0cd3919a`.
3. **Changes existing behavior? Yes, repository instructions only.** Restoring `AGENTS.md` makes the already owner-supplied BAR rule discoverable at repo root. It has its own branch and commit; the historical packet is restored separately and is archival data only.
4. **Failing-before/passing-after check? Yes.** Commit a static reference checker and source manifest before restoration; require absent paths to fail and exact bytes, Git blob IDs, file modes, and inventory to pass afterward.
5. **Independently revertible? Yes.** Operating-instruction restoration and packet restoration are separate commits. Root `BAR.md` and all runtime/skill files remain unchanged.
6. **Unrequested setting/dependency/surface? No.** No dependencies, settings, runtimes, approvals, or new execution routes. Only read/hash checks and inert Python compilation are permitted.

Do not run the historical evaluator, renderer, reproduction commands, or fixtures. Do not execute restricted bytecode or forged/re-chained ledger/context probes. No PEOS code access, remote writes, merges, or deployment.
