"""Check frozen cohort integrity and honest whole-panel reporting, without models."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from evaluate_development import MODEL, ROOT, load_panel, make_plan, partition_plan, source_collection_ids, summarize, wilson_interval


class DevelopmentSuiteTests(unittest.TestCase):
    def setUp(self):
        self.panel = load_panel()
        self.size = len(self.panel["tasks"])
        self.plan = make_plan(self.panel, {"candidate": Path("config")}, 20261019)

    def rows(self, passes=None):
        passes = self.size if passes is None else passes
        return [{"label": case["label"], "task_id": case["task_id"], "seed": case["seed"],
                 "actual_seed": case["seed"], "model": MODEL, "config_sha256": {"agent.yaml": "same"},
                 "independently_verified": index < passes, "verifier_agreement": True,
                 "nonempty_patch_artifact": index < passes, "agent_error": None if index < passes else "timeout",
                 "task_seconds": 12.0, "tokens": {"total_tokens": 100},
                 "junit_case_names_sha256": case["task_id"]}
                for index, case in enumerate(self.plan)]

    def test_fixed_unique_stratified_and_unseen_at_selection(self):
        self.assertEqual(self.size, 30)
        self.assertEqual(sorted(self.panel["quota_by_repository"].values()), [1, 4, 10, 15])

    def test_frozen_draw_reproduced_from_metadata_only(self):
        original = json.loads((ROOT / "tests/fixtures/public_task_metadata.json").read_text())
        excluded = set(self.panel["new_selection_excluded_ids"])
        chosen = set(self.panel["previously_used_core_ids"])
        confirmation = json.loads((ROOT / "agent/research/confirmation_set.json").read_text())
        commits = {task["base_commit"] for task in confirmation["tasks"]}
        for repo, quota in self.panel["quota_by_repository"].items():
            eligible = [task["instance_id"] for task in original
                        if task["repo"] == repo and task["instance_id"] not in excluded
                        and task["base_commit"] not in commits]
            eligible.sort(key=lambda item: hashlib.sha256(f"{self.panel['selection_seed']}:{item}".encode()).hexdigest())
            core_count = sum(task["repo"] == repo and task["instance_id"] in self.panel["previously_used_core_ids"] for task in original)
            chosen.update(eligible[:quota - core_count])
        self.assertEqual(chosen, {task["instance_id"] for task in self.panel["tasks"]})

    def test_confirmation_is_disjoint_and_preserves_original_six(self):
        confirmation = load_panel(ROOT / "agent/research/confirmation_set.json")
        self.assertEqual(len(confirmation["tasks"]), 24)
        legacy = json.loads((ROOT / "tests/fixtures/holdout_manifest.json").read_text())
        self.assertTrue({task["instance_id"] for task in legacy["tasks"]} <= {task["instance_id"] for task in confirmation["tasks"]})
        self.assertFalse({task["base_commit"] for task in self.panel["tasks"]} & {task["base_commit"] for task in confirmation["tasks"]})

    def test_reserved_original_unchanged(self):
        path = ROOT / "tests/fixtures/holdout_manifest.json"
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), self.panel["reserved_holdout_manifest_sha256"])

    def test_invalid_manifest_rejected(self):
        for kind in ["duplicate", "reserved", "quota"]:
            panel = copy.deepcopy(self.panel)
            if kind == "duplicate":
                panel["tasks"][1] = panel["tasks"][0]
            elif kind == "reserved":
                panel["reserved_holdout_ids"].append(panel["tasks"][0]["instance_id"])
            else:
                panel["quota_by_repository"][panel["tasks"][0]["repo"]] += 1
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "panel.json"
                path.write_text(json.dumps(panel))
                with self.assertRaises(AssertionError):
                    load_panel(path)

    def test_complete_failure_stays_in_denominator(self):
        result = summarize(self.panel, self.plan, self.rows(self.size - 3))["conditions"]["candidate"]
        self.assertTrue(result["complete"])
        self.assertEqual(result["resolution_rate"], (self.size - 3) / self.size)
        self.assertEqual(result["empty_patch_cases"], 3)
        self.assertEqual(result["agent_error_cases"], 3)

    def test_partial_run_not_reported_as_complete_score(self):
        result = summarize(self.panel, self.plan, self.rows()[:-1])["conditions"]["candidate"]
        self.assertEqual(result["completed"], self.size - 1)
        self.assertFalse(result["complete"])
        self.assertIsNone(result["resolution_rate"])
        self.assertIsNone(result["eligible_pool_repository_weighted_rate"])
        self.assertEqual(len(result["missing"]), 1)

    def test_repository_weight_uses_remaining_pool_not_ten_equal_shares(self):
        rows = self.rows(0)
        repositories = {task["instance_id"]: task["repo"] for task in self.panel["tasks"]}
        for row in rows:
            row["independently_verified"] = repositories[row["task_id"]] == "encode/httpx"
        result = summarize(self.panel, self.plan, rows)["conditions"]["candidate"]
        self.assertEqual(result["resolution_rate"], 1 / self.size)
        pool = self.panel["eligible_by_repository"]
        self.assertAlmostEqual(result["eligible_pool_repository_weighted_rate"], pool["encode/httpx"] / sum(pool.values()))

    def test_duplicate_or_unplanned_observations_rejected(self):
        rows = self.rows()
        with self.assertRaises(AssertionError):
            summarize(self.panel, self.plan, rows + rows[:1])
        rows[0]["task_id"] = "not_in_panel"
        with self.assertRaises(AssertionError):
            summarize(self.panel, self.plan, rows)

    def test_seed_or_config_mismatch_blocks_score(self):
        for field, value in [("actual_seed", 1), ("config_sha256", {"agent.yaml": "changed"}), ("verifier_agreement", False)]:
            rows = self.rows()
            rows[0][field] = value
            result = summarize(self.panel, self.plan, rows)["conditions"]["candidate"]
            self.assertFalse(result["complete"])
            self.assertIsNone(result["resolution_rate"])

    def test_paired_plan_balances_order_and_keeps_zero_seed(self):
        plan = make_plan(self.panel, {"control": Path("a"), "candidate": Path("b")}, 0)
        self.assertEqual(len(plan), self.size * 2)
        self.assertEqual([row["label"].split("/")[0] for row in plan[:4]], ["control", "candidate", "candidate", "control"])
        self.assertTrue(all(row["seed"] == 0 for row in plan))

    def test_three_conditions_are_balanced_and_partitioned_by_task(self):
        plan = make_plan(self.panel, {name: Path(name) for name in ("control", "reference", "candidate")}, 0)
        shards = partition_plan(self.panel, plan, 4)
        self.assertEqual(sum(map(len, shards)), self.size * 3)
        owners = {}
        for index, shard in enumerate(shards):
            for row in shard:
                owners.setdefault(row["task_id"], set()).add(index)
        self.assertTrue(all(len(value) == 1 for value in owners.values()))
        for position in range(3):
            names = [plan[index + position]["label"].split("/")[0] for index in range(0, len(plan), 3)]
            self.assertTrue(all(names.count(name) == self.size // 3 for name in ("control", "reference", "candidate")))

    def paired_rows(self, wins, losses):
        plan = make_plan(self.panel, {"control": Path("control"), "candidate": Path("candidate")}, 0)
        rows = []
        for index, row in enumerate(self.rows(0)):
            for name in ("control", "candidate"):
                current = dict(row, label=f"{name}/seed-0", seed=0, actual_seed=0)
                current["independently_verified"] = index < wins if name == "candidate" else wins <= index < wins + losses
                rows.append(current)
        return plan, rows

    def test_independent_gate_rejects_small_or_regressing_gain(self):
        panel = copy.deepcopy(self.panel)
        panel["promotion_rule"] = {"minimum_net_repairs": 2, "one_sided_exact_mcnemar_p_max": 0.05}
        for wins, losses, accepted in [(1, 0, False), (5, 0, True), (5, 3, False)]:
            plan, rows = self.paired_rows(wins, losses)
            result = summarize(panel, plan, rows)["paired_comparisons"]["control"]
            self.assertEqual(result["promotion_eligible"], accepted)

    def test_junit_identity_and_missing_side_block_promotion(self):
        panel = copy.deepcopy(self.panel)
        panel["promotion_rule"] = {"minimum_net_repairs": 2, "one_sided_exact_mcnemar_p_max": 0.05}
        plan, rows = self.paired_rows(5, 0)
        rows[0]["junit_case_names_sha256"] = "different"
        self.assertFalse(summarize(panel, plan, rows)["paired_comparisons"]["control"]["promotion_eligible"])
        self.assertFalse(summarize(panel, plan, rows[:-1])["paired_comparisons"]["control"]["promotion_eligible"])

    def test_rate_uncertainty_is_not_a_point_guarantee(self):
        low, high = wilson_interval(0, 30)
        self.assertAlmostEqual(low, 0)
        self.assertGreater(high, 0)

    def test_collection_failure_needs_pre_model_environment_review(self):
        plan, rows = self.paired_rows(5, 0)
        task = rows[0]["task_id"]
        rows[0]["junit_case_names_sha256"] = "collection-error-only"
        rows[0]["junit_collection_blocked"] = True
        comparison = summarize(self.panel, plan, rows)["paired_comparisons"]["control"]
        self.assertFalse(comparison["development_screen_positive"])
        panel = dict(self.panel, expected_source_collection_failure_ids=[task])
        comparison = summarize(panel, plan, rows)["paired_comparisons"]["control"]
        self.assertTrue(comparison["development_screen_positive"])
        self.assertFalse(comparison["matching_junit_identities"])
        self.assertEqual(comparison["prequalified_source_collection_exceptions"], [task])

    def test_prequalified_task_without_actual_collection_error_is_not_exempt(self):
        plan, rows = self.paired_rows(5, 0)
        task = rows[0]["task_id"]
        rows[0]["junit_case_names_sha256"] = "changed-tests"
        panel = dict(self.panel, expected_source_collection_failure_ids=[task])
        self.assertFalse(summarize(panel, plan, rows)["paired_comparisons"]["control"]["development_screen_positive"])

    def test_zero_repairs_has_no_cost_per_success_claim(self):
        failed = summarize(self.panel, self.plan, self.rows(0))["conditions"]["candidate"]
        self.assertIsNone(failed["task_seconds_per_verified_repair"])
        self.assertIsNone(failed["recorded_tokens_per_verified_repair"])
        passed = summarize(self.panel, self.plan, self.rows(3))["conditions"]["candidate"]
        self.assertEqual(passed["task_seconds_per_verified_repair"], self.size * 12 / 3)

    def test_original_ten_case_cohort_remains_readable(self):
        panel = load_panel(ROOT / "tests/fixtures/legacy_cohort.json")
        self.assertEqual(len(panel["tasks"]), 10)

    def test_different_condition_seeds_do_not_form_a_paired_gain(self):
        plan, rows = self.paired_rows(5, 0)
        for row in rows:
            if row["label"].startswith("control/"):
                row["seed"] = row["actual_seed"] = 1
        plan = [dict(case, seed=1) if case["label"].startswith("control/") else case for case in plan]
        result = summarize(self.panel, plan, rows)["paired_comparisons"]["control"]
        self.assertFalse(result["matching_execution_seeds"])
        self.assertFalse(result["development_screen_positive"])


class EnvironmentReviewTests(unittest.TestCase):
    def test_explicit_collection_list_is_preserved(self):
        review = {"expected_source_collection_failure_ids": ["declared"], "cases": []}
        self.assertEqual(source_collection_ids(review), ["declared"])

    def test_only_predeclared_source_flags_are_derived(self):
        review = {"cases": [{"task_id": "source", "baseline_collection_blocked_by_expected_source_defect": True},
                            {"task_id": "other", "baseline_collection_blocked_by_expected_source_defect": False},
                            {"task_id": "unspecified"}]}
        self.assertEqual(source_collection_ids(review), ["source"])

    def test_empty_source_flags_add_no_exception(self):
        self.assertEqual(source_collection_ids({"cases": []}), [])


if __name__ == "__main__":
    unittest.main()
