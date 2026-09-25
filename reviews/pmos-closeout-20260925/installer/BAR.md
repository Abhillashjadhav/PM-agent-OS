# Installer closeout BAR

Scope: verify and, only for a reproduced defect, extend the existing PMOS installer safety repair in PR #59. PEOS, skills, contracts, frozen packets, and unrelated work are outside this unit.

1. **Does this already exist? Yes.** Reuse `scripts/install.py` and its seven CLI regressions from `9d09327a4fca24d111f98e895874eed0f609aa5a`; no parallel installer.
2. **Approved criterion or reproduced blocker? Yes.** The owner's PMOS-only takeover asks to finish and publish remaining repairs; the existing installer promises validated clean installation, explicit overwrite consent, and preservation of source and symlink referents.
3. **Changes existing behavior? No, initially.** This unit first verifies the existing repair. Any reproduced defect will receive a separate behavior-change BAR entry before edits.
4. **Failing-before/passing-after check? Yes, for the existing repair.** Reuse the existing seven CLI regressions; run them against the prior installer and repaired installer in disposable copies to record which cases demonstrate the fix. New implementation is prohibited without a reproduced failing check.
5. **Independently revertible? Yes.** Evidence lives in this installer-specific directory on `fix/pmos-installer-closeout-20260925`; any necessary repair remains confined to installer implementation and its tests.
6. **New unrequested setting/dependency/extension? No.** No new settings, dependencies, extension points, skills, or execution providers are planned.
