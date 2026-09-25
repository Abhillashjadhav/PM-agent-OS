# PMOS installer closeout

**Result: existing PR #59 repair verified; no additional installer code change required by the observed cases.**

Source checked: `9d09327a4fca24d111f98e895874eed0f609aa5a`, tree `6f0c883b5ad84ae350e0384fef6e0ee4423d5fe8`.

| Check | Result |
| --- | --- |
| `python3 -B tests/test_install.py -v` | Exit 0, seven tests pass. Tests execute the real public CLI in disposable repository copies. |
| Same tests with only `scripts/install.py` replaced by its parent-commit version | Exit 1, six tests fail and one passes. This is retrospective RED evidence; the original implementation and tests were committed together. |
| `python3 -B tests/audit_repository.py` | Exit 0: 40 lifecycle skills, three supporting skills, seven reviewer personas. |
| Source-directory alias and target nested inside a source group | Both return exit 2 with `INSTALLATION BLOCKED`, unchanged source content, and no new target. |
| Invalid inventory and missing source group | Both return exit 2 before writing the target; source content remains unchanged. |

The seven existing cases prove clean installation, refusal without `--force`, explicit replacement, dangling destination links, directory destination links, direct source-target overlap, a destination parent link into the source, and safe replacement of a leaf link pointing to source. Source and referent content comparisons check the side effects, not just exit codes.

The four additional disposable checks use an unchanged copy of this source. For the alias case, `claude-home` links to the copy's `.claude`. For the nested case, the target is `.claude/skills/nested-target`. For invalid inventory, the last lifecycle entry is removed from the copy's `inventory.json`; for missing source, the copy's `.claude/agents` is removed. Each invokes `python3 -B scripts/install.py --target <case-target> --force`, expects exit 2, and compares source SHA-256 inventories before and after. `PYTHONDONTWRITEBYTECODE=1` is set for these probes.

Suite output (trailing whitespace trimmed) and structured results are retained in [prior-installer-tests.txt](prior-installer-tests.txt), [repaired-installer-tests.txt](repaired-installer-tests.txt), and [verification.json](verification.json).

Integration requirement: the installer invokes `tests/audit_repository.py` as a separate process and writes only after that audit succeeds. Re-run the existing seven tests on the combined PMOS branch after validator changes. No external execution engine is used by these installer checks. No skills, workflows, contracts, or frozen packets changed in this closeout.

Independent `/pr-review` remains required before any merge. These checks establish installer behavior for the tested paths; they do not establish live skill-routing or model-output quality.
