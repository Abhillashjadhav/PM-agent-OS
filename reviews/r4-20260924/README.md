# R4 retained handoff inspection

F-C3-1 is repaired by deriving state, cause and provider-call count from the
terminal ledger, requiring its event type to match the fixture outcome, and
calling PEOS's shared retained-evidence validator. The PMOS test-only issuer
check remains an additional fixture constraint; it is no substitute for
re-verifying the receipt against the retained contract and recorded authority.

C4-F3 adds `--inspect-evidence-dir`, `--case`, and an optional
`--expected-head-digest` for read-only inspection of a retained fixture packet.
It computes a fresh `head_anchor` result and does not read `summary.json` or run
the provider/candidate. Fixture generation now labels its earlier comparison
`head_check_at_capture: MATCHED_RUNTIME_HEAD`. A saved claim cannot establish
the independence of a reader's anchor.

The reader rejects an inconsistent packet without an anchor, but a consistently
rewritten unsigned packet can still pass. The original independently retained
head rejects that rewrite. The receipt and ledger authenticate no owner; the
synthetic issuer remains synthetic. This assumes a trusted verifier process
and does not protect against malicious in-process code or root.

## Verification

The regression tests were committed before implementation. All mutations use
temporary copies of the original TEST-ONLY packet; retained F10 evidence and
the historical intake fixtures are unchanged.

| Evidence | Result and purpose |
| --- | --- |
| `retained-inspection-red.txt` | 10 methods, 15 assertion failures, exit 1 on the old PMOS implementation. |
| `retained-inspection-dependency-red.txt` | 13 methods, two receipt-consistency failures, exit 1 after the PMOS repair with the old PEOS shared validator. This is why a repaired dependency is required. |
| `retained-inspection-green.txt` | Final focused result against the named PEOS revision in `validation.json`. |
| `repository-audit.txt` | Offline repository inventory/structure audit, exit 0. |
| `validation.json` | Exact source identity, commands, exit codes, preservation check and publication boundary. |

The focused suite covers spoofed caller state, a halt after release, an unknown
terminal event, changed subject, stripped plan, receipt/authority contradiction
for both positive and halted cases, propagation of shared-validator rejection,
read-only CLI behavior, forged in-packet anchor claims, and generation labeling.
Existing runtime-observed-head and seeded positive/negative controls remain.
No SKILL.md changes are included, so changed-skill lint is not applicable.

## Public identities and limits

C4-F5 replaces the R3 narrative's local test/implementation IDs with their
published GitHub identities. `publication-provenance.json` copies only the PMOS
records from the R3 publication receipt, including exact trees and the receipt
SHA-256. These identities describe publication, not merge or owner approval.

The parent integration must pin the current-handoff CI job to the repaired
public PEOS revision before publication. The legacy-intake job retains its
historical pin. Independent review, final cross-repository pinning and GitHub
publication are coordinator actions; this work records local engineering proof.
No model call, live sandbox retry, product approval, deployment or merge is
included.

## Resumed handoff verification

The current-handoff job is now pinned to public PEOS review source `297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6` (tree `c2d6ba8467eae13e774f5c9f161dda18099c3961`). The unchanged ordinary fixture was rerun against those exact source bytes: valid candidate RELEASE_READY, broken candidate HALTED, unbound gate CONTRACT_BLOCKED before execution. See `../r4-resume/ordinary-handoff.json` and `summary.json`. These are TEST-ONLY deterministic programs, with no model service or owner approval.

This combined source is published for review without advancing the existing PR heads or invoking CI as a substitute for the previously blocked adversarial rechecks. The final integration review remains open.
