# PMOS handoff closeout — 25 September 2026

The current PMOS handoff is already implemented and passes the permitted ordinary
compatibility checks. This unit found no new PMOS code defect requiring a repair.
It changes evidence records only; PEOS remains separately owned.

## Exact scope checked

- PMOS commit: `c95469338b64f22edcd9d260246e3c9186b0d302`.
- PMOS tree: `59703d2980477e1321441bf3c440888cfa90fdc7`.
- Existing dependency pin installed as a black box:
  `297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6`.
- Python 3.12.14; only the existing declared requirements were installed into
  an isolated verification environment. No repository dependency was changed.

The recovered PMOS code includes current-run compatibility, deriving retained
state/cause/call count from ledger contents, and the read-only inspection CLI.
Its current-run dependency pin is already separate from the historical intake
pin. No implementation was duplicated and no PEOS source was reviewed or changed.

## Results

| Check | Observed result |
| --- | --- |
| Fixed valid health program | `RELEASE_READY`; gate `PASS`; two fixture calls |
| Fixed broken health program | `HALTED`; gate `FAIL`; one fixture call |
| Missing criterion binding | `CONTRACT_BLOCKED`; zero fixture and execution calls |
| Four explicitly selected existing tests | All passed |
| Missing inspection directory | Exit 3, `EVIDENCE_INVALID`, no writes |
| Malformed contract JSON | Exit 3, `EVIDENCE_INVALID`, no writes |

The selected tests cover the ordinary entrypoint and submitted receipt bytes,
reading state and call count from retained events, read-only inspection of the
unchanged positive and broken packets, and rejecting a head argument outside
inspection mode. Exact commands and logs are stored beside this report.

`ordinary-fixtures.tar.gz` retains all 29 files from the new fixture run,
including the complete ledgers. Its SHA-256 is
`1c714bdf7313aab999754350ef3c7dcd5baa1592a13431382f007739efbfd3fc`.
The package contains TEST-ONLY programs and synthetic test-issued approvals.
No model or external service was called. The initial missing-package error was
an environment setup issue, not evidence of a PMOS behavior regression.

## Limits and publication constraint

These ordinary fixtures establish PMOS compatibility with its existing pinned
dependency. They do not establish new model generation, owner approval, release
authorization, deployment, or a PEOS security verdict. Printed runtime heads are
capture evidence; storing a head beside the packet does not create an independent
trust anchor.

The prior automatic security screening stopped planted-bytecode execution and
forged/re-chained ledger or context rechecks. Those checks were not executed here
and remain unverified. Full test discovery was not run.

The current `.github/workflows/repository-audit.yml` invokes full discovery of
the handoff tests on `pull_request`, including the restricted ledger probes.
Opening or updating a PR on this source would therefore start those probes.
Publish this result on a review branch while that restriction remains unresolved;
do not disable CI or use remote CI to substitute for the blocked execution.

The integration owner should compare the four PMOS source digests in
`verification-metadata.json` with the final PMOS branch before attributing these
results to it. The frozen historical intake artifacts were left unchanged.
