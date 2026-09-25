# Restored PMOS references

These files restore existing references requested in architecture review F7.
They do **not** approve the current workflow or certify fresh model behavior.

- [Root operating instructions](../../../AGENTS.md) are copied unchanged from
  `5d79b20cc16703cb8fd6fa98040659db8881c579` (`origin/docs/pmos-peos-bar-gate`).
- [Historical task-store packet](../../task-tracker-v1/README.md) is copied unchanged
  from `33a35962d13fb13163d61beb938f9e593a742197`
  (`origin/docs/task-tracker-acceptance`), directory tree
  `101567cc26c83dc51a3d19fbe96bcd94da90763b`.

The packet's contracts, approval receipt, evaluator, scripts, scenarios and prior
results are archival evidence for that historical demonstration. They are not new
owner approval, a current acceptance baseline, proof of live generation, or release
authorization. No archived script or fixture was executed during restoration.
Preserve the frozen folder byte-for-byte; current explanation belongs outside it.

`source-manifest.json` records all 33 source files, exact Git blobs/modes, sizes and
SHA-256 digests. `check_reference_snapshot.py` only reads file bytes and metadata.
It failed with 33 missing files before restoration (`red.json`) and passes after
restoration (`green.json`). Run only this static check to verify the copies:

```bash
python3 -B reviews/pmos-workflow-20260925/references/check_reference_snapshot.py
```

Test-first commit: `7269f1a9d707a9d8be8efaac88e5ffc2f50296fe`.
The operating instructions were restored separately in
`7320080cd58b8781bf557d6e9dcaafc5ffba88bf`.
