# BAR: preserve case identity and human-label provenance

1. **Existing path? Yes.** Extend `failure-to-eval-capture` → `golden-dataset-builder`; do not add another dataset or recorder.
2. **Approved criterion/blocker? Yes.** Output-only dedup can merge distinct source cases, and the capture schema omits fields its golden consumer requires.
3. **Behavior change? Yes.** Dedup uses input/output/criterion identity; disputed or missing human-label records stay quarantined instead of becoming goldens.
4. **Rejecting check first? Yes.** Commit identical-output/different-input, conflicting-label and incomplete-capture witnesses first. The baseline rules lack these required distinctions; these are specification witnesses, not executed model tests.
5. **Independently revertible? Yes.** The two skills and their fixtures are one producer/consumer contract correction.
6. **New unrequested surface? No.** No dependency, storage system, label generator or automatic incident execution is introduced.
