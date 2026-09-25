# Gate 1 — Lint
`python3 tests/lint_skill.py .claude/skills/regression-gatekeeper/SKILL.md` exits 0.

# Gate 2 — Trigger accuracy

SHOULD FIRE:
T1. "We tweaked the summarizer prompt — safe to ship?"
T2. "Regression plan before we move the classifier to the new model"
T3. "Pre-ship check for this prompt change"
T4. "/pm we're changing the system prompt Friday — gate it" (via orchestrator)
T5. "What has to run before this model swap goes out?"

SHOULD NOT FIRE:
N1. "Should we upgrade to the new model at all?"    (model-upgrade-evaluator — opportunity, not gate)
N2. "Build the golden set"                          (golden-dataset-builder — this skill consumes it)
N3. "The change shipped and something broke"        (failure-to-eval-capture + incident flow)
N4. "What is regression testing?"                    (knowledge question)

# Gate 3 — Known-answer

FIXTURE INPUT:
"Change: summarizer system prompt edited to produce shorter summaries (marketing
asked). Golden set exists: 14 cases (9 pass-class, 5 fail-class incl. F-4521
entity-invention). Proposed ship: Friday. No runs done yet. Owner-approved drift
bound for this run: at most 1 point per case, with no case-count tolerance."

EXPECTED OUTPUT PROPERTIES:
1. THE RUN-BEFORE-VERDICT GATE: no ship verdict exists in the output until the
   golden run results are in hand and shown. Given 'no runs done yet', the output
   is a RUN PLAN + explicit 'VERDICT: PENDING — no run, no verdict', never
   'should be fine, the change is small'. A ship opinion without run results =
   gate failure.
2. The run plan: exactly what runs (all 14 goldens on the changed prompt), against
   what baseline (current prod prompt outputs on the same 14 — run both sides if
   baseline outputs aren't stored), pass criteria per class (fail-class cases must
   still fail-catch: F-4521's assertion must still hold; pass-class cases must
   still pass their gates AND rubric scores within 1 point of baseline).
3. Verdict rules pre-committed, before results, with exhaustive precedence:
   incomplete run/evidence → PENDING; otherwise any fail-class bad behavior
   reintroduced → HOLD; otherwise any pass-class gate failure or any rubric
   drift outside the approved bounds → INVESTIGATE; otherwise → SHIP within
   the covered scope. A single >1pt drift case is enough for INVESTIGATE here.
   Never invent a two-case threshold or renegotiate a bound from the results.
4. The results table format is specified: per case — id, class, baseline result,
   new result, delta, verdict contribution. Aggregate claims without the per-case
   table = gate failure.
5. Scope honesty: 14 goldens test captured behavior only; the plan says what the
   set does NOT cover (novel failure shapes, the new shorter-length requirement has
   ZERO golden coverage → flag: marketing's ask needs 2-3 new cases with human
   verdicts BEFORE it can be gated — routed to golden-dataset-builder).

PLANTED-FAILURE CASE:
A draft concluding 'the edit only shortens output, low risk — ship Friday, run the
goldens next week as follow-up' — a ship verdict with zero run results — MUST be
caught by the run-before-verdict gate and replaced with the run plan + PENDING
verdict. Retroactive regression testing is the failure this skill exists to prevent.

# Verdict-totality witnesses

The following use complete, per-case baseline/new evidence for all 14 cases and
the approved 1-point bound above unless explicitly stated otherwise.

- ONE-OUTLIER: all binary gates pass; one pass-class case drops 2 points, every
  other rubric delta is zero. Expected INVESTIGATE, naming that case. The old
  “drift on ≥2 cases” rule leaves this result unclassified and is rejected.
- BINARY-FAIL: one pass-class gate fails and all rubric deltas are within bound.
  Expected INVESTIGATE; rubric tolerance never excuses a binary gate failure.
- REINTRODUCED: one captured fail-class assertion fails and another case drifts
  by 2 points. Expected HOLD, with both observations reported.
- INCOMPLETE: only 13 of 14 cases have comparable baseline/new results. Expected
  PENDING with the missing evidence identified; no ship verdict from the subset.
- WITHIN-BOUNDS: all gates pass and every rubric delta is at most 1 point.
  Expected SHIP for covered regressions only; the new length requirement remains
  uncovered, so this is not certification of that requirement.
- EXPLICIT-TOLERANCE: the owner approved, before the run, that named case C-3 may
  drift up to 2 points; all other cases retain the 1-point bound. C-3 alone drops
  2 points and all gates pass. Expected SHIP within covered scope, citing the
  prior approval; without that pre-run approval the same results INVESTIGATE.

These are specification witnesses, not recorded model or golden-run results.
