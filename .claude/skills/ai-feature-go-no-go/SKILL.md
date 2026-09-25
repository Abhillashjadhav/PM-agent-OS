---
name: ai-feature-go-no-go
description: "Strategy-stage skill: turns an AI-feature idea plus context into a build/kill decision with ranked decisive criteria and the complete reversal conditions. Use when the user asks for a go/no-go, build-or-kill, or ship-worthiness call on an AI or LLM-powered feature — 'should we build AI auto-replies', 'build or kill: LLM search', 'make the call on this AI feature' — or when /pm routes such a request here. Do NOT use for non-AI feature prioritization, for mapping assumptions without deciding (assumption-mapper), for model/vendor selection, or for launch-timing decisions."
argument-hint: "<the AI feature + context: users, error tolerance, volume, team, cost>"
---

# AI Feature Go/No-Go

A decision with accountable conditions. Name the primary blocker, every other independent blocker and the full change set needed to reverse the call.

## Verification gates (defined first; output is blocked until all pass)

- **G1 — Decisive criteria complete:** NO-GO ranks a primary blocker and lists every independently disqualifying criterion. GO requires all stated required conditions to be satisfied by supplied evidence. GO-IF names all pending conditions and is not present approval to ship; "it depends" without conditions is not a decision.
- **G2 — Honest reversal set:** state the minimum set of changes/evidence needed to remove all blockers, with any unresolved required facts. If fixing one blocker leaves another, the call stays NO-GO. Mark a supporting factor non-decisive only if it cannot independently prevent GO; ranking never removes a blocker.
- **G3 — No fabricated context:** the decision argues from provided context only. No invented compliance rulings, competitor moves, usage benchmarks, or user demand. Arithmetic uses input numbers; anything else is a labeled estimate.

## Steps

1. **Fix the failure surface.** What happens when the AI is wrong, who sees it, and can it be caught before harm? Error tolerance × review point is where most AI features live or die — check it first.
2. **Check the remaining axes,** in order: value density (does the feature remove real work — do the arithmetic on volume and FTEs), feasibility at quality bar (can current models meet the tolerance found in step 1), economics (per-unit cost vs. price/margin — route deep dives to roadmap-reality-check), and trust/adoption (will users accept AI in this moment).
3. **Identify the decisive set.** List every failed required condition and rank a primary blocker by stated priority or deployment order, explaining that ordering. Test each independently: would it still prevent GO if the others were fixed? If yes, retain it as a blocker. A single pivot is appropriate only when the evidence supports exactly one blocker.
4. **Write the decision.** GO / NO-GO / GO-IF (all exact conditions). Then state the complete reversal set: changes plus evidence that would satisfy every failed requirement. Missing load-bearing facts require a question or a provisional decision, never a claimed sufficient reversal. A design change such as agent-reviewed drafts is a different, smaller feature; review must demonstrably meet the error bar before it justifies GO. For GO, name what violation would reverse it.
5. **Gate pass.** Required conditions and independent blockers complete (G1), full reversal set and supporting factors honest (G2), every contextual claim traceable to input (G3). Fix and re-run; maximum 2 repair loops, then report the failure instead of the output.

## Output format

```
DECISION: NO-GO
PRIMARY BLOCKER (disqualifying): unreviewed generative output in a regulated,
payments-adjacent support flow with stated near-zero error tolerance. One wrong
auto-sent answer about a payment is an incident, and nothing in the design catches
it before the customer does.
OTHER INDEPENDENT BLOCKERS: none established by the supplied context.
SUPPORTING FACTORS (not independently disqualifying on supplied evidence):
- volume: 400 tickets/mo ÷ 1.5 FTE — capacity unknown without time-per-ticket evidence
- CSAT 4.6/5 — protecting a strength, not fixing a weakness
REVERSAL SET: replace auto-send with agent-reviewed drafts (a different, smaller
feature) AND demonstrate that review meets the stated error bar. Remaining required
axes must still pass; adding a review step alone is not evidence they do.
GATE CHECK: G1 pass (blockers named) · G2 pass (full reversal set) · G3 pass
```

## Hard rules

1. Rank blockers without hiding any. A primary blocker plus independent blockers is valid; relabeling a failed required condition as non-decisive to force one pivot is not.
2. Never hedge a decision into meaninglessness. "GO with monitoring and phased rollout" that doesn't name what would disqualify it is not a decision — it's postponed accountability.
3. Never invent context to make the call easier. Missing load-bearing context (error tolerance, volume) → ask for it or state the decision is provisional on the named missing fact.
4. The reversal line is mandatory and complete. Satisfying one of two independent requirements does not reverse a NO-GO; unknown requirements keep the proposed reversal provisional.

## Limitations

- The call is a structured judgment on provided context — it cannot see org politics, roadmap opportunity cost, or strategy fit beyond what the input states.
- Feasibility-at-quality-bar reads current-generation model capability as commonly known; a borderline call deserves a technical spike, and the output says so rather than guessing.
- GO-IF conditions are design requirements, not guarantees the condition is achievable.
- One feature per call; portfolio-level sequencing across many candidate features is roadmap territory.
