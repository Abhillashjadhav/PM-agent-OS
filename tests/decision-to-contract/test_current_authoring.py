#!/usr/bin/env python3
"""Ordinary authoring compatibility; no engineering run or model is invoked."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import unittest

from pmpe.barebones import default_template
from pmpe.contracts.acceptance import AcceptanceCompileError, compile_acceptance_plan
from pmpe.contracts.authoring import (
    approve_contract_draft,
    build_contract_draft,
    verify_contract_approval,
)


ROOT = Path(__file__).resolve().parents[2]
ANSWERS = Path(__file__).with_name("current-authoring-answers.json")
SKILL = ROOT / ".claude/skills/decision-to-contract/SKILL.md"
TEST_ISSUER = "test-only-current-authoring-issuer"


def answers() -> dict:
    return json.loads(ANSWERS.read_text(encoding="utf-8"))


def instantiate_example(example, supplied):
    """Fill documentation placeholders using supplied test truth, not guesses.

    Keep literal IDs, executable bindings and the example's set of keys intact.
    In particular, a required gate binding absent from the example stays absent.
    """
    if isinstance(example, dict):
        return {key: instantiate_example(value, supplied[key])
                for key, value in example.items()}
    if isinstance(example, list):
        return [instantiate_example(value, supplied[index])
                for index, value in enumerate(example)]
    if isinstance(example, str) and ("<" in example or example == "low|medium|high"):
        return copy.deepcopy(supplied)
    return example


def approve_test_input(supplied):
    """Exercise only synthetic fixture issuance; never claim owner approval."""
    draft = build_contract_draft(supplied)
    if draft.draft is None or draft.draft_digest is None:
        raise AssertionError(f"fixture input blocked: {draft.blocking_questions}")
    approved = approve_contract_draft(
        draft.draft,
        expected_draft_digest=draft.draft_digest,
        approver=TEST_ISSUER,
        approved_at="2026-09-25T00:00:00Z",
    )
    return draft, approved


def compile_current(contract):
    template = default_template()
    return compile_acceptance_plan(
        contract,
        repository_root=ROOT,
        registered_actions=frozenset(template.actions),
        template_version=template.version,
        template_test_digests={},
        registered_measures=frozenset(template.measures),
    )


class CurrentAuthoringTests(unittest.TestCase):
    def test_skill_example_publishes_and_compiles_with_supplied_truth(self):
        block = re.search(r"```json\s*\n(.*?)\n```", SKILL.read_text(), re.DOTALL)
        self.assertIsNotNone(block, "skill must expose its publisher-input shape")
        supplied = instantiate_example(json.loads(block.group(1)), answers())
        _, approved = approve_test_input(supplied)
        compile_current(approved.contract)

    def test_new_input_remains_draft_until_exact_test_digest_is_approved(self):
        supplied = answers()
        original = copy.deepcopy(supplied)
        draft, approved = approve_test_input(supplied)
        self.assertEqual(supplied, original, "publisher must not rewrite supplied truth")
        self.assertEqual(draft.draft["contract_status"], "DRAFT")
        self.assertEqual(draft.draft["approved_by"], "")
        self.assertEqual(draft.draft["approved_at"], "")
        self.assertEqual(approved.receipt["draft_digest"], draft.draft_digest)
        self.assertEqual(approved.contract["contract_status"], "APPROVED")
        self.assertEqual(approved.contract["approved_by"], TEST_ISSUER)
        self.assertEqual(
            verify_contract_approval(approved.contract, approved.receipt,
                                     expected_approver=TEST_ISSUER),
            approved.receipt["receipt_digest"],
        )
        for key, value in original.items():
            self.assertEqual(approved.contract[key], value, key)
        compile_current(approved.contract)

    def test_missing_product_truth_returns_questions_before_approval(self):
        supplied = answers()
        del supplied["target_user"]
        draft = build_contract_draft(supplied)
        self.assertIsNone(draft.draft)
        self.assertIsNone(draft.draft_digest)
        self.assertTrue(draft.blocking_questions)

    def test_description_only_gate_is_rejected_by_current_compiler(self):
        supplied = answers()
        del supplied["binary_release_gates"][0]["acceptance_criterion_refs"]
        _, approved = approve_test_input(supplied)
        with self.assertRaises(AcceptanceCompileError) as failure:
            compile_current(approved.contract)
        self.assertIn("RELEASE_GATE_UNBOUND", {d.code for d in failure.exception.diagnostics})

    def test_unregistered_action_remains_blocked_without_registry_extension(self):
        supplied = answers()
        supplied["acceptance_criteria"][0]["when"]["action"] = "create_task"
        _, approved = approve_test_input(supplied)
        with self.assertRaises(AcceptanceCompileError) as failure:
            compile_current(approved.contract)
        self.assertIn("ACTION_NOT_REGISTERED", {d.code for d in failure.exception.diagnostics})


if __name__ == "__main__":
    unittest.main()
