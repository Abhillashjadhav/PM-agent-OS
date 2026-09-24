# R3 retained-evidence and documentation corrections

F-R3-05 adds an optional caller-supplied `expected_head_digest` to the existing
verifier. The current synthetic fixture always supplies the genuine final head
captured from real ledger append return values, before reopening retained files.
This transparent observer changes neither append inputs nor return values.

`retained-head-red.txt` records the missing argument/anchor failures before the
implementation; test commit `906efbd` precedes implementation commit `f8baf96`.
These are local development IDs; the publisher must record their GitHub mapping
before advertising remote commit identities. `retained-head-green.txt` records
all three focused tests passing against the already reviewed PEOS gate source.

The seeded forgery changes the stored health program to return `broken`, updates
its candidate and gate references, and reconstructs a valid unsigned chain.
Unanchored verification still accepts its internal consistency. Supplying the
trusted original head rejects it. A separate test substitutes that packet after
the real runtime completes and proves the current fixture retained the genuine
head before inspection; the normal positive and negative fixture cases pass.

There is no signature or approver authentication here. The runtime observer
assumes a trusted process and does not defend against malicious in-process code
or root. For later independent inspection, retain the printed original heads in
an independently controlled record and supply that value to the verifier. The
head copied into a packet summary is diagnostic only and is not a trust anchor.

F-R3-06 clarifies that `status: "VERIFIED"` is insufficient for owner approval;
the consumer must inspect `authority`, and a synthetic issuer remains synthetic.
F-R3-09 distinguishes canonical receipt-content checking in PEOS from the
fixture's stricter byte-identity assertion. F-R3-07's published commit/tree
mappings are copied from the publication receipt into
`publication-provenance.json`; the receipt SHA-256 and pre-split source checks
are retained there. Local development IDs are explicitly distinguished from
GitHub identities.

Frozen v1 inputs and all previously retained F10 evidence remain unchanged.
No live model, sandbox retry, deployment or GitHub write was performed. The
focused fixture executes only its existing fixed local health programs.
This record is author evidence; independent review and publication are separate.
