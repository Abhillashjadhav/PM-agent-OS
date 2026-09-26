# PRD: Service Check demonstration
Date: 2026-09-25
Revision: 1
Status: Approved
Contract status: APPROVED
Approved by: TEST-ONLY Draft Owner
Approval record: Designed rehearsal input; product definition revision 1 approved by TEST-ONLY Draft Owner.
Canonical decisions: ../DECISIONS.md

This is a synthetic demonstration, not approval by the real PMOS owner. All product meaning and executable bindings are supplied in the canonical input below. The product-definition approval does not include approval of any generated contract digest.

## Approved definition

```json
{
  "acceptance_criteria": [
    {
      "criterion": "Given a running service, the health action returns status ok.",
      "given": [
        {
          "operator": "eq",
          "path": "service.running",
          "value": true
        }
      ],
      "id": "AC-001",
      "requirement": "FR-001",
      "then": [
        {
          "operator": "eq",
          "path": "result.status",
          "value": "ok"
        }
      ],
      "when": {
        "action": "health",
        "arguments": {}
      }
    }
  ],
  "approved_product_decisions": [
    {
      "decision": "Reviewed TEST-ONLY health fixture; synthetic test issuance is not owner approval.",
      "id": "APD-001"
    }
  ],
  "binary_release_gates": [
    {
      "acceptance_criterion_refs": [
        "AC-001"
      ],
      "description": "All executable acceptance criteria pass.",
      "id": "GATE-001"
    }
  ],
  "contract_id": "TEST-ONLY-PMOS-CURRENT-AUTHORING",
  "contract_version": 1,
  "desired_outcome": "An operator can verify that the service is alive with one call.",
  "functional_requirements": [
    {
      "capability": "health.check",
      "description": "The local service reports an OK health status.",
      "id": "FR-001",
      "title": "Report service health"
    }
  ],
  "golden_cases": [
    "A running service returns status ok."
  ],
  "guardrails": [
    "No network or deployment action occurs during contract authoring."
  ],
  "known_risks": [
    {
      "description": "A process health check does not prove external dependency health.",
      "level": "low"
    }
  ],
  "leading_metrics": [
    "First-pass contract acceptance rate"
  ],
  "non_functional_requirements": [
    {
      "category": "reliability",
      "id": "NFR-001",
      "requirement": "The local health result is deterministic."
    }
  ],
  "north_star_metric": "Percentage of service checks that correctly identify availability.",
  "out_of_scope": [
    "Cloud deployment"
  ],
  "problem": "Operators need a deterministic heartbeat before relying on a service.",
  "product_name": "TEST-ONLY current PMOS authoring compatibility",
  "required_approvals": [
    {
      "for": "release",
      "role": "product-owner"
    }
  ],
  "scope": [
    "Local health behavior"
  ],
  "scored_eval_rubric": [
    {
      "criterion": "The result is unambiguous.",
      "id": "RUB-001",
      "scale": "1-5"
    }
  ],
  "target_user": "Operators monitoring small self-hosted services."
}
```
