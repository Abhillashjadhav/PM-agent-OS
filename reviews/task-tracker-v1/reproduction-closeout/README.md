# Frozen-handoff reproduction correction

Independent review [4059411783](https://github.com/Abhillashjadhav/PM-agent-OS/pull/58#discussion_r4059411783)
identified that the old README only validated draft/review artifacts.

- `before-command.py` is the exact historical README snippet, retained only as
  evidence. `before.json` shows it printing PASS after `desired_outcome` changed
  in a disposable approved-contract replica. It is not the current verifier.
- `after-command.sh` is the replacement README command. It calls the existing
  PEOS authoritative verifier, with the fixed approval-time freeze anchor.
- `original/` records all 14 criteria passing with 30 matching before/after
  digest observations. `tampered/` records rejection of the same changed replica
  before any candidate process. `validation.json` summarizes the result.

Correction attempt 1 passed. No original approval-bound bytes, expected outcomes,
product code or execution profile changed. The full Phase 5 clone/install/journey
reproduction is retained in PEOS #203. Root authority, receipt forgery and the
closed sandbox exception remain limitations; none is repaired or waived here.
