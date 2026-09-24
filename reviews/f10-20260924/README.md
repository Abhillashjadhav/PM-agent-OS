# F-10 current-run compatibility evidence

This packet is **TEST-ONLY deterministic integration evidence**. The fixture
issuer is `test-only-fixture-issuer`; its receipt is not product-owner approval.
No external model was called, no new live candidate was generated, and no
deployment or release was authorized. Fixed health programs ran in local
processes; this check does not establish OS isolation.

## Reproduced gap and test order

The original PMOS validator returned success after legacy `assessment`
admission. It made zero calls to `run_to_release_ready`. The regression was
committed first in `c036163`; `red-before-current-run.txt` records that failure.

A second regression in `06d4362` checks that the bytes submitted to the runner
are exactly the retained receipt file, including its serialization. It initially
caught a reconstruction that omitted the publisher's final newline; the fixture
now reads the original file bytes. `red-submitted-receipt-bytes.txt` and
`green-current-run.txt` retain the failing and corrected checks. Each reproduced
failure passed after its first implementation correction.

## Results and retained artifacts

| Case | Required result | Observed result |
| --- | --- | --- |
| Fixed `ok` health candidate | Meaningful RED, verified test receipt, bound GATE-001 PASS, RELEASE_READY | PASS |
| Fixed `broken` health candidate | AC-001 and GATE-001 FAIL, HALTED, no release event | PASS |
| Description-only gate with its own valid test receipt | RELEASE_GATE_UNBOUND before provider or process invocation | PASS; both invocation counts zero |

The `evidence/` directory contains synthetic contracts and receipts, candidate
files, positive and negative content-addressed evidence ledgers and blobs, and
`summary.json`. The fixture verifies each ledger chain, approval identity,
contract/plan/candidate binding, criterion result, and release-gate evidence
reference before reporting success. `source-digests.json` records the tested
PMOS validator and PEOS source bytes.

The current-run CI job installs PEOS commit
`5ccc46ce220092451032397cd7a951a0e8d163e0`. Its tree
`6d481cd6245f7742111cc6d88ecbb17b607dae89` is identical to independently
reviewed local head `f18395a3edb53d7c450fc87660e55b1dc1ce073b`. All eight
retained source hashes were checked against the final reviewed implementation.
`compatibility-pin.json` records this provenance. CI retains the synthetic
contract/receipt files and complete ledgers, including their hidden storage.

Reproduce with that PEOS gate implementation installed:

```sh
python -m unittest discover -s tests/decision-to-contract -p test_handoff.py -v
python tests/decision-to-contract/validate_contract.py --evidence-dir /tmp/f10-fresh-evidence
```

Use a new empty evidence directory. No API credentials or external model are
needed. The original authoring/intake check remains available as
`python tests/decision-to-contract/validate_contract.py --legacy-intake` against
its historical pinned PEOS version. It also passed locally against the
unchanged pre-gate main core.

## Scope and compatibility

The historical health answers, approved contract, approval receipt, and invalid
prose fixture are byte-identical to PMOS base `27d0418`. The original approved
task-store packet and every frozen receipt are untouched. Its unbound process
gates remain blocked under the new compiler; this fixture does not replace its
historical owner-qualified demonstration or claim a new one.

Both changed skill files pass repository lint; the repository audit and
`git diff --check` pass. Current-run compatibility and historical intake run in
separate CI jobs so each uses its own exact PEOS pin. The historical job keeps
`5c0f9e3a8f2c66b212c5e1adfb373e4fd2681bf9`; its validator command explicitly
selects `--legacy-intake`. Local evidence here is not a claim that remote CI
has already run or passed.
