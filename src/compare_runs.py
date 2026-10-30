"""Compare complete matched local cases without selecting favorable tasks or seeds."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", nargs="+", type=Path, required=True)
    parser.add_argument("--control", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--budget-field", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    groups = {args.control, args.candidate}
    planned, observed = {}, {}
    for directory in args.runs:
        for case in json.loads((directory / "plan.json").read_text()):
            group = case["label"].split("/")[0]
            if group in groups:
                key = (case["task_id"], case.get("seed"))
                planned.setdefault(key, set()).add(group)
        for case in json.loads((directory / "analysis.json").read_text())["cases"]:
            group = case["label"].split("/")[0]
            if group not in groups:
                continue
            key = (case["task_id"], case.get("seed"))
            identifier = (key, group)
            if identifier in observed:
                raise ValueError(f"Ambiguous repeated condition: {identifier}")
            location = directory / case["label"] / case["task_id"]
            observed[identifier] = (case, json.loads((location / "protocol.json").read_text()))

    runtime_fields = ["model", "model_name", "tensor_parallel_size", "max_model_len",
                      "max_num_seqs", "sandbox", "packages", "context_cache", "events_compaction",
                      "enforce_eager", "server_port", "cuda_visible_devices", "source_imports",
                      "task_dependencies_scope", "graph_dir", "embeddings_dir", "wheels_dir",
                      "startup_timeout", "nvidia_lib_dir"]
    runtime_fields.append("evaluation_concurrency")
    runtime_fields.append("prefix_caching")
    rows, violations, missing = [], [], []
    for key, design in sorted(planned.items()):
        if design != groups or any((key, group) not in observed for group in groups):
            missing.append({"task_id": key[0], "seed": key[1]})
            continue
        control, first = observed[(key, args.control)]
        candidate, second = observed[(key, args.candidate)]
        different = [f for f in runtime_fields if first.get(f) != second.get(f)]
        hashes_a, hashes_b = first["config_sha256"], second["config_sha256"]
        paths = {p for p in hashes_a.keys() | hashes_b.keys() if hashes_a.get(p) != hashes_b.get(p)}
        budgets_a, budgets_b = first["budget"], second["budget"]
        budget_changes = {p for p in budgets_a.keys() | budgets_b.keys()
                          if budgets_a.get(p) != budgets_b.get(p)}
        same_tests = control.get("junit_case_names_sha256") == candidate.get("junit_case_names_sha256")
        incompatible_compaction = any(
            "No LlmAgent model available for event compaction summarizer" in str(row.get("agent_error") or "")
            for row in [control, candidate])
        valid = (not different and same_tests and not incompatible_compaction and paths == set(args.changed_file)
                 and budget_changes == set(args.budget_field)
                 and control["actual_seed"] == candidate["actual_seed"] == key[1]
                 and control["verifier_agreement"] and candidate["verifier_agreement"])
        if not valid:
            violations.append({"task_id": key[0], "seed": key[1], "runtime_fields": different,
                               "changed_files": sorted(paths), "budget_fields": sorted(budget_changes),
                               "junit_test_identities_match": same_tests,
                               "native_compaction_configuration_incompatible": incompatible_compaction})
        rows.append({"task_id": key[0], "seed": key[1], "valid_control": valid,
                     "control": control, "candidate": candidate})

    tasks = {key[0] for key in planned}
    seeds = {key[1] for key in planned}
    enough = (len(rows) >= 4 and len(tasks) >= 2 and len(seeds) >= 2
              and all(isinstance(seed, int) for seed in seeds)
              and set(planned) == {(task, seed) for task in tasks for seed in seeds})
    complete = bool(planned) and not missing and not violations and enough
    wins = sum(r["candidate"]["independently_verified"] and not r["control"]["independently_verified"] for r in rows)
    regressions = sum(r["control"]["independently_verified"] and not r["candidate"]["independently_verified"] for r in rows)
    totals = {}
    for group in ["control", "candidate"]:
        totals[group] = {
            "verified": sum(r[group]["independently_verified"] for r in rows),
            "task_seconds": round(sum(r[group]["task_seconds"] for r in rows), 3),
            "total_tokens": sum(r[group]["tokens"]["total_tokens"] for r in rows),
            "trace_interactions": sum(r[group]["trace_interactions"] for r in rows),
        }
    all_pass = bool(rows) and all(r[g]["independently_verified"] for r in rows for g in ["control", "candidate"])
    efficiency = all_pass and any(totals["candidate"][metric] < totals["control"][metric]
                                  for metric in ["task_seconds", "total_tokens", "trace_interactions"])
    report = {"control": args.control, "candidate": args.candidate,
              "complete_controlled_comparison": complete, "planned_pairs": len(planned),
              "matched_pairs": len(rows), "missing": missing, "violations": violations,
              "quality_wins": wins, "quality_regressions": regressions, "totals": totals,
              "local_quality_signal": bool(complete and wins and not regressions),
              "local_efficiency_signal": bool(complete and efficiency),
              "official_score_claimed": False,
              "counting_note": "Signals require mechanism review; repeated mechanisms and selection bias do not create extra positive points",
              "pairs": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ["matched_pairs", "quality_wins", "quality_regressions",
                                           "local_quality_signal", "local_efficiency_signal"]}))


if __name__ == "__main__":
    main()
