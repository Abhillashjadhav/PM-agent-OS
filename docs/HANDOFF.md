# Set up the approved-contract handoff

Ordinary PMOS skills need only the [PMOS installation](../README.md#install-safely).
Creating a receipt-bound engineering contract additionally needs the existing
Production Engineering OS publisher. PMOS collects and preserves product meaning;
the publisher serializes it and creates the approval receipt.

## 1. Install the reviewed publisher in a separate environment

From the PMOS checkout, using Python 3.12 (the pinned package supports 3.11–3.12):

```bash
python3.12 -m venv ../pmos-handoff-venv
source ../pmos-handoff-venv/bin/activate
python -m pip install 'git+https://github.com/Abhillashjadhav/production-engineering-os.git@297a11d79e5d1e1eda1f8f94b7bec3046c41a0d6'
python scripts/check_handoff.py
pmpe legacy contract draft --help
```

The commit is PMOS's reviewed compatibility snapshot. It contains work not yet
merged into the engineering repository's main branch; this is not a claim that
the latest engineering code is compatible. Keep this pin until a replacement has
been reviewed. PMOS's installer does not install the publisher automatically.

`HANDOFF_SETUP_OK` means the selected Python environment records that exact Git
revision and the `pmpe` console entry point. The check reads installation metadata
only: it performs no network calls, imports no publisher code and writes nothing.
It does not authenticate package contents or certify a contract, runtime or build.
The help command separately confirms that the CLI can start in this environment.

| Diagnostic | Next action |
|---|---|
| `PUBLISHER_NOT_INSTALLED` | Activate the environment above and install the pin. |
| `PUBLISHER_REVISION_MISMATCH` | Use the reviewed environment; do not silently change the pin. |
| `PUBLISHER_PROVENANCE_UNKNOWN` | Reinstall the exact Git pin in a fresh environment. A version label alone is insufficient. |
| `PUBLISHER_ENTRY_POINT_MISSING` | Reinstall the pin in a fresh environment. |

If CLI help fails after metadata passes, resolve the reported installation error
before continuing. Use the same activated environment for every command below.

## 2. Complete and approve the product definition

Ask `/pm` to turn the idea into an engineering contract. Keep the product PRD in
the target project's `prds/` folder and decisions in that project's `DECISIONS.md`.
PMOS asks about unresolved product decisions one at a time and reuses answers
already given. Approve the product definition explicitly before publication.

Have `decision-to-contract` prepare `handoff/answers.json` in the product project.
Its field mapping and executable acceptance bindings must satisfy that skill's
gates. An unanswered required decision, unsupported binding or publisher rejection
is `CONTRACT_BLOCKED`; neither PMOS nor the publisher may guess the missing truth.
The repository's health fixture is a bounded example, not a template for every
product's actions or business metrics.

## 3. Create a draft and review its exact digest

From the product project, with the publisher environment still active:

```bash
pmpe legacy contract draft --answers handoff/answers.json --output handoff/draft
```

On success the publisher creates:

- `handoff/draft/contract-draft.json`
- `handoff/draft/draft-summary.json`, including `draft_digest`
- `handoff/draft/source-map.json`

It prints `draft ready` and `approve exact digest: sha256:...`. Review the generated
draft against the approved PRD and source map. Ask the accountable owner to approve
that exact printed digest. Product-definition approval does not approve unseen
contract bytes. Any draft change requires another draft review and digest approval.

## 4. Publish only after exact-digest approval

Replace all three placeholders with the owner's actual approval record. Do not
invent an approver or timestamp, or treat the example command as approval.

```bash
pmpe legacy contract approve \
  --draft handoff/draft/contract-draft.json \
  --expected-digest '<OWNER_APPROVED_SHA256_DIGEST>' \
  --approver '<ACCOUNTABLE_APPROVER>' \
  --approved-at '<RFC3339_APPROVAL_TIME>' \
  --output handoff/approved
```

The publisher creates `handoff/approved/contract-approved.json` and
`handoff/approved/approval-receipt.json`. Preserve these files unchanged. After any
edit, return to draft review and obtain renewed approval; never repair a receipt.

## 5. Verify the receipt, then compile

This pinned CLI has no standalone receipt-verification command. Use its existing
public verification API; `contract validate` alone does not verify a receipt.
Replace the approver placeholder with the same approved identity:

```bash
python - <<'PY'
import json
from pathlib import Path
from pmpe.contracts.authoring import verify_contract_approval

root = Path("handoff/approved")
contract = json.loads((root / "contract-approved.json").read_text(encoding="utf-8"))
receipt = json.loads((root / "approval-receipt.json").read_text(encoding="utf-8"))
print(verify_contract_approval(
    contract, receipt, expected_approver="<ACCOUNTABLE_APPROVER>"
))
PY
```

Only if verification succeeds and prints the receipt digest, run:

```bash
pmpe barebones compile handoff/approved/contract-approved.json --repository-root .
```

Require `status: COMPILES` and inspect coverage and diagnostics. Current release
gates must explicitly reference their acceptance criteria. Unsupported actions,
measures or trusted-test bindings remain blocked; do not relabel product behavior
as `health` to make compilation succeed.

## 6. Hand off the verified packet

Provide engineering the unchanged approved contract and receipt, expected approver,
source answers and source map, PRD and decision-log paths, compiler result and
publisher revision. Preserve the distinct statuses: product approved, exact digest
approved, receipt verified and compiler accepted.

Compilation is not product delivery. The current runner, trusted-test/template
bindings and any product-specific bundle must also support the intended behavior.
`pmpe legacy contract handoff` is the historical admission route; its existence
does not prove a current build completed. Do not invent a general build command or
promise release readiness for an unsupported product. Report the unsupported
binding and leave that engineering dependency open.

The verified checks for this guide exercised one health fixture through authoring,
receipt verification and current compilation. They did not run a product, a live
model interview or the restricted adversarial handoff probes.
