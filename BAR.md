# BAR — PMOS validator closeout, 2026-09-25

Scope: finish the existing PR #60 validation repair; PMOS only.

1. **Does this already exist in either repository? Yes.** Reuse and extend `tests/yaml.py` and `tests/test_validation_regressions.py`; no parallel validator is added and PEOS is outside this workstream.
2. **Approved criterion or reproduced blocker? Yes.** On base `0504e07a3f6797085fef2183d6bdcdf9106cc957`, both lint and repository audit accept `description: [Use when needed., Do NOT use otherwise.]` even though skill descriptions must be scalar strings.
3. **Changes existing behavior? Yes.** The scalar-only loader will reject unquoted flow collections; quoted descriptions and all 43 existing installed skills must continue passing. This repair has its own branch and regression.
4. **Automated RED then GREEN? Yes.** Commit the collection-description regression before changing the loader, record the observed failure, then run the same check after the narrow fix.
5. **Independently revertible? Yes.** The added input rejection, its regression, and this evidence form one bounded validator concern.
6. **Unrequested setting, dependency, or extension? No.** No new options or dependencies; preserve the existing scalar-only frontmatter contract.
