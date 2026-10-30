"""Qualification exceptions retain failures and cannot manufacture positive repairs."""
import copy
import unittest

from evaluate_development import expected_empty_verification_skip, qualified_original_timeout_pair


class QualifiedBaselineTests(unittest.TestCase):
    def empty(self):
        return dict(task_id='task', agent_error='Agent exceeded tool call budget (8 calls)',
            resolved=False, native_test_exit_code=-1, audit_resolved=True, audit_test_exit_code=0,
            patch_bytes=0, nonempty_patch_artifact=False, independently_verified=False)

    def test_only_prequalified_empty_budget_failure_is_comparable(self):
        row = self.empty()
        before = copy.deepcopy(row)
        self.assertTrue(expected_empty_verification_skip(row, dict(prequalified_clean_pass_ids=['task'])))
        self.assertFalse(expected_empty_verification_skip(row, {}))
        self.assertEqual(row, before)
        for key, value in [('patch_bytes', 1), ('nonempty_patch_artifact', True),
                           ('independently_verified', True), ('resolved', True),
                           ('audit_test_exit_code', 124), ('native_test_exit_code', 1),
                           ('agent_error', 'Sandbox execution error')]:
            with self.subTest(key=key):
                self.assertFalse(expected_empty_verification_skip(dict(row, **{key: value}),
                    dict(prequalified_clean_pass_ids=['task'])))

    def fixture(self):
        bad = dict(audit_test_exit_code=124, resolved=False, verifier_agreement=True,
            independently_verified=False, junit_case_names_sha256=None)
        good = dict(audit_test_exit_code=0, resolved=True, verifier_agreement=True,
            independently_verified=True, junit_case_names_sha256='complete', junit_skipped_case_names=[])
        expected = dict(original_test_exit_code=124, collection_only_qualified=True,
                        case_names_sha256='complete', skipped_case_names=[['test', 'known-skip']])
        return bad, good, expected

    def test_precollected_timeout_keeps_a_full_success_and_failure(self):
        bad, good, expected = self.fixture()
        before = copy.deepcopy([bad, good])
        self.assertTrue(qualified_original_timeout_pair(bad, good, expected))
        self.assertTrue(qualified_original_timeout_pair(good, bad, expected))
        self.assertTrue(qualified_original_timeout_pair(bad, bad, expected))
        self.assertEqual([bad, good], before)

    def test_timeout_without_prequalification_or_full_success_coverage_rejected(self):
        bad, good, expected = self.fixture()
        self.assertFalse(qualified_original_timeout_pair(bad, good, {}))
        for key, value in [('junit_case_names_sha256', 'partial'), ('verifier_agreement', False),
                           ('junit_skipped_case_names', [['test', 'new-skip']]),
                           ('test_like_patch_paths', ['tests/test.py'])]:
            with self.subTest(key=key):
                self.assertFalse(qualified_original_timeout_pair(bad, dict(good, **{key: value}), expected))
        for key, value in [('audit_test_exit_code', -1), ('resolved', True),
                           ('verifier_agreement', False), ('independently_verified', True)]:
            with self.subTest(key=key):
                self.assertFalse(qualified_original_timeout_pair(dict(bad, **{key: value}), good, expected))


if __name__ == '__main__':
    unittest.main()
