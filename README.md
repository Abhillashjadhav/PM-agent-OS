# pm-agent-os

An agentic PM operating system for Claude Code. One `/pm` command orchestrates the full product lifecycle — discovery, strategy, build, launch, iterate — through 40 skills, each with binary verification gates, tested fixtures, and a public PR-review record.

---

## The problem

Every PM operating system on the market generates. None of them verifies.

Prompt packs, skill collections, "PM copilots" — they all produce output that looks right: a clean synthesis, a confident market size, a tidy competitive matrix. Whether the synthesis quotes interviews that actually happened, whether the market size has a source, whether "competitor X has no API" was observed or assumed — nothing checks. The output ships, the decision gets made, and the error surfaces weeks later in a roadmap built on an invented quote.

The failure isn't generation quality. It's that nothing sits between the model and you to verify the output before you act on it.

## What's different

Every skill in this repo carries three things, written in this order:

1. **Binary verification gates.** Pass/fail checks defined *before* the skill's instructions were written. Example: interview-synthesizer blocks any output where a pattern cites fewer than 2 verbatim quotes, or where any quote fails a character-for-character match against the source transcript. A gate failure means the output does not reach you — it gets fixed or reported as a failure, never silently shipped.
2. **Tested fixtures.** Each skill has `tests/<skill>/fixtures.md` covering a three-gate harness: frontmatter lint (`tests/lint_skill.py`), trigger accuracy (fire / no-fire phrasings), and a known-answer run (fixture input → expected gated output).
3. **A PR-review record.** Every skill entered this repo through a pull request reviewed by `/pr-review` before merge, with the lint run before the verdict. Gates and fixtures are committed before instructions — the commit order shows it.

None of this asks to be trusted. The repo's own git history is the proof: open any skill's PR and read the review, the fixtures, and the commit sequence.

## Architecture

```
                        /pm  (orchestrator)
                              │
             classifies request → lifecycle stage(s)
                              │
   ┌───────────┬───────────┬──┴────────┬───────────┐
   │ Discovery │ Strategy  │  Build    │  Launch   │  Iterate
   │ 7 skills  │ 6 skills  │ 10 skills │  planned  │  planned
   └───────────┴───────────┴──┬────────┴───────────┘
                              │
                    reliability spine
      binary gates · tested fixtures · lint harness · PR-review record
```

The orchestrator routes; stage skills execute; the reliability spine verifies. No output crosses from a stage skill back to you until its verification gate passes.

## Install

```bash
git clone https://github.com/Abhillashjadhav/PM-agent-OS- pm-agent-os && mkdir -p ~/.claude/skills && cp -r pm-agent-os/.claude/skills/* ~/.claude/skills/
```

Skills follow the open SKILL.md standard — works with Codex, Cursor, Windsurf, and any agent that reads Agent Skills; the /pm orchestrator and one-command install are Claude Code-native.

## Watch a gate catch a failure

*(Demo lands at launch.)* A real transcript set goes through `/pm` → interview-synthesizer. The draft synthesis contains one quote that doesn't exist in any transcript. The zero-invented-quotes gate fails the character-for-character match, blocks the output, and the corrected synthesis — with the fabricated quote removed — is what actually returns. The full run will be recorded here, unedited.

## Roadmap

| Stage | Skills | Status |
|---|---|---|
| Discovery | interview-synthesizer · feedback-pattern-miner · assumption-mapper · competitor-teardown · opportunity-sizer · jtbd-framer · research-brief | **Shipped** |
| Strategy | strategy-review · roadmap-reality-check · ai-feature-go-no-go · north-star-designer · build-buy-partner · pricing-tradeoff | **Shipped** |
| Build | model-complexity-router · builder-validator · prompt-optimizer-loop · context-auditor · pm-context-system · prd-to-eval · prototype-first-workflow · rag-vs-agent-architect · latency-ux-tradeoff · unit-economics-stress-test | **Shipped** |
| Launch | planned | Not started |
| Iterate | planned | Not started |

Target: 40 skills across the five stages, every one gated, fixtured, and PR-reviewed before it ships. `/pm` routes to Discovery, Strategy, and Build today (23 skills) and says "stage not yet shipped" for Launch and Iterate — it does not improvise stages that don't exist.

## Credits

Harness patterns — the lint gate, the three-gate fixtures convention, and the PR-review agent — carried over from [AI-PM-essential-skills](https://github.com/Abhillashjadhav/AI-PM-essential-skills).

## License

MIT.

---

*Built by [Abhillash Jadhav](https://github.com/Abhillashjadhav) — GenAI PM. Evals, context engineering, agentic reliability.*
