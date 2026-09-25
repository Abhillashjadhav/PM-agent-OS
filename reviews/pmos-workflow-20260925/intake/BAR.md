# BAR — PMOS conversational intake

Scope: implement the accepted `/pm` → `prd-first` intake architecture in existing
skill instructions and fixture specifications. No new workflow runtime.

1. **Already exists? Yes.** Extend the two existing skills and their fixtures; use the existing specialist skills and contract publisher.
2. **Approved criterion or reproduced blocker? Yes.** The accepted architecture and source review require adaptive completeness, Draft resumption, and explicit approval; the existing five-question cap and Draft/skip instructions contradict those requirements.
3. **Changes existing behavior? Yes.** Instruction changes affect engineering intake and ordinary prototype routing; isolate them on `fix/pmos-intake-flow-20260925`.
4. **Automated behavioral RED/GREEN? No.** No existing conversational runner is available. Restructure as fixture-first instruction repair: commit the rejecting conversation specifications before skill edits, record source-level contradictions, and report static checks separately from unverified model behavior.
5. **Independently revertible? Yes.** The intake instructions, bundled field map, and corresponding fixtures form one concern; contract publishing, installation and CI are unchanged.
6. **Unrequested setting, dependency, or extension? No.** No new engine, dependency, model call, inferred product decision, or external-system change.

The fixture-first instruction work is explicitly authorized by the accepted
architecture; it does not certify runtime enforcement or live conversation quality.
