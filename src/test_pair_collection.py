"""Do not turn a jointly failed, reviewed collection error into repair credit."""

import copy
import unittest
import xml.etree.ElementTree as ET

from analyze_runs import snapshot_teardown_coverage
from evaluate_development import paired_comparison


class PairCollectionTests(unittest.TestCase):
    def fixture(self):
        rows = []
        for index in range(10):
            for label in ("control", "candidate"):
                rows.append({"label": f"{label}/seed-1", "task_id": f"task-{index}",
                             "actual_seed": 1, "independently_verified": label == "candidate" and index < 5,
                             "junit_case_names_sha256": f"same-{index}", "junit_collection_blocked": False})
        panel = {"promotion_rule": {"minimum_net_repairs": 2, "one_sided_exact_mcnemar_p_max": 0.05},
                 "pre_model_environment_reviewed_ids": ["task-6"]}
        conditions = {name: {"complete": True} for name in ("control", "candidate")}
        return rows, panel, conditions

    def result(self, rows, panel, conditions):
        return paired_comparison(rows, conditions, panel)["control"]

    def broken_collection(self, rows, index=6):
        row = next(item for item in rows if item["task_id"] == f"task-{index}" and item["label"].startswith("candidate"))
        row.update(junit_case_names_sha256="collection-only", junit_collection_blocked=True)
        return row

    def test_reviewed_joint_failure_stays_failed_without_invalidating_wins(self):
        rows, panel, conditions = self.fixture()
        before = copy.deepcopy(rows)
        self.broken_collection(rows)
        result = self.result(rows, panel, conditions)
        self.assertTrue(result["promotion_eligible"])
        self.assertEqual(result["candidate_only_repairs"], 5)
        self.assertEqual(result["control_only_repairs"], 0)
        self.assertEqual(result["reviewed_dual_failure_collection_mismatches"], ["task-6"])
        self.assertEqual([r["independently_verified"] for r in rows], [r["independently_verified"] for r in before])

    def test_missing_pre_model_review_is_not_exempt(self):
        rows, panel, conditions = self.fixture()
        self.broken_collection(rows)
        panel.pop("pre_model_environment_reviewed_ids")
        self.assertFalse(self.result(rows, panel, conditions)["promotion_eligible"])

    def test_missing_junit_is_not_exempt(self):
        rows, panel, conditions = self.fixture()
        self.broken_collection(rows)["junit_case_names_sha256"] = None
        self.assertFalse(self.result(rows, panel, conditions)["promotion_eligible"])

    def test_unknown_coverage_change_without_collection_error_is_not_exempt(self):
        rows, panel, conditions = self.fixture()
        self.broken_collection(rows)["junit_collection_blocked"] = False
        self.assertFalse(self.result(rows, panel, conditions)["promotion_eligible"])

    def test_any_repair_keeps_existing_strict_identity_requirement(self):
        rows, panel, conditions = self.fixture()
        self.broken_collection(rows, 0)
        panel["pre_model_environment_reviewed_ids"].append("task-0")
        self.assertFalse(self.result(rows, panel, conditions)["promotion_eligible"])

    def test_failed_verifier_or_incomplete_condition_is_not_exempt(self):
        rows, panel, conditions = self.fixture()
        self.broken_collection(rows)
        conditions["candidate"]["complete"] = False
        self.assertFalse(self.result(rows, panel, conditions)["promotion_eligible"])

    def test_review_does_not_erase_a_real_regression(self):
        rows, panel, conditions = self.fixture()
        row = self.broken_collection(rows)
        next(r for r in rows if r["task_id"] == "task-6" and r["label"].startswith("control"))["independently_verified"] = True
        self.assertFalse(row["independently_verified"])
        result = self.result(rows, panel, conditions)
        self.assertEqual(result["control_only_repairs"], 1)
        self.assertFalse(result["promotion_eligible"])

    def test_only_paired_snapshot_teardown_record_is_normalized(self):
        tests = list(ET.fromstring('<testsuite><testcase classname="x" name="a"><failure/></testcase>'
            '<testcase classname="x" name="a"><error message="failed on teardown with snapshot mismatch">'
            'some snapshots in this test have incorrect values.</error></testcase></testsuite>'))
        normalized = snapshot_teardown_coverage(tests)
        self.assertEqual(normalized['junit_snapshot_teardown_duplicate_records'], 1)
        self.assertEqual(normalized['junit_snapshot_teardown_normalized_case_names_sha256'],
                         snapshot_teardown_coverage(tests[:1])['junit_snapshot_teardown_normalized_case_names_sha256'])
        self.assertIsNotNone(tests[0].find('failure'))
        self.assertIsNotNone(tests[1].find('error'))

    def test_unpaired_or_unrelated_errors_are_not_normalized(self):
        tests = list(ET.fromstring('<testsuite><testcase classname="x" name="a"><failure/></testcase>'
            '<testcase classname="x" name="b"><error message="failed on teardown with mismatch">'
            'some snapshots in this test have incorrect values.</error></testcase>'
            '<testcase classname="x" name="a"><error message="failed on teardown with unrelated">'
            'database unavailable</error></testcase></testsuite>'))
        self.assertEqual(snapshot_teardown_coverage(tests)['junit_snapshot_teardown_duplicate_records'], 0)

    def test_snapshot_identity_equivalence_requires_prequalification_and_preserves_loss(self):
        rows, panel, conditions = self.fixture()
        bad = self.broken_collection(rows)
        bad['junit_collection_blocked'] = False
        pair = [r for r in rows if r['task_id'] == 'task-6']
        for row in pair:
            row['junit_snapshot_teardown_normalized_case_names_sha256'] = 'same-real-tests'
        bad['junit_snapshot_teardown_duplicate_records'] = 1
        next(r for r in pair if r['label'].startswith('control'))['independently_verified'] = True
        self.assertFalse(self.result(rows, panel, conditions)['junit_identity_check_passed'])
        panel['expected_snapshot_teardown_identity_ids'] = ['task-6']
        result = self.result(rows, panel, conditions)
        self.assertTrue(result['junit_identity_check_passed'])
        self.assertEqual(result['control_only_repairs'], 1)
        self.assertFalse(result['promotion_eligible'])
        self.assertFalse(bad['independently_verified'])

    def test_snapshot_equivalence_does_not_hide_a_missing_real_test(self):
        rows, panel, conditions = self.fixture()
        bad = self.broken_collection(rows)
        bad.update(junit_collection_blocked=False, junit_snapshot_teardown_duplicate_records=1,
                   junit_snapshot_teardown_normalized_case_names_sha256='missing-a-test')
        next(r for r in rows if r['task_id'] == 'task-6' and r['label'].startswith('control'))[
            'junit_snapshot_teardown_normalized_case_names_sha256'] = 'complete-tests'
        panel['expected_snapshot_teardown_identity_ids'] = ['task-6']
        self.assertFalse(self.result(rows, panel, conditions)['junit_identity_check_passed'])


if __name__ == "__main__":
    unittest.main()
