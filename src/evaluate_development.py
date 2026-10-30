"""Prepare, run and report frozen development and independent confirmation panels."""

import argparse
from collections import Counter
import hashlib
import json
import math
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "agent/research/development_set.json"
MODEL = "gemma-4-31b-it-qat-w4a16-ct"
ALLOWED_MODELS = {f"gemma-4-{size}-it-qat-w4a16-ct" for size in ("31b", "12b", "e4b", "e2b")}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_panel(path=MANIFEST):
    panel = json.loads(path.read_text())
    tasks = panel["tasks"]
    identifiers = [task["instance_id"] for task in tasks]
    assert len(identifiers) == len(set(identifiers)) == panel.get("panel_size", 10)
    assert Counter(task["repo"] for task in tasks) == panel["quota_by_repository"]
    assert not set(identifiers).intersection(panel["reserved_holdout_ids"])
    assert not set(identifiers).intersection(panel["prior_plan_or_execution_ids"])
    return panel


def task_inputs(task):
    prefix = task["repo"].split("/")[-1]
    stem = f"{prefix}_{task['base_commit']}"
    return [ROOT / "data/competition" / name for name in [
        f"snapshots/{task['instance_id']}.tgz", f"graphs/{stem}.json", f"embeddings/{stem}.npz"]]


def prepare(panel):
    for task in panel["tasks"]:
        if any(not path.is_file() for path in task_inputs(task)):
            subprocess.run([sys.executable, "src/prepare_inputs.py", "--task-only",
                            "--task-id", task["instance_id"]], check=True, cwd=ROOT)
    print(f"{len(panel['tasks'])} fixed task inputs ready; no model or official submission started")


def make_plan(panel, folders, seed):
    plan = []
    for index, task in enumerate(panel["tasks"]):
        conditions = list(folders)
        if len(conditions) > 2:
            offset = (index // 2) % len(conditions)
            conditions = conditions[offset:] + conditions[:offset]
        if index % 2:
            conditions.reverse()
        for name in conditions:
            plan.append({"label": f"{name}/seed-{seed}", "task_id": task["instance_id"],
                         "seed": seed, "agent_dir": str(folders[name])})
    return plan


def wilson_interval(passed, total):
    z = 1.959963984540054
    rate = passed / total
    denominator = 1 + z * z / total
    center = (rate + z * z / (2 * total)) / denominator
    width = z * math.sqrt(rate * (1 - rate) / total + z * z / (4 * total * total)) / denominator
    return [max(0, center - width), min(1, center + width)]


def source_collection_ids(review):
    return review.get("expected_source_collection_failure_ids", [
        case["task_id"] for case in review["cases"]
        if case.get("baseline_collection_blocked_by_expected_source_defect", False)])


def qualified_syntax_collection_pair(left, right, expected):
    """A bad implementation stays failed; only a full clean-qualified success is comparable."""
    if not expected or left["independently_verified"] == right["independently_verified"]:
        return False
    good, bad = (left, right) if left["independently_verified"] else (right, left)
    return bool(bad.get("patch_source_syntax_collection_failure")
                and bad.get("junit_collection_blocked") and bad.get("verifier_agreement")
                and bad.get("resolved") is False
                and not bad.get("test_like_patch_paths") and not bad.get("verification_sensitive_patch_paths")
                and expected.get("case_names_sha256") is not None
                and good.get("junit_case_names_sha256") == expected["case_names_sha256"]
                and "junit_skipped_case_names" in good
                and set(map(tuple, good["junit_skipped_case_names"]))
                    <= set(map(tuple, expected.get("skipped_case_names", []))))


def expected_empty_verification_skip(row, panel):
    """An empty budget failure stays failed, even if the original tests were already green."""
    budget_error = re.fullmatch(
        r"Agent exceeded (?:session timeout \(\d+(?:\.\d+)? min\)|"
        r"tool call budget \(\d+ calls\)|turns budget \(\d+ turns\)|maximum allowed LLM turns)",
        row.get("agent_error") or "")
    return bool(row["task_id"] in panel.get("prequalified_clean_pass_ids", [])
                and budget_error and row.get("resolved") is False
                and row.get("native_test_exit_code") == -1
                and row.get("audit_resolved") is True and row.get("audit_test_exit_code") == 0
                and row.get("patch_bytes") == 0 and not row.get("nonempty_patch_artifact")
                and not row.get("independently_verified"))


def qualified_original_timeout_pair(left, right, expected):
    """Only pre-collected full coverage may be compared with an original-source timeout."""
    if not expected or expected.get("original_test_exit_code") != 124:
        return False

    def timed_out(row):
        return (row.get("audit_test_exit_code") == 124 and row.get("resolved") is False
                and row.get("verifier_agreement") and not row.get("independently_verified")
                and row.get("junit_case_names_sha256") is None)

    def complete(row):
        return (row.get("verifier_agreement")
                and expected.get("case_names_sha256") is not None
                and row.get("junit_case_names_sha256") == expected["case_names_sha256"]
                and "junit_skipped_case_names" in row
                and set(map(tuple, row["junit_skipped_case_names"]))
                    <= set(map(tuple, expected.get("skipped_case_names", []))))

    return bool(expected.get("collection_only_qualified")
                and (timed_out(left) or timed_out(right))
                and all(not row.get("test_like_patch_paths")
                        and not row.get("verification_sensitive_patch_paths") for row in (left, right))
                and all(timed_out(row) or complete(row) for row in (left, right)))


def paired_comparison(rows, conditions, panel):
    candidate = {row["task_id"]: row for row in rows if row["label"].split("/")[0] == "candidate"}
    comparisons = {}
    for name in conditions:
        if name == "candidate":
            continue
        control = {row["task_id"]: row for row in rows if row["label"].split("/")[0] == name}
        complete = conditions[name]["complete"] and conditions["candidate"]["complete"]
        if not complete:
            comparisons[name] = {"complete": False, "promotion_eligible": False}
            continue
        wins = sum(candidate[key]["independently_verified"] and not control[key]["independently_verified"] for key in candidate)
        losses = sum(control[key]["independently_verified"] and not candidate[key]["independently_verified"] for key in candidate)
        discordant = wins + losses
        p = sum(math.comb(discordant, k) for k in range(wins, discordant + 1)) / 2 ** discordant if discordant else 1.0
        paired_seed = all(candidate[key]["actual_seed"] == control[key]["actual_seed"] for key in candidate)
        same_junit = {key: candidate[key].get("junit_case_names_sha256") is not None
                      and candidate[key]["junit_case_names_sha256"] == control[key].get("junit_case_names_sha256") for key in candidate}
        source_collection = set(panel.get("expected_source_collection_failure_ids", []))
        exceptions = [key for key in candidate if not same_junit[key] and key in source_collection
                      and (candidate[key].get("junit_collection_blocked", False)
                           or control[key].get("junit_collection_blocked", False))]
        reviewed = set(panel.get("pre_model_environment_reviewed_ids", []))
        reviewed_snapshots = set(panel.get("expected_snapshot_teardown_identity_ids", []))
        snapshot_exceptions = [key for key in candidate if not same_junit[key] and key in reviewed_snapshots
            and (candidate[key].get("junit_snapshot_teardown_duplicate_records", 0)
                 or control[key].get("junit_snapshot_teardown_duplicate_records", 0))
            and candidate[key].get("junit_snapshot_teardown_normalized_case_names_sha256") is not None
            and candidate[key].get("junit_snapshot_teardown_normalized_case_names_sha256")
                == control[key].get("junit_snapshot_teardown_normalized_case_names_sha256")]
        dual_failure_collection = [key for key in candidate if not same_junit[key] and key in reviewed and key not in exceptions
                                   and not candidate[key]["independently_verified"]
                                   and not control[key]["independently_verified"]
                                   and candidate[key].get("junit_case_names_sha256") is not None
                                   and control[key].get("junit_case_names_sha256") is not None
                                   and (candidate[key].get("junit_collection_blocked", False)
                                        or control[key].get("junit_collection_blocked", False))]
        syntax_coverage = panel.get("prequalified_source_syntax_coverage", {})
        syntax_exceptions = [key for key in candidate if not same_junit[key]
            and qualified_syntax_collection_pair(candidate[key], control[key], syntax_coverage.get(key))]
        timeout_coverage = panel.get("prequalified_source_timeout_coverage", {})
        timeout_exceptions = [key for key in candidate if not same_junit[key]
            and qualified_original_timeout_pair(candidate[key], control[key], timeout_coverage.get(key))]
        matching = all(same_junit[key] or key in exceptions or key in dual_failure_collection
                       or key in snapshot_exceptions or key in syntax_exceptions
                       or key in timeout_exceptions for key in candidate)
        rule = panel.get("promotion_rule", {})
        eligible = (bool(rule) and wins - losses >= rule["minimum_net_repairs"]
                    and p <= rule["one_sided_exact_mcnemar_p_max"] and matching and paired_seed)
        comparisons[name] = {"complete": True, "candidate_only_repairs": wins,
                             "control_only_repairs": losses, "net_repairs": wins - losses,
                             "one_sided_exact_mcnemar_p": p,
                             "matching_junit_identities": all(same_junit.values()),
                             "junit_identity_check_passed": matching,
                             "prequalified_source_collection_exceptions": exceptions,
                             "reviewed_dual_failure_collection_mismatches": dual_failure_collection,
                             "prequalified_snapshot_teardown_identity_exceptions": snapshot_exceptions,
                             "matching_execution_seeds": paired_seed,
                             "development_screen_positive": wins > losses and matching and paired_seed,
                             "promotion_eligible": eligible,
                             "official_score_improvement_claimed": False}
        if syntax_coverage:
            comparisons[name]["prequalified_patch_syntax_collection_mismatches"] = syntax_exceptions
        if timeout_coverage:
            comparisons[name]["prequalified_original_source_timeout_pairs"] = timeout_exceptions
    return comparisons


def summarize(panel, plan, rows, condition_models=None):
    """No complete score until the entire frozen condition has finished."""
    task_repo = {task["instance_id"]: task["repo"] for task in panel["tasks"]}
    planned = {(case["label"], case["task_id"], case["seed"]) for case in plan}
    assert len(planned) == len(plan)
    observed = {(row["label"], row["task_id"], row["seed"]) for row in rows}
    assert len(observed) == len(rows) and observed <= planned
    names = set(case["label"].split("/")[0] for case in plan)
    expected_models = condition_models if condition_models is not None else {name: MODEL for name in names}
    assert set(expected_models) == names and set(expected_models.values()) <= ALLOWED_MODELS
    conditions = {}
    for name in dict.fromkeys(case["label"].split("/")[0] for case in plan):
        expected = [case for case in plan if case["label"].split("/")[0] == name]
        actual = [row for row in rows if row["label"].split("/")[0] == name]
        assert len(expected) == len(task_repo) and {case["task_id"] for case in expected} == set(task_repo)
        fingerprints = {json.dumps(row["config_sha256"], sort_keys=True) for row in actual}
        consistent = len(fingerprints) <= 1 and all(
            row["actual_seed"] == row["seed"] and row["model"] == expected_models[name]
            and (row["verifier_agreement"] or expected_empty_verification_skip(row, panel)) for row in actual)
        complete = len(actual) == len(expected) and consistent
        by_repo = {}
        for repo, count in panel["quota_by_repository"].items():
            subset = [row for row in actual if task_repo[row["task_id"]] == repo]
            passed = sum(row["independently_verified"] for row in subset)
            by_repo[repo] = {"planned": count, "completed": len(subset), "verified": passed,
                             "resolution_rate": passed / count if complete else None}
        verified = sum(row["independently_verified"] for row in actual)
        pool = panel["eligible_by_repository"]
        conditions[name] = {
            "planned": len(expected), "completed": len(actual), "complete": complete,
            "configuration_seed_model_and_verifier_consistent": consistent,
            "verified": verified, "resolution_rate": verified / len(expected) if complete else None,
            "wilson95_interval": wilson_interval(verified, len(expected)) if complete else None,
            "eligible_pool_repository_weighted_rate": sum(
                pool[repo] * stats["resolution_rate"] for repo, stats in by_repo.items()
            ) / sum(pool.values()) if complete else None,
            "by_repository": by_repo,
            "empty_patch_cases": sum(not row["nonempty_patch_artifact"] for row in actual),
            "agent_error_cases": sum(bool(row["agent_error"]) for row in actual),
            "native_task_seconds_including_verification": round(sum(row["task_seconds"] for row in actual), 3),
            "trace_recorded_tokens": sum(row["tokens"]["total_tokens"] for row in actual),
            "task_seconds_per_verified_repair": round(sum(row["task_seconds"] for row in actual) / verified, 3) if complete and verified else None,
            "recorded_tokens_per_verified_repair": sum(row["tokens"]["total_tokens"] for row in actual) / verified if complete and verified else None,
            "invalid_argument_steps": sum(row.get("steps_with_invalid_arguments", 0) for row in actual),
            "identical_call_repeats": sum(row.get("identical_call_repeats", 0) for row in actual),
            "missing": [case["task_id"] for case in expected
                        if (case["label"], case["task_id"], case["seed"]) not in observed],
        }
        if panel.get("prequalified_clean_pass_ids"):
            conditions[name]["prequalified_empty_native_verification_skips"] = [
                row["task_id"] for row in actual if expected_empty_verification_skip(row, panel)]
    return {"scope": ("Frozen independent paired confirmation, not a hidden-score estimate" if panel.get("promotion_rule")
                      else "Fixed development screen, not a new holdout or hidden-score estimate"),
            "official_score_claimed": False, "single_seed_screen_not_confirmed_strategy_effect": True,
            "weight_scope": panel["weighted_metric"],
            "time_scope": "Native task seconds include verification; Trace usage is not all HTTP billing or the official charged clock",
            "conditions": conditions, "cases": rows,
            "paired_comparisons": paired_comparison(rows, conditions, panel)}


def report(output):
    from analyze_runs import analyze_case

    panel = load_panel(output / "cohort.json")
    environment = output / "environment-review.json"
    if environment.exists():
        review = json.loads(environment.read_text())
        panel["expected_source_collection_failure_ids"] = source_collection_ids(review)
        panel["expected_snapshot_teardown_identity_ids"] = review.get("expected_snapshot_teardown_identity_ids", [])
        panel["prequalified_source_syntax_coverage"] = review.get("prequalified_source_syntax_coverage", {})
        panel["prequalified_clean_pass_ids"] = review.get("prequalified_clean_pass_ids", [])
        panel["prequalified_source_timeout_coverage"] = review.get("prequalified_source_timeout_coverage", {})
        panel["pre_model_environment_reviewed_ids"] = [case["task_id"] for case in review["cases"] if case["ready"]]
    plan = json.loads((output / "plan.json").read_text())
    rows = []
    for case in plan:
        roots = [output, *sorted((output / "shards").glob("*"))]
        matches = [root / case["label"] / case["task_id"] for root in roots
                   if (root / case["label"] / case["task_id"] / "audit/summary.json").exists()]
        assert len(matches) <= 1, "Duplicate task output across shards"
        if matches:
            row = analyze_case(matches[0], case)
            junit = matches[0] / "audit/junit.xml"
            tests = list(ET.parse(junit).getroot().iter("testcase")) if junit.exists() else []
            row["junit_collection_blocked"] = any(
                t.find("error") is not None and t.find("error").get("message") == "collection failure" for t in tests)
            rows.append(row)
    settings = json.loads((output / "settings.json").read_text())
    condition_models = settings.get("condition_models")
    if condition_models is not None:
        from adk_submission.discovery import discover_declared_models
        assert all(discover_declared_models(output / "configs" / name) == {model}
                   for name, model in condition_models.items()), "Frozen model declarations differ from settings"
    result = summarize(panel, plan, rows, condition_models=condition_models)
    execution_path = output / "execution.json"
    execution = json.loads(execution_path.read_text()) if execution_path.exists() else None
    integrity = all(execution.get(key) for key in ["completed_normally", "formal_zip_unchanged",
                    "task_data_unchanged", "core_unchanged"]) if execution else None
    if execution and not execution.get("environment_review_unchanged", True):
        integrity = False
    if execution and not execution.get("configuration_unchanged", True):
        integrity = False
    result["execution_integrity"] = integrity
    result["analysis_source_sha256"] = digest(Path(__file__))
    result["execution_analyzer_sha256"] = json.loads((output / "settings.json").read_text())["core_sha256"]["evaluate_development.py"]
    if integrity is not True:
        for condition in result["conditions"].values():
            condition.update(complete=False, resolution_rate=None, eligible_pool_repository_weighted_rate=None)
            condition["wilson95_interval"] = None
            condition["task_seconds_per_verified_repair"] = None
            condition["recorded_tokens_per_verified_repair"] = None
        for comparison in result["paired_comparisons"].values():
            comparison.update(complete=False, promotion_eligible=False, development_screen_positive=False)
    (output / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({name: {key: item[key] for key in ["completed", "planned", "verified", "resolution_rate"]}
                      for name, item in result["conditions"].items()}))


def execute_plan(plan, output, gpu, tensor_parallel_size, port):
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu
    os.environ["HF_HUB_OFFLINE"] = "1"
    import run_experiments

    create = run_experiments.create_server

    def factory(runtime_args, model, adapters):
        server = create(runtime_args, model, adapters)
        server.config.extra_args.extend(["--attention-config.backend", "TRITON_ATTN"])
        return server

    run_experiments.create_server = factory
    sys.argv = ["src/run_experiments.py", "--plan", str(plan), "--output", str(output),
                "--model", str(ROOT / "data/models/31b"), "--tensor-parallel-size", str(tensor_parallel_size),
                "--port", str(port), "--check-service-health"]
    run_experiments.main()


def partition_plan(panel, plan, count):
    task_shard = {task["instance_id"]: index % count for index, task in enumerate(panel["tasks"])}
    return [[case for case in plan if task_shard[case["task_id"]] == index] for index in range(count)]


def run(args, panel):
    missing = [str(path.relative_to(ROOT)) for task in panel["tasks"]
               for path in task_inputs(task) if not path.is_file()]
    assert not missing, f"Run prepare first; missing inputs: {missing}"
    metadata = {task["instance_id"]: task for task in map(json.loads,
                (ROOT / "data/competition/tasks.jsonl").read_text().splitlines())}
    for task in panel["tasks"]:
        current = metadata[task["instance_id"]]
        assert current["base_commit"] == task["base_commit"] and current["repo"] == task["repo"]
        assert hashlib.sha256(current["problem_statement"].encode()).hexdigest() == task["description_sha256"]
    from adk_submission import validate_directory

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(args.manifest, output / "cohort.json")
    environment = output / "environment-review.json"
    if args.environment_review:
        review = json.loads(args.environment_review.read_text())
        assert review["ready"] == review["planned"] == len(panel["tasks"])
        assert {row["task_id"] for row in review["cases"]} == {task["instance_id"] for task in panel["tasks"]}
        shutil.copyfile(args.environment_review, environment)
    sources = {}
    if args.control_dir:
        sources["control"] = args.control_dir.resolve()
    if args.reference_dir:
        sources["reference"] = args.reference_dir.resolve()
    sources["candidate"] = args.agent_dir.resolve()
    if panel.get("promotion_rule"):
        assert args.control_dir and not args.reference_dir, "Confirmation requires exactly one frozen candidate/control pair"
    folders = {}
    for name, source in sources.items():
        folders[name] = output / "configs" / name
        shutil.copytree(source, folders[name])
        validate_directory(folders[name])
    seed = args.seed if args.seed is not None else panel["default_execution_seed"]
    plan = make_plan(panel, folders, seed)
    (output / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    formal_zip = ROOT / "output/submission.zip"
    gpus = args.gpu.split(",")
    assert len(set(gpus)) == len(gpus) and all(gpu.isdigit() for gpu in gpus)
    assert len(gpus) == 1 or args.tensor_parallel_size == 1
    settings = {"cohort_sha256": digest(args.manifest),
                "environment_review_sha256": digest(environment) if environment.exists() else None,
                "task_data_sha256": digest(ROOT / "data/competition/tasks.jsonl"),
                "formal_zip_sha256_before": digest(formal_zip) if formal_zip.exists() else None,
                "model": MODEL, "local_profile": "A6000,TP1 default,eager,Triton,cache/compaction matching official guide section 7.2; subprocess not proven identical to scoring Docker",
                "gpu": args.gpu, "tensor_parallel_size": args.tensor_parallel_size, "port": args.port,
                "core_sha256": {name: digest(ROOT / "src" / name) for name in ["run_baseline.py",
                    "run_experiments.py", "local_sandbox.py", "check_patch.py", "analyze_runs.py", "evaluate_development.py"]},
                "plan_only": args.plan_only, "official_submission_created": False}
    settings["network_profile"] = os.environ.get("GEMMA_LOCAL_NETWORK_PROFILE", "host-network")
    if settings["network_profile"] == "experimental-offline-same-user":
        namespace = os.readlink("/proc/self/ns/net")
        capabilities = next(line.split(":", 1)[1].strip() for line in
                            Path("/proc/self/status").read_text().splitlines() if line.startswith("CapEff:"))
        assert namespace != os.environ["GEMMA_PARENT_NETNS"]
        assert os.getuid() == int(os.environ["GEMMA_PARENT_UID"]) and int(capabilities, 16) == 0
        settings["process_network"] = {"namespace": namespace, "effective_uid": os.getuid(),
                                       "effective_capabilities": capabilities,
                                       "official_equivalence_claimed": False}
    (output / "settings.json").write_text(json.dumps(settings, indent=2) + "\n")
    if args.plan_only:
        print(f"Frozen {len(plan)} cases; no model started")
        return
    started, completed = time.perf_counter(), False
    shard_codes = []
    try:
        if len(gpus) == 1:
            execute_plan(output / "plan.json", output, args.gpu, args.tensor_parallel_size, args.port)
        else:
            workers = []
            for index, cases in enumerate(partition_plan(panel, plan, len(gpus))):
                shard = output / "shards" / str(index)
                shard.mkdir(parents=True)
                (shard / "plan.json").write_text(json.dumps(cases, indent=2) + "\n")
                command = [sys.executable, str(Path(__file__).resolve()), "worker", "--plan",
                           str(shard / "plan.json"), "--output", str(shard), "--gpu", gpus[index],
                           "--port", str(args.port + index)]
                with (shard / "run.log").open("wb") as log:
                    workers.append(subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT))
            shard_codes = [worker.wait() for worker in workers]
            assert all(code == 0 for code in shard_codes), shard_codes
        completed = True
    finally:
        receipt = {"completed_normally": completed, "shard_exit_codes": shard_codes,
                   "process_seconds": round(time.perf_counter() - started, 3),
                   "formal_zip_unchanged": (digest(formal_zip) if formal_zip.exists() else None) == settings["formal_zip_sha256_before"],
                   "environment_review_unchanged": (digest(environment) if environment.exists() else None) == settings["environment_review_sha256"],
                   "task_data_unchanged": digest(ROOT / "data/competition/tasks.jsonl") == settings["task_data_sha256"],
                   "core_unchanged": all(digest(ROOT / "src" / name) == value for name, value in settings["core_sha256"].items())}
        (output / "execution.json").write_text(json.dumps(receipt, indent=2) + "\n")
        report(output)


def main():
    os.chdir(ROOT)
    os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prepare_command = sub.add_parser("prepare", help="Download missing official task inputs only; no model")
    prepare_command.add_argument("--manifest", type=Path, default=MANIFEST)
    execute = sub.add_parser("run", help="Evaluate the fixed panel using fresh sandboxes")
    execute.add_argument("--agent-dir", type=Path, default=ROOT / "submission")
    execute.add_argument("--control-dir", type=Path)
    execute.add_argument("--reference-dir", type=Path)
    execute.add_argument("--manifest", type=Path, default=MANIFEST)
    execute.add_argument("--environment-review", type=Path, help="Frozen clean-environment diagnosis, prepared before model outcomes")
    execute.add_argument("--output", type=Path, required=True)
    execute.add_argument("--seed", type=int)
    execute.add_argument("--gpu", default="0", help="One GPU or comma-separated independent TP1 GPU workers")
    execute.add_argument("--tensor-parallel-size", type=int, default=1)
    execute.add_argument("--port", type=int, default=8062)
    execute.add_argument("--plan-only", action="store_true")
    summarize_command = sub.add_parser("report", help="Report completed cases without restarting inference")
    summarize_command.add_argument("--output", type=Path, required=True)
    worker = sub.add_parser("worker", help=argparse.SUPPRESS)
    worker.add_argument("--plan", type=Path, required=True)
    worker.add_argument("--output", type=Path, required=True)
    worker.add_argument("--gpu", required=True)
    worker.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if args.action == "worker":
        execute_plan(args.plan, args.output, args.gpu, 1, args.port)
    elif args.action == "report":
        report(args.output.resolve())
    else:
        panel = load_panel(args.manifest)
        prepare(panel) if args.action == "prepare" else run(args, panel)


if __name__ == "__main__":
    main()
