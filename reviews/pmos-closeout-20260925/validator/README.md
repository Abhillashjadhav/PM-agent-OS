# PMOS validator closeout

Base: `0504e07a3f6797085fef2183d6bdcdf9106cc957` (PR #60).
Implementation: `ffa1e3af86ed71ee7a2a80f1d7a284eea68d2406`.
Implementation tree: `ec90dd59a13299c22724c8d11ec45de1b885234f`.

## What changed

The existing scalar-only frontmatter loader accepted a YAML collection as a string.
For example, `description: [Use when needed., Do NOT use otherwise.]` passed both
skill lint and the repository audit, although descriptions must be strings.
The loader now rejects unquoted flow collections. Quoted descriptions containing
the same brackets remain valid. No skill, installer, contract, or workflow changed.

## Test-first evidence

1. Base checks: all 7 existing validation regressions, inventory audit, and lint
   for all 43 installed skills passed.
2. Test commit `36050d2f13cc30937d349662ec9fbab345a2d8ea` added the failing
   collection-description regression and a quoted-string positive case. Running
   `python3 -B tests/test_validation_regressions.py
   ValidationRegressions.test_collection_description_cannot_bypass_string_requirement -v`
   exited 1: both lint and audit wrongly exited 0.
3. Fix commit `ffa1e3af86ed71ee7a2a80f1d7a284eea68d2406` added the two-line rejection.
   `python3 -B tests/test_validation_regressions.py -v` passed all 9 tests.
4. `python3 -B tests/audit_repository.py` passed: 40 lifecycle skills, 3 supporting
   skills, and 7 reviewer personas.
5. `PYTHONPYCACHEPREFIX=/tmp/pmos-validator-closeout-cache python3 -B
   tests/pr_quality_gate.py --base-ref 0504e07a3f6797085fef2183d6bdcdf9106cc957`
   passed, including all 47 SKILL.md files and syntax compilation of changed Python.
6. `git diff --check` passed.

The existing regression suite also rejects unquoted mapping separators, boolean
descriptions, duplicate inventory substitutions, noncanonical skill paths,
unlisted installable skills, and frontmatter/inventory name mismatches.

## Limits

These are local structural and fixture checks, not live-model behavioral evidence
or a general YAML compliance claim. The existing scalar-only grammar remains in
place. PEOS was neither inspected nor modified. No screened bytecode or release
evidence probe ran. Independent review, publication, and any merge decision remain
with the coordinating workstream; this branch has not been remotely published.
