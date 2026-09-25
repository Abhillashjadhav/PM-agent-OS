# Saved task and boundaries

The owner asked to collect the current PMOS state, take over unfinished implementation, finish it, and push reviewable changes. Their latest correction limits this thread to PMOS; PEOS is separately owned.

Delegated unit: finish verification of the existing installer safety repair, starting from `origin/fix/pmos-installer-safety-20260923` (`9d09327a4fca24d111f98e895874eed0f609aa5a`, PR #59). Reuse existing tests, execute public CLI clean install/refusal/force and source/destination/symlink boundary checks. Repair only a concretely reproduced remaining bug using test-first commits. Do not inspect or modify PEOS. Do not touch skills, frozen packets, handoff, validator, or unrelated workflows. No remote writes or merges from this worker. Root performs integration, independent review, and publication.

Previously blocked planted-bytecode and forged release-ledger probes remain excluded. Ordinary disposable installer fixtures are permitted.
