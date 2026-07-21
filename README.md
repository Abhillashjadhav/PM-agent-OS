# PM-agent-OS

An agentic product-management skill collection for **Claude Code**, organized across discovery, strategy, build, launch, and iteration. The repository includes 40 lifecycle skills and seven reviewer personas.

## What is validated

- **Validated host runtime:** Claude Code is the currently validated host runtime.
- **Portability:** the skills use `SKILL.md` files, but operation in other runtimes is **not certified** by this repository.
- **Verification gates:** skill gates are instructions for the host agent to follow; they are not an independent execution runtime or enforcement system.
- **Evidence status:** fixtures specify expected inputs, outputs, and failure cases. They are not executed behavioural tests. No recorded behavioural model-run evidence is committed in this repository.

See [the validation guide](docs/VALIDATION.md) for the distinction between structural checks, fixture specifications, and behavioural evidence. The machine-readable [inventory](inventory.json) is the source for the audited lifecycle count and paths.

## Install

```bash
git clone https://github.com/Abhillashjadhav/PM-agent-OS.git
cd PM-agent-OS
mkdir -p ~/.claude/skills
cp -r .claude/skills/* ~/.claude/skills/
```

After installation, invoke the `/pm` skill in Claude Code. The host agent interprets each skill's instructions and verification gates.

## Repository layout

- `.claude/skills/` — lifecycle skills plus the `/pm` orchestrator and supporting skills.
- `.claude/agents/` — seven reviewer personas.
- `tests/<skill>/fixtures.md` — fixture specifications for lifecycle skills.
- `inventory.json` — lifecycle-skill and reviewer-persona inventory.
- `tests/audit_repository.py` — offline structural repository audit.
- `docs/VALIDATION.md` — validation scope and evidence policy.

## Lifecycle inventory

| Stage | Lifecycle skills |
| --- | ---: |
| Discovery | 7 |
| Strategy | 6 |
| Build | 10 |
| Launch | 5 |
| Iterate | 12 |
| **Total** | **40** |

The seven reviewer personas are separate from the 40 lifecycle skills. Their paths and identities are listed in `inventory.json`.

## Verification

Run the offline audit from the repository root:

```bash
python3 tests/audit_repository.py
```

The audit checks the inventory, listed paths, YAML frontmatter, required skill metadata and sections, fixture presence, README-local links, and declared totals. It does not execute a model, evaluate skill output, or certify portability to another runtime.

## License

MIT.
