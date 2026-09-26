# Reconciliation with the external PMOS review

Source: the owner's supplied `Pasted markdown(20260925-182649).md`, retained
unchanged as [EXTERNAL_REVIEW.md](EXTERNAL_REVIEW.md). Its baseline was the PMOS
closeout snapshot `8f9768c4`. The independent PMOS review examined the same skill
sources. The owner's later instruction authorizes implementing accepted changes
and completing independent merges; PEOS remains separately owned.

## Decisions on every external finding

| Finding | Decision | Implementation or boundary |
| --- | --- | --- |
| F1: contract example omits release-gate binding | **Accept** | Add explicit acceptance-criterion references to the current skill example and meaningful compiler regression. **Modify the suggested repair:** create a separate current fixture; do not edit frozen legacy answers, contract or receipt. |
| F2: current handoff depends on an unmerged reader | **Accept dependency risk; reject blanket merge order** | Retain exact compatible pin until the PEOS owner supplies a merged compatible revision. An immutable review pin does not itself make PMOS CI fail after a merge. Installer/validator/Beacon fixes are independent and can merge now. The reported failure against PEOS `dd4271b` is external-review evidence, not a new PEOS test in this thread. |
| F3: product authority is in the wrong repository | **Accept authority requirement; reject location as sufficient proof** | PMOS must author and preserve product decisions. Reusing PEOS's canonical publisher is intentional and avoids a second compiler. A product project's chosen record may live outside the PMOS skill-library repository. Do not relocate the active planner's record without owner/cross-thread coordination; keep that location decision open. |
| F4: PRD shortcuts conflict with handoff authority | **Accept** | Strict engineering intake never treats a skip, vague answer, TBD, autonomous task description or inferred identity as approval. Preserve explicit casual-prototype opt-out as a separate unapproved path. |
| F5: PRD-to-contract field flow is incomplete | **Accept** | Add dependency-ordered field coverage, bounded one-at-a-time questions, explicit OPEN decisions and specialist routing. Reuse known answers. Golden-dataset-builder is conditional on real reviewed outputs; do not fabricate human-labelled goldens for a new product. |
| F6: general-product binding guidance is incomplete | **Accept gap; qualify the claim** | The frozen action registry only registers health, but the skill already lists trusted-test and template-proof forms. Document only routes verified against the pinned public interface. Restore the immutable historical task-store packet as a reference. Do not invent W5 flags, change PEOS, or imply the historical approval covers a new product. |
| F7: required pieces remain outside the integrated/main source | **Accept, with current status correction** | Restore the exact BAR instructions and frozen reference. Finish reviewed independent merges. The review branch deliberately has no PR because its broad handoff CI contains previously screened probes; do not evade that restriction or equate a branch with a shipped workflow. |
| F8: evidence overhead, root copies and potential skill collisions | **Accept maintainability concern; reject blind deletion/renaming** | Preserve required frozen evidence and existing paths. The four root skill copies are uninstalled and excluded from installed inventory; file-count ratios are not a correctness measure. No actual account-level collision was reproduced, so do not break installed names speculatively. Keep one indexed closeout and avoid more framework layers. |
| F9: Beacon observes lifecycle, not skill-gate truth | **Accept limitation** | Keep lifecycle observations separate from gate evidence. Do not present a session stop as verification success. The contract's explicit validation/approval records remain the proof source; native collector delivery and per-gate telemetry are not certified by offline hooks. |
| F10: clean handoff setup does not check its publisher | **Accept; narrow the repair** | Add a clean-user handoff guide and optional read-only prerequisite check. Ordinary PM skill installation remains dependency-free and does not silently install PEOS. Verify the canonical draft/approve/receipt commands against the pinned public interface. |

## External decision requests

- **D-A, merge order:** resolved for independent PMOS changes: merge reviewed fixes
  now. A merged compatible PEOS revision remains an external integration dependency;
  this thread cannot choose or merge another team's changing implementation.
- **D-B, planner record location:** remains open for the owner and PEOS workstream.
  PMOS authority is required; physical relocation is not inferred from that rule.
- **D-C, strict intake:** resolved by the existing approved architecture: keep
  `/pm` → product definition → approval → contract publishing. A raw idea cannot
  enter the publisher directly. Strictness is the engineering path's existing
  safety requirement, not a new product-policy choice for the sleeping owner.

The proposed compiler first-pass rate is useful as a leading measure. It is not
adopted as the North Star: the standing goal in PMOS issue #56 is working software
that implements the approved request, with checkable evidence. No new metric
target, runtime-support promise, product threshold or owner approval is inferred.

## Additional independent PMOS findings included in this implementation

| Area | Correction |
| --- | --- |
| Draft PRD routing | Existing Draft files still require missing decisions and approval; file existence is not approval. |
| Adaptive intake | Replace completion by five-question count with explicit required-field and behavior coverage. |
| Decision persistence | Make existing root DECISIONS.md the shared log; link context memory and preserve/reconcile its legacy file without silent deletion. |
| Golden identity | Include input and evaluation context in identity; identical output text alone must not erase a distinct case or conflicting human label. |
| Failure-to-golden handoff | Carry required observed output and human-label provenance, or quarantine missing fields instead of claiming complete ingestion. |
| Regression verdicts | Define a result for the one-case out-of-bound drift gap; keep captured-defect HOLD precedence. |
| Go/no-go | Represent independent blockers honestly; removing one blocker need not reverse a verdict while another remains. |
| Compact model recommendation | Preserve the four visible axis scores required by its gate. |
| GTM fixture | Remove the expected four-person sales motion that its input never supplied. |
| Retrospective fixture | Separate what was knowable when the decision was made from later ticket outcomes. |
| Old fixture routing | Remove obsolete claims that shipped Build/Strategy stages do not exist. |

These are source-level contradictions or missing procedures, not claims that a
particular model failure was observed. The historical task-store live demonstration
remains bounded feasibility evidence. Current health fixtures do not replace a
fresh idea-to-approved-contract-to-working-product run.
