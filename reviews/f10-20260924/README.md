# F-10 current-run compatibility evidence

This packet is **TEST-ONLY deterministic integration evidence**. The fixture
issuer is `test-only-fixture-issuer`; its receipt is not product-owner approval.
No external model was called, no new live candidate was generated, and no
deployment or release was authorized. Fixed health programs ran in local
processes; this check does not establish OS isolation.

## Reproduced gap and test order

The original PMOS validator returned success after legacy `assessment`
admission. It made zero calls to `run_to_release_ready`. The regression was
committed first in published commit
`7af92c467d019eb65591d18f4f6ef880b22bf3cf`;
`red-before-current-run.txt` records that failure.

A second fixture regression in published commit
`0d0740828bcb3b77acf5c68f30fb157943e57b92` checks that the submitted bytes equal
the retained receipt file. This byte-identity requirement belongs to the fixture;
PEOS runtime verifies canonical receipt-content identity and accepts equivalent
serialization. The fixture regression initially
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
PMOS validator and PEOS source bytes for that original capture; it is not a hash
manifest for later verifier repairs.

## Retained-evidence trust boundary (R3)

The ledger is unsigned. Calling `verify_current_evidence` without an independent
`expected_head_digest` checks self-consistency only; a writer who replaces the
whole packet can substitute a candidate and re-chain it. With a caller-held
trusted original head, the verifier rejects that rewritten chain. The head must
come from outside the attacker-controlled packet, never its `summary.json`.

The current TEST-ONLY fixture transparently observes the real ledger append
return values in trusted process memory and always supplies the final digest
when reopening retained evidence. It also prints each observed head so a caller
can retain it in an independently controlled log. A copied summary/log inside
the evidence directory is not an independent trust anchor. No signing or
authentication was added, and malicious code in the verifier process or root
is outside this scope. The original `evidence/` capture remains unchanged; this
repair does not retroactively authenticate it. R3 RED/GREEN checks are retained
in [`../r3-20260924/`](../r3-20260924/README.md).

The current-run CI job installs PEOS commit
`5ccc46ce220092451032397cd7a951a0e8d163e0`. Its tree
`6d481cd6245f7742111cc6d88ecbb17b607dae89` is identical to independently
reviewed local head `f18395a3edb53d7c450fc87660e55b1dc1ce073b`. All eight
retained source hashes were checked against the final reviewed implementation.
`compatibility-pin.json` records this provenance. CI retains the synthetic
contract/receipt files and complete ledgers, including their hidden storage.

The publication receipt maps the pre-publication local commit identifiers to
the following GitHub commits and identical trees. The extracted mappings and
source receipt digest are retained in
[`publication-provenance.json`](../r3-20260924/publication-provenance.json).

| Published unit | GitHub commit | Tree |
| --- | --- | --- |
| Current-run implementation | `5d9cd06c5eca562361a4d080d09ea00bc5eee1a3` | `123309d52d0c6e1ff0ccd673954371e550662a58` |
| Reviewed CI pin | `be0158d8c7c1ddb544fa882099fcd7374cdbadbe` | `5624f2d542b86d66bbea5dc47b324028d4a34823` |
| Final original runtime head | `0b6bd55152efc918f9a042fc898e961dcf527b96` | `66432bddf807c295a5e78d03ce1f58e5d597bb11` |

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
