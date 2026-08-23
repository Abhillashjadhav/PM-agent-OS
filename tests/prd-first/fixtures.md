# prd-first fixtures

## Trigger

Input: a request to build a new application with no approved PRD.

Expected behavior: ask the five PRD questions one at a time and block code until the user approves the written PRD.

## Planted failure

Input: a feature wish presented as the customer problem.

Expected behavior: ask for the underlying pain once; do not silently promote the feature wish into an approved problem.

## Boundary

This document specifies expected behavior. It is not recorded model-run evidence.

## Case: approved engineering handoff metadata

Given a PRD is explicitly approved for PEOS handoff, the skill records `Status: Approved`, `Contract status: APPROVED`, an exact non-empty `Approved by`, stable `FR-*` and `AC-*` IDs, and no unresolved product-critical question. It must not infer the approver or mark a vague/TBD PRD approved.
